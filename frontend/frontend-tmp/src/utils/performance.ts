// Performance monitoring utility
class PerformanceMonitor {
  private static instance: PerformanceMonitor;
  private metrics: {
    [key: string]: {
      startTime: number;
      endTime?: number;
      duration?: number;
    };
  } = {};

  private constructor() {}

  public static getInstance(): PerformanceMonitor {
    if (!PerformanceMonitor.instance) {
      PerformanceMonitor.instance = new PerformanceMonitor();
    }
    return PerformanceMonitor.instance;
  }

  public startMeasure(name: string): void {
    if (process.env.NODE_ENV === 'development') {
      this.metrics[name] = {
        startTime: performance.now(),
      };
    }
  }

  public endMeasure(name: string): void {
    if (process.env.NODE_ENV === 'development' && this.metrics[name]) {
      const endTime = performance.now();
      this.metrics[name].endTime = endTime;
      this.metrics[name].duration =
        endTime - this.metrics[name].startTime;
      
      console.log(
        `Performance [${name}]: ${this.metrics[name].duration?.toFixed(2)}ms`
      );
    }
  }

  public clearMetrics(): void {
    this.metrics = {};
  }

  public getMetrics() {
    return this.metrics;
  }
}

export const performanceMonitor = PerformanceMonitor.getInstance();

// React component performance HOC
export function withPerformanceTracking<P extends object>(
  WrappedComponent: React.ComponentType<P>,
  componentName: string
): React.FC<P> {
  return function PerformanceTrackedComponent(props: P) {
    React.useEffect(() => {
      performanceMonitor.startMeasure(`${componentName}_mount`);
      return () => {
        performanceMonitor.endMeasure(`${componentName}_mount`);
      };
    }, []);

    return <WrappedComponent {...props} />;
  };
}

// API performance tracking
export const trackAPIPerformance = async <T,>(
  apiCall: () => Promise<T>,
  name: string
): Promise<T> => {
  performanceMonitor.startMeasure(`API_${name}`);
  try {
    const result = await apiCall();
    performanceMonitor.endMeasure(`API_${name}`);
    return result;
  } catch (error) {
    performanceMonitor.endMeasure(`API_${name}`);
    throw error;
  }
};

// React Query performance hooks
export const useQueryWithPerformance = (queryKey: string[], queryFn: () => Promise<any>, options?: any) => {
  const wrappedQueryFn = async () => {
    return trackAPIPerformance(queryFn, queryKey.join('_'));
  };

  return useQuery(queryKey, wrappedQueryFn, options);
};
