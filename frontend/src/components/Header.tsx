import { Alignment, Button, H2, Navbar } from "@blueprintjs/core";
import { useAuthToken } from '@src/hooks/useToken';
import React, { useCallback } from 'react';
import styled from 'styled-components';
import { useNavigate } from "react-router-dom";


const GradientNavbar = styled(Navbar)`
  background-image: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const NavTitle = styled(H2)`
  margin: 0;
`;

export const Header: React.FC = () => {
  const [, setToken] = useAuthToken();

  const logout = useCallback(() => {
    setToken(null);
  }, [setToken]);

  const navigate = useNavigate();

  return (
    <GradientNavbar>
      <Navbar.Group align={Alignment.LEFT}>
        <Navbar.Heading>
          <NavTitle>Travel Buddies</NavTitle>
        </Navbar.Heading>

        <Navbar.Divider />
        <Button
          minimal
          icon="home"
          onClick={() => navigate('/')}
          text="Home" />
        <Button
          minimal
          icon="path-search"
          onClick={() => navigate('/all-trips')}
          text="All trips" />
        <Button
          minimal
          icon="map-marker"
          onClick={() => navigate('/my-trips')}
          text="My trips" />
      </Navbar.Group>

      <Navbar.Group align={Alignment.RIGHT}>
        <Navbar.Divider />
        <Button minimal icon="user" onClick={() => navigate('/me')} />
        <Button minimal icon="log-out" onClick={logout} />
      </Navbar.Group>
    </GradientNavbar>
  );
};