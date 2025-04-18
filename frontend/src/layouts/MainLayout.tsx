import React from 'react'; // Reverted import
import { Outlet, Link, useNavigate } from 'react-router-dom';
import {
  AppShell,
  // Header, // Removed Header import
  Group,
  Text,
  Button,
  Menu, // Restore Menu
  Avatar,
  UnstyledButton, // Restore UnstyledButton
  Container,
  Burger,
  Drawer,
  Stack,
  Loader // Import Loader for session loading state
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { IconUser, IconLogout } from '@tabler/icons-react'; // Restore needed icons (IconLogout was already here)
import { useSessionContext } from 'supertokens-auth-react/recipe/session'; // Use SuperTokens context
import { signOut } from 'supertokens-auth-react/recipe/emailpassword'; // Use SuperTokens signout

// Removed dynamic import for IconUser

export const MainLayout: React.FC = () => { // Kept React.FC as TS errors are fixed
  const sessionContext = useSessionContext();
  const navigate = useNavigate();
  const [drawerOpened, { toggle: toggleDrawer, close: closeDrawer }] = useDisclosure(false);
  const [isLoggingOut, setIsLoggingOut] = React.useState(false); // Kept React.useState

  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      await signOut();
      navigate('/auth/login'); // Explicitly navigate after successful sign out
    } catch (error) {
      console.error("Logout failed:", error);
      // Handle logout error (e.g., show notification)
    } finally {
      setIsLoggingOut(false);
    }
  };

  // Display loading indicator while session is loading
  if (sessionContext.loading) {
    return (
      <AppShell header={{ height: 60 }} padding="md">
        {/* Use AppShell.Header directly */}
        <AppShell.Header>
          <Container size="xl" style={{ display: 'flex', alignItems: 'center', height: '100%' }}>
            <Loader size="sm" />
          </Container>
        </AppShell.Header>
        <AppShell.Main>
           {/* Optionally show a full page loader */}
        </AppShell.Main>
      </AppShell>
    );
  }

  // Extract user ID for display (email/username not directly available here)
  const userId = sessionContext.doesSessionExist ? sessionContext.userId : null;
  // Placeholder for user details - these should be fetched and potentially stored
  // in a separate context or state management solution after login/profile fetch.
  const userDisplayName = userId ? `User ${userId.substring(0, 6)}...` : 'Guest';
  const userInitial = userId ? 'U' : '?'; // Simple initial based on existence

  return (
    <AppShell
      header={{ height: 60 }}
      padding="md"
    >
      {/* Use AppShell.Header directly */}
      <AppShell.Header>
        <Container size="xl">
          <Group justify="space-between" h="100%" style={{ alignItems: 'center' }}>
            {/* Logo */}
            <Text size="xl" fw={700} component={Link} to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
              Creator Platform
            </Text>

            {/* Desktop Navigation */}
            <Group gap="xs" visibleFrom="sm" style={{ alignItems: 'center' }}> {/* Added alignment */}
              {/* User Menu - Only show if session exists */}
              {sessionContext.doesSessionExist && (
                <Menu position="bottom-end" withArrow>
                  <Menu.Target>
                    {/* Use UnstyledButton for better accessibility and click handling */}
                    <UnstyledButton style={{ display: 'flex', alignItems: 'center' }}>
                      <Avatar color="blue" radius="xl" size="lg"> {/* Kept larger size */}
                        {userInitial}
                      </Avatar>
                      {/* Optionally add user name or chevron icon here if desired */}
                    </UnstyledButton>
                  </Menu.Target>

                  <Menu.Dropdown>
                    <Menu.Item leftSection={<IconUser size={16} />} component={Link} to="/profile">
                      Profile
                    </Menu.Item>
                    <Menu.Divider />
                    <Menu.Item
                      leftSection={<IconLogout size={16} />}
                      onClick={handleLogout}
                      color="red"
                      disabled={isLoggingOut}
                    >
                      {isLoggingOut ? 'Logging out...' : 'Logout'}
                    </Menu.Item>
                  </Menu.Dropdown>
                </Menu>
              )}
              {/* Optionally show Login button if session doesn't exist */}
              {!sessionContext.doesSessionExist && (
                 <Button component={Link} to="/auth/login" variant="default">Login</Button>
              )}
            </Group>

            {/* Mobile Burger */}
            <Burger opened={drawerOpened} onClick={toggleDrawer} hiddenFrom="sm" />
          </Group>
        </Container>
      </AppShell.Header>

      {/* Mobile Navigation Drawer */}
      <Drawer
        opened={drawerOpened}
        onClose={closeDrawer}
        size="100%"
        padding="md"
        title="Navigation"
        hiddenFrom="sm"
        zIndex={1000}
      >
        <Stack>
          {sessionContext.doesSessionExist ? (
            <>
              <Button component={Link} to="/profile" variant="subtle" onClick={closeDrawer}>
                Profile
              </Button>
            </>
          ) : (
            <Button component={Link} to="/auth/login" variant="default" onClick={closeDrawer}>
              Login
            </Button>
          )}
        </Stack>
      </Drawer>

      <AppShell.Main>
        <Container size="xl" py="md">
          <Outlet /> {/* Child routes (like ProfilePage) render here */}
        </Container>
      </AppShell.Main>
    </AppShell>
  );
};
