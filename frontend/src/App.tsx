import React from 'react';
import './App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import MainPage from '@src/pages/main/MainPage';
import TripsPage from '@src/pages/trips/TripsPage';
import AllTripsPage from '@src/pages/allTrips/AllTripsPage';
import MyTripsPage from './pages/myTrips/MyTripsPage';
import LoggedInUserProfile from './pages/loggedInUserProfile/LoggedInUserProfile';
import UserProfilePage from './pages/userProfilePage/UserProfilePage';

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<MainPage />} />
                <Route path="/all-trips" element={<AllTripsPage />} />
                <Route path="/my-trips" element={<MyTripsPage />} />
                <Route path="/trip/:id" element={<TripsPage />} />
                <Route path="/me" element={<LoggedInUserProfile />}/>
                <Route path="/user/:name" element={<UserProfilePage />} />
            </Routes>
        </BrowserRouter>
    );
}
