import Page from '@src/components/Page';
import { UserProfile } from '@src/components/UserProfile';
import React from 'react';
import { useParams } from 'react-router-dom';

export default function UserProfilePage() {
    const { name } = useParams();

    return (
        <Page>
            <UserProfile endpoint={`/user/${name}`} />
        </Page>
    );
}