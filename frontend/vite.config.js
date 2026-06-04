import react from '@vitejs/plugin-react'
import { defineConfig, loadEnv } from 'vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiUrl = env.VITE_API_PROXY_TARGET || env.VITE_API_URL || ''
  const proxyTarget = apiUrl.replace(/\/api\/?$/, '')

  return {
    plugins: [react()],
    server: {
      host: env.VITE_DEV_HOST || '127.0.0.1',
      port: Number(env.VITE_DEV_PORT || 3000),
      proxy: proxyTarget
        ? {
            '/api': {
              target: proxyTarget,
              changeOrigin: true
            }
          }
        : undefined
    }
  }
})
