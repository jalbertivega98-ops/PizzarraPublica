# Conectar Instagram para que los reels se publiquen solos

Se hace **una sola vez** (unos 15 minutos). Todo desde el navegador del móvil.
Si alguna página se ve rara, en el menú del navegador marca **«Versión para ordenador»**.

## 1. Crear la app en Meta (5 min)

1. Abre **developers.facebook.com/apps** e inicia sesión con tu Facebook.
   Si te lo pide, regístrate como desarrollador (nombre, teléfono, «Desarrollador»).
2. Pulsa **Crear app**. Nombre: `Pizarra Publica Publicador`. Siguiente.
3. En «Casos de uso» elige **Administrar mensajes y contenido en Instagram**
   (*Manage messaging & content on Instagram*). Siguiente.
4. Si pregunta por un portfolio comercial, elige **No quiero conectar ninguno ahora**. Siguiente → **Ir al panel**.

## 2. Conectar tu cuenta de Instagram y sacar el token (5 min)

1. En el panel de la app: **Casos de uso → Personalizar** (o **Instagram → Configuración de la API con inicio de sesión de Instagram**).
2. En **«Generar identificadores de acceso»** pulsa **Añadir cuenta** e inicia sesión con **@pizarrapublica** (la cuenta Empresa). Acepta los permisos.
3. Al lado de la cuenta pulsa **Generar identificador** y copia el texto largo (empieza por `IGAA…`).
   - **No lo pegues en ningún chat.** Solo va en GitHub (paso 3).
   - Si sale un aviso de «evaluador» (*tester*): en la app de Instagram ve a
     Configuración → Permisos de sitios web → Apps y sitios web → **Invitaciones de evaluador** y acéptala. Luego repite este paso.

## 3. Guardar el token en GitHub (2 min)

1. Abre **github.com/jalbertivega98-ops/pizzarrapublica/settings/secrets/actions/new**
   (en el navegador, la app de GitHub no deja hacerlo).
2. **Name:** `IG_TOKEN`
3. **Secret:** pega el token.
4. Pulsa **Add secret**.

## 4. Comprobar

En 10-15 minutos abre **ESTADO.md** en el repositorio. Si pone
**✅ Conectado con Instagram como @pizarrapublica**, ya está: cada reel sale solo a su hora
y te llega un aviso de GitHub al móvil cuando se publica.

Si pone ❌, dile a Claude qué mensaje sale.

## A tener en cuenta

- El token **caduca a los 60 días**. Antes de que caduque hay que repetir los pasos 2 y 3.
- Instagram no deja **fijar** comentarios por API: el comentario de fuentes se publica solo,
  pero para fijarlo arriba mantenlo pulsado en la app → **Fijar**.
- Para cambiar una fecha, pausar un reel (`"estado": "pausado"`) o añadir nuevos: edita
  `publicar/calendario.json` o pídeselo a Claude.
