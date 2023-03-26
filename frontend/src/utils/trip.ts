import { BASE_URL } from "../constants";
import { ITripEvent } from "./event";
import { IUser } from "./user";

export interface ITrip {
  id: number;
  startDate: Date;
  endDate: Date;
  origin: string;
  destination: string;
  users: IUser[];
}

export interface ITripDetailsFull {
    basic: ITrip;
    events: ITripEvent[];
}

export async function loadTripDetails(tripId: number, token: string): Promise<ITripDetailsFull> {
  const response = await fetch(`${BASE_URL}/trip/${tripId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  const data = await response.json();
  return data;
}
