<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { get } from '$lib/services/apiClient'; // Import the API client
	import { initializeSuperTokens, isUserLoggedIn, signOut } from '$lib/auth/supertokens';

	let { children } = $props();

	let backendApiStatus = $state('checking...');
	let userLoggedIn = $state(false);

	onMount(async () => {
		// Initialize SuperTokens
		initializeSuperTokens();

		// Check if user is logged in
		userLoggedIn = await isUserLoggedIn();

		console.log(`Checking backend health using API client...`);
		try {
			// Use the API client's get method instead of direct fetch
			const data = await get('/health');
			// Assuming the /health endpoint returns { "status": "ok" }
			backendApiStatus = data.status === 'ok' ? 'OK' : 'Unexpected Response';
			console.log('Backend /health check successful:', data);
		} catch (error) {
			backendApiStatus = 'Unreachable';
			console.error('Error fetching backend /health status:', error);
		}
	});

	// Handle logout
	async function handleLogout() {
		try {
			await signOut();
			userLoggedIn = false;
			window.location.href = '/'; // Redirect to home page after logout
		} catch (error) {
			console.error('Error signing out:', error);
		}
	}
</script>

<div class="layout">
	<!-- Navigation bar -->
	<nav class="navbar">
		<div class="nav-brand">AI Video Platform</div>
		<div class="nav-links">
			<a href="/" class="nav-link">Home</a>
			{#if userLoggedIn}
				<a href="/dashboard" class="nav-link">Dashboard</a>
				<button on:click={handleLogout} class="nav-button logout-button">Logout</button>
			{:else}
				<a href="/auth" class="nav-button login-button">Login</a>
			{/if}
		</div>
	</nav>

	<!-- API Status indicator -->
	<div class="api-status">
		Backend API: <span class={backendApiStatus === 'OK' ? 'status-ok' : 'status-error'}>
			{backendApiStatus}
		</span>
	</div>

	<!-- Main content -->
	{@render children()}
</div>

<style>
	.layout {
		max-width: 1200px;
		margin: 0 auto;
		padding: 1rem;
	}

	.navbar {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem 0;
		margin-bottom: 1rem;
		border-bottom: 1px solid #eaeaea;
	}

	.nav-brand {
		font-size: 1.25rem;
		font-weight: bold;
	}

	.nav-links {
		display: flex;
		gap: 1rem;
		align-items: center;
	}

	.nav-link {
		text-decoration: none;
		color: #333;
	}

	.nav-link:hover {
		text-decoration: underline;
	}

	.nav-button {
		padding: 0.5rem 1rem;
		border-radius: 4px;
		border: none;
		cursor: pointer;
		font-size: 0.875rem;
	}

	.login-button {
		background-color: #4f46e5;
		color: white;
		text-decoration: none;
	}

	.logout-button {
		background-color: #ef4444;
		color: white;
	}

	.api-status {
		padding: 0.5rem;
		margin-bottom: 1rem;
		border-radius: 4px;
		background-color: #f5f5f5;
		font-size: 0.875rem;
	}

	.status-ok {
		color: green;
		font-weight: bold;
	}

	.status-error {
		color: red;
		font-weight: bold;
	}
</style>
