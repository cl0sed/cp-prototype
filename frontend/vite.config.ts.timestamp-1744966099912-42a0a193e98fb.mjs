// vite.config.ts
import { defineConfig } from "file:///app/node_modules/vite/dist/node/index.js";
import react from "file:///app/node_modules/@vitejs/plugin-react/dist/index.mjs";
import { fileURLToPath } from "url";
import { dirname, resolve } from "path";
var __vite_injected_original_import_meta_url = "file:///app/vite.config.ts";
var __filename = fileURLToPath(__vite_injected_original_import_meta_url);
var __dirname = dirname(__filename);
var vite_config_default = defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": resolve(__dirname, "./src")
    }
  },
  server: {
    port: 5173,
    // Proxy is handled by Nginx now, so this section can be removed or commented out
    // proxy: {
    //   '/api': {
    //     target: process.env.VITE_API_URL || 'http://localhost:8000', // This points to backend directly, not proxy
    //     changeOrigin: true,
    //     secure: false,
    //   },
    // },
    // HMR configuration (useful when running in Docker)
    hmr: {
      protocol: "ws",
      // Use 'ws' for http, 'wss' for https
      host: "localhost",
      // Use the host accessible from the browser (via Nginx)
      port: 80
      // Use the Nginx proxy port
      // Optional: If HMR still fails, specify clientPort explicitly
      // clientPort: 80
    }
  },
  optimizeDeps: {
    include: [
      "@mantine/core",
      "@mantine/hooks",
      "@mantine/form",
      "@mantine/notifications",
      "@tabler/icons-react",
      // Explicitly include icon library
      "supertokens-auth-react/recipe/session",
      "supertokens-auth-react/recipe/emailpassword"
    ]
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvYXBwXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCIvYXBwL3ZpdGUuY29uZmlnLnRzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9hcHAvdml0ZS5jb25maWcudHNcIjtpbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tICd2aXRlJztcclxuaW1wb3J0IHJlYWN0IGZyb20gJ0B2aXRlanMvcGx1Z2luLXJlYWN0JztcclxuaW1wb3J0IHsgZmlsZVVSTFRvUGF0aCB9IGZyb20gJ3VybCc7XHJcbmltcG9ydCB7IGRpcm5hbWUsIHJlc29sdmUgfSBmcm9tICdwYXRoJztcclxuXHJcbmNvbnN0IF9fZmlsZW5hbWUgPSBmaWxlVVJMVG9QYXRoKGltcG9ydC5tZXRhLnVybCk7XHJcbmNvbnN0IF9fZGlybmFtZSA9IGRpcm5hbWUoX19maWxlbmFtZSk7XHJcblxyXG4vLyBodHRwczovL3ZpdGVqcy5kZXYvY29uZmlnL1xyXG5leHBvcnQgZGVmYXVsdCBkZWZpbmVDb25maWcoe1xyXG4gIHBsdWdpbnM6IFtyZWFjdCgpXSxcclxuICByZXNvbHZlOiB7XHJcbiAgICBhbGlhczoge1xyXG4gICAgICAnQCc6IHJlc29sdmUoX19kaXJuYW1lLCAnLi9zcmMnKSxcclxuICAgIH0sXHJcbiAgfSxcclxuICBzZXJ2ZXI6IHtcclxuICAgIHBvcnQ6IDUxNzMsXHJcbiAgICAvLyBQcm94eSBpcyBoYW5kbGVkIGJ5IE5naW54IG5vdywgc28gdGhpcyBzZWN0aW9uIGNhbiBiZSByZW1vdmVkIG9yIGNvbW1lbnRlZCBvdXRcclxuICAgIC8vIHByb3h5OiB7XHJcbiAgICAvLyAgICcvYXBpJzoge1xyXG4gICAgLy8gICAgIHRhcmdldDogcHJvY2Vzcy5lbnYuVklURV9BUElfVVJMIHx8ICdodHRwOi8vbG9jYWxob3N0OjgwMDAnLCAvLyBUaGlzIHBvaW50cyB0byBiYWNrZW5kIGRpcmVjdGx5LCBub3QgcHJveHlcclxuICAgIC8vICAgICBjaGFuZ2VPcmlnaW46IHRydWUsXHJcbiAgICAvLyAgICAgc2VjdXJlOiBmYWxzZSxcclxuICAgIC8vICAgfSxcclxuICAgIC8vIH0sXHJcbiAgICAvLyBITVIgY29uZmlndXJhdGlvbiAodXNlZnVsIHdoZW4gcnVubmluZyBpbiBEb2NrZXIpXHJcbiAgICBobXI6IHtcclxuICAgICAgcHJvdG9jb2w6ICd3cycsIC8vIFVzZSAnd3MnIGZvciBodHRwLCAnd3NzJyBmb3IgaHR0cHNcclxuICAgICAgaG9zdDogJ2xvY2FsaG9zdCcsIC8vIFVzZSB0aGUgaG9zdCBhY2Nlc3NpYmxlIGZyb20gdGhlIGJyb3dzZXIgKHZpYSBOZ2lueClcclxuICAgICAgcG9ydDogODAsIC8vIFVzZSB0aGUgTmdpbnggcHJveHkgcG9ydFxyXG4gICAgICAvLyBPcHRpb25hbDogSWYgSE1SIHN0aWxsIGZhaWxzLCBzcGVjaWZ5IGNsaWVudFBvcnQgZXhwbGljaXRseVxyXG4gICAgICAvLyBjbGllbnRQb3J0OiA4MFxyXG4gICAgfVxyXG4gIH0sXHJcbiAgb3B0aW1pemVEZXBzOiB7XHJcbiAgICBpbmNsdWRlOiBbXHJcbiAgICAgICdAbWFudGluZS9jb3JlJyxcclxuICAgICAgJ0BtYW50aW5lL2hvb2tzJyxcclxuICAgICAgJ0BtYW50aW5lL2Zvcm0nLFxyXG4gICAgICAnQG1hbnRpbmUvbm90aWZpY2F0aW9ucycsXHJcbiAgICAgICdAdGFibGVyL2ljb25zLXJlYWN0JywgLy8gRXhwbGljaXRseSBpbmNsdWRlIGljb24gbGlicmFyeVxyXG4gICAgICAnc3VwZXJ0b2tlbnMtYXV0aC1yZWFjdC9yZWNpcGUvc2Vzc2lvbicsXHJcbiAgICAgICdzdXBlcnRva2Vucy1hdXRoLXJlYWN0L3JlY2lwZS9lbWFpbHBhc3N3b3JkJ1xyXG4gICAgXSxcclxuICB9LFxyXG59KTsiXSwKICAibWFwcGluZ3MiOiAiO0FBQThMLFNBQVMsb0JBQW9CO0FBQzNOLE9BQU8sV0FBVztBQUNsQixTQUFTLHFCQUFxQjtBQUM5QixTQUFTLFNBQVMsZUFBZTtBQUgrRSxJQUFNLDJDQUEyQztBQUtqSyxJQUFNLGFBQWEsY0FBYyx3Q0FBZTtBQUNoRCxJQUFNLFlBQVksUUFBUSxVQUFVO0FBR3BDLElBQU8sc0JBQVEsYUFBYTtBQUFBLEVBQzFCLFNBQVMsQ0FBQyxNQUFNLENBQUM7QUFBQSxFQUNqQixTQUFTO0FBQUEsSUFDUCxPQUFPO0FBQUEsTUFDTCxLQUFLLFFBQVEsV0FBVyxPQUFPO0FBQUEsSUFDakM7QUFBQSxFQUNGO0FBQUEsRUFDQSxRQUFRO0FBQUEsSUFDTixNQUFNO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUEsSUFVTixLQUFLO0FBQUEsTUFDSCxVQUFVO0FBQUE7QUFBQSxNQUNWLE1BQU07QUFBQTtBQUFBLE1BQ04sTUFBTTtBQUFBO0FBQUE7QUFBQTtBQUFBLElBR1I7QUFBQSxFQUNGO0FBQUEsRUFDQSxjQUFjO0FBQUEsSUFDWixTQUFTO0FBQUEsTUFDUDtBQUFBLE1BQ0E7QUFBQSxNQUNBO0FBQUEsTUFDQTtBQUFBLE1BQ0E7QUFBQTtBQUFBLE1BQ0E7QUFBQSxNQUNBO0FBQUEsSUFDRjtBQUFBLEVBQ0Y7QUFDRixDQUFDOyIsCiAgIm5hbWVzIjogW10KfQo=
