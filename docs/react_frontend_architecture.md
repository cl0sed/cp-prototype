# React/Mantine Frontend Architecture Plan

### 1. High-Level Architecture Description

The new frontend will be a Single Page Application (SPA) built with **React 19.1.0**. We will leverage **React Router v6** for client-side navigation and **Mantine UI** (latest stable version) for the component library, ensuring a consistent and modern user interface.

Global authentication state (user details, token, loading/error status) will be managed using the **React Context API**, potentially utilizing the new `use` hook for cleaner consumption.

Interaction with the existing backend API (presumably the FastAPI backend mentioned in the Memory Bank, potentially using SuperTokens for auth logic) will be handled through a dedicated service layer using the native **`fetch` API** or `axios`, incorporating basic request/response handling, including attaching authentication tokens.

We will emphasize creating reusable UI components using Mantine and structuring the application for scalability and maintainability. While React 19 Actions are available, for stability in this initial design, we'll focus on standard async function patterns for form submissions, noting Actions as a potential future enhancement.

### 2. Proposed Folder Structure

A clear folder structure is crucial for maintainability. We'll adopt a feature-oriented approach where feasible, grouped by technical concern:

```
/frontend-react/          # New root directory for the React app
├── public/               # Static assets (index.html, favicons, etc.)
├── src/                  # Application source code
│   ├── App.tsx           # Main application component (providers, router setup)
│   ├── main.tsx          # Application entry point (renders App)
│   ├── index.css         # Global styles (minimal, Mantine handles most)
│   │
│   ├── assets/           # Static assets like images, fonts
│   ├── components/       # Shared, reusable UI components (e.g., Button, Loader)
│   │   └── common/       # General purpose components
│   │   └── layout/       # Layout components (Header, Footer, Sidebar)
│   │
│   ├── contexts/         # React Context definitions and providers
│   │   └── AuthContext.tsx # Authentication state management
│   │
│   ├── hooks/            # Custom React hooks (e.g., useAuth, useApi)
│   │   └── useAuth.ts      # Hook to consume AuthContext
│   │
│   ├── layouts/          # Page layout wrappers (e.g., AuthLayout, MainLayout)
│   │   ├── AuthLayout.tsx  # Layout for unauthenticated pages (Login, Signup)
│   │   └── MainLayout.tsx  # Layout for authenticated pages (includes Header/Nav)
│   │
│   ├── pages/            # Page-level components, mapped to routes
│   │   ├── LoginPage.tsx
│   │   ├── SignupPage.tsx
│   │   └── ProfilePage.tsx
│   │   └── NotFoundPage.tsx
│   │
│   ├── routes/           # Routing configuration
│   │   ├── index.tsx       # Main router setup (AppRoutes)
│   │   └── ProtectedRoute.tsx # Component for protecting routes
│   │
│   ├── services/         # API interaction logic
│   │   ├── apiService.ts   # Base fetch/axios wrapper (handles base URL, auth headers)
│   │   └── authService.ts  # Specific auth-related API calls (login, signup)
│   │
│   └── utils/            # Utility functions (validators, formatters)
│       └── validators.ts
│
├── .eslintrc.cjs         # ESLint configuration
├── .gitignore
├── index.html            # Main HTML entry point (in /public usually handled by Vite)
├── package.json
├── tsconfig.json         # TypeScript configuration
├── tsconfig.node.json
└── vite.config.ts        # Vite build tool configuration
```

*(Note: This assumes Vite as the build tool, which is common for modern React projects).*

### 3. Key Component/Module Responsibilities

*   **`main.tsx`**: Entry point, renders `<App />`.
*   **`App.tsx`**: Sets up `MantineProvider`, `BrowserRouter`, and `AuthProvider`. Renders `AppRoutes`.
*   **`MantineProvider`**: (From `@mantine/core`) Wraps the entire application to provide theme context and global styles.
*   **`AuthProvider` (`/src/contexts/AuthContext.tsx`)**:
    *   Holds authentication state (e.g., `user`, `token`, `isAuthenticated`, `isLoading`, `error`).
    *   Provides functions (`login`, `signup`, `logout`) that interact with `authService`.
    *   Manages storing/clearing the auth token (e.g., in `localStorage`).
    *   Uses `React.createContext` and provides state/functions via the provider component.
*   **`useAuth` (`/src/hooks/useAuth.ts`)**: Custom hook for easy access to the `AuthContext` values (`useContext(AuthContext)` or `React.use(AuthContext)`).
*   **`AppRoutes` (`/src/routes/index.tsx`)**: Defines all application routes using `<Routes>` and `<Route>` from `react-router-dom`. Uses `ProtectedRoute` for authenticated routes.
*   **`ProtectedRoute` (`/src/routes/ProtectedRoute.tsx`)**:
    *   Checks `isAuthenticated` status from `AuthContext` (via `useAuth`).
    *   If authenticated, renders the child component (`<Outlet />` or `children`).
    *   If not authenticated, redirects the user to the login page (`<Navigate to="/login" />`).
*   **Layouts (`/src/layouts/`)**: Provide consistent page structure (e.g., `AuthLayout` for login/signup forms centered, `MainLayout` with header/navigation for logged-in users). Render `{children}` or `<Outlet />`.
*   **Pages (`/src/pages/`)**: Container components for specific routes. Fetch page-specific data (if any) and compose UI using smaller components.
    *   `LoginPage.tsx`, `SignupPage.tsx`: Render the respective forms.
    *   `ProfilePage.tsx`: Fetches/displays user data from `AuthContext` or a dedicated API call, wrapped by `ProtectedRoute`.
*   **Forms (`LoginForm.tsx`, `SignupForm.tsx` - potentially within `/pages` or `/components/auth/`)**:
    *   Use Mantine components (`TextInput`, `PasswordInput`, `Button`, `Checkbox`, etc.).
    *   Utilize Mantine's `useForm` hook (`@mantine/form`) for managing form state, validation (can integrate with Zod), and submission.
    *   On submit, call the relevant function from `AuthContext` (e.g., `login(formData)`).
    *   Display loading states (e.g., on buttons) and error messages (e.g., using Mantine `Alert` or `Notification`).
*   **`apiService.ts` (`/src/services/apiService.ts`)**: A wrapper around `fetch` or `axios`. Configures base URL, handles setting `Authorization` headers automatically by retrieving the token from `AuthContext` or `localStorage`, and potentially standardizes error handling.
*   **`authService.ts` (`/src/services/authService.ts`)**: Uses `apiService` to make specific calls to backend authentication endpoints (`/api/auth/login`, `/api/auth/signup`, etc.).

### 4. Illustrative Code Snippets

**a) AuthContext (`src/contexts/AuthContext.tsx`)**

```typescript
import React, { createContext, useState, useMemo, useEffect, useCallback } from 'react';
import { loginUser, signupUser, UserCredentials, UserData } from '../services/authService'; // Assuming these types/functions exist
import { apiService } from '../services/apiService'; // To set token for other requests

interface AuthContextType {
    user: UserData | null;
    token: string | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    error: string | null;
    login: (credentials: UserCredentials) => Promise<void>;
    signup: (credentials: UserCredentials) => Promise<void>; // Adjust credentials type as needed
    logout: () => void;
}

// Create context with a default value (can be undefined if checked properly)
export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<UserData | null>(null);
    const [token, setToken] = useState<string | null>(() => localStorage.getItem('authToken')); // Initialize from localStorage
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    // Effect to update user state if token exists on initial load (e.g., fetch user profile)
    useEffect(() => {
        if (token) {
            // Optionally: Verify token / fetch user profile here
            // For simplicity, we assume token presence means potential authentication
            // A dedicated fetch user profile call on load is better
            apiService.setAuthToken(token); // Configure apiService with the token
            // Example: fetchUserProfile().then(setUser).catch(() => logout());
        } else {
            setUser(null);
        }
    }, [token]);

    const login = useCallback(async (credentials: UserCredentials) => {
        setIsLoading(true);
        setError(null);
        try {
            const { token: newToken, user: loggedInUser } = await loginUser(credentials);
            setToken(newToken);
            setUser(loggedInUser);
            localStorage.setItem('authToken', newToken);
            apiService.setAuthToken(newToken);
        } catch (err: any) {
            setError(err.message || 'Login failed');
            // Consider more specific error handling
        } finally {
            setIsLoading(false);
        }
    }, []);

    const signup = useCallback(async (credentials: UserCredentials) => {
        setIsLoading(true);
        setError(null);
        try {
            // Assuming signup API might automatically log in or just create user
            await signupUser(credentials);
            // Optionally: Call login() automatically or redirect to login page
        } catch (err: any) {
            setError(err.message || 'Signup failed');
        } finally {
            setIsLoading(false);
        }
    }, []);


    const logout = useCallback(() => {
        setUser(null);
        setToken(null);
        localStorage.removeItem('authToken');
        apiService.setAuthToken(null); // Clear token in apiService
        // Redirect logic might happen in the component calling logout or via router state
    }, []);

    // Memoize context value to prevent unnecessary re-renders
    const value = useMemo(() => ({
        user,
        token,
        isAuthenticated: !!token, // Simple check, might need refinement based on token validation
        isLoading,
        error,
        login,
        signup,
        logout,
    }), [user, token, isLoading, error, login, signup, logout]);

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook (in src/hooks/useAuth.ts)
// import React, { useContext } from 'react';
// import { AuthContext } from '../contexts/AuthContext';
// export const useAuth = () => {
//     const context = useContext(AuthContext); // or React.use(AuthContext) in React 19+ components
//     if (context === undefined) {
//         throw new Error('useAuth must be used within an AuthProvider');
//     }
//     return context;
// };
```

**b) ProtectedRoute (`src/routes/ProtectedRoute.tsx`)**

```typescript
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth'; // Assuming useAuth hook exists

interface ProtectedRouteProps {
    // Optional: Add role-based access control props if needed
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = () => {
    const { isAuthenticated, isLoading } = useAuth();

    // Optional: Show a loading spinner while auth state is being determined initially
    if (isLoading) {
         // return <LoadingOverlay visible={true} />; // Example using Mantine Loader
         return <div>Loading...</div>; // Placeholder
    }

    return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};
```

**c) LoginForm Submission Example (within `src/pages/LoginPage.tsx` or a component)**

```typescript
import React from 'react';
import { useForm, zodResolver } from '@mantine/form';
import { TextInput, PasswordInput, Button, Box, Alert, LoadingOverlay } from '@mantine/core';
import { z } from 'zod';
import { useAuth } from '../hooks/useAuth';
import { IconAlertCircle } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom'; // For redirection

// Zod schema for validation
const schema = z.object({
    email: z.string().email({ message: 'Invalid email address' }),
    password: z.string().min(6, { message: 'Password must be at least 6 characters long' }),
});

export const LoginForm: React.FC = () => {
    const { login, isLoading, error } = useAuth();
    const navigate = useNavigate();

    const form = useForm({
        initialValues: {
            email: '',
            password: '',
        },
        validate: zodResolver(schema),
    });

    const handleSubmit = async (values: typeof form.values) => {
        await login(values);
        // Check if login was successful (e.g., error is null after await)
        // Note: The AuthProvider handles setting state. We might need to check the state *after* await.
        // A better approach might be for login() to return success/failure or throw on error.
        // Assuming login throws on error or sets error state reliably:
        if (!error) { // This check might be slightly delayed depending on state updates
             navigate('/profile'); // Redirect on successful login
        }
    };

    return (
        <Box maw={340} mx="auto" pos="relative">
            <LoadingOverlay visible={isLoading} overlayProps={{ radius: "sm", blur: 2 }} />
            <form onSubmit={form.onSubmit(handleSubmit)}>
                {error && (
                    <Alert icon={<IconAlertCircle size="1rem" />} title="Login Failed" color="red" withCloseButton onClose={() => form.setFieldError('root', null)} mb="md">
                        {error}
                    </Alert>
                )}

                <TextInput
                    required
                    label="Email"
                    placeholder="your@email.com"
                    {...form.getInputProps('email')}
                    mb="sm"
                />

                <PasswordInput
                    required
                    label="Password"
                    placeholder="Your password"
                    {...form.getInputProps('password')}
                    mb="md"
                />

                <Button type="submit" fullWidth loading={isLoading}>
                    Login
                </Button>
            </form>
        </Box>
    );
};
```

### 5. Mermaid Diagram (Component Interaction - Login Flow)

```mermaid
sequenceDiagram
    participant User
    participant LoginForm
    participant AuthContext
    participant AuthService
    participant BackendAPI

    User->>LoginForm: Enters credentials
    User->>LoginForm: Clicks Login Button
    LoginForm->>LoginForm: Validate form (useForm/Zod)
    alt Form Invalid
        LoginForm->>User: Show validation errors
    else Form Valid
        LoginForm->>AuthContext: call login(credentials)
        AuthContext->>AuthContext: Set isLoading=true, clear error
        AuthContext->>AuthService: loginUser(credentials)
        AuthService->>BackendAPI: POST /api/auth/login (credentials)
        BackendAPI-->>AuthService: Return {token, user} or error
        alt Login Success
            AuthService-->>AuthContext: Return {token, user}
            AuthContext->>AuthContext: Set token, user, isLoading=false
            AuthContext->>LocalStorage: Store token
            AuthContext->>ApiService: Set auth token
            LoginForm->>ReactRouter: Navigate to /profile
        else Login Failure
            AuthService-->>AuthContext: Throw error
            AuthContext->>AuthContext: Set error, isLoading=false
            AuthContext-->>LoginForm: Return error state
            LoginForm->>User: Show error message (Alert)
        end
    end
