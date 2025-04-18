import EmailPassword from 'supertokens-auth-react/recipe/emailpassword';
import Session from 'supertokens-auth-react/recipe/session';

// Define the proxy address (must match backend and how you access the app)
const PROXY_ADDRESS = "http://localhost"; // Assuming Nginx listens on port 80

// Import environment variables from Vite (still useful for appName)
const appName = import.meta.env.VITE_APP_NAME || 'AI Video Platform (React)';

// Define the SuperTokens configuration using the proxy address
export const SuperTokensConfig = {
  appInfo: {
    appName,
    apiDomain: PROXY_ADDRESS, // Use proxy address
    websiteDomain: PROXY_ADDRESS, // Use proxy address
    apiBasePath: "/auth", // Reverted base path
    websiteBasePath: "/auth/login", // Point redirect to the actual login route
  },
  recipeList: [
    EmailPassword.init({
      // No style object here; use CSS overrides if needed
      signInAndUpFeature: {
        signUpForm: {
          formFields: [
            { id: "email", label: "Email", placeholder: "Email" },
            { id: "password", label: "Password", placeholder: "Password" },
            { id: "username", label: "Username", placeholder: "Username" }
          ]
        }
      },
    }),
    Session.init({
      // Frontend doesn't set cookie attributes like sameSite; relies on backend.
      // tokenTransferMethod: "cookie" // Default is cookie
    }),
  ],
};
