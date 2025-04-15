<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { get } from '$lib/services/apiClient'; // Import the API client

	let { children } = $props();

	let backendApiStatus = $state('checking...');

	onMount(async () => {
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
</script>

<div class="layout">
	<!-- Add a status indicator at the top of the layout -->
	<div class="api-status">
		Backend API: <span class={backendApiStatus === 'OK' ? 'status-ok' : 'status-error'}>
			{backendApiStatus}
		</span>
	</div>

	{@render children()}
</div>

<style>
	.layout {
		max-width: 1200px;
		margin: 0 auto;
		padding: 1rem;
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
