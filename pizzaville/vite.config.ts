import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import { pizzavilleApi } from './server/api'

export default defineConfig({
  plugins: [react(), pizzavilleApi()],
})
