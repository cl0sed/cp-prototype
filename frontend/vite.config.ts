import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      // Alias to force static icon exports and prevent excessive chunk generation
      '@tabler/icons-react': '@tabler/icons-react/dist/esm/icons/index.mjs',
    },
  },
  server: {
    port: 5173,
    // Proxy is handled by Nginx for initial routing, but Vite handles API proxying
    // Proxy API requests (including /auth) to the backend
    proxy: {
      '/auth': { // Proxy requests starting with /auth
        target: 'http://backend:8000', // Target the backend service
        changeOrigin: true, // Recommended for virtual hosted sites
        bypass: (req, res, options) => {
          // Don't proxy requests that accept HTML - these are likely page navigations
          if (req.headers?.accept?.includes('text/html')) {
            // console.log(`[Vite Proxy Bypass] Bypassing: ${req.url} (Accepts HTML)`);
            return req.url; // Return the original URL to let Vite handle it (via React Router)
          }
          // Otherwise, let the proxy handle it (API calls)
          // console.log(`[Vite Proxy Bypass] Proxying: ${req.url}`);
          return undefined; // Returning undefined proceeds with proxying
        },
      },
      // TODO: Add '/api' proxy here if needed, targeting http://backend:8000
    },

    hmr: {
      protocol: 'ws',
      host: 'localhost',
      port: 80, // Nginx port
    }
  },
  optimizeDeps: {
    include: [
      '@mantine/core',
      '@mantine/hooks',
      '@mantine/form',
      '@mantine/notifications',
      '@tabler/icons-react',
      'supertokens-auth-react/recipe/session',
      'supertokens-auth-react/recipe/emailpassword'
    ],
  },
});
