import React from 'react';
import { Button, FormGroup, InputGroup, Toast } from "@blueprintjs/core";
import { useState } from "react";
import { BASE_URL } from '../../constants';

interface Props {
    setToken: (token: string) => void;
    onBack: () => void;
};

export const SignIn: React.FC<Props> = (props: Props) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSignIn = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${BASE_URL}/login`, {
                method: "POST",
                headers: {
                    Authorization: "Basic " + btoa(username + ":" + password),
                },
            });
            if (!response.ok) {
                throw new Error((await response.json()).detail);
            }
            const { access_token } = await response.json();
            console.log(access_token);
            props.setToken(access_token);
        } catch (error: any) {
            if (error.message) {
                setError(error.message);
            } else {
                setError("Unknown error! Please try again.")
            }
        }
        setLoading(false);
    };

    return (
        <div style={{ textAlign: "center"}}>
            <FormGroup label="Username">
                <InputGroup
                    placeholder="Enter username"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                />
            </FormGroup>
            <FormGroup label="Password">
                <InputGroup
                    type="password"
                    placeholder="Enter password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                />
            </FormGroup>
            <Button
                intent="primary"
                disabled={!username || !password || loading}
                onClick={handleSignIn}
                style={{width: 300}}
            >
                Sign In
            </Button>
            <div style={{marginTop: 12}}>
                <Button text="Back" icon="backlink" onClick={() => props.onBack()} />
            </div>
            {error && (
                <Toast
                    icon="error"
                    intent="danger"
                    message={error}
                    onDismiss={() => setError("")}
                />
            )}
        </div>
    );
};