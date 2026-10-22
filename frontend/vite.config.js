import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite yapılandırması
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Backend API'ye proxy - CORS sorunlarını önler
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
