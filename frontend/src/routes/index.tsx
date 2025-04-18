import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { SessionAuth } from 'supertokens-auth-react/recipe/session';
import { MainLayout } from '../layouts/MainLayout';

// Pages
import ProfilePage from '../pages/ProfilePage';
import NotFoundPage from '../pages/NotFoundPage';
import LoginPage from '../pages/auth/LoginPage';
import SignupPage from '../pages/auth/SignupPage';

const AppRoutes = () => {
  return (
    <Routes>
      {/* Auth routes */}
      <Route path="/auth">
        <Route path="login" element={<LoginPage />} />
        <Route path="signup" element={<SignupPage />} />
      </Route>

      {/* Protected routes wrapped with SessionAuth */}
      <Route
        element={
          <SessionAuth>
            <MainLayout />
          </SessionAuth>
        }
      >
        <Route path="/profile" element={<ProfilePage />} />
        {/* Add more authenticated routes here */}
      </Route>

      {/* Redirect home to profile */}
      <Route path="/" element={<Navigate to="/profile" replace />} />

      {/* 404 Not Found */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};

export default AppRoutes;
