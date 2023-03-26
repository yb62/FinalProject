import React, { useCallback, useEffect, useState } from "react";
import axios from "axios";
import { BASE_URL } from "@src/constants";
import { useAuthToken } from "./useToken";

type TDataProgress = 'NOT_STARTED' | 'IN_PROGRESS' | 'ERROR' | 'FINISHED';

export const useGetData = (
  { endpoint }: { endpoint: string }
) => {
  const [token] = useAuthToken();
  const [progress, setProgress] = useState<TDataProgress>('NOT_STARTED');
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);

  const fetchData = useCallback(async () => {
    setProgress('IN_PROGRESS');
    setError(null);
    setData(null);

    try {
      if (token == null) {
        throw new Error('Token is invalid');
      }

      const response = await axios.get(
        `${BASE_URL}${endpoint}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setProgress('FINISHED');
      setData(response.data);
    } catch (e: any) {
      setProgress('ERROR');
      setError(e.message);
    }
  }, [token, endpoint]);

  useEffect(() => {
    fetchData()
  }, []);

  const refetch = useCallback(() => {
    fetchData();
  }, [fetchData])

  return { data, progress, error, refetch };
};
