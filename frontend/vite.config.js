import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'node:fs'
import path from 'node:path'
import { getProxyOptions } from 'frappe-ui/src/utils/vite-dev-server'
import { webserver_port } from '../../../sites/common_site_config.json'

// Custom plugin to copy build output to www/frontend
const copyBuildOutput = () => {
  return {
    name: 'copy-build-output',
    closeBundle: async () => {
      const outDir = path.resolve(__dirname, '../employee_management/public/frontend')
      const wwwDir = path.resolve(__dirname, '../employee_management/www/frontend')
      
      console.log(`Copying build output from ${outDir} to ${wwwDir}...`)
      
      if (fs.existsSync(wwwDir)) {
        fs.rmSync(wwwDir, { recursive: true, force: true })
      }
      fs.mkdirSync(wwwDir, { recursive: true })

      // Copy all files from public/frontend to www/frontend
      fs.cpSync(outDir, wwwDir, { recursive: true })
      console.log('Build output successfully copied to www/frontend.')
    }
  }
}

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [
    vue(),
    copyBuildOutput()
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    port: 8080,
    proxy: getProxyOptions({ port: webserver_port }),
  },
  optimizeDeps: {
    include: ['frappe-ui'],
  },
  // In production, assets are served from /assets/employee_management/frontend/
  // In dev, Vite serves everything from /
  base: mode === 'production' ? '/assets/employee_management/frontend/' : '/',
  build: {
    outDir: `../employee_management/public/frontend`,
    emptyOutDir: true,
    target: 'es2015',
    commonjsOptions: {
      include: [/node_modules/],
    },
  },
}))
