import React from "react";
import axios from "axios";
import { Button, H1, Text } from "@blueprintjs/core";
import { BASE_URL } from "../constants";
import { ITrip } from "../utils/trip";
import { useAuthToken } from "@src/hooks/useToken";
import styled from "styled-components";
import { Link, useNavigate, useNavigation } from "react-router-dom";

interface Props {
  trip: ITrip;
  reloadCb: () => void;
}

const Card = styled.div`
  position: relative;
  width: 500px;
  height: 220px;
  background-image: linear-gradient(
      rgba(255, 255, 255, 0.7),
      rgba(255, 255, 255, 0.7)
    ),
    url("trip_image_2.jpeg");
  background-size: cover;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 15px;
  backdrop-filter: blur(5px);
  display: flex;
  justify-content: space-between;
  flex-direction: column;
`;

const Details = styled.div`
  display: flex;
  justify-content: space-between;
  gap: 10px;
  width: 90%;
`;

const Column = styled.div`
  display: flex;
  flex-direction: column;
  max-width: 300px;
`;

const TripTitle = styled(H1)`
  max-width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const ActionsPanel = styled.div`
  display: flex;
  justify-content: end;
`;

const deleteTrip = (tripId: number, token: string, reloadCb: () => void) => {
  axios
    .delete(`${BASE_URL}/trips/${tripId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    .then((_) => {
      alert("Deleted!");
      reloadCb();
    })
    .catch((error) => {
      console.error(error);
    });
};

export const Trip: React.FC<Props> = ({ trip, reloadCb }: Props) => {
  const [token] = useAuthToken();

  const navigate = useNavigate();

  if (token == null) {
    return null;
  }

  return (
    <Card>
      <TripTitle>🛬{trip.destination}🚕</TripTitle>
      <Details>
        <Column>
          <Text>
            <b>{trip.startDate}</b> &mdash; <b>{trip.endDate}</b>
          </Text>
          <Text>Travelling from:</Text>
          <Text>🚕{trip.origin}🛫</Text>
        </Column>
        <Column>
          <Text>Created By:</Text>
          <Text>
            <Link to={`/user/${trip.users[0].username}`}>
              @{trip.users[0].username}
            </Link>
          </Text>
        </Column>
      </Details>

      <ActionsPanel>
        <Button
          icon="trash"
          minimal
          onClick={() => deleteTrip(trip.id, token, reloadCb)}
        />
        <Button
          icon="widget-button"
          minimal
          onClick={() => navigate("/trip/" + trip.id)}
        />
      </ActionsPanel>
    </Card>
  );
};
