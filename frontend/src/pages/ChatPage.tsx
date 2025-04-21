import React, { useState, useEffect } from 'react'; // Import useEffect
import { Container, Title, Paper, Stack, Text, Alert } from '@mantine/core';
import { IconAlertCircle } from '@tabler/icons-react';
import ChatInput from '../components/ChatInput.tsx'; // Update import path
import MessageList from '../components/MessageList.tsx'; // Update import path
// Assuming apiService is in frontend/src/services
import { sendMessage, getChatHistory, getGreeting, ChatMessage, ApiError } from '../services/apiService'; // Import new functions and ApiError

function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]); // Renamed for clarity
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | undefined>(undefined); // State for session ID
  const [greeting, setGreeting] = useState<string>('Loading greeting...'); // State for greeting

  // Load greeting and history on component mount
  useEffect(() => {
    console.log('ChatPage mounted');

    const fetchInitialData = async () => {
      setError(null); // Clear previous errors

      // 1. Fetch Greeting
      try {
        const greetingResponse = await getGreeting();
        setGreeting(greetingResponse.greeting);
      } catch (err) {
        console.error('Error fetching greeting:', err);
        setGreeting('Failed to load greeting.'); // Set a fallback greeting
        // Optionally set an error state if greeting is critical
        // setError('Failed to load greeting.');
      }

      // 2. Load Session ID from local storage and fetch history
      const storedSessionId = localStorage.getItem('chatSessionId');
      if (storedSessionId) {
        setSessionId(storedSessionId);
        console.log(`Loading history for session: ${storedSessionId}`);
        try {
          const historyResponse = await getChatHistory(storedSessionId);
          setMessages(historyResponse.messages);
        } catch (err) {
          console.error(`Error fetching history for session ${storedSessionId}:`, err);
          setError('Failed to load chat history.');
          // Optionally clear stored session ID if history fetch fails
          // localStorage.removeItem('chatSessionId');
          // setSessionId(undefined);
        }
      } else {
          console.log('No session ID found in local storage. Starting a new session.');
          // No history to load, messages state is already empty
      }
    };

    fetchInitialData();

    return () => {
      console.log('ChatPage unmounted');
    };
  }, []); // Empty dependency array means this runs once on mount

  const handleSendMessage = async (message: string) => {
    console.log('handleSendMessage called with message:', message);
    if (!message.trim()) {
        return; // Don't send empty messages
    }

    // Create a temporary user message to display immediately
    const tempUserMessage: ChatMessage = {
        id: `temp-${Date.now()}`, // Temporary ID
        session_id: sessionId || 'temp', // Use current session ID or temp
        role: 'user',
        content: message,
        timestamp: new Date().toISOString(),
        metadata: {},
    };

    // Optimistically add user message to the messages state
    setMessages((prevMessages) => [...prevMessages, tempUserMessage]);
    setIsLoading(true);
    setError(null); // Clear previous errors

    try {
      // Call the backend API with the message and current session ID
      const response = await sendMessage(message, sessionId);

      console.log('sendMessage response:', response);

      // Update session ID from the response if it's a new session
      if (response.session_id && response.session_id !== sessionId) {
          setSessionId(response.session_id);
          localStorage.setItem('chatSessionId', response.session_id); // Store in local storage
          console.log(`New session ID received and stored: ${response.session_id}`);
      }

      // Fetch the updated history to get the agent's response and correct message IDs/timestamps
      // This is a simpler approach than trying to construct the agent message client-side
      // and ensures we have the correct state from the backend.
      const updatedHistoryResponse = await getChatHistory(response.session_id || sessionId);
      setMessages(updatedHistoryResponse.messages);


    } catch (err) {
      console.error('Error sending message:', err);
      // Check if it's an ApiError to get more details
      const errorMessage = err instanceof ApiError ? err.message : 'An unexpected error occurred.';
      setError(`Failed to send message: ${errorMessage}`);

      // Optionally remove the optimistic user message if the API call failed
      // setMessages((prevMessages) => prevMessages.filter(msg => msg.id !== tempUserMessage.id));
      // Or replace the temp message with an error indicator
    } finally {
      setIsLoading(false);
    }
  };

  // Add useEffect here later for history loading and add logs inside it
  /*
  useEffect(() => {
    console.log('ChatPage mounted');
    // History loading logic will go here
    return () => {
      console.log('ChatPage unmounted');
    };
  }, []);
  */
  return (
    <Container size="md" style={{ height: 'calc(100vh - 60px)', display: 'flex', flexDirection: 'column' }}> {/* Adjust height based on header */}
      <Title order={2} ta="center" mt="md" mb="md">{greeting}</Title> {/* Use dynamic greeting */}

      {error && (
        <Alert variant="light" color="red" title="Error" icon={<IconAlertCircle size={16} />}>
          {error}
        </Alert>
      )}

      <Paper shadow="sm" radius="md" style={{ flexGrow: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <MessageList messages={messages} /> {/* Use 'messages' state */}
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </Paper>
    </Container>
  );
}

export default ChatPage;
