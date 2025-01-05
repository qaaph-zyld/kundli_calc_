/**
 * Frontend Performance Optimization Module
 * PGF Protocol: OPT_002
 * Gate: GATE_5
 * Version: 1.0.0
 */

import { lazy, Suspense } from 'react';
import { debounce, throttle } from 'lodash';

// Lazy loading utility for components
export const lazyLoad = (importFunc: () => Promise<any>, fallback: JSX.Element) => {
  const LazyComponent = lazy(importFunc);
  return (props: any) => (
    <Suspense fallback={fallback}>
      <LazyComponent {...props} />
    </Suspense>
  );
};

// Image optimization utility
export const optimizeImage = (url: string, width?: number, quality?: number): string => {
  const params = new URLSearchParams();
  if (width) params.append('w', width.toString());
  if (quality) params.append('q', quality.toString());
  return `${url}?${params.toString()}`;
};

// Performance monitoring
export class PerformanceMonitor {
  private metrics: {
    [key: string]: {
      start: number;
      end?: number;
      duration?: number;
    };
  } = {};

  startMeasure(name: string): void {
    this.metrics[name] = {
      start: performance.now()
    };
  }

  endMeasure(name: string): number {
    const metric = this.metrics[name];
    if (metric) {
      metric.end = performance.now();
      metric.duration = metric.end - metric.start;
      return metric.duration;
    }
    return 0;
  }

  getMetrics(): Record<string, number> {
    return Object.entries(this.metrics).reduce((acc, [key, value]) => ({
      ...acc,
      [key]: value.duration || 0
    }), {});
  }
}

// Resource preloading
export const preloadResources = (resources: string[]): void => {
  resources.forEach(resource => {
    const link = document.createElement('link');
    link.rel = 'preload';
    link.href = resource;
    link.as = resource.endsWith('.js') ? 'script' : 
              resource.endsWith('.css') ? 'style' : 
              resource.match(/\.(jpg|png|gif|webp)$/) ? 'image' : 
              'fetch';
    document.head.appendChild(link);
  });
};

// Debounced API calls
export const createDebouncedApi = <T>(
  apiCall: (...args: any[]) => Promise<T>,
  wait: number = 300
) => debounce(apiCall, wait);

// Throttled event handlers
export const createThrottledHandler = (
  handler: (...args: any[]) => void,
  wait: number = 100
) => throttle(handler, wait);

// Virtual scrolling utility
export class VirtualScroller {
  private itemHeight: number;
  private containerHeight: number;
  private items: any[];
  private overscan: number;

  constructor(
    itemHeight: number,
    containerHeight: number,
    items: any[],
    overscan: number = 3
  ) {
    this.itemHeight = itemHeight;
    this.containerHeight = containerHeight;
    this.items = items;
    this.overscan = overscan;
  }

  getVisibleRange(scrollTop: number): {
    start: number;
    end: number;
    paddingTop: number;
    paddingBottom: number;
  } {
    const startIndex = Math.floor(scrollTop / this.itemHeight);
    const endIndex = Math.min(
      startIndex + Math.ceil(this.containerHeight / this.itemHeight) + this.overscan,
      this.items.length
    );

    return {
      start: Math.max(0, startIndex - this.overscan),
      end: endIndex,
      paddingTop: Math.max(0, startIndex - this.overscan) * this.itemHeight,
      paddingBottom: Math.max(
        0,
        (this.items.length - endIndex) * this.itemHeight
      )
    };
  }
}

// Progressive image loading
export class ProgressiveImage {
  private src: string;
  private placeholder: string;
  private onLoad: () => void;

  constructor(src: string, placeholder: string, onLoad: () => void) {
    this.src = src;
    this.placeholder = placeholder;
    this.onLoad = onLoad;
    this.preloadImage();
  }

  private preloadImage(): void {
    const img = new Image();
    img.src = this.src;
    img.onload = this.onLoad;
  }

  getSrc(): string {
    return this.placeholder;
  }
}

// Bundle size analyzer
export const analyzeBundleSize = async (
  bundlePath: string
): Promise<{ size: number; gzipSize: number }> => {
  const response = await fetch(bundlePath);
  const content = await response.text();
  
  return {
    size: content.length,
    gzipSize: await getGzipSize(content)
  };
};

// Memory leak detector
export class MemoryLeakDetector {
  private intervals: Set<number> = new Set();
  private timeouts: Set<number> = new Set();
  private observers: Set<any> = new Set();

  trackInterval(id: number): void {
    this.intervals.add(id);
  }

  trackTimeout(id: number): void {
    this.timeouts.add(id);
  }

  trackObserver(observer: any): void {
    this.observers.add(observer);
  }

  cleanup(): void {
    this.intervals.forEach(clearInterval);
    this.timeouts.forEach(clearTimeout);
    this.observers.forEach(observer => observer.disconnect());
    
    this.intervals.clear();
    this.timeouts.clear();
    this.observers.clear();
  }

  getStats(): { intervals: number; timeouts: number; observers: number } {
    return {
      intervals: this.intervals.size,
      timeouts: this.timeouts.size,
      observers: this.observers.size
    };
  }
}

// Service worker registration
export const registerServiceWorker = async (): Promise<void> => {
  if ('serviceWorker' in navigator) {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js');
      console.log('ServiceWorker registered:', registration);
    } catch (error) {
      console.error('ServiceWorker registration failed:', error);
    }
  }
};

// Performance metrics collector
export class PerformanceMetrics {
  private metrics: {
    fcp: number;
    lcp: number;
    fid: number;
    cls: number;
  } = {
    fcp: 0,
    lcp: 0,
    fid: 0,
    cls: 0
  };

  constructor() {
    this.initializeObservers();
  }

  private initializeObservers(): void {
    // First Contentful Paint
    new PerformanceObserver((entryList) => {
      const entries = entryList.getEntries();
      this.metrics.fcp = entries[entries.length - 1].startTime;
    }).observe({ entryTypes: ['paint'] });

    // Largest Contentful Paint
    new PerformanceObserver((entryList) => {
      const entries = entryList.getEntries();
      this.metrics.lcp = entries[entries.length - 1].startTime;
    }).observe({ entryTypes: ['largest-contentful-paint'] });

    // First Input Delay
    new PerformanceObserver((entryList) => {
      const entries = entryList.getEntries();
      this.metrics.fid = entries[0].duration;
    }).observe({ entryTypes: ['first-input'] });

    // Cumulative Layout Shift
    new PerformanceObserver((entryList) => {
      let cls = 0;
      entryList.getEntries().forEach((entry: any) => {
        if (!entry.hadRecentInput) {
          cls += entry.value;
        }
      });
      this.metrics.cls = cls;
    }).observe({ entryTypes: ['layout-shift'] });
  }

  getMetrics(): typeof this.metrics {
    return { ...this.metrics };
  }
}

// Helper function for gzip size calculation
async function getGzipSize(content: string): Promise<number> {
  const blob = new Blob([content], { type: 'text/plain' });
  return blob.size;
}
