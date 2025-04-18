import React from 'react';
import { useForm, zodResolver } from '@mantine/form';
import {
  TextInput,
  PasswordInput,
  Button,
  Box,
  Alert,
  Paper,
  Title,
  Divider,
  Text,
  Group,
  Anchor
} from '@mantine/core';
import { z } from 'zod';
import { Link, useNavigate } from 'react-router-dom';
import { IconAlertCircle } from '@tabler/icons-react';
import { useAuth } from '../hooks/useAuth';

// Validation schema with Zod
const schema = z.object({
  email: z
    .string()
    .min(1, { message: 'Email is required' })
    .email({ message: 'Invalid email address' }),
  password: z
    .string()
    .min(6, { message: 'Password must be at least 6 characters' }),
});

const LoginPage: React.FC = () => {
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
    try {
      await login(values);
      navigate('/profile');
    } catch (err) {
      // Error is handled in AuthContext, no need to do anything here
    }
  };

  return (
    <Paper shadow="md" p="lg" radius="md" withBorder>
      <Title order={2} mb="md" ta="center">Welcome back</Title>
      <form onSubmit={form.onSubmit(handleSubmit)}>
        {error && (
          <Alert
            icon={<IconAlertCircle size="1rem" />}
            title="Login Failed"
            color="red"
            variant="filled"
            mb="md"
          >
            {error}
          </Alert>
        )}

        <TextInput
          withAsterisk
          label="Email"
          placeholder="your@email.com"
          {...form.getInputProps('email')}
          mb="md"
        />

        <PasswordInput
          withAsterisk
          label="Password"
          placeholder="Your password"
          {...form.getInputProps('password')}
          mb="xl"
        />

        <Button
          type="submit"
          fullWidth
          loading={isLoading}
        >
          Sign in
        </Button>
      </form>

      <Divider my="md" label="Don't have an account?" labelPosition="center" />

      <Group justify="center">
        <Anchor component={Link} to="/signup" size="sm">
          Create account
        </Anchor>
      </Group>
    </Paper>
  );
};

export default LoginPage;
