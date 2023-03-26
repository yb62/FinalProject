import React from 'react';

import Page from '@src/components/Page';
import { TripsFeed } from '@src/components/TripsFeed';

export default function MyTripsPage() {
    return (
        <Page>
            <TripsFeed endpoint='/my-trips' />
        </Page>
    );
}