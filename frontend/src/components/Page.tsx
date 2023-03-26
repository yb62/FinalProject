import React from 'react';
import { Header } from "@src/components/Header";

interface Props {
    children: React.ReactNode
}

export default function Page({children}: Props) {
    return (
        <div>
            <Header />
            {children}
        </div>
    )
}