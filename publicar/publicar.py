#!/usr/bin/env python3
"""Publica en Instagram los reels de publicar/calendario.json cuando llega su hora.

Lo ejecuta la GitHub Action .github/workflows/publicar.yml cada 10 minutos.
Usa la API de Instagram con inicio de sesión de Instagram (graph.instagram.com):
  1. crea un contenedor REELS con la URL pública del MP4 en GitHub,
  2. espera a que Instagram procese el vídeo,
  3. lo publica y añade el comentario de fuentes.
Después actualiza el calendario, regenera ESTADO.md y deja un aviso en el issue
de avisos del repositorio (GitHub manda la notificación al móvil).

Solo usa la librería estándar. Variables de entorno:
  IG_TOKEN           token de acceso de Instagram (secreto del repositorio)
  GITHUB_REPOSITORY  usuario/repo (lo pone GitHub)
  GITHUB_TOKEN       para escribir los avisos (lo pone GitHub)
  RAMA               rama de la que se sirven los vídeos (por defecto main)
  IG_API_BASE        para pruebas; por defecto https://graph.instagram.com/v23.0
  FORZAR_ID          publica ya esta entrada aunque no sea su hora (ejecución manual)
"""
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

RAIZ = Path(__file__).resolve().parent.parent
CALENDARIO = RAIZ / "publicar" / "calendario.json"
ESTADO_MD = RAIZ / "ESTADO.md"
SEPARADOR_COMENTARIO = "--- Comentario fijado ---"
TITULO_ISSUE = "📣 Avisos de publicación"

API = os.environ.get("IG_API_BASE", "https://graph.instagram.com/v23.0").rstrip("/")
TOKEN = os.environ.get("IG_TOKEN", "").strip()
REPO = os.environ.get("GITHUB_REPOSITORY", "jalbertivega98-ops/pizzarrapublica")
RAMA = os.environ.get("RAMA", "main")
GH_TOKEN = os.environ.get("GITHUB_TOKEN", "")
FORZAR_ID = os.environ.get("FORZAR_ID", "").strip()

MAX_RETRASO = dt.timedelta(hours=3)   # más tarde que esto no se publica sola
MAX_INTENTOS = 3
ESPERA_PROCESADO_S = 600              # máximo esperando a que Instagram procese el vídeo

ICONOS = {
    "programado": "⏳ Programado",
    "publicado": "✅ Publicado",
    "error": "❌ Error",
    "atrasado": "⚠️ No publicado (se pasó la hora)",
    "manual": "✋ Subido a mano",
    "pausado": "⏸️ Pausado",
}


class ErrorApi(Exception):
    pass


# ---------------------------------------------------------------- Instagram

def ig(metodo, ruta, **params):
    params["access_token"] = TOKEN
    url = f"{API}/{ruta.lstrip('/')}"
    datos = None
    if metodo == "GET":
        url += "?" + urllib.parse.urlencode(params)
    else:
        datos = urllib.parse.urlencode(params).encode()
    peticion = urllib.request.Request(url, data=datos, method=metodo)
    try:
        with urllib.request.urlopen(peticion, timeout=60) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        cuerpo = e.read().decode(errors="replace")
        try:
            err = json.loads(cuerpo).get("error", {})
            msg = err.get("error_user_msg") or err.get("message") or cuerpo
            codigo = err.get("code")
        except ValueError:
            msg, codigo = cuerpo, None
        raise ErrorApi(f"{msg} (HTTP {e.code}{', código ' + str(codigo) if codigo else ''})") from None
    except urllib.error.URLError as e:
        raise ErrorApi(f"No se pudo contactar con Instagram: {e.reason}") from None


def url_publica(ruta):
    camino = urllib.parse.quote(ruta)
    return f"https://raw.githubusercontent.com/{REPO}/{RAMA}/{camino}"


def leer_publicacion(carpeta):
    """Devuelve (vídeo, portada, descripción, comentario) de una carpeta de vídeos/."""
    d = RAIZ / carpeta
    mp4 = sorted(d.glob("*.mp4"))
    txt = sorted(d.glob("*_publicacion.txt"))
    png = sorted(d.glob("portada*.png"))
    if not mp4 or not txt:
        raise ErrorApi(f"Falta el .mp4 o el _publicacion.txt en {carpeta}")
    texto = txt[0].read_text(encoding="utf-8")
    descripcion, _, comentario = texto.partition(SEPARADOR_COMENTARIO)
    rel = lambda p: p.relative_to(RAIZ).as_posix()
    return (rel(mp4[0]), rel(png[0]) if png else None,
            descripcion.strip(), comentario.strip())


def ya_esta_en_instagram(ig_id, descripcion):
    """Evita duplicados: busca la primera línea de la descripción en los últimos posts."""
    primera = descripcion.splitlines()[0].strip()
    medios = ig("GET", f"{ig_id}/media", fields="id,caption,permalink,timestamp", limit=15)
    for m in medios.get("data", []):
        if (m.get("caption") or "").strip().startswith(primera):
            return m
    return None


def publicar(ig_id, entrada):
    video, portada, descripcion, comentario = leer_publicacion(entrada["carpeta"])

    previo = ya_esta_en_instagram(ig_id, descripcion)
    if previo:
        return previo["id"], previo.get("permalink", ""), "ya estaba"

    params = dict(media_type="REELS", video_url=url_publica(video),
                  caption=descripcion, share_to_feed="true")
    if portada:
        params["cover_url"] = url_publica(portada)
    contenedor = ig("POST", f"{ig_id}/media", **params)["id"]

    limite = time.time() + ESPERA_PROCESADO_S
    while True:
        estado = ig("GET", contenedor, fields="status_code,status")
        codigo = estado.get("status_code")
        if codigo == "FINISHED":
            break
        if codigo in ("ERROR", "EXPIRED"):
            raise ErrorApi(f"Instagram no pudo procesar el vídeo: {estado.get('status', codigo)}")
        if time.time() > limite:
            raise ErrorApi("Instagram tardó demasiado en procesar el vídeo")
        time.sleep(15)

    media_id = ig("POST", f"{ig_id}/media_publish", creation_id=contenedor)["id"]
    enlace = ""
    try:
        enlace = ig("GET", media_id, fields="permalink").get("permalink", "")
    except ErrorApi:
        pass

    nota_comentario = "sin comentario"
    if comentario:
        try:
            ig("POST", f"{media_id}/comments", message=comentario)
            nota_comentario = "comentario de fuentes puesto"
        except ErrorApi as e:
            nota_comentario = f"no se pudo poner el comentario de fuentes ({e})"
    return media_id, enlace, nota_comentario


# ---------------------------------------------------------------- avisos (issue)

def github(metodo, ruta, cuerpo=None):
    peticion = urllib.request.Request(
        f"https://api.github.com/{ruta.lstrip('/')}",
        data=json.dumps(cuerpo).encode() if cuerpo is not None else None,
        method=metodo,
        headers={"Authorization": f"Bearer {GH_TOKEN}",
                 "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(peticion, timeout=30) as r:
        return json.loads(r.read() or b"{}")


def avisar(textos):
    if not textos:
        return
    for t in textos:
        print("AVISO:", t)
    if not GH_TOKEN:
        return
    try:
        abiertos = github("GET", f"repos/{REPO}/issues?state=open&per_page=100")
        issue = next((i for i in abiertos if i.get("title") == TITULO_ISSUE), None)
        if issue is None:
            issue = github("POST", f"repos/{REPO}/issues", {
                "title": TITULO_ISSUE,
                "body": "Aquí aparece un aviso cada vez que se publica un reel o algo falla. "
                        f"El calendario completo está en [ESTADO.md](https://github.com/{REPO}/blob/{RAMA}/ESTADO.md)."})
        github("POST", f"repos/{REPO}/issues/{issue['number']}/comments",
               {"body": "\n\n".join(textos)})
    except Exception as e:  # los avisos nunca deben romper la publicación
        print("No se pudo escribir el aviso en GitHub:", e)


# ---------------------------------------------------------------- estado

def fecha_local(entrada, tz):
    return dt.datetime.strptime(entrada["fecha"], "%Y-%m-%d %H:%M").replace(tzinfo=tz)


def escribir_estado_md(cal, tz):
    dias = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
    con = cal.get("conexion", {})
    if con.get("estado") == "ok":
        linea_con = f"✅ Conectado con Instagram como **@{con.get('usuario', '?')}**"
    elif con.get("estado") == "sin_token":
        linea_con = "⚠️ Falta conectar Instagram (no hay token guardado en GitHub)"
    else:
        linea_con = f"❌ Instagram rechaza la conexión: {con.get('detalle', '')}"

    filas = []
    for e in cal["publicaciones"]:
        f = fecha_local(e, tz)
        cuando = f"{dias[f.weekday()]} {f:%d/%m %H:%M}"
        estado = ICONOS.get(e["estado"], e["estado"])
        if e["estado"] == "publicado":
            hora = e.get("publicado_en", "")
            estado += f" {hora}"
            if e.get("enlace"):
                estado += f" · [ver en Instagram]({e['enlace']})"
        if e["estado"] == "error" and e.get("ultimo_error"):
            estado += f": {e['ultimo_error']}"
        elif e["estado"] == "programado" and e.get("ultimo_error"):
            estado += f" (reintento {e.get('intentos', 0)}/{MAX_INTENTOS}: {e['ultimo_error']})"
        filas.append(f"| {e['titulo']} | {cuando} | {estado} |")

    ESTADO_MD.write_text(
        "# 📅 Publicaciones en Instagram\n\n"
        f"{linea_con}\n\n"
        "| Reel | Cuándo (hora de Madrid) | Estado |\n|---|---|---|\n"
        + "\n".join(filas) + "\n\n"
        "Se comprueba cada 10 minutos, así que cada reel sale entre la hora "
        "programada y unos 15 minutos después.\n\n"
        "🔔 Cada publicación o fallo deja un aviso en el issue "
        f"[{TITULO_ISSUE}](https://github.com/{REPO}/issues) y GitHub te lo notifica en el móvil.\n\n"
        "Para cambiar fechas, añadir reels o pausar uno, edita "
        "[publicar/calendario.json](publicar/calendario.json) o pídeselo a Claude.\n",
        encoding="utf-8")


def main():
    cal = json.loads(CALENDARIO.read_text(encoding="utf-8"))
    tz = ZoneInfo(cal.get("zona_horaria", "Europe/Madrid"))
    ahora = dt.datetime.now(tz)
    avisos = []
    con_antes = dict(cal.get("conexion", {}))

    ig_id = None
    if not TOKEN:
        cal["conexion"] = {"estado": "sin_token"}
    else:
        try:
            yo = ig("GET", "me", fields="user_id,username")
            ig_id = yo.get("user_id") or yo.get("id")
            cal["conexion"] = {"estado": "ok", "usuario": yo.get("username", "")}
        except ErrorApi as e:
            cal["conexion"] = {"estado": "error", "detalle": str(e)}

    if cal["conexion"].get("estado") != con_antes.get("estado"):
        if cal["conexion"]["estado"] == "ok":
            avisos.append(f"✅ Conectado con Instagram como @{cal['conexion']['usuario']}. "
                          "Los reels se publicarán solos a su hora.")
        elif cal["conexion"]["estado"] == "error":
            avisos.append(f"❌ Instagram rechaza el token: {cal['conexion']['detalle']}")

    for e in cal["publicaciones"]:
        if e["estado"] != "programado":
            continue
        forzado = FORZAR_ID and e["id"] == FORZAR_ID
        hora = fecha_local(e, tz)
        if ahora < hora and not forzado:
            continue
        if ahora - hora > MAX_RETRASO and not forzado:
            e["estado"] = "atrasado"
            avisos.append(f"⚠️ **{e['titulo']}** no se publicó: tocaba el "
                          f"{hora:%d/%m a las %H:%M} y "
                          + ("Instagram no estaba conectado." if not ig_id else "no se pudo a tiempo.")
                          + " Cambia la fecha en el calendario o pídeselo a Claude.")
            continue
        if not ig_id:
            continue  # se intentará en la siguiente pasada, dentro del margen

        print(f"Publicando {e['id']}…")
        try:
            media_id, enlace, nota = publicar(ig_id, e)
        except ErrorApi as err:
            e["intentos"] = e.get("intentos", 0) + 1
            e["ultimo_error"] = str(err)[:300]
            if e["intentos"] >= MAX_INTENTOS:
                e["estado"] = "error"
                avisos.append(f"❌ **{e['titulo']}** falló {MAX_INTENTOS} veces y se ha "
                              f"parado: {e['ultimo_error']}")
            print("Error:", err)
            continue
        e.update(estado="publicado", media_id=media_id, enlace=enlace,
                 publicado_en=dt.datetime.now(tz).strftime("%d/%m %H:%M"))
        e.pop("ultimo_error", None)
        if nota == "ya estaba":
            avisos.append(f"✅ **{e['titulo']}** ya estaba en Instagram, no se ha vuelto a subir. {enlace}")
        else:
            avisos.append(f"✅ **{e['titulo']}** publicado a las {e['publicado_en']}. {enlace}\n"
                          f"Nota: {nota}. Recuerda fijarlo arriba desde la app (mantén pulsado → Fijar).")

    CALENDARIO.write_text(json.dumps(cal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    escribir_estado_md(cal, tz)
    avisar(avisos)


if __name__ == "__main__":
    sys.exit(main())
