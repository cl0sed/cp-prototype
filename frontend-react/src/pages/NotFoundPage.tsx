import React from 'react';
import { Container, Title, Text, Button, Group, Image, Box } from '@mantine/core';
import { Link } from 'react-router-dom';

const NotFoundPage: React.FC = () => {
  return (
    <Container py={80} size="md">
      <Box maw={500} mx="auto" style={{ textAlign: 'center' }}>
        <Title
          mb="xl"
          sx={(theme) => ({
            fontSize: 100,
            fontWeight: 900,
            lineHeight: 1,
            [theme.fn.smallerThan('sm')]: {
              fontSize: 50,
            },
          })}
        >
          404
        </Title>

        <Title order={2} mb="md">Page not found</Title>
        <Text size="lg" mb="lg">
          The page you are looking for doesn't exist or has been moved to another URL.
        </Text>

        <Group justify="center">
          <Button component={Link} to="/" variant="filled" size="md">
            Back to Home
          </Button>
          <Button component={Link} to="/login" variant="outline" size="md">
            Go to Login
          </Button>
        </Group>
      </Box>
    </Container>
  );
};

export default NotFoundPage;
