// Vitest Configuration for Frontend
//
// This file configures how Vitest runs unit tests.
//
// What each setting does:
// - environment: "jsdom" = Fake browser (don't need real browser for unit tests)
// - globals: true = Can use test(), expect() without importing
// - setupFiles = Files to run before tests (global setup)

import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.js'],
  },
})
