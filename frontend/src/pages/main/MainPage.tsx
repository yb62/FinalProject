import React, { useState } from "react";
import { Button, Dialog, Text } from "@blueprintjs/core";

import { Auth } from "@src/components/auth/Auth";
import { useAuthToken } from "@src/hooks/useToken";
import { CreateNewTrip } from "@src/components/CreateNewTrip";
import Page from "@src/components/Page";

export default function MainPage() {
  const [token, setToken] = useAuthToken();

  const [isOpen, setIsOpen] = useState(false);

  if (token == null) {
    return <Auth setToken={setToken} />;
  }

  return (
    <Page>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Text style={{ fontSize: 32 }}>Welcome to Travel Buddies!👋🏻</Text>
        <Text style={{ fontSize: 32 }}>Hit the ➕ 🔆 button </Text>
        <Text style={{ fontSize: 32 }}>Plan Collaboratively👨‍👩‍👧‍👦</Text>
      </div>
      <Dialog
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        style={{ backgroundColor: "rgb(165, 187, 255)" }}
      >
        <CreateNewTrip token={token} closeDialog={() => setIsOpen(false)} />
      </Dialog>
      <Button
        icon="plus"
        style={{
          position: "fixed",
          width: 50,
          height: 50,
          bottom: 20,
          right: 20,
          borderRadius: "50%",
          lineHeight: 50,
          textAlign: "center",
        }}
        onClick={() => setIsOpen(true)}
      />
    </Page>
  );
}
