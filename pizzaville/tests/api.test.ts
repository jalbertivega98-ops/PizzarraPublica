// Prueba la API real (SQLite) en un directorio temporal.
import { test } from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'

const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'pv-'))
process.chdir(dir)
const { addInhabitant } = await import('../server/api')

test('un comentario procesado dos veces no crea dos casas', () => {
  const a = addInhabitant('sandbox', { comment_id: 'c1', text: 'Soy Marta de España' })
  const b = addInhabitant('sandbox', { comment_id: 'c1', text: 'Soy Marta de España' })
  assert.equal(a.ok, true)
  assert.equal(b.duplicate, 'comment')
  assert.equal((b.inhabitant as { id: string }).id, (a.inhabitant as { id: string }).id)
})

test('una cuenta = una vivienda principal', () => {
  addInhabitant('sandbox', { comment_id: 'c2', platform: 'tiktok', account_id: '@x', text: 'Pedro de Chile' })
  const r = addInhabitant('sandbox', { comment_id: 'c3', platform: 'tiktok', account_id: '@x', text: 'Pedro de Perú' })
  assert.equal(r.duplicate, 'account')
})

test('cada habitante recibe una parcela distinta y se guarda el JSON', () => {
  const r = addInhabitant('sandbox', { comment_id: 'c4', country: 'jp' })
  const snap = JSON.parse(fs.readFileSync(path.join(dir, 'data/sandbox/world.json'), 'utf8'))
  const plots = snap.inhabitants.map((h: { plot_id: string }) => h.plot_id)
  assert.equal(new Set(plots).size, plots.length)
  assert.equal(snap.inhabitants.length, 3)
  assert.ok(r.ok)
})

test('el mundo oficial está separado del de pruebas', () => {
  const r = addInhabitant('official', { comment_id: 'c1', country: 'es' })
  assert.equal(r.duplicate, undefined)
})

test('país desconocido se rechaza', () => {
  assert.equal(addInhabitant('sandbox', { comment_id: 'c9', text: 'qué bonito' }).ok, false)
})
