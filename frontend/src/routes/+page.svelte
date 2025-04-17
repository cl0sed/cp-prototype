<script lang="ts">
  import { onMount } from 'svelte';
  import { isUserLoggedIn } from '$lib/auth/supertokens';
  import { agentInteract } from '$lib/services/apiClient';

  let userLoggedIn = $state(false);
  let agentResponse = $state(null);
  let loading = $state(false);
  let error = $state<string | null>(null);

  onMount(async () => {
    userLoggedIn = await isUserLoggedIn();
  });

  async function testProtectedEndpoint() {
    loading = true;
    error = null;

    try {
      const response = await agentInteract({ message: "Hello Agent" });
      agentResponse = response;
    } catch (err) {
      error = err instanceof Error ? err.message : 'An unknown error occurred';
      console.error('Error testing protected endpoint:', err);
    } finally {
      loading = false;
    }
  }
</script>

<div class="container">
  <h1>AI Video Platform</h1>

  {#if userLoggedIn}
    <div class="authenticated-content">
      <h2>Welcome, Authenticated User!</h2>
      <p>You are successfully logged in and can access protected features.</p>

      <div class="card">
        <h3>Test Protected API Endpoint</h3>
        <p>Click the button below to test the protected /agent/interact endpoint:</p>

        <button on:click={testProtectedEndpoint} disabled={loading} class="button">
          {loading ? 'Loading...' : 'Test Protected Endpoint'}
        </button>

        {#if agentResponse}
          <div class="response-box success">
            <h4>Response from Protected Endpoint:</h4>
            <pre>{JSON.stringify(agentResponse, null, 2)}</pre>
          </div>
        {/if}

        {#if error}
          <div class="response-box error">
            <h4>Error:</h4>
            <p>{error}</p>
          </div>
        {/if}
      </div>
    </div>
  {:else}
    <div class="unauthenticated-content">
      <h2>Welcome to the AI Video Platform</h2>
      <p>This platform helps content creators drastically reduce pre-production time for educational videos.</p>

      <div class="features">
        <div class="feature-card">
          <h3>Creator DNA Technology</h3>
          <p>Captures your unique linguistic patterns, terminology, pacing, tone, and teaching style.</p>
        </div>

        <div class="feature-card">
          <h3>Pre-Production Accelerator</h3>
          <p>Automates time-consuming tasks like research, content structuring, and initial script drafting.</p>
        </div>

        <div class="feature-card">
          <h3>Human-in-the-Loop Workflow</h3>
          <p>You maintain control with an AI assistant that guides you through the pre-production process.</p>
        </div>
      </div>

      <div class="cta-container">
        <p>Please log in to access the platform features:</p>
        <a href="/auth" class="button">Log In / Sign Up</a>
      </div>
    </div>
  {/if}
</div>

<style>
  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  h1 {
    font-size: 2rem;
    margin-bottom: 2rem;
    text-align: center;
  }

  h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }

  .card {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 1.5rem;
    margin-top: 2rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .button {
    background-color: #4f46e5;
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    border: none;
    cursor: pointer;
    font-size: 1rem;
    display: inline-block;
    text-decoration: none;
  }

  .button:hover {
    background-color: #4338ca;
  }

  .button:disabled {
    background-color: #9ca3af;
    cursor: not-allowed;
  }

  .response-box {
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 4px;
    background-color: #f3f4f6;
  }

  .response-box.success {
    border-left: 4px solid #10b981;
  }

  .response-box.error {
    border-left: 4px solid #ef4444;
    background-color: #fee2e2;
  }

  pre {
    white-space: pre-wrap;
    word-break: break-word;
    background-color: #f3f4f6;
    padding: 0.5rem;
    border-radius: 4px;
    overflow-x: auto;
  }

  .features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
  }

  .feature-card {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .feature-card h3 {
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
    color: #4f46e5;
  }

  .cta-container {
    text-align: center;
    margin-top: 2rem;
  }
</style>
