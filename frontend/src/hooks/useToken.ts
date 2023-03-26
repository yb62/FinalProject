import { useState, useEffect, useCallback } from "react";

export const useAuthToken = () => {
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("token")
  );

  const setTokenLocalUpdate = useCallback((newToken) => {
    if (newToken) {
      localStorage.setItem("token", newToken);
    } else {
      localStorage.removeItem("token");
    }

    setToken(newToken);
  }, []);

  return [token, setTokenLocalUpdate] as const;
};
