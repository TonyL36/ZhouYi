import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 6400,
    proxy: {
      '/api': {
        target: 'http://localhost:6401',
        changeOrigin: true,
      },
      '/images': {
        target: 'http://localhost:6401',
        changeOrigin: true,
      }
    }
  },
  base: '/book/ZhouYi/',
})
