import React from 'react';
import { Box, Text, Paper, Stack } from '@mantine/core';
import { ChatMessage } from '../services/apiService'; // Import ChatMessage type

interface MessageListProps {
  messages: ChatMessage[];
}

function MessageList({ messages }: MessageListProps) {
console.log('MessageList received messages:', messages);
  return (
    <Stack
      gap="md"
      style={{
        flexGrow: 1,
        overflowY: 'auto',
        flex: 1,
        display: 'flex', // Ensure flex properties are applied
        flexDirection: 'column-reverse', // Render messages from bottom to top
        paddingTop: 'var(--mantine-spacing-md)', // Add top padding
        paddingBottom: 'var(--mantine-spacing-md)', // Add bottom padding
      }}
    > {/* Increased vertical spacing */}
      {[...messages].reverse().map((message, index) => { // Reverse messages array
         console.log('Processing message:', message);
         return (
        <Box
          key={index}
          style={{
            display: 'flex',
            justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
            paddingLeft: 'var(--mantine-spacing-sm)', // Add padding to the left side
            paddingRight: 'var(--mantine-spacing-sm)', // Add padding to the right side
          }}
        >
          <Paper
            shadow="xs"
            radius="md"
            p="sm"
            maw="80%" // Max width for messages
            style={{
              backgroundColor: message.role === 'user' ? 'var(--mantine-color-blue-light)' : 'var(--mantine-color-gray-light)',
              color: message.role === 'user' ? 'var(--mantine-color-blue-light-color)' : 'var(--mantine-color-black)',
            }}
          >
            <Text size="md">{message.content}</Text> {/* Increased font size */}
          </Paper>
        </Box>
         );
      })}
    </Stack>
  );
}

export default MessageList;
