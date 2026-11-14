// Country detection for comments like «Soy Marta de España 🇪🇸».
// Works in browser and Node (Intl.DisplayNames gives Spanish names for every ISO code).

export const ISO_CODES = 'ad ae af ag ai al am ao ar as at au aw ax az ba bb bd be bf bg bh bi bj bl bm bn bo br bs bt bw by bz ca cd cf cg ch ci ck cl cm cn co cr cu cv cw cy cz de dj dk dm do dz ec ee eg eh er es et fi fj fk fm fo fr ga gb gd ge gf gg gh gi gl gm gn gp gq gr gt gu gw gy hk hn hr ht hu id ie il im in iq ir is it je jm jo jp ke kg kh ki km kn kp kr kw ky kz la lb lc li lk lr ls lt lu lv ly ma mc md me mf mg mh mk ml mm mn mo mp mq mr ms mt mu mv mw mx my mz na nc ne nf ng ni nl no np nr nu nz om pa pe pf pg ph pk pl pm pn pr ps pt pw py qa re ro rs ru rw sa sb sc sd se sg sh si sk sl sm sn so sr ss st sv sx sy sz tc td tg th tj tk tl tm tn to tr tt tv tw tz ua ug us uy uz va vc ve vg vi vn vu wf ws xk ye yt za zm zw'.split(' ')

const dn = new Intl.DisplayNames(['es'], { type: 'region' })
export function countryName(iso: string) {
  try { return dn.of(iso.toUpperCase()) ?? iso.toUpperCase() } catch { return iso.toUpperCase() }
}

const norm = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()

const ALIASES: Record<string, string> = {
  eeuu: 'us', 'ee.uu': 'us', usa: 'us', 'estados unidos': 'us', 'reino unido': 'gb', inglaterra: 'gb', uk: 'gb', escocia: 'gb', gales: 'gb',
  holanda: 'nl', 'paises bajos': 'nl', 'republica dominicana': 'do', rd: 'do', 'corea del sur': 'kr', corea: 'kr', rusia: 'ru',
  'costa de marfil': 'ci', brasil: 'br', 'el salvador': 'sv', salvador: 'sv', catalunya: 'es', cataluna: 'es', 'pais vasco': 'es', euskadi: 'es',
  andalucia: 'es', galicia: 'es', canarias: 'es', madrid: 'es', mexico: 'mx', 'puerto rico': 'pr', chequia: 'cz', 'republica checa': 'cz',
}

let table: [string, string][] | null = null
function names(): [string, string][] {
  if (table) return table
  const t: [string, string][] = ISO_CODES.map((c) => [norm(countryName(c)), c])
  for (const [k, v] of Object.entries(ALIASES)) t.push([k, v])
  table = t.sort((a, b) => b[0].length - a[0].length) // longest match first
  return table
}

/** flag emoji (regional indicators) → iso */
function fromEmoji(text: string): string | null {
  const cps = [...text].map((c) => c.codePointAt(0)!)
  for (let i = 0; i < cps.length - 1; i++) {
    const a = cps[i] - 0x1f1e6, b = cps[i + 1] - 0x1f1e6
    if (a >= 0 && a < 26 && b >= 0 && b < 26) {
      const iso = String.fromCharCode(97 + a) + String.fromCharCode(97 + b)
      if (ISO_CODES.includes(iso)) return iso
    }
  }
  return null
}

export function parseComment(text: string): { name: string | null; iso: string | null } {
  let iso = fromEmoji(text)
  const t = ' ' + norm(text).replace(/[^\p{L}\p{N}.\s]/gu, ' ').replace(/\s+/g, ' ') + ' '
  if (!iso) for (const [n, c] of names()) if (t.includes(' ' + n + ' ')) { iso = c; break }
  // «soy X», «me llamo X», «X de País»
  let name: string | null = null
  const m = text.match(/(?:soy|me llamo|mi nombre es)\s+([\p{L}][\p{L}'-]{1,24})/iu) ?? text.match(/^\s*([\p{L}][\p{L}'-]{1,24})\s+(?:de|desde)\s/iu)
  const STOP = new Set(['hola', 'holaa', 'saludos', 'buenas', 'hello', 'hi', 'hey', 'yo', 'aqui', 'aquí', 'gente', 'alguien'])
  if (m && !STOP.has(norm(m[1]))) name = m[1][0].toUpperCase() + m[1].slice(1)
  return { name, iso }
}
