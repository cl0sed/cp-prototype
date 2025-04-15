// Configuration file for SvelteKit
//
// This file configures the Svelte compiler and SvelteKit framework behavior.
//
// Key options:
// - `preprocess`: Configures preprocessors like `vitePreprocess` for handling TypeScript, SCSS, etc.
// - `kit`: SvelteKit specific options:
//   - `adapter`: Configures how the application is adapted for deployment (e.g., adapter-auto, adapter-node, adapter-static).
//   - `alias`: Defines path aliases (e.g., `$lib` for `src/lib`).
//   - `files`: Customizes file/directory names (e.g., `assets`, `routes`).
//   - `outDir`: Specifies the output directory for builds.
// - `compilerOptions`: Options passed directly to the Svelte compiler (e.g., `runes: true`).
//
// See: https://kit.svelte.dev/docs/configuration

// Example basic configuration (adapt as needed):
import adapter from '@sveltejs/adapter-auto'; // Or your chosen adapter
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(), // Enables TypeScript, PostCSS, SCSS, etc.

	kit: {
		adapter: adapter()
		// Add aliases if needed:
		// alias: {
		// 	// Example: '@components': 'src/lib/components'
		// }
	},

	compilerOptions: {
		// MANDATORY: Enable runes mode for Svelte 5
		runes: true
	}
};

export default config;
