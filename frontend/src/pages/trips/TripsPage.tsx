import React, { useCallback, useState } from "react";
import { Link, useParams } from "react-router-dom";
import styled from "styled-components";

import {
  Button,
  Card,
  FormGroup,
  H2,
  H4,
  InputGroup,
  Spinner,
  Text,
} from "@blueprintjs/core";

import Page from "@src/components/Page";
import { useGetData } from "@src/hooks/useGetData";
import Timeline from "@src/components/Timeline";
import { usePostData } from "@src/hooks/usePostData";
import Modal from "./Modal";
import { Trip } from "@src/components/Trip";

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px;
`;

const Panel = styled(Card)`
  width: 100%;
  max-width: 800px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const ParticipantsContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
`;

const AddEventCard = styled(Card)`
  margin-bottom: 20px;
  padding: 20px;
`;

const ActionModalContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  border: none;
`;

const ParticipantCard = styled.div`
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  width: 220px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

export default function TripsPage() {
  const { id } = useParams();

  const [newEventDescription, setNewEventDescription] = useState("");
  const [newEventTime, setNewEventTime] = useState("");

  const { error, progress, data, refetch } = useGetData({
    endpoint: "/trip/" + id,
  });

  console.log(JSON.stringify(data, null, 4));

  const { postData: postDataForAddEvent } = usePostData({
    endpoint: "/trip/add-event",
    onFinish: refetch,
  });

  const { postData: postDataForRemoveEvent } = usePostData({
    endpoint: "/trip/remove-event",
    onFinish: refetch,
  });

  const { postData: postDataForAddParticipant } = usePostData({
    endpoint: "/trip/add-participant",
    onFinish: refetch,
  });

  const { postData: postDataForRemoveParticipant } = usePostData({
    endpoint: "/trip/remove-participant",
    onFinish: refetch,
  });

  const addEvent = useCallback(() => {
    postDataForAddEvent({
      description: newEventDescription,
      time: newEventTime,
      trip_id: id,
    });
  }, [postDataForAddEvent, newEventDescription, newEventTime, id]);

  const removeEvent = useCallback(
    (event_id) => {
      postDataForRemoveEvent({
        event_id,
      });
    },
    [postDataForRemoveEvent]
  );

  const addParticipant = useCallback(() => {
    postDataForAddParticipant({
      trip_id: id,
    });
  }, [id]);

  const removeParticipant = useCallback(() => {
    postDataForRemoveParticipant({
      trip_id: id,
    });
  }, [id]);

  const isUserInTrip = data?.isCurrentUserInParticipants ?? false;

  switch (progress) {
    case "NOT_STARTED":
    case "IN_PROGRESS":
      return <Spinner />;
    case "ERROR":
      return <Text>{error}</Text>;
  }

  return (
    <Page>
      <Container>
        <Panel>
          <H2>Description</H2>
          <Text>{data?.destination ?? "-"}</Text>
        </Panel>

        <Panel>
          <H2>Start and end time</H2>
          <Text>Start Time: {data?.startDate ?? "-"}</Text>
          <Text>End Time: {data?.endDate ?? "-"}</Text>
        </Panel>

        <Panel>
          <H2>Events</H2>
          <Timeline events={data?.events ?? []} removeEvent={removeEvent} />

          <ActionModalContainer>
            <Modal>
              <AddEventCard>
                <FormGroup label="New Event">
                  <InputGroup
                    placeholder="Description"
                    value={newEventDescription}
                    onChange={(e) => setNewEventDescription(e.target.value)}
                  />
                  <InputGroup
                    type="date"
                    placeholder="Time"
                    value={newEventTime}
                    onChange={(e) => setNewEventTime(e.target.value)}
                    style={{ marginTop: "10px" }}
                  />
                  <Button
                    onClick={addEvent}
                    intent="primary"
                    style={{ marginTop: "10px" }}
                  >
                    Create Event
                  </Button>
                </FormGroup>
              </AddEventCard>
            </Modal>
          </ActionModalContainer>
        </Panel>

        <Panel>
          <H2>Participants</H2>
          <ParticipantsContainer>
            {(data?.users ?? []).map((user: any, index: number) => (
              <ParticipantCard key={index}>
                <H4>Username</H4>
                <Text>
                  <Link to={`/user/${user.username}`}>@{user.username}</Link>
                </Text>
                <div style={{ paddingTop: "20px" }} />
                <H4>Full name</H4>
                <Text>{user.fullName}</Text>
              </ParticipantCard>
            ))}
          </ParticipantsContainer>
        </Panel>

        <Panel>
          <H2>Join or Leave</H2>
          {isUserInTrip ? (
            <Button intent="danger" icon="cross" onClick={removeParticipant}>
              Leave Trip
            </Button>
          ) : (
            <Button intent="success" icon="tick" onClick={addParticipant}>
              Join Trip
            </Button>
          )}
        </Panel>
      </Container>
    </Page>
  );
}
