import { Spinner, Toast } from "@blueprintjs/core";
import React from "react";
import { Text } from "@blueprintjs/core";
import { IUser } from "../utils/user";
import { useGetData } from "@src/hooks/useGetData";
import styled from "styled-components";

export type Props = {
  endpoint: string;
};

const Center = styled.div`
  width: 100%;
  height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const Card = styled.div`
  width: 500px;
  height: 200px;
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.2), 0 3px 5px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
`;

const UserProfileDetails = (user: IUser) => {
  if (user == null) return null;
  return (
    <Center>
      <Card>
        <div>
            <Text style={{fontSize: 36}}>😎</Text>
        </div>
        <div>
          <Text style={{fontSize: 28}}>Username: <b>@{user.username}</b></Text>
        </div>
        <div>
          <Text style={{fontSize: 28}}>Full Name: <b>{user.fullName}</b></Text>
        </div>
      </Card>
    </Center>
  );
};

export const UserProfile: React.FC<Props> = ({ endpoint }: Props) => {
  const { data, progress, error, refetch } = useGetData({
    endpoint,
  });

  const userDetails = data as IUser;

  switch (progress) {
    case "NOT_STARTED":
    case "IN_PROGRESS":
      return <Spinner />;
    case "ERROR":
      return (
        <Center>
          <Card>
            <Toast
              icon="error"
              intent="danger"
              message={error}
              onDismiss={() => refetch()}
            />
          </Card>
        </Center>
      );
    case "FINISHED":
      return UserProfileDetails(userDetails);
  }
};
