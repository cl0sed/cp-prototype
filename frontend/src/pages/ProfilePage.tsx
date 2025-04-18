import React, { useEffect, useState } from 'react';
import {
  Paper,
  Title,
  Text,
  Grid,
  Card,
  Avatar,
  Group,
  Stack,
  Button,
  Divider,
  Box,
  Loader,
  Center,
  Alert
} from '@mantine/core';
import { IconPencil, IconKey, IconAlertCircleFilled } from '@tabler/icons-react';
import { useSessionContext } from 'supertokens-auth-react/recipe/session';
import EmailPassword from 'supertokens-auth-react/recipe/emailpassword';
import { apiService, ApiError } from '@/services/apiService'; // Use alias for import

// Define the expected shape of profile data from the backend
interface UserProfileData {
  id: string;
  email: string;
  username?: string;
}

const ProfilePage: React.FC = () => {
  const [profileData, setProfileData] = useState<UserProfileData | null>(null);
  const [loading, setLoading] = useState(true); // Component-level loading state for the API call
  const [error, setError] = useState<string | null>(null);
  const sessionContext = useSessionContext(); // Use the hook

  useEffect(() => {
    // Only proceed if session context is done loading
    if (!sessionContext.loading) {
      // Check if a session exists using doesSessionExist (available when loading is false)
      if (sessionContext.doesSessionExist) {
        setLoading(true); // Start loading profile data
        setError(null);

        // Fetch profile data from backend endpoint
        apiService.get<UserProfileData>('/api/user/profile') // Use apiService instance
          .then((data: UserProfileData) => { // Add type for data
            setProfileData(data);
          })
          .catch((err: Error | ApiError) => { // Add type for err
            console.error("Error fetching profile:", err);
            setError(err.message || 'Failed to load profile data.');
          })
          .finally(() => {
            setLoading(false); // Finish loading profile data
          });
      } else {
        // No session exists. SessionAuth should redirect, but stop loading state here.
        setLoading(false);
      }
    }
    // Depend on the entire sessionContext object or specific fields if preferred and stable
  }, [sessionContext]); // Using the whole context object is often safer

  const handleLogout = async () => {
    setLoading(true); // Show loading indicator during logout process
    setError(null);
    try {
      await EmailPassword.signOut();
      // SuperTokens handles redirection after sign out.
    } catch (err) {
      console.error("Logout failed:", err);
      setError("Logout failed. Please try again.");
      setLoading(false); // Stop loading only if logout fails
    }
  };

  // Show loading indicator while session context is loading OR profile data is loading
  if (sessionContext.loading || loading) {
    return (
      <Center style={{ height: '80vh' }}>
        <Loader size="xl" />
      </Center>
    );
  }

  // If session doesn't exist after loading (should be handled by SessionAuth, but as a fallback)
  if (!sessionContext.doesSessionExist) {
     return (
        <Center style={{ height: '80vh' }}>
           <Text>No active session. Redirecting...</Text>
           {/* SessionAuth should handle the redirect */}
        </Center>
     );
  }

  // Show error message if fetching profile data failed
  if (error) {
    return (
      <Center style={{ height: '80vh' }}>
        <Alert icon={<IconAlertCircleFilled size={16} />} title="Error Loading Profile" color="red">
          {error}
          <Button color="red" onClick={handleLogout} mt="md" loading={loading}>Logout</Button>
        </Alert>
      </Center>
    );
  }

  // If profile data hasn't loaded yet (edge case after loading flags are false)
  if (!profileData) {
    return (
      <Center style={{ height: '80vh' }}>
        <Text>Loading profile data...</Text>
      </Center>
    );
  }

  // Display profile information
  // Access userId directly from sessionContext now that we know doesSessionExist is true
  const sessionUserId = sessionContext.userId;

  return (
    <>
      <Group justify="space-between" mb="md">
        <Title order={1}>User Profile</Title>
        <Button color="red" onClick={handleLogout} loading={loading}>Logout</Button>
      </Group>

      <Grid gutter="md">
        {/* User Information Card */}
        <Grid.Col span={{ base: 12, md: 4 }}>
          <Paper shadow="sm" radius="md" p="lg" withBorder>
            <Stack align="center" mb="md">
              <Avatar size="xl" radius="xl" color="blue" src={null}>
                {profileData.username?.charAt(0)?.toUpperCase() || profileData.email.charAt(0).toUpperCase()}
              </Avatar>
              <Title order={3}>{profileData.username || 'User'}</Title>
              <Text c="dimmed" size="sm">{profileData.email}</Text>
            </Stack>
            <Divider my="sm" />
            <Stack>
              <Button leftSection={<IconPencil size={16} />} variant="outline" fullWidth disabled>
                Edit Profile (Not Implemented)
              </Button>
              <Button leftSection={<IconKey size={16} />} variant="outline" fullWidth disabled>
                Change Password (Not Implemented)
              </Button>
            </Stack>
          </Paper>
        </Grid.Col>

        {/* User Stats and Info */}
        <Grid.Col span={{ base: 12, md: 8 }}>
          <Grid>
            <Grid.Col span={12}>
              <Card shadow="sm" padding="lg" radius="md" withBorder>
                <Card.Section p="md">
                  <Title order={4}>Account Information</Title>
                </Card.Section>
                <Group mt="md" mb="xs">
                  <Text fw={500}>Username:</Text>
                  <Text>{profileData.username || '-'}</Text>
                </Group>
                <Group mb="xs">
                  <Text fw={500}>Email:</Text>
                  <Text>{profileData.email}</Text>
                </Group>
                <Group mb="xs">
                  <Text fw={500}>Backend User ID:</Text>
                  <Text>{profileData.id}</Text>
                </Group>
                <Group mb="xs">
                  <Text fw={500}>SuperTokens User ID:</Text>
                  <Text>{sessionUserId}</Text>
                </Group>
              </Card>
            </Grid.Col>
            {/* Add other sections like Recent Activity if needed */}
          </Grid>
        </Grid.Col>
      </Grid>
    </>
  );
};

export default ProfilePage;
