#!/usr/bin/env python3
"""
Dasha Bhukti Report Extractor
Extracts planetary dasha reports from AstroVed URLs
Supports JSON, CSV, and Markdown output formats
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import csv
import sys
import argparse
import logging
from urllib.parse import urlparse, parse_qs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class BirthDetails:
    """Birth details data structure"""
    birth_date: str
    birth_time: str
    city: str
    state: str
    country: str
    moon_sign: str
    birth_star: str


@dataclass
class DashaEntry:
    """Individual dasha period entry"""
    planet: str
    start_date: str
    end_date: str


@dataclass
class DashaReport:
    """Complete dasha report structure"""
    birth_details: BirthDetails
    current_dasha: Optional[Dict[str, Dict[str, str]]]
    dasha_periods: List[DashaEntry]
    extracted_at: str


class DashaExtractor:
    """Main extractor class for Dasha Bhukti reports"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
    
    def extract_birth_details(self, soup: BeautifulSoup) -> BirthDetails:
        """Extract birth details from the page"""
        details_table = soup.find('table', {'class': 'table'})
        
        if not details_table:
            # Fallback: try to find by headers
            details_table = soup.find('h3', string='Birth Details')
            if details_table:
                details_table = details_table.find_next('table')
        
        details = {}
        if details_table:
            rows = details_table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    key = cols[0].get_text(strip=True).rstrip(':')
                    value = cols[1].get_text(strip=True)
                    details[key] = value
        
        return BirthDetails(
            birth_date=details.get('Birth Date', ''),
            birth_time=details.get('Birth Time', ''),
            city=details.get('City', ''),
            state=details.get('State', ''),
            country=details.get('Country', ''),
            moon_sign=details.get('Moon sign', ''),
            birth_star=details.get('Birth Star', '')
        )
    
    def extract_current_dasha(self, soup: BeautifulSoup) -> Optional[Dict[str, str]]:
        """Extract current dasha information"""
        current_dasha = {}
        
        # Look for Saturn and Venus boxes
        dasha_boxes = soup.find_all('div', class_='box')
        
        for box in dasha_boxes:
            planet_elem = box.find('h3')
            if planet_elem:
                planet = planet_elem.get_text(strip=True)
                
                # Extract date range
                date_text = box.get_text()
                if 'From' in date_text and 'To' in date_text:
                    lines = [l.strip() for l in date_text.split('\n') if l.strip()]
                    from_date = ''
                    to_date = ''
                    
                    for i, line in enumerate(lines):
                        if 'From' in line and i + 1 < len(lines):
                            from_date = lines[i + 1]
                        if 'To' in line and i + 1 < len(lines):
                            to_date = lines[i + 1]
                    
                    current_dasha[planet] = {
                        'from': from_date,
                        'to': to_date
                    }
        
        if current_dasha:
            return current_dasha

        # Fallback: parse current dasha information from plain text when boxes are not present
        text = soup.get_text("\n", strip=True)
        lines = [l.strip() for l in text.splitlines() if l.strip()]

        planet_names = [
            'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter',
            'Venus', 'Saturn', 'Rahu', 'Ketu'
        ]

        def find_planet(text_segment: str) -> Optional[str]:
            lower = text_segment.lower()
            for name in planet_names:
                if name.lower() in lower:
                    return name
            return None

        def extract_range(start_idx: int) -> Optional[Dict[str, str]]:
            from_date = ''
            to_date = ''
            for j in range(start_idx + 1, min(len(lines), start_idx + 10)):
                line_j = lines[j]
                lower_j = line_j.lower()
                if lower_j.startswith('from:'):
                    from_date = line_j.split(':', 1)[1].strip()
                elif lower_j.startswith('to:'):
                    to_date = line_j.split(':', 1)[1].strip()
                if from_date and to_date:
                    break
            if from_date and to_date:
                return {
                    'from': from_date,
                    'to': to_date
                }
            return None

        for idx, line in enumerate(lines):
            lowered = line.lower()
            if 'major period of' in lowered:
                planet = find_planet(' '.join(lines[idx:idx + 3]))
                period = extract_range(idx)
                if planet and period and planet not in current_dasha:
                    current_dasha[planet] = period
            elif 'minor period of' in lowered:
                planet = find_planet(' '.join(lines[idx:idx + 3]))
                period = extract_range(idx)
                if planet and period and planet not in current_dasha:
                    current_dasha[planet] = period

        return current_dasha if current_dasha else None
    
    def extract_dasha_periods(self, soup: BeautifulSoup) -> List[DashaEntry]:
        """Extract planetary dasha periods table"""
        periods = []
        
        # Find the table with planetary periods
        table = None

        # First, try to locate the section header across all heading levels
        period_header = soup.find(
            lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
            and tag.get_text(strip=True)
            and 'Duration of Planetary' in tag.get_text()
        )

        if period_header:
            table = period_header.find_next('table')

        # Fallback: scan all tables and pick the one whose header row contains
        # "Start Date" and "End Date"
        if not table:
            for candidate in soup.find_all('table'):
                header_row = candidate.find('tr')
                if not header_row:
                    continue
                header_text = ' '.join(
                    cell.get_text(strip=True) for cell in header_row.find_all(['th', 'td'])
                )
                if 'Start Date' in header_text and 'End Date' in header_text:
                    table = candidate
                    break

        if table:
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                cols = row.find_all(['td', 'th'])
                if len(cols) >= 3:
                    planet_cell = cols[0]
                    # Extract planet name from img alt or text
                    planet = planet_cell.get_text(strip=True)
                    if not planet:
                        img = planet_cell.find('img')
                        if img and img.get('alt'):
                            planet = img['alt']
                    
                    start_cell = cols[-2]
                    end_cell = cols[-1]
                    start_date = start_cell.get_text(strip=True).replace('Start Date:', '').strip()
                    end_date = end_cell.get_text(strip=True).replace('End Date:', '').strip()
                    
                    if planet and start_date and end_date:
                        periods.append(DashaEntry(
                            planet=planet,
                            start_date=start_date,
                            end_date=end_date
                        ))

        return periods
    
    def _parse_soup(self, soup: BeautifulSoup) -> DashaReport:
        birth_details = self.extract_birth_details(soup)
        current_dasha = self.extract_current_dasha(soup)
        dasha_periods = self.extract_dasha_periods(soup)

        return DashaReport(
            birth_details=birth_details,
            current_dasha=current_dasha,
            dasha_periods=dasha_periods,
            extracted_at=datetime.now().isoformat()
        )

    def fetch_and_parse(self, url: str) -> DashaReport:
        """Fetch URL and parse the dasha report"""
        logger.info(f"Fetching URL: {url}")

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch URL: {e}")
            raise

        soup = BeautifulSoup(response.content, 'html.parser')
        return self._parse_soup(soup)

    def fetch_and_parse_html(self, html: str) -> DashaReport:
        soup = BeautifulSoup(html, 'html.parser')
        return self._parse_soup(soup)

    def fetch_and_parse_selenium(self, url: str, driver) -> DashaReport:
        logger.info(f"Fetching URL with browser driver: {url}")
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        return self._parse_soup(soup)

    def fetch_and_parse_api_html(self, api_url: str, params: Optional[Dict[str, str]] = None) -> DashaReport:
        logger.info(f"Fetching API HTML from: {api_url}")
        try:
            response = self.session.get(api_url, params=params, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch API URL: {e}")
            raise

        return self.fetch_and_parse_html(response.text)
    
    def to_json(self, report: DashaReport) -> str:
        """Convert report to JSON format"""
        data = {
            'birth_details': asdict(report.birth_details),
            'current_dasha': report.current_dasha,
            'dasha_periods': [asdict(entry) for entry in report.dasha_periods],
            'extracted_at': report.extracted_at
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def to_csv(self, report: DashaReport) -> str:
        """Convert report to CSV format (dasha periods)"""
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write birth details as header comments
        writer.writerow(['# Birth Details'])
        for key, value in asdict(report.birth_details).items():
            writer.writerow([f'# {key}', value])
        writer.writerow([])
        
        # Write dasha periods
        writer.writerow(['Planet', 'Start Date', 'End Date'])
        for period in report.dasha_periods:
            writer.writerow([period.planet, period.start_date, period.end_date])
        
        return output.getvalue()
    
    def to_markdown(self, report: DashaReport) -> str:
        """Convert report to Markdown format"""
        md = []
        md.append("# Dasha Bhukti Report\n")
        
        # Birth Details
        md.append("## Birth Details\n")
        for key, value in asdict(report.birth_details).items():
            if value:
                md.append(f"- **{key.replace('_', ' ').title()}**: {value}")
        md.append("")
        
        # Current Dasha
        if report.current_dasha:
            md.append("## Current Dasha\n")
            for planet, dates in report.current_dasha.items():
                md.append(f"### {planet}")
                md.append(f"- From: {dates['from']}")
                md.append(f"- To: {dates['to']}")
                md.append("")
        
        # Dasha Periods
        md.append("## Planetary Dasha Periods\n")
        md.append("| Planet | Start Date | End Date |")
        md.append("|--------|------------|----------|")
        for period in report.dasha_periods:
            md.append(f"| {period.planet} | {period.start_date} | {period.end_date} |")
        
        md.append(f"\n---\n*Extracted at: {report.extracted_at}*")
        
        return "\n".join(md)


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description='Extract Dasha Bhukti reports from AstroVed URLs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -u "https://astroved.com/..." -f json
  %(prog)s -u "https://astroved.com/..." -f csv -o report.csv
  %(prog)s -u "https://astroved.com/..." -f markdown -o report.md
        """
    )
    
    parser.add_argument(
        '-u', '--url',
        required=True,
        help='AstroVed Dasha Bhukti calculator URL'
    )
    parser.add_argument(
        '-f', '--format',
        choices=['json', 'csv', 'markdown'],
        default='json',
        help='Output format (default: json)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: stdout)'
    )
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=30,
        help='Request timeout in seconds (default: 30)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Initialize extractor
    extractor = DashaExtractor(timeout=args.timeout)
    
    try:
        # Fetch and parse report
        report = extractor.fetch_and_parse(args.url)
        
        # Convert to requested format
        if args.format == 'json':
            output = extractor.to_json(report)
        elif args.format == 'csv':
            output = extractor.to_csv(report)
        else:  # markdown
            output = extractor.to_markdown(report)
        
        # Write output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            logger.info(f"Report saved to {args.output}")
        else:
            print(output)
        
        logger.info("Extraction completed successfully")
        
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
