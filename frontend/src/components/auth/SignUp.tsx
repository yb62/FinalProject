import React from 'react';
import { Button, FormGroup, InputGroup, Toast } from "@blueprintjs/core";
import { useState } from "react";
import { BASE_URL } from '../../constants';

interface Props {
    onBack: () => void;
}

export const SignUp: React.FC<Props> = (props: Props) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [fullName, setFullName] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [successMsg, setSucessMsg] = useState("");

    const handleSignUp = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${BASE_URL}/signup`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password, full_name: fullName }),
            });
            if (!response.ok) {
                throw new Error((await response.json()).detail);
            }
            const result = await response.json();
            if (result.success) {
                setSucessMsg("You have successfully signed up! Proceed to login.");
            } else {
                setError("Unknown error occured! Please try again.")
            }
        } catch (error: any) {
            if (error.message) {
                setError(error.message);
            } else {
                setError("Unknown error occured! Please try again.")
            }
        }
        setLoading(false);
    };

    return (
        <div style={{ textAlign: "center", width: 600, height: 300 }}>
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
            <FormGroup label="Full Name">
                <InputGroup
                    placeholder="Enter full name"
                    value={fullName}
                    onChange={(event) => setFullName(event.target.value)}
                />
            </FormGroup>
            <Button
                intent="primary"
                disabled={!username || !password || !fullName || loading}
                onClick={handleSignUp}
                style={{width: 300}}
            >
                Sign Up
            </Button>
            {
        error && (
            <Toast
                icon="error"
                intent="danger"
                message={error}
                onDismiss={() => setError("")}
            />
        )
    }
    {
        successMsg && (
            <Toast
                icon="info-sign"
                intent="success"
                message={successMsg}
                timeout={3000}
                onDismiss={() => setSucessMsg("")}
            />
        )
    }
    <div style={{ marginTop: 12 }}>
        <Button text="Back" icon="backlink" onClick={() => props.onBack()} />
    </div>
        </div >
    );
};