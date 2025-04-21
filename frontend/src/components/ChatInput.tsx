import React, { useState } from 'react';
import { TextInput, ActionIcon, rem, Loader } from '@mantine/core';
import { IconSend } from '@tabler/icons-react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

function ChatInput({ onSendMessage, isLoading }: ChatInputProps) {
  const [message, setMessage] = useState('');

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (message.trim() && onSendMessage && !isLoading) {
      onSendMessage(message);
      setMessage('');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', alignItems: 'center', padding: '16px' }}>
      <TextInput
        style={{ flexGrow: 1, marginRight: '8px' }}
        placeholder="Type your message..."
        value={message}
        onChange={(event) => setMessage(event.currentTarget.value)}
        disabled={isLoading}
        rightSection={
          isLoading ? (
            <Loader size="xs" />
          ) : (
            <ActionIcon
              size={32}
              radius="xl"
              color="blue"
              variant="filled"
              type="submit"
              disabled={!message.trim() || isLoading}
            >
              <IconSend style={{ width: rem(18), height: rem(18) }} stroke={1.5} />
            </ActionIcon>
          )
        }
        rightSectionWidth={40}
      />
    </form>
  );
}

export default ChatInput;
