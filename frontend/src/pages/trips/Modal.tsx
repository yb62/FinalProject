import { Button, Dialog } from '@blueprintjs/core';
import React, { useState } from 'react';
import styled from "styled-components";

interface Props {
    children: React.ReactNode
}

const ModalButtonContainer = styled.div`
    width: 50,
    height: 50,
`;

export default function Modal({ children }: Props) {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <ModalButtonContainer>
            <Button
                icon="plus"
                style={{
                    width: 50,
                    height: 50,
                    borderRadius: "50%",
                    lineHeight: 50,
                    textAlign: "center",
                }}
                onClick={() => setIsOpen(true)}
            />
            <Dialog
                isOpen={isOpen}
                onClose={() => setIsOpen(false)}
            >
                {children}
            </Dialog>
        </ModalButtonContainer>
    );
}

