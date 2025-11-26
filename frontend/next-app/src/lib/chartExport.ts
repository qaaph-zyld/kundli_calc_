/**
 * Chart Export Utilities
 * High-quality PDF and PNG export for Vedic charts
 */

import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

export interface ExportOptions {
  format: 'pdf' | 'png' | 'jpg';
  quality: 'standard' | 'high' | 'print';
  includeDetails: boolean;
  paperSize: 'a4' | 'letter' | 'a3';
  orientation: 'portrait' | 'landscape';
  title?: string;
  subtitle?: string;
  includeTimestamp: boolean;
}

const QUALITY_SETTINGS = {
  standard: { scale: 1.5, dpi: 150 },
  high: { scale: 2, dpi: 200 },
  print: { scale: 3, dpi: 300 }
};

const PAPER_SIZES = {
  a4: { width: 210, height: 297 },
  letter: { width: 215.9, height: 279.4 },
  a3: { width: 297, height: 420 }
};

/**
 * Export chart element to PNG
 */
export async function exportToPNG(
  element: HTMLElement,
  options: Partial<ExportOptions> = {}
): Promise<Blob> {
  const quality = QUALITY_SETTINGS[options.quality || 'high'];
  
  const canvas = await html2canvas(element, {
    scale: quality.scale,
    useCORS: true,
    allowTaint: true,
    backgroundColor: '#1a1a2e',
    logging: false
  });

  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => {
        if (blob) {
          resolve(blob);
        } else {
          reject(new Error('Failed to create PNG blob'));
        }
      },
      'image/png',
      1.0
    );
  });
}

/**
 * Export chart element to PDF
 */
export async function exportToPDF(
  element: HTMLElement,
  options: Partial<ExportOptions> = {}
): Promise<Blob> {
  const quality = QUALITY_SETTINGS[options.quality || 'high'];
  const paperSize = PAPER_SIZES[options.paperSize || 'a4'];
  const orientation = options.orientation || 'portrait';
  
  // Capture the element
  const canvas = await html2canvas(element, {
    scale: quality.scale,
    useCORS: true,
    allowTaint: true,
    backgroundColor: '#1a1a2e',
    logging: false
  });
  
  // Create PDF
  const pdf = new jsPDF({
    orientation,
    unit: 'mm',
    format: options.paperSize || 'a4'
  });
  
  const pageWidth = orientation === 'portrait' ? paperSize.width : paperSize.height;
  const pageHeight = orientation === 'portrait' ? paperSize.height : paperSize.width;
  
  // Calculate dimensions to fit the page with margins
  const margin = 10;
  const maxWidth = pageWidth - (margin * 2);
  const maxHeight = pageHeight - (margin * 2) - 30; // Space for header
  
  const imgWidth = canvas.width / quality.scale;
  const imgHeight = canvas.height / quality.scale;
  
  const ratio = Math.min(maxWidth / imgWidth, maxHeight / imgHeight);
  const finalWidth = imgWidth * ratio;
  const finalHeight = imgHeight * ratio;
  
  const x = (pageWidth - finalWidth) / 2;
  const y = margin + 25; // After header
  
  // Add header
  pdf.setFillColor(26, 26, 46);
  pdf.rect(0, 0, pageWidth, 20, 'F');
  
  pdf.setTextColor(255, 255, 255);
  pdf.setFontSize(14);
  pdf.text(options.title || 'Vedic Birth Chart', margin, 12);
  
  if (options.subtitle) {
    pdf.setFontSize(10);
    pdf.text(options.subtitle, margin, 17);
  }
  
  // Add chart image
  const imgData = canvas.toDataURL('image/png', 1.0);
  pdf.addImage(imgData, 'PNG', x, y, finalWidth, finalHeight);
  
  // Add footer with timestamp
  if (options.includeTimestamp) {
    pdf.setFontSize(8);
    pdf.setTextColor(128, 128, 128);
    const timestamp = new Date().toLocaleString();
    pdf.text(`Generated: ${timestamp}`, margin, pageHeight - 5);
    pdf.text('Kundli Calculator', pageWidth - margin - 30, pageHeight - 5);
  }
  
  return pdf.output('blob');
}

/**
 * Export full chart with details to multi-page PDF
 */
export async function exportFullChartPDF(
  chartElement: HTMLElement,
  analysisElement: HTMLElement | null,
  birthDetails: {
    name?: string;
    date: string;
    time: string;
    place: string;
  },
  options: Partial<ExportOptions> = {}
): Promise<Blob> {
  const quality = QUALITY_SETTINGS[options.quality || 'high'];
  const paperSize = PAPER_SIZES[options.paperSize || 'a4'];
  const orientation = options.orientation || 'portrait';
  
  const pdf = new jsPDF({
    orientation,
    unit: 'mm',
    format: options.paperSize || 'a4'
  });
  
  const pageWidth = orientation === 'portrait' ? paperSize.width : paperSize.height;
  const pageHeight = orientation === 'portrait' ? paperSize.height : paperSize.width;
  const margin = 15;
  
  // === PAGE 1: Title Page ===
  
  // Header background
  pdf.setFillColor(102, 126, 234);
  pdf.rect(0, 0, pageWidth, 60, 'F');
  
  // Title
  pdf.setTextColor(255, 255, 255);
  pdf.setFontSize(24);
  pdf.text('जन्म कुण्डली', pageWidth / 2, 25, { align: 'center' });
  pdf.setFontSize(16);
  pdf.text('Vedic Birth Chart', pageWidth / 2, 35, { align: 'center' });
  
  if (birthDetails.name) {
    pdf.setFontSize(18);
    pdf.text(birthDetails.name, pageWidth / 2, 50, { align: 'center' });
  }
  
  // Birth details box
  pdf.setTextColor(0, 0, 0);
  pdf.setFillColor(245, 245, 245);
  pdf.roundedRect(margin, 70, pageWidth - (margin * 2), 40, 5, 5, 'F');
  
  pdf.setFontSize(11);
  pdf.text('Birth Details', pageWidth / 2, 80, { align: 'center' });
  pdf.setFontSize(10);
  pdf.text(`Date: ${birthDetails.date}`, margin + 10, 92);
  pdf.text(`Time: ${birthDetails.time}`, margin + 10, 100);
  pdf.text(`Place: ${birthDetails.place}`, pageWidth / 2, 92);
  
  // Capture and add chart
  const chartCanvas = await html2canvas(chartElement, {
    scale: quality.scale,
    useCORS: true,
    backgroundColor: '#1a1a2e'
  });
  
  const maxChartWidth = pageWidth - (margin * 2);
  const maxChartHeight = pageHeight - 150;
  const chartRatio = Math.min(
    maxChartWidth / (chartCanvas.width / quality.scale),
    maxChartHeight / (chartCanvas.height / quality.scale)
  );
  
  const chartWidth = (chartCanvas.width / quality.scale) * chartRatio;
  const chartHeight = (chartCanvas.height / quality.scale) * chartRatio;
  const chartX = (pageWidth - chartWidth) / 2;
  const chartY = 120;
  
  const chartImgData = chartCanvas.toDataURL('image/png', 1.0);
  pdf.addImage(chartImgData, 'PNG', chartX, chartY, chartWidth, chartHeight);
  
  // Footer
  pdf.setFontSize(8);
  pdf.setTextColor(128, 128, 128);
  pdf.text(`Generated: ${new Date().toLocaleString()}`, margin, pageHeight - 10);
  pdf.text('Page 1', pageWidth - margin - 15, pageHeight - 10);
  
  // === PAGE 2: Analysis (if provided) ===
  if (analysisElement && options.includeDetails) {
    pdf.addPage();
    
    // Header
    pdf.setFillColor(102, 126, 234);
    pdf.rect(0, 0, pageWidth, 25, 'F');
    pdf.setTextColor(255, 255, 255);
    pdf.setFontSize(14);
    pdf.text('Detailed Analysis', pageWidth / 2, 15, { align: 'center' });
    
    // Capture analysis
    const analysisCanvas = await html2canvas(analysisElement, {
      scale: quality.scale,
      useCORS: true,
      backgroundColor: '#1a1a2e'
    });
    
    const maxAnalysisWidth = pageWidth - (margin * 2);
    const maxAnalysisHeight = pageHeight - 50;
    const analysisRatio = Math.min(
      maxAnalysisWidth / (analysisCanvas.width / quality.scale),
      maxAnalysisHeight / (analysisCanvas.height / quality.scale)
    );
    
    const analysisWidth = (analysisCanvas.width / quality.scale) * analysisRatio;
    const analysisHeight = (analysisCanvas.height / quality.scale) * analysisRatio;
    const analysisX = (pageWidth - analysisWidth) / 2;
    
    const analysisImgData = analysisCanvas.toDataURL('image/png', 1.0);
    pdf.addImage(analysisImgData, 'PNG', analysisX, 35, analysisWidth, analysisHeight);
    
    // Footer
    pdf.setFontSize(8);
    pdf.setTextColor(128, 128, 128);
    pdf.text('Page 2', pageWidth - margin - 15, pageHeight - 10);
  }
  
  return pdf.output('blob');
}

/**
 * Download blob as file
 */
export function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Quick export with automatic filename
 */
export async function quickExport(
  element: HTMLElement,
  format: 'pdf' | 'png',
  name: string = 'chart'
): Promise<void> {
  const timestamp = new Date().toISOString().split('T')[0];
  const filename = `${name}_${timestamp}.${format}`;
  
  if (format === 'pdf') {
    const blob = await exportToPDF(element, {
      quality: 'high',
      title: name,
      includeTimestamp: true
    });
    downloadBlob(blob, filename);
  } else {
    const blob = await exportToPNG(element, { quality: 'high' });
    downloadBlob(blob, filename);
  }
}

/**
 * Generate shareable chart image
 */
export async function generateShareableImage(
  element: HTMLElement,
  watermark: string = 'Kundli Calculator'
): Promise<string> {
  const canvas = await html2canvas(element, {
    scale: 2,
    useCORS: true,
    backgroundColor: '#1a1a2e'
  });
  
  // Add watermark
  const ctx = canvas.getContext('2d');
  if (ctx) {
    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.font = '14px Arial';
    ctx.fillText(watermark, 10, canvas.height - 10);
  }
  
  return canvas.toDataURL('image/png', 0.9);
}
