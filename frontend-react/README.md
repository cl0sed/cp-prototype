# React/Mantine Frontend

This project is a React 19.1.0 frontend application using Mantine UI components to provide user authentication features including user signup, user login, and a protected user profile page.

## Architecture Overview

The application follows the architecture plan outlined in `docs/react_frontend_architecture.md` and includes:

- React 19.1.0 with TypeScript
- Mantine UI component library for the user interface
- React Router v6 for client-side navigation
- React Context API for global authentication state
- Form validation with Zod
- API communication using a custom service layer

## Core Features

1. **Authentication**
   - User signup with validation
   - User login with validation
   - Protected routes
   - User profile management

2. **UI Components**
   - Responsive layouts for both desktop and mobile
   - Form components with validation
   - User-friendly error handling and loading states

## Project Structure

```
frontend-react/
├── src/
│   ├── assets/            # Static assets
│   ├── components/        # Reusable UI components
│   ├── contexts/          # React context providers (AuthContext)
│   ├── hooks/             # Custom React hooks (useAuth)
│   ├── layouts/           # Page layout components (AuthLayout, MainLayout)
│   ├── pages/             # Page components
│   ├── routes/            # Routing configuration
│   ├── services/          # API services
│   └── utils/             # Utility functions
├── App.tsx                # Main App component
├── main.tsx               # Entry point
└── index.css              # Global styles
```

## Getting Started

1. Install dependencies:
   ```
   cd frontend-react
   npm install
   ```

2. Create a `.env` file in the root directory with:
   ```
   VITE_API_URL=http://localhost:8000
   ```

3. Start the development server:
   ```
   npm run dev
   ```

4. Build for production:
   ```
   npm run build
   ```

## Implementation Details

### Authentication Flow

The authentication flow uses React Context API to manage the global authentication state, including the user object and JWT token. The token is stored in localStorage for persistence between sessions.

### Protected Routes

Routes that require authentication are protected using the `ProtectedRoute` component, which redirects unauthenticated users to the login page.

### Form Validation

Forms are implemented using Mantine's form components with Zod schema validation, providing immediate feedback to users.

### API Integration

The application includes a service layer that handles API requests using the fetch API. The service automatically attaches authentication tokens to requests when available.

## Next Steps

1. Configure the API endpoints to match your backend
2. Implement additional features like password reset
3. Add end-to-end tests using Playwright
4. Deploy the application to a hosting provider
