import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: process.env.STACK_API_TARGET || 'http://127.0.0.1:8000',
        changeOrigin: false,
      },
    },
  },
  preview: { proxy: { '/api': { target: 'http://127.0.0.1:8000', changeOrigin: false } } },
  test: {
    environment: 'jsdom',
    setupFiles: './src/test-setup.js',
    css: false,
    include: ['src/**/*.test.{js,jsx}'],
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules') && /recharts|d3-|victory-vendor/.test(id)) return 'charts'
          if (
            id.includes('node_modules') &&
            /\/(react|react-dom|react-router|react-router-dom)\//.test(id)
          )
            return 'ui'
        },
      },
    },
  },
})
