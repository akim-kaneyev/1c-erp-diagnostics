import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: '../plugins/one-c-erp-diagnostics/ui/dist',
    emptyOutDir: true,
    sourcemap: false,
    target: 'es2022',
  },
  server: { host: '127.0.0.1', strictPort: true },
})
