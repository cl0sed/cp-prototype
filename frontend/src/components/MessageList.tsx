import React from 'react';
import { Box, Text, Paper, Stack } from '@mantine/core';
import { ChatMessage } from '../services/apiService'; // Import ChatMessage type

interface MessageListProps {
  messages: ChatMessage[];
}

function MessageList({ messages }: MessageListProps) {
console.log('MessageList received messages:', messages);
  return (
    <Stack gap="sm" style={{ flexGrow: 1, overflowY: 'auto', padding: '16px' }}>
      {messages.map((message, index) => {
         console.log('Processing message:', message);
         return (
        <Box
          key={index}
          style={{
            display: 'flex',
            justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
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
            <Text size="sm">{message.content}</Text>
          </Paper>
        </Box>
         );
      })}
    </Stack>
  );
}

export default MessageList;
