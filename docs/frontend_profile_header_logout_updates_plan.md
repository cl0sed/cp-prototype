# Frontend Profile, Header, and Logout Updates Plan

This plan outlines the steps to update the frontend application based on the requirements provided on 2025-04-18.

## Requirements Summary

1.  **Profile Username Display:** Display the actual username on the profile page instead of "-".
2.  **Header UI (Logged-in):** Remove profile link/menu, keep only a slightly larger avatar, vertically center header elements.
3.  **Logout Redirection:** Ensure immediate redirection to the login page upon logout.
4.  **Logout Button Position:** Remove the button from the profile page/header menu and place it as a fixed element in the bottom-right corner.

## Implementation Plan

### 1. Backend: Verify/Add `username` to Database Model

*   **Goal:** Ensure the `User` model in the database includes a `username` field.
*   **Action:**
    *   Check `backend/app/db/models/user.py` for a `username` column.
    *   If missing: Add the column (e.g., `username: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True, nullable=True)`).
    *   Generate a database migration using Alembic (e.g., `docker-compose run --rm backend alembic revision --autogenerate -m "Add username to User model"`).
    *   Apply the migration (e.g., `docker-compose run --rm backend alembic upgrade head`).

### 2. Backend: Update API Response Schema

*   **Goal:** Include the username in the data returned by the `/api/user/profile` endpoint.
*   **File:** `backend/app/schemas/user.py`
*   **Action:** Modify the `UserProfile` Pydantic schema to include the username field (e.g., `username: Optional[str] = None`).

### 3. Frontend: Update Profile Username Display (Requirement 1)

*   **Goal:** Display the fetched username on the profile page.
*   **File:** `frontend/src/pages/ProfilePage.tsx`
*   **Action:**
    *   Modify the username display logic (around line 161) to use `profileData.username`.
    *   Ensure the `UserProfileData` interface (lines 24-28) reflects the updated backend schema (`username?: string;`).

### 4. Frontend: Refactor Header UI (Logged-in Users) (Requirement 2)

*   **Goal:** Simplify the header for logged-in users, retaining only the avatar.
*   **File:** `frontend/src/layouts/MainLayout.tsx`
*   **Action:**
    *   Remove the standalone "Profile" link.
    *   Remove the user dropdown menu.
    *   Retain the `<Avatar>`, place it directly in the header `Group`, increase its size (e.g., `size="lg"`), and ensure it's only shown when logged in.
    *   Ensure vertical alignment of header elements (Logo text and Avatar) using CSS (`alignItems: 'center'` on the parent `Group`).

### 5. Frontend: Ensure Immediate Logout Redirection (Requirement 3)

*   **Goal:** Redirect users immediately to the login page upon logout.
*   **File:** `frontend/src/layouts/MainLayout.tsx`
*   **Action:** Modify the `handleLogout` function to add an explicit `navigate('/auth/login')` call after `await signOut()` completes successfully.

### 6. Frontend: Relocate Logout Button (Requirement 4)

*   **Goal:** Remove the logout button from the profile page/header menu and add a fixed button to the viewport corner.
*   **Files:**
    *   `frontend/src/pages/ProfilePage.tsx`: Remove the logout button.
    *   `frontend/src/layouts/MainLayout.tsx`: Remove logout options from the menu/drawer. Add a new, fixed-position `<Button>` (e.g., `style={{ position: 'fixed', bottom: 20, right: 20, zIndex: 1000 }}`) within the `<AppShell>`, visible only when logged in, and linked to the `handleLogout` function.

### 7. Cleanup & Testing

*   **Goal:** Ensure code quality and verify all changes work as expected.
*   **Action:** Remove unused imports/variables. Test the backend API endpoint. Test the frontend profile page, header appearance (desktop/mobile), logout redirection, and the new fixed logout button.
