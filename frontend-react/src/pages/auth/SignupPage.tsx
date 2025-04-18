import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
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
import { signUp } from 'supertokens-auth-react/recipe/emailpassword';

interface SignupFormValues {
  email: string;
  password: string;
  username: string;
}

const SignupPage: React.FC = () => {
  const navigate = useNavigate();
  const [error, setError] = React.useState<string | null>(null);
  const [loading, setLoading] = React.useState(false);

  const form = useForm<SignupFormValues>({
    initialValues: {
      email: '',
      password: '',
      username: '',
    },
    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
      password: (value) => {
        if (value.length < 8) return 'Password should be at least 8 characters';
        if (!/[A-Z]/.test(value)) return 'Password should contain at least one uppercase letter';
        if (!/[a-z]/.test(value)) return 'Password should contain at least one lowercase letter';
        if (!/[0-9]/.test(value)) return 'Password should contain at least one number';
        return null;
      },
      username: (value) => (value.length < 3 ? 'Username should be at least 3 characters' : null),
    },
  });

  const handleSubmit = async (values: SignupFormValues) => {
    try {
      setLoading(true);
      setError(null);

      // Using SuperTokens signUp function from the SDK
      const response = await signUp({
        formFields: [
          {
            id: "email",
            value: values.email
          },
          {
            id: "password",
            value: values.password
          },
          {
            id: "username",
            value: values.username
          }
        ]
      });

      if (response.status === "OK") {
        // Successfully signed up and logged in
        navigate('/profile');
      } else {
        // Handle other status like EMAIL_ALREADY_EXISTS_ERROR
        if (response.status === "EMAIL_ALREADY_EXISTS_ERROR") {
          setError('An account with this email already exists');
        } else {
          setError('Something went wrong. Please try again.');
        }
      }
    } catch (err: any) {
      console.error('Signup error:', err);
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container size={420} my={40}>
      <Title ta="center" fw={900}>
        Create an account
      </Title>
      <Text c="dimmed" size="sm" ta="center" mt={5}>
        Already have an account?{' '}
        <Anchor size="sm" component={Link} to="/auth/login">
          Sign in
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

            <TextInput
              required
              label="Username"
              placeholder="Your username"
              {...form.getInputProps('username')}
            />

            <PasswordInput
              required
              label="Password"
              placeholder="Your password"
              description="Password must include at least one letter, number and special character"
              {...form.getInputProps('password')}
            />
          </Stack>

          <Group justify="space-between" mt="lg">
            <Text size="xs" c="dimmed">
              By registering, you agree to our{' '}
              <Anchor size="xs" component={Link} to="#">
                Terms of Service
              </Anchor>
            </Text>
          </Group>

          <Button type="submit" fullWidth mt="xl" loading={loading}>
            Create account
          </Button>
        </form>
      </Paper>
    </Container>
  );
};

export default SignupPage;
