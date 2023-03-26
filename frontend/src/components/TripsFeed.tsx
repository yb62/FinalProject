import React, { useState, useEffect } from "react";
import { Spinner, Text } from "@blueprintjs/core";

import { Trip } from "@src/components/Trip";
import { ITrip } from "@src/utils/trip";
import { useGetData } from "@src/hooks/useGetData";

interface Props {
  endpoint: string;
}

export const TripsFeed: React.FC<Props> = ({ endpoint }) => {
  const { data, progress, error, refetch } = useGetData({
    endpoint,
  });

  const trips = (data?.trips as ITrip[]) ?? [];

  switch (progress) {
    case "NOT_STARTED":
    case "IN_PROGRESS":
      return <Spinner />;
    case "ERROR":
      return <Text>{error}</Text>;
    case "FINISHED":
      return <TripsList trips={trips} refetch={refetch} />;
  }
};

interface TripsListProps {
  trips: ITrip[];
  refetch: () => void;
}

const TripsList: React.FC<TripsListProps> = ({ trips, refetch }) => (
  <div
    style={{
      display: "flex",
      alignItems: "center",
      flexDirection: "column",
    }}
  >
    {trips.length > 0 ? (
      trips.map((trip, index) => (
        <div style={{ marginTop: 12 }}>
          <Trip trip={trip} reloadCb={refetch} key={`trip_${index}`} />
        </div>
      ))
    ) : (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <Text style={{ fontSize: 32 }}>No Trips Found 😿</Text>
        <Text style={{ fontSize: 32 }}>How about creating one? 🧳🚀</Text>
        <Text style={{ fontSize: 32 }}>Navigate ➡️ 🏠</Text>
      </div>
    )}
  </div>
);
