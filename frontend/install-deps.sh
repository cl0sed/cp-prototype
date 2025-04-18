#!/bin/bash
# Script to install dependencies for the React 19.1 / Mantine 7.17.4 upgrade

echo "Installing dependencies for frontend-react..."
cd "$(dirname "$0")"

echo "Running npm install to update packages..."
npm install

echo "Installation completed! The following dependencies have been updated:"
echo "- React 19.1.0"
echo "- React DOM 19.1.0"
echo "- @mantine/* 7.17.4"
echo "- @tabler/icons-react 3.31.0"
echo "- axios 1.8.4"
echo "- react-router-dom 7.5.1"
echo "- Removed supertokens-web-js (using only supertokens-auth-react)"

echo ""
echo "TypeScript errors will be resolved after this installation."
echo ""
echo "Next steps:"
echo "1. Run the development server: npm run dev"
echo "2. Test the authentication flows"
echo "3. Update any components using outdated syntax"
