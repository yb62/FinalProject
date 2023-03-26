import React, { useState } from "react";
import {
  FormGroup,
  InputGroup,
  Button,
  H1,
  Text,
  Toast,
} from "@blueprintjs/core";
import { LocationSearchInput } from "./LocationSearch";
import { BASE_URL } from "../constants";

interface Props {
  token: string;
  closeDialog: () => void;
}

export const CreateNewTrip = ({ token, closeDialog }: Props) => {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleStartDateChange = (event: any) => {
    setStartDate(event.target.value);
  };

  const handleEndDateChange = (event: any) => {
    setEndDate(event.target.value);
  };

  const handleOriginChange = (address: any) => {
    setOrigin(address);
  };

  const handleDestinationChange = (address: any) => {
    setDestination(address);
  };

  const handleSubmit = () => {
    // make a post request to create a new trip
    fetch(`${BASE_URL}/trip/create`, {
      method: "POST",
      body: JSON.stringify({ startDate, endDate, origin, destination }),
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => response.json())
      .then((data: any) => {
        if (data.success) {
          setSuccess(true);
          closeDialog();
        } else {
          throw new Error("Unknown error creating a trip. Please try again!");
        }
      })
      .catch((error: any) => {
        setError(error.message);
      });
  };

  return (
    <div style={{ padding: 12, fontSize: 18 }}>
      {success && (
        <Toast intent="success" message="Successfully created new trip!" />
      )}
      <H1 style={{ textAlign: "center" }}>Create New Trip</H1>
      <FormGroup>
        <Text>
          <b>Start Date:</b>
        </Text>
        <InputGroup
          value={startDate}
          onChange={handleStartDateChange}
          type="date"
        />
        <Text>
          <b>End Date:</b>
        </Text>
        <InputGroup
          value={endDate}
          onChange={handleEndDateChange}
          type="date"
        />
      </FormGroup>
      <FormGroup>
        <Text>
          <b>Origin:</b>
        </Text>
        <LocationSearchInput setPlaceName={handleOriginChange} />
        <Text>
          <b>Destination:</b>
        </Text>
        <LocationSearchInput setPlaceName={handleDestinationChange} />
      </FormGroup>
      <Button
        intent="primary"
        style={{ width: "100%" }}
        disabled={!startDate || !endDate || !origin || !destination}
        onClick={handleSubmit}
      >
        <b>Submit</b>
      </Button>
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
