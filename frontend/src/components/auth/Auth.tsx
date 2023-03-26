import React, { useCallback, useState } from 'react';
import { SignIn } from './SignIn';
import { SignUp } from './SignUp';
import { Button, ButtonGroup } from '@blueprintjs/core';

interface Props {
    setToken: (token: string) => void;
};

export const Auth: React.FC<Props> = ({ setToken }: Props) => {
    const [showSignIn, setShowSignIn] = useState(false);
    const [showSignUp, setShowSignUp] = useState(false);
    const resetScreen = useCallback(() => {
        setShowSignIn(false);
        setShowSignUp(false);
    }, [setShowSignIn, setShowSignUp]);
    return <div style={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
    }}>
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            {showSignIn && <SignIn setToken={setToken} onBack={() => resetScreen()} />}
            {showSignUp && <SignUp onBack={() => resetScreen()} />}
            {!showSignIn && !showSignUp && <div>
                <ButtonGroup vertical={true} large={true} style={{ width: 300 }}>
                    <Button icon="log-in" text="Sign In" intent="primary" onClick={() => setShowSignIn(true)} />
                    <Button icon="one-to-one" text="Sign Up" intent="none" onClick={() => setShowSignUp(true)} />
                </ButtonGroup>
            </div>}
        </div>
    </div>
}
