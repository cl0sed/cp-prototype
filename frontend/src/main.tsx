import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { MantineProvider, createTheme } from '@mantine/core';
import { Notifications } from '@mantine/notifications';
import SuperTokens from 'supertokens-auth-react';
import { SuperTokensConfig } from './config/supertokens';

import App from './App.tsx';
import './index.css';
import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';

// Initialize SuperTokens
SuperTokens.init(SuperTokensConfig);

// Create Mantine theme (new in Mantine 7.17.4)
const theme = createTheme({
  primaryColor: 'blue',
  defaultRadius: 'md',
  fontFamily: '-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif',
  components: {
    Button: {
      defaultProps: {
        radius: 'md',
      },
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <MantineProvider theme={theme} defaultColorScheme="light">
      <Notifications position="top-right" />
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </MantineProvider>
  </React.StrictMode>
);
