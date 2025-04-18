import { AppShell } from '@mantine/core';
import { SuperTokensWrapper } from 'supertokens-auth-react';
import AppRoutes from './routes';

function App() {
  return (
    <SuperTokensWrapper>
      <AppShell padding="md">
        <AppRoutes />
      </AppShell>
    </SuperTokensWrapper>
  );
}

export default App;
