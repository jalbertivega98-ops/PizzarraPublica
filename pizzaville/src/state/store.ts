import { create } from 'zustand'
import { clock } from '../engine/clock'

export type Inhabitant = {
  id: string; comment_id: string | null; account_id: string | null; platform: string; public_name: string | null; display_name: string | null
  show_name: number; country: string; joined_at: string; plot_id: string | null; x: number; z: number; y: number; rot: number
  house_seed: number; look_seed: number; status: 'pending' | 'approved' | 'rejected' | 'built' | 'removed'; source_text: string | null
}
export type WorldData = { env: string; inhabitants: Inhabitant[]; stats: { population: number; houses: number; pending: number; countries: { iso: string; name: string; n: number }[] } }

type S = {
  env: 'official' | 'sandbox'
  data: WorldData | null
  error: string | null
  cinema: boolean
  builds: Record<string, number> // id → clock.t at which the live construction started
  focus: { x: number; y: number; z: number; at: number } | null
  setEnv: (e: 'official' | 'sandbox') => void
  load: () => Promise<void>
  add: (b: Record<string, unknown>) => Promise<{ ok: boolean; error?: string; duplicate?: string }>
  act: (id: string, action: string) => Promise<void>
  build: (id: string) => void
  setCinema: (v: boolean) => void
  locate: (x: number, y: number, z: number) => void
}

export const BUILD_SECONDS = 22

const api = (path: string, env: string, body?: unknown) =>
  fetch(`/api/${path}${path.includes('?') ? '&' : '?'}env=${env}`, body === undefined ? undefined : { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) }).then((r) => r.json())

export const useStore = create<S>((set, get) => ({
  env: (localStorage.getItem('pv-env') as 'official' | 'sandbox') || 'sandbox',
  data: null,
  error: null,
  cinema: false,
  builds: {},
  focus: null,
  setEnv: (env) => { try { localStorage.setItem('pv-env', env) } catch { /* private mode */ } set({ env, data: null, builds: {} }); get().load() },
  load: async () => {
    try { set({ data: await api('world', get().env), error: null }) } catch { set({ error: 'Sin conexión con el servidor de Pizzaville' }) }
  },
  add: async (b) => {
    const r = await api('inhabitants', get().env, b)
    await get().load()
    return r
  },
  act: async (id, action) => { set({ data: await api(`inhabitants/${id}`, get().env, { action }) }) },
  build: (id) => {
    set({ builds: { ...get().builds, [id]: clock.t } })
    setTimeout(() => get().act(id, 'built'), BUILD_SECONDS * 1000 / Math.max(0.1, clock.speed) + 500)
  },
  setCinema: (cinema) => set({ cinema }),
  locate: (x, y, z) => set({ focus: { x, y, z, at: performance.now() } }),
}))
