import Page from '@src/components/Page';
import { TripsFeed } from '@src/components/TripsFeed';
import React from 'react';

export default function AllTripsPage() {
    return (
        <Page>
            <TripsFeed endpoint='/all-trips' />
        </Page>
    );
}