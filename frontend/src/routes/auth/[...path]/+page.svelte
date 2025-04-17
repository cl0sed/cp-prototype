<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import SuperTokensWebJS from 'supertokens-web-js';
  import EmailPassword from 'supertokens-web-js/recipe/emailpassword';
  import Session from 'supertokens-web-js/recipe/session';

  onMount(() => {
    // Initialize SuperTokens with minimal configuration
    SuperTokensWebJS.init({
      appInfo: {
        appName: "AI Video Platform",
        apiDomain: "http://backend:8000",
        apiBasePath: "/auth"
      },
      recipeList: [
        EmailPassword.init(),
        Session.init()
      ]
    });

    // Check if the user is already logged in
    Session.doesSessionExist().then(exists => {
      if (exists) {
        // User is already logged in, redirect to home page
        goto('/');
      } else {
        // Basic auth UI - create simple sign-in/sign-up form
        const container = document.getElementById('auth-container');
        if (container) {
          // Get the path to determine if we're showing sign-in or sign-up
          const path = window.location.pathname.split('/').pop();

          if (path === 'signin' || path === 'sign-in') {
            renderSignInForm(container);
          } else if (path === 'signup' || path === 'sign-up') {
            renderSignUpForm(container);
          } else {
            // Default to sign-in
            renderSignInForm(container);
          }
        }
      }
    });
  });

  function renderSignInForm(container: HTMLElement) {
    container.innerHTML = `
      <div class="auth-form">
        <h2>Sign In</h2>
        <form id="signin-form">
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" required>
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" required>
          </div>
          <div class="form-actions">
            <button type="submit">Sign In</button>
          </div>
          <div class="form-links">
            <a href="/auth/signup">Don't have an account? Sign up</a>
          </div>
        </form>
        <div id="error-message" class="error-message"></div>
      </div>
    `;

    const form = document.getElementById('signin-form');
    form?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const emailInput = document.getElementById('email') as HTMLInputElement;
      const passwordInput = document.getElementById('password') as HTMLInputElement;
      const errorDisplay = document.getElementById('error-message');

      try {
        const response = await EmailPassword.signIn({
          formFields: [
            { id: "email", value: emailInput.value },
            { id: "password", value: passwordInput.value }
          ]
        });

        if (response.status === "OK") {
          // Redirect to home page
          goto('/');
        } else {
          // Handle other statuses
          if (errorDisplay) errorDisplay.textContent = "Sign in failed. Please check your credentials.";
        }
      } catch (error) {
        console.error("Sign in error:", error);
        if (errorDisplay) errorDisplay.textContent = "An error occurred. Please try again.";
      }
    });
  }

  function renderSignUpForm(container: HTMLElement) {
    container.innerHTML = `
      <div class="auth-form">
        <h2>Sign Up</h2>
        <form id="signup-form">
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" required>
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" required>
          </div>
          <div class="form-actions">
            <button type="submit">Sign Up</button>
          </div>
          <div class="form-links">
            <a href="/auth/signin">Already have an account? Sign in</a>
          </div>
        </form>
        <div id="error-message" class="error-message"></div>
      </div>
    `;

    const form = document.getElementById('signup-form');
    form?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const emailInput = document.getElementById('email') as HTMLInputElement;
      const passwordInput = document.getElementById('password') as HTMLInputElement;
      const errorDisplay = document.getElementById('error-message');

      try {
        const response = await EmailPassword.signUp({
          formFields: [
            { id: "email", value: emailInput.value },
            { id: "password", value: passwordInput.value }
          ]
        });

        if (response.status === "OK") {
          // Redirect to home page or sign-in
          goto('/');
        } else {
          // Handle other statuses
          if (errorDisplay) errorDisplay.textContent = "Sign up failed. Please try again.";
        }
      } catch (error) {
        console.error("Sign up error:", error);
        if (errorDisplay) errorDisplay.textContent = "An error occurred. Please try again.";
      }
    });
  }
</script>

<div id="auth-container" class="auth-container"></div>

<style>
  .auth-container {
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .auth-form {
    width: 100%;
    max-width: 400px;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    background-color: white;
  }

  .form-group {
    margin-bottom: 1rem;
  }

  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
  }

  .form-group input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  .form-actions {
    margin-top: 1.5rem;
  }

  .form-actions button {
    width: 100%;
    padding: 0.75rem;
    background-color: #4f46e5;
    color: white;
    border: none;
    border-radius: 4px;
    font-weight: 500;
    cursor: pointer;
  }

  .form-actions button:hover {
    background-color: #4338ca;
  }

  .form-links {
    margin-top: 1rem;
    text-align: center;
  }

  .form-links a {
    color: #4f46e5;
    text-decoration: none;
  }

  .error-message {
    color: #ef4444;
    margin-top: 1rem;
    text-align: center;
  }
</style>
