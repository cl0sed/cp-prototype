// Configuration file for Vite (Build Tool)
//
// This file configures Vite, the build tool used by SvelteKit.
//
// Key configurations:
// - `plugins`: Must include the `sveltekit()` plugin.
//             Add other Vite plugins here (e.g., for image optimization, PWA support).
// - `server`: Configure the development server (port, proxy, HTTPS).
// - `build`: Configure the production build (output directory, minification, chunking).
// - `resolve`: Configure module resolution (aliases - though usually managed in svelte.config.js).
//
// Customize this file primarily for adding Vite plugins or tweaking dev server/build options.
// SvelteKit handles most of the core Vite setup via its plugin.
// See: https://vitejs.dev/config/

import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [
		sveltekit() // SvelteKit plugin is essential
		// Add other Vite plugins here if needed
	],
	// Example: Configure dev server port
	// server: {
	// 	port: 5173
	// },
	// Example: Add build options if needed
	// build: {
	// 	target: 'esnext'
	// }
});
