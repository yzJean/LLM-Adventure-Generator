import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  // setup proxy for API requests to backend server during development
  server: {
    proxy: {
      "/api": { // whatever we gets to /api, automatically forward to backend server
        target: "http://localhost:8000",
        changeOrigin: true,
        secure: false
      }
    }
  }
})
