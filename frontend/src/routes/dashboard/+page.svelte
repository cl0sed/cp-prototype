<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { isUserLoggedIn, getUserId } from '$lib/auth/supertokens';

  let userLoggedIn = $state(false);
  let userId = $state<string | undefined>(undefined);
  let loading = $state(true);

  onMount(async () => {
    loading = true;

    try {
      userLoggedIn = await isUserLoggedIn();

      if (!userLoggedIn) {
        // Redirect to login page if not authenticated
        goto('/auth');
        return;
      }

      // Get user ID if logged in
      userId = await getUserId();
    } catch (error) {
      console.error('Error checking authentication:', error);
    } finally {
      loading = false;
    }
  });
</script>

<div class="dashboard-container">
  {#if loading}
    <div class="loading">
      <p>Loading dashboard...</p>
    </div>
  {:else if userLoggedIn}
    <div class="dashboard-content">
      <h1>Dashboard</h1>
      <p>Welcome to your personal dashboard!</p>

      <div class="user-info">
        <h2>User Information</h2>
        <p>User ID: <code>{userId || 'Unknown'}</code></p>
      </div>

      <div class="dashboard-cards">
        <div class="dashboard-card">
          <h3>Projects</h3>
          <p>You don't have any projects yet.</p>
          <button class="button">Create New Project</button>
        </div>

        <div class="dashboard-card">
          <h3>Creator DNA Profiles</h3>
          <p>No DNA profiles created yet.</p>
          <button class="button">Create DNA Profile</button>
        </div>

        <div class="dashboard-card">
          <h3>Recent Activity</h3>
          <p>No recent activity to display.</p>
        </div>
      </div>
    </div>
  {:else}
    <div class="unauthorized">
      <h1>Unauthorized</h1>
      <p>You need to be logged in to view this page.</p>
      <a href="/auth" class="button">Log In</a>
    </div>
  {/if}
</div>

<style>
  .dashboard-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  h1 {
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  h2 {
    font-size: 1.5rem;
    margin: 1.5rem 0 1rem;
  }

  h3 {
    font-size: 1.25rem;
    margin-bottom: 0.75rem;
  }

  .loading {
    text-align: center;
    padding: 2rem;
  }

  .user-info {
    background-color: #f3f4f6;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 2rem;
  }

  .user-info code {
    background-color: #e5e7eb;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-family: monospace;
  }

  .dashboard-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .dashboard-card {
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 1.5rem;
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
    margin-top: 1rem;
  }

  .button:hover {
    background-color: #4338ca;
  }

  .unauthorized {
    text-align: center;
    padding: 3rem 1rem;
  }

  .unauthorized p {
    margin-bottom: 1.5rem;
  }
</style>
