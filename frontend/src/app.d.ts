// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces

// Environment variable type definitions
interface ImportMetaEnv {
	readonly PUBLIC_API_BASE_URL: string;
	// Add other PUBLIC_ variables here as needed
}

interface ImportMeta {
	readonly env: ImportMetaEnv;
}

declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
