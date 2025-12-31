import { useState, useEffect, useCallback, useRef } from 'react';
import { ApiError } from '../lib/api-client';

interface UseAsyncState<T> {
  data: T | null;
  loading: boolean;
  error: ApiError | null;
}

interface UseAsyncOptions<T> {
  immediate?: boolean;
  onSuccess?: (data: T) => void;
  onError?: (error: ApiError) => void;
  dependencies?: any[];
}

export function useAsync<T>(
  asyncFunction: () => Promise<T>,
  options: UseAsyncOptions<T> = {}
) {
  const {
    immediate = true,
    onSuccess,
    onError,
    dependencies = [],
  } = options;

  const [state, setState] = useState<UseAsyncState<T>>({
    data: null,
    loading: immediate,
    error: null,
  });

  const isMountedRef = useRef(true);
  const executionIdRef = useRef(0);

  useEffect(() => {
    return () => {
      isMountedRef.current = false;
    };
  }, []);

  const execute = useCallback(
    async () => {
      const currentExecutionId = ++executionIdRef.current;

      setState((prev) => ({
        ...prev,
        loading: true,
        error: null,
      }));

      try {
        const data = await asyncFunction();

        if (isMountedRef.current && currentExecutionId === executionIdRef.current) {
          setState({
            data,
            loading: false,
            error: null,
          });

          if (onSuccess) {
            onSuccess(data);
          }
        }

        return data;
      } catch (error) {
        if (isMountedRef.current && currentExecutionId === executionIdRef.current) {
          const apiError = error as ApiError;
          setState({
            data: null,
            loading: false,
            error: apiError,
          });

          if (onError) {
            onError(apiError);
          }
        }

        throw error;
      }
    },
    [asyncFunction, onSuccess, onError]
  );

  const reset = useCallback(() => {
    setState({
      data: null,
      loading: false,
      error: null,
    });
  }, []);

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, [immediate, ...dependencies]);

  return {
    ...state,
    execute,
    reset,
  };
}

export default useAsync;
