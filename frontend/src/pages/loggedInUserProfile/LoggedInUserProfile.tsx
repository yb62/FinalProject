import Page from '@src/components/Page';
import { UserProfile } from '@src/components/UserProfile';
import { Auth } from '@src/components/auth/Auth';
import { useAuthToken } from '@src/hooks/useToken';
import React from 'react';

export default function LoggedInUserProfilePage() {
    const [token, setToken] = useAuthToken();

    // Given we are showing the profile of the logged in user,
    // we must ensure the user is logged in, otherwise /me endpoint
    // wouldn't work.
    if (token == null) {
        return <Auth setToken={setToken} />;
    }

    return (
        <Page>
            <UserProfile endpoint='/users/me' />
        </Page>
    );
}