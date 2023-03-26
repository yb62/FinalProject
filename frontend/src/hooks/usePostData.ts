import React, { useCallback, useEffect, useState } from "react";
import axios from "axios";
import { BASE_URL } from "@src/constants";
import { useAuthToken } from "./useToken";

type TDataProgress = 'NOT_STARTED' | 'IN_PROGRESS' | 'ERROR' | 'FINISHED';

export const usePostData = (
  { endpoint, onFinish }: { endpoint: string, onFinish: () => void }
) => {
  const [token] = useAuthToken();
  const [progress, setProgress] = useState<TDataProgress>('NOT_STARTED');
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<any>(null);

  const postData = useCallback(async (bodyData: any) => {
    setProgress('IN_PROGRESS');
    setError(null);
    setData(null);

    try {
      if (token == null) {
        throw new Error('Token is invalid');
      }

      console.log(bodyData);

      const response = await axios.post(
        `${BASE_URL}${endpoint}`, bodyData,
        {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setProgress('FINISHED');
      setData(response.data);
      onFinish();
    } catch (e: any) {
      setProgress('ERROR');
      setError(e.message);
    }
  }, [token, endpoint]);

  return { data, progress, error, postData };
};
