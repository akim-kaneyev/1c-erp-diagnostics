import { defineConfig, mergeConfig } from 'vitest/config'
import vite from './vite.config.ts'

export default mergeConfig(vite, defineConfig({ test: {
  environment: 'jsdom', setupFiles: ['./src/test/setup.ts'],
  fileParallelism: false,
} }))
