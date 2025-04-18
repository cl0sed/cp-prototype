import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import {
  TextInput,
  PasswordInput,
  Paper,
  Title,
  Container,
  Button,
  Text,
  Anchor,
  Group,
  Stack,
  Alert
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { IconAlertCircleFilled } from '@tabler/icons-react';
import { signIn } from 'supertokens-auth-react/recipe/emailpassword';

interface LoginFormValues {
  email: string;
  password: string;
}

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [error, setError] = React.useState<string | null>(null);
  const [loading, setLoading] = React.useState(false);

  const form = useForm<LoginFormValues>({
    initialValues: {
      email: '',
      password: '',
    },
    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
      password: (value) => (value.length >= 8 ? null : 'Password should be at least 8 characters'),
    },
  });

  const handleSubmit = async (values: LoginFormValues) => {
    try {
      setLoading(true);
      setError(null);

      // Using SuperTokens signIn function from the SDK
      const response = await signIn({
        formFields: [
          {
            id: "email",
            value: values.email
          },
          {
            id: "password",
            value: values.password
          }
        ]
      });

      if (response.status === "OK") {
        // Successfully logged in
        // Determine where to redirect - either the page they were trying to access or profile
        const redirectTo = (location.state as any)?.from?.pathname || '/profile';
        navigate(redirectTo);
      } else {
        // Sign-in failed due to invalid credentials
        if (response.status === "WRONG_CREDENTIALS_ERROR") {
          setError('Invalid email or password');
        } else {
          setError('Something went wrong. Please try again.');
        }
      }
    } catch (err: any) {
      console.error('Login error:', err);
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container size={420} my={40}>
      <Title ta="center" fw={900}>
        Welcome back!
      </Title>
      <Text c="dimmed" size="sm" ta="center" mt={5}>
        Don't have an account yet?{' '}
        <Anchor size="sm" component={Link} to="/auth/signup">
          Create account
        </Anchor>
      </Text>

      <Paper withBorder shadow="md" p={30} mt={30} radius="md">
        {error && (
          <Alert icon={<IconAlertCircleFilled size={16} />} color="red" mb="lg">
            {error}
          </Alert>
        )}

        <form onSubmit={form.onSubmit(handleSubmit)}>
          <Stack>
            <TextInput
              required
              label="Email"
              placeholder="your@email.com"
              {...form.getInputProps('email')}
            />

            <PasswordInput
              required
              label="Password"
              placeholder="Your password"
              {...form.getInputProps('password')}
            />
          </Stack>

          <Group justify="space-between" mt="lg">
            <Anchor component={Link} to="#" size="sm">
              Forgot password?
            </Anchor>
          </Group>

          <Button type="submit" fullWidth mt="xl" loading={loading}>
            Sign in
          </Button>
        </form>
      </Paper>
    </Container>
  );
};

export default LoginPage;
