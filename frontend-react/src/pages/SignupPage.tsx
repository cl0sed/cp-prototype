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
  username: z
    .string()
    .min(3, { message: 'Username must be at least 3 characters' }),
  email: z
    .string()
    .min(1, { message: 'Email is required' })
    .email({ message: 'Invalid email address' }),
  password: z
    .string()
    .min(8, { message: 'Password must be at least 8 characters' }),
  confirmPassword: z
    .string()
    .min(1, { message: 'Confirm your password' })
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

const SignupPage: React.FC = () => {
  const { signup, isLoading, error } = useAuth();
  const navigate = useNavigate();

  const form = useForm({
    initialValues: {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
    },
    validate: zodResolver(schema),
  });

  const handleSubmit = async (values: typeof form.values) => {
    try {
      // Exclude confirmPassword from the API request
      const { confirmPassword, ...signupData } = values;
      await signup(signupData);
      navigate('/profile');
    } catch (err) {
      // Error is handled in AuthContext, no need to do anything here
    }
  };

  return (
    <Paper shadow="md" p="lg" radius="md" withBorder>
      <Title order={2} mb="md" ta="center">Create an account</Title>
      <form onSubmit={form.onSubmit(handleSubmit)}>
        {error && (
          <Alert
            icon={<IconAlertCircle size="1rem" />}
            title="Signup Failed"
            color="red"
            variant="filled"
            mb="md"
          >
            {error}
          </Alert>
        )}

        <TextInput
          withAsterisk
          label="Username"
          placeholder="Your username"
          {...form.getInputProps('username')}
          mb="md"
        />

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
          placeholder="Create a password"
          {...form.getInputProps('password')}
          mb="md"
        />

        <PasswordInput
          withAsterisk
          label="Confirm Password"
          placeholder="Confirm your password"
          {...form.getInputProps('confirmPassword')}
          mb="xl"
        />

        <Button
          type="submit"
          fullWidth
          loading={isLoading}
        >
          Create account
        </Button>
      </form>

      <Divider my="md" label="Already have an account?" labelPosition="center" />

      <Group justify="center">
        <Anchor component={Link} to="/login" size="sm">
          Log in
        </Anchor>
      </Group>
    </Paper>
  );
};

export default SignupPage;
