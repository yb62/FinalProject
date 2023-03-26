import React from 'react';
import styled from 'styled-components';
import { Button, H4, Text } from '@blueprintjs/core';

const TimelineWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const TimelineEventNonFirst = styled.div`
  display: flex;
  position: relative;
  margin: 20px 0;


  &:before {
    content: '';
    position: absolute;
    width: 6px;
    height: 100px;
    background-color: #6a65a5;
    left: -33px;
    top: 5%;
    transform: translateY(-75%);
  }
`;

const TimelineEventFirst = styled.div`
  display: flex;
  position: relative;
  margin: 20px 0;
`;

const TimelinePoint = styled.div`
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: #6a65a5;
  position: absolute;
  left: -38px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
`;

const TimelineContent = styled.div`
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  width: 220px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

export default function Timeline({
  events,
  removeEvent
}: {
  events: Array<any>,
  removeEvent: (event_id: number) => void
}
) {
  return (
    <TimelineWrapper>
      {events.map((event, index) => (
        <div key={index}>
          {index == 0 ? (
            <TimelineEventFirst >
              <TimelinePoint />
              <TimelineContent>
                <H4>{event.time}</H4>
                <Text>{event.description}</Text>
              </TimelineContent>
              <Button
                icon="trash"
                minimal
                onClick={() => removeEvent(event.id)}
              />
            </TimelineEventFirst>)
            : <TimelineEventNonFirst>
              <TimelinePoint />
              <TimelineContent>
                <H4>{event.time}</H4>
                <Text>{event.description}</Text>
              </TimelineContent>
              <Button
                icon="trash"
                minimal
                onClick={() => removeEvent(event.id)}
              />
            </TimelineEventNonFirst>}
        </div>
      ))}
    </TimelineWrapper>
  );
};
