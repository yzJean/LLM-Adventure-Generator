import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig((command, mode) =>{
  const env = loadEnv(mode, process.cwd(), "") // Use env variables to dinstinguish between development and production mode. This allows us to set different configurations based on the environment. For example, we can enable debugging features in development mode while keeping them disabled in production for better performance and security.
  console.log(env.VITE_DEBUG)
    return {
      plugins: [react()],

      // setup proxy for API requests to backend server during development
      server: {
        ...(env.VITE_DEBUG === "true" && { // only define proxy when in development mode. This ensures that API requests are correctly forwarded to the backend server during development, while in production mode, the frontend can directly communicate with the backend without needing a proxy.
          proxy: {
            "/api": { // whatever we gets to /api, automatically forward to backend server
              target: "http://localhost:8000",
              changeOrigin: true,
              secure: false
            }
          }
        })
      }
    }
})
