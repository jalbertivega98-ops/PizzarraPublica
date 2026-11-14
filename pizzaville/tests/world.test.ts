import { test } from 'node:test'
import assert from 'node:assert/strict'
import { parseComment } from '../src/world/countries'
import { plotSlots } from '../src/world/plots'
import { heightAt, WATER_LEVEL, waterDist } from '../src/world/terrain'

test('detecta país y nombre en comentarios', () => {
  assert.deepEqual(parseComment('Soy Marta de España 🇪🇸'), { name: 'Marta', iso: 'es' })
  assert.equal(parseComment('Kenji 🇯🇵').iso, 'jp')
  assert.equal(parseComment('Me llamo Luis, desde México').iso, 'mx')
  assert.equal(parseComment('saludos desde EEUU').iso, 'us')
  assert.equal(parseComment('hola desde argentina!!').name, null)
  assert.equal(parseComment('me encanta el vídeo').iso, null)
})

test('el terreno es determinista (misma semilla, mismas alturas)', () => {
  assert.equal(heightAt(123.4, -56.7), heightAt(123.4, -56.7))
  assert.ok(Math.abs(heightAt(0, 0) - 1.25) < 0.5, 'claro llano en la casa de Pizz')
})

test('las parcelas no se solapan, no están en el agua y son estables', () => {
  const s = plotSlots()
  assert.ok(s.length >= 100, `parcelas: ${s.length}`)
  const ids = new Set(s.map((p) => p.id))
  assert.equal(ids.size, s.length)
  for (let i = 0; i < 60; i++) {
    for (let j = i + 1; j < 60; j++) assert.ok(Math.hypot(s[i].x - s[j].x, s[i].z - s[j].z) > 10, `${s[i].id}/${s[j].id}`)
    assert.ok(s[i].y > WATER_LEVEL + 0.5)
    assert.ok(waterDist(s[i].x, s[i].z) > 5)
    assert.ok(Math.hypot(s[i].x, s[i].z) > 12, 'lejos de la casa de Pizz')
  }
  assert.equal(s[0].id, 'p0es')
})
