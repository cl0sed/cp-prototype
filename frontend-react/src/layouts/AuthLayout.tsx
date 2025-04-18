import React from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import { Box, Center, Container, Image, Title, Text, Stack } from '@mantine/core';
import { useAuth } from '../hooks/useAuth';

export const AuthLayout: React.FC = () => {
  const { isAuthenticated } = useAuth();

  // If already authenticated, redirect to profile
  if (isAuthenticated) {
    return <Navigate to="/profile" replace />;
  }

  return (
    <Container size="md" py="xl">
      <Center maw={400} mx="auto">
        <Stack w="100%">
          <Box ta="center" mb="lg">
            <Title order={1} mb="xs">Content Creator Platform</Title>
            <Text c="dimmed" size="sm">Sign in to access the platform</Text>
          </Box>

          <Outlet />
        </Stack>
      </Center>
    </Container>
  );
};
