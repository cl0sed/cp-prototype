import React from 'react'; // Reverted import
import { Outlet, Link, useNavigate } from 'react-router-dom';
import {
  AppShell,
  // Header, // Removed Header import
  Group,
  Text,
  Button,
  Menu,
  Avatar,
  UnstyledButton,
  Container,
  Box,
  Burger,
  Drawer,
  Stack,
  Loader // Import Loader for session loading state
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { IconUser, IconLogout, IconChevronDown } from '@tabler/icons-react'; // Re-added IconUser
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
      // SuperTokens handles redirection, but you might want to navigate explicitly
      // navigate('/auth/login'); // Optional: navigate after signout if needed
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
          <Group justify="space-between" h="100%">
            {/* Logo */}
            <Text size="xl" fw={700} component={Link} to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
              Creator Platform
            </Text>

            {/* Desktop Navigation */}
            <Group gap="xs" visibleFrom="sm">
              <Button component={Link} to="/profile" variant="subtle">
                Profile
              </Button>

              {/* User Menu - Only show if session exists */}
              {sessionContext.doesSessionExist && (
                <Menu position="bottom-end" withArrow>
                  <Menu.Target>
                    <UnstyledButton>
                      <Group gap="xs">
                        <Avatar color="blue" radius="xl">
                          {userInitial}
                        </Avatar>
                        <Box>
                          {/* Display placeholder or fetched name */}
                          <Text size="sm" fw={500}>{userDisplayName}</Text>
                          {/* Email is not available in session context directly */}
                          {/* <Text size="xs" c="dimmed">{user?.email}</Text> */}
                        </Box>
                        <IconChevronDown size={16} />
                      </Group>
                    </UnstyledButton>
                  </Menu.Target>

                  <Menu.Dropdown>
                    {/* Reverted IconUser usage */}
                    <Menu.Item leftSection={<IconUser size={16} />} component={Link} to="/profile">
                      Profile
                    </Menu.Item>
                    <Menu.Divider />
                    <Menu.Item
                      leftSection={<IconLogout size={16} />}
                      onClick={handleLogout}
                      color="red"
                      disabled={isLoggingOut} // Disable button during logout
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
              <Button color="red" onClick={handleLogout} loading={isLoggingOut}>
                Logout
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
