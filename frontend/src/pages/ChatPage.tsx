import React, { useState, useEffect } from 'react'; // Import useEffect
import { Container, Title, Paper, Stack, Text } from '@mantine/core'; // Removed Alert
import { showNotification } from '@mantine/notifications'; // Added for toasts
import { IconAlertCircle } from '@tabler/icons-react';
import ChatInput from '../components/ChatInput.tsx'; // Update import path
import MessageList from '../components/MessageList.tsx'; // Update import path
// Assuming apiService is in frontend/src/services
import { sendMessage, getGreeting, ChatMessage, ApiError } from '../services/apiService'; // Import new functions and ApiError

function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]); // Renamed for clarity
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null); // Re-add error state
  const [sessionId, setSessionId] = useState<string | undefined>(undefined); // State for session ID
  const [greeting, setGreeting] = useState<string>('Loading greeting...'); // State for greeting

  // Load greeting and history on component mount
  useEffect(() => {
    console.log('ChatPage mounted');

    const fetchInitialData = async () => {

      // 1. Fetch Greeting
      try {
        const greetingResponse = await getGreeting();
        setGreeting(greetingResponse.greeting);
      } catch (err) {
        console.error('Error fetching greeting:', err);
        // Display error as a toast notification
        showNotification({
          title: 'Error',
          message: 'Failed to load greeting.',
          color: 'red',
        });
      }

      // 2. Load Session ID from local storage and fetch history
      // const storedSessionId = localStorage.getItem('chatSessionId'); // Commented out for debugging
      // if (storedSessionId) { // Commented out for debugging
      //   setSessionId(storedSessionId); // Commented out for debugging
      //   console.log(`Loading history for session: ${storedSessionId}`); // Commented out for debugging
      //   try { // Commented out for debugging
      //     const historyResponse = await getChatHistory(storedSessionId); // Commented out for debugging
      //     setMessages(historyResponse.messages); // Commented out for debugging
      //   } catch (err) { // Commented out for debugging
      //     console.error(`Error fetching history for session ${storedSessionId}:`, err); // Commented out for debugging
      //     setError('Failed to load chat history.'); // Commented out for debugging
      //     // Optionally clear stored session ID if history fetch fails // Commented out for debugging
      //     // localStorage.removeItem('chatSessionId'); // Commented out for debugging
      //     // setSessionId(undefined); // Commented out for debugging
      //   } // Commented out for debugging
      // } else { // Commented out for debugging
          console.log('No session ID found in local storage. Starting a new session (history disabled).'); // Modified log
          // No history to load, messages state is already empty
      // } // Commented out for debugging
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

    try {
      // Call the backend API with the message and current session ID
      const response = await sendMessage(message, sessionId);

      console.log('sendMessage response:', response);

      // Update session ID from the response if it's a new session
      if (response.session_id && response.session_id !== sessionId) {
          setSessionId(response.session_id);
          // localStorage.setItem('chatSessionId', response.session_id); // Store in local storage (Commented out for debugging)
          console.log(`New session ID received and stored: ${response.session_id}`);
      }

      // Add the assistant's reply to the messages state
      const assistantMessage: ChatMessage = {
          id: `assistant-${Date.now()}`, // Temporary ID for display
          session_id: response.session_id || sessionId || 'temp', // Use session ID from response or current
          role: 'assistant',
          content: response.reply,
          timestamp: new Date().toISOString(), // Use current time for display
          metadata: { model: response.model }, // Include model info if available in response
      };
      setMessages((prevMessages) => [...prevMessages, assistantMessage]);


    } catch (err) {
      console.error('Error sending message:', err);
      // Check if it's an ApiError to get more details
      const errorMessage = err instanceof ApiError ? err.message : 'An unexpected error occurred.';
      // Display error as a toast notification
      showNotification({
        title: 'Error',
        message: `Failed to send message: ${errorMessage}`,
        color: 'red',
      });

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
    <Container size="md" style={{ height: 'calc(100vh - 140px)', display: 'flex', flexDirection: 'column', position: 'relative' }} pt="md"> {/* Adjust height based on header, add relative positioning for absolute children, added top padding */}
      <Paper shadow="sm" radius="md" style={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}> {/* Removed overflow: hidden */}
        <MessageList messages={messages} /> {/* Use 'messages' state */}
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </Paper>
    </Container>
  );
}

export default ChatPage;
