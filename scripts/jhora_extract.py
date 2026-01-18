#!/usr/bin/env python3
"""
JHora Reference Data Extraction Toolkit

Automates extraction of calculation outputs from Jagannatha Hora for validation.
Supports Windows (native JHora) and Wine (Linux/Mac).

Usage:
    python jhora_extract.py --birth-data birth_data.json --output reference_output.json
    python jhora_extract.py --batch batch_births.json --output-dir ./fixtures/
"""

import argparse
import json
import subprocess
import sys
import time
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional
import platform

# Conditional imports for Windows automation
try:
    if platform.system() == "Windows":
        import pyautogui
        import pyperclip
        HAS_GUI_AUTOMATION = True
    else:
        HAS_GUI_AUTOMATION = False
except ImportError:
    HAS_GUI_AUTOMATION = False


@dataclass
class BirthData:
    """Canonical birth data format"""
    name: str
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int = 0
    latitude: float = 0.0
    longitude: float = 0.0
    timezone_offset: float = 0.0  # Hours from UTC
    timezone_name: str = ""
    location_name: str = ""
    dst: bool = False
    
    @classmethod
    def from_dict(cls, d: dict) -> 'BirthData':
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class PlanetaryPosition:
    """Single planet position data"""
    planet: str
    longitude: float  # Degrees (0-360)
    latitude: float
    speed: float  # Degrees per day
    sign: str
    sign_num: int  # 1-12
    degree_in_sign: float
    nakshatra: str
    nakshatra_num: int  # 1-27
    nakshatra_pada: int  # 1-4
    retrograde: bool


@dataclass
class DashaPeriod:
    """Dasha/Bhukti period data"""
    level: str  # "mahadasha", "bhukti", "antardasha", "pratyantara"
    planet: str
    start_date: str  # ISO format
    end_date: str
    duration_days: int


@dataclass 
class JHoraReference:
    """Complete JHora reference output"""
    extraction_date: str
    jhora_version: str
    birth_data: dict
    ayanamsa: str
    ayanamsa_value: float
    house_system: str
    planetary_positions: list
    house_cusps: list
    vimshottari_dasha: list
    lagna_degree: float
    moon_nakshatra: str
    moon_nakshatra_pada: int
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


class JHoraTextParser:
    """
    Parses JHora text export format.
    JHora can export chart data as text via Edit → Copy Chart Data
    """
    
    PLANET_NAMES = [
        "Sun", "Moon", "Mars", "Mercury", "Jupiter", 
        "Venus", "Saturn", "Rahu", "Ketu"
    ]
    
    SIGN_NAMES = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    
    NAKSHATRA_NAMES = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
        "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]

    def __init__(self, text: str):
        self.text = text
        self.lines = text.strip().split('\n')
    
    def parse_planetary_positions(self) -> list[PlanetaryPosition]:
        """Extract planetary positions from JHora text output"""
        positions = []
        
        # Pattern: Planet  Sign  Deg:Min:Sec  Nakshatra  Pada  Speed  R
        # Example: Sun     Ari   15:23:45     Bharani    2     0.98   
        planet_pattern = re.compile(
            r'(\w+)\s+'           # Planet name
            r'(\w+)\s+'           # Sign abbreviation
            r'(\d+):(\d+):(\d+)'  # Degrees:Minutes:Seconds
            r'\s+(\w+)\s+'        # Nakshatra
            r'(\d+)\s+'           # Pada
            r'([-\d.]+)'          # Speed
            r'\s*(R)?'            # Retrograde marker
        )
        
        for line in self.lines:
            match = planet_pattern.search(line)
            if match:
                planet, sign_abbr, deg, min_, sec, nakshatra, pada, speed, retro = match.groups()
                
                if planet in self.PLANET_NAMES:
                    sign_full = self._expand_sign(sign_abbr)
                    sign_num = self.SIGN_NAMES.index(sign_full) + 1 if sign_full in self.SIGN_NAMES else 0
                    
                    degree_in_sign = float(deg) + float(min_)/60 + float(sec)/3600
                    longitude = (sign_num - 1) * 30 + degree_in_sign
                    
                    positions.append(PlanetaryPosition(
                        planet=planet,
                        longitude=round(longitude, 6),
                        latitude=0.0,  # JHora text export may not include
                        speed=float(speed),
                        sign=sign_full,
                        sign_num=sign_num,
                        degree_in_sign=round(degree_in_sign, 6),
                        nakshatra=nakshatra,
                        nakshatra_num=self._nakshatra_num(nakshatra),
                        nakshatra_pada=int(pada),
                        retrograde=retro == 'R'
                    ))
        
        return positions
    
    def parse_dasha_periods(self) -> list[DashaPeriod]:
        """Extract Vimshottari dasha periods"""
        periods = []
        
        # Pattern: Planet  Start-Date  End-Date
        # Example: Sun MD  2020-01-15  2026-01-15
        dasha_pattern = re.compile(
            r'(\w+)\s+(MD|AD|PD|SD)\s+'  # Planet and level
            r'(\d{4}-\d{2}-\d{2})\s+'     # Start date
            r'(\d{4}-\d{2}-\d{2})'        # End date
        )
        
        level_map = {
            'MD': 'mahadasha',
            'AD': 'bhukti', 
            'PD': 'antardasha',
            'SD': 'pratyantara'
        }
        
        for line in self.lines:
            match = dasha_pattern.search(line)
            if match:
                planet, level_abbr, start, end = match.groups()
                
                start_dt = datetime.strptime(start, '%Y-%m-%d')
                end_dt = datetime.strptime(end, '%Y-%m-%d')
                
                periods.append(DashaPeriod(
                    level=level_map.get(level_abbr, level_abbr),
                    planet=planet,
                    start_date=start,
                    end_date=end,
                    duration_days=(end_dt - start_dt).days
                ))
        
        return periods
    
    def parse_ayanamsa(self) -> tuple[str, float]:
        """Extract ayanamsa name and value"""
        # Pattern: Ayanamsa: Lahiri  24:07:23
        pattern = re.compile(r'Ayanamsa:\s*(\w+)\s+(\d+):(\d+):(\d+)')
        
        for line in self.lines:
            match = pattern.search(line)
            if match:
                name, deg, min_, sec = match.groups()
                value = float(deg) + float(min_)/60 + float(sec)/3600
                return name, round(value, 6)
        
        return "Unknown", 0.0
    
    def _expand_sign(self, abbr: str) -> str:
        """Expand sign abbreviation to full name"""
        abbr_map = {
            'Ari': 'Aries', 'Tau': 'Taurus', 'Gem': 'Gemini',
            'Can': 'Cancer', 'Leo': 'Leo', 'Vir': 'Virgo',
            'Lib': 'Libra', 'Sco': 'Scorpio', 'Sag': 'Sagittarius',
            'Cap': 'Capricorn', 'Aqu': 'Aquarius', 'Pis': 'Pisces'
        }
        return abbr_map.get(abbr, abbr)
    
    def _nakshatra_num(self, name: str) -> int:
        """Get nakshatra number (1-27)"""
        # Handle partial matches
        for i, nk in enumerate(self.NAKSHATRA_NAMES, 1):
            if name.lower() in nk.lower() or nk.lower().startswith(name.lower()):
                return i
        return 0


class JHoraFileParser:
    """
    Parses JHora .jhd save files directly.
    JHora save files are XML-based.
    """
    
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.data = None
    
    def parse(self) -> Optional[JHoraReference]:
        """Parse JHora save file"""
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            
            # Extract birth data
            birth_elem = root.find('.//BirthData')
            if birth_elem is None:
                return None
            
            # Extract planetary positions
            planets_elem = root.find('.//Planets')
            positions = []
            if planets_elem is not None:
                for planet_elem in planets_elem.findall('Planet'):
                    positions.append(PlanetaryPosition(
                        planet=planet_elem.get('name', ''),
                        longitude=float(planet_elem.get('longitude', 0)),
                        latitude=float(planet_elem.get('latitude', 0)),
                        speed=float(planet_elem.get('speed', 0)),
                        sign=planet_elem.get('sign', ''),
                        sign_num=int(planet_elem.get('signNum', 0)),
                        degree_in_sign=float(planet_elem.get('degreeInSign', 0)),
                        nakshatra=planet_elem.get('nakshatra', ''),
                        nakshatra_num=int(planet_elem.get('nakshatraNum', 0)),
                        nakshatra_pada=int(planet_elem.get('pada', 0)),
                        retrograde=planet_elem.get('retrograde', 'false') == 'true'
                    ))
            
            # Build reference object
            return JHoraReference(
                extraction_date=datetime.now().isoformat(),
                jhora_version=root.get('version', 'unknown'),
                birth_data=self._extract_birth_dict(birth_elem),
                ayanamsa=root.find('.//Ayanamsa').get('name', 'Lahiri'),
                ayanamsa_value=float(root.find('.//Ayanamsa').get('value', 0)),
                house_system=root.find('.//HouseSystem').get('name', 'Whole Sign'),
                planetary_positions=[asdict(p) for p in positions],
                house_cusps=self._extract_houses(root),
                vimshottari_dasha=self._extract_dasha(root),
                lagna_degree=float(root.find('.//Lagna').get('degree', 0)),
                moon_nakshatra=root.find('.//Moon').get('nakshatra', ''),
                moon_nakshatra_pada=int(root.find('.//Moon').get('pada', 0))
            )
            
        except Exception as e:
            print(f"Error parsing JHora file: {e}", file=sys.stderr)
            return None
    
    def _extract_birth_dict(self, elem) -> dict:
        return {
            'year': int(elem.get('year', 0)),
            'month': int(elem.get('month', 0)),
            'day': int(elem.get('day', 0)),
            'hour': int(elem.get('hour', 0)),
            'minute': int(elem.get('minute', 0)),
            'second': int(elem.get('second', 0)),
            'latitude': float(elem.get('latitude', 0)),
            'longitude': float(elem.get('longitude', 0)),
            'timezone_offset': float(elem.get('timezone', 0))
        }
    
    def _extract_houses(self, root) -> list:
        houses = []
        houses_elem = root.find('.//Houses')
        if houses_elem:
            for h in houses_elem.findall('House'):
                houses.append({
                    'house': int(h.get('num', 0)),
                    'cusp_degree': float(h.get('cusp', 0)),
                    'sign': h.get('sign', '')
                })
        return houses
    
    def _extract_dasha(self, root) -> list:
        periods = []
        dasha_elem = root.find('.//VimshottariDasha')
        if dasha_elem:
            for period in dasha_elem.findall('.//Period'):
                periods.append({
                    'level': period.get('level', ''),
                    'planet': period.get('planet', ''),
                    'start_date': period.get('start', ''),
                    'end_date': period.get('end', ''),
                    'duration_days': int(period.get('days', 0))
                })
        return periods


class JHoraAutomation:
    """
    GUI automation for JHora (Windows only).
    Automates: Open JHora → Enter birth data → Copy chart data → Parse
    """
    
    def __init__(self, jhora_path: str = r"C:\Program Files\JHora\jhora.exe"):
        if not HAS_GUI_AUTOMATION:
            raise RuntimeError("GUI automation requires Windows with pyautogui and pyperclip")
        self.jhora_path = jhora_path
        self.delay = 0.5  # Seconds between actions
    
    def extract_reference(self, birth_data: BirthData) -> Optional[JHoraReference]:
        """Automate JHora to extract reference data"""
        try:
            # Launch JHora
            subprocess.Popen([self.jhora_path])
            time.sleep(3)  # Wait for app to load
            
            # Open new chart dialog (Ctrl+N)
            pyautogui.hotkey('ctrl', 'n')
            time.sleep(1)
            
            # Enter birth data
            self._enter_birth_data(birth_data)
            
            # Wait for chart to calculate
            time.sleep(2)
            
            # Copy chart data (Edit → Copy Chart Data or custom hotkey)
            pyautogui.hotkey('ctrl', 'shift', 'c')  # Assuming custom hotkey
            time.sleep(0.5)
            
            # Get clipboard content
            chart_text = pyperclip.paste()
            
            # Parse the text
            parser = JHoraTextParser(chart_text)
            
            ayanamsa_name, ayanamsa_value = parser.parse_ayanamsa()
            
            return JHoraReference(
                extraction_date=datetime.now().isoformat(),
                jhora_version="8.0",  # Update as needed
                birth_data=asdict(birth_data),
                ayanamsa=ayanamsa_name,
                ayanamsa_value=ayanamsa_value,
                house_system="Whole Sign",
                planetary_positions=[asdict(p) for p in parser.parse_planetary_positions()],
                house_cusps=[],  # May not be in text export
                vimshottari_dasha=[asdict(d) for d in parser.parse_dasha_periods()],
                lagna_degree=0.0,  # Extract from positions
                moon_nakshatra="",  # Extract from Moon position
                moon_nakshatra_pada=0
            )
            
        except Exception as e:
            print(f"Automation error: {e}", file=sys.stderr)
            return None
        finally:
            # Close JHora
            pyautogui.hotkey('alt', 'F4')
    
    def _enter_birth_data(self, bd: BirthData):
        """Tab through JHora's birth data dialog and enter values"""
        fields = [
            str(bd.year), str(bd.month), str(bd.day),
            str(bd.hour), str(bd.minute), str(bd.second),
            str(bd.latitude), str(bd.longitude),
            str(bd.timezone_offset)
        ]
        
        for value in fields:
            pyautogui.typewrite(value, interval=0.05)
            pyautogui.press('tab')
            time.sleep(self.delay)
        
        # Submit dialog
        pyautogui.press('enter')


def create_manual_template(birth_data: BirthData, output_path: Path):
    """
    Create a template JSON for manual JHora data entry.
    User fills in values from JHora manually.
    """
    template = {
        "_instructions": [
            "1. Open JHora and enter the birth data below",
            "2. Go to Edit → Copy Chart Data (or use text export)",
            "3. Fill in the planetary positions from JHora",
            "4. Fill in the dasha periods from JHora",
            "5. Remove this _instructions field before saving"
        ],
        "extraction_date": datetime.now().isoformat(),
        "jhora_version": "FILL_IN",
        "birth_data": asdict(birth_data),
        "ayanamsa": "Lahiri",
        "ayanamsa_value": 0.0,  # FILL_IN: e.g., 24.123456
        "house_system": "Whole Sign",
        "planetary_positions": [
            {
                "planet": planet,
                "longitude": 0.0,  # FILL_IN
                "latitude": 0.0,
                "speed": 0.0,
                "sign": "",  # FILL_IN
                "sign_num": 0,
                "degree_in_sign": 0.0,  # FILL_IN
                "nakshatra": "",  # FILL_IN
                "nakshatra_num": 0,
                "nakshatra_pada": 0,  # FILL_IN
                "retrograde": False
            }
            for planet in JHoraTextParser.PLANET_NAMES
        ],
        "house_cusps": [
            {"house": i, "cusp_degree": 0.0, "sign": ""}
            for i in range(1, 13)
        ],
        "vimshottari_dasha": [
            {
                "level": "mahadasha",
                "planet": "",  # FILL_IN
                "start_date": "",  # FILL_IN: YYYY-MM-DD
                "end_date": "",  # FILL_IN
                "duration_days": 0
            }
        ],
        "lagna_degree": 0.0,  # FILL_IN
        "moon_nakshatra": "",  # FILL_IN
        "moon_nakshatra_pada": 0  # FILL_IN
    }
    
    with open(output_path, 'w') as f:
        json.dump(template, f, indent=2)
    
    print(f"Template created: {output_path}")


def validate_reference(ref: JHoraReference) -> list[str]:
    """Validate a reference file for completeness"""
    issues = []
    
    if not ref.planetary_positions:
        issues.append("No planetary positions found")
    elif len(ref.planetary_positions) < 9:
        issues.append(f"Only {len(ref.planetary_positions)} planets found, expected 9")
    
    for planet in ref.planetary_positions:
        if planet.get('longitude', 0) == 0 and planet.get('planet') != 'Rahu':
            issues.append(f"{planet.get('planet', 'Unknown')}: longitude is 0 (likely unfilled)")
    
    if not ref.vimshottari_dasha:
        issues.append("No dasha periods found")
    
    if ref.ayanamsa_value == 0:
        issues.append("Ayanamsa value is 0 (likely unfilled)")
    
    return issues


def main():
    parser = argparse.ArgumentParser(description="JHora Reference Data Extraction")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Template command
    template_parser = subparsers.add_parser('template', help='Create manual entry template')
    template_parser.add_argument('--birth-data', '-b', required=True, help='Birth data JSON file')
    template_parser.add_argument('--output', '-o', required=True, help='Output template path')
    
    # Parse command (from text)
    parse_parser = subparsers.add_parser('parse', help='Parse JHora text export')
    parse_parser.add_argument('--input', '-i', required=True, help='JHora text export file')
    parse_parser.add_argument('--birth-data', '-b', required=True, help='Birth data JSON file')
    parse_parser.add_argument('--output', '-o', required=True, help='Output reference JSON')
    
    # Parse JHD file
    jhd_parser = subparsers.add_parser('parse-jhd', help='Parse JHora .jhd save file')
    jhd_parser.add_argument('--input', '-i', required=True, help='JHora .jhd file')
    jhd_parser.add_argument('--output', '-o', required=True, help='Output reference JSON')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate reference file')
    validate_parser.add_argument('--input', '-i', required=True, help='Reference JSON file')
    
    # Batch template
    batch_parser = subparsers.add_parser('batch-template', help='Create templates for multiple charts')
    batch_parser.add_argument('--births', '-b', required=True, help='JSON array of birth data')
    batch_parser.add_argument('--output-dir', '-o', required=True, help='Output directory')
    
    args = parser.parse_args()
    
    if args.command == 'template':
        with open(args.birth_data) as f:
            bd_dict = json.load(f)
        birth_data = BirthData.from_dict(bd_dict)
        create_manual_template(birth_data, Path(args.output))
    
    elif args.command == 'parse':
        with open(args.input) as f:
            text = f.read()
        with open(args.birth_data) as f:
            bd_dict = json.load(f)
        
        parser = JHoraTextParser(text)
        ayanamsa_name, ayanamsa_value = parser.parse_ayanamsa()
        
        ref = JHoraReference(
            extraction_date=datetime.now().isoformat(),
            jhora_version="8.0",
            birth_data=bd_dict,
            ayanamsa=ayanamsa_name,
            ayanamsa_value=ayanamsa_value,
            house_system="Whole Sign",
            planetary_positions=[asdict(p) for p in parser.parse_planetary_positions()],
            house_cusps=[],
            vimshottari_dasha=[asdict(d) for d in parser.parse_dasha_periods()],
            lagna_degree=0.0,
            moon_nakshatra="",
            moon_nakshatra_pada=0
        )
        
        with open(args.output, 'w') as f:
            f.write(ref.to_json())
        print(f"Reference saved: {args.output}")
    
    elif args.command == 'parse-jhd':
        parser = JHoraFileParser(Path(args.input))
        ref = parser.parse()
        if ref:
            with open(args.output, 'w') as f:
                f.write(ref.to_json())
            print(f"Reference saved: {args.output}")
        else:
            print("Failed to parse JHD file", file=sys.stderr)
            sys.exit(1)
    
    elif args.command == 'validate':
        with open(args.input) as f:
            data = json.load(f)
        ref = JHoraReference(**data)
        issues = validate_reference(ref)
        if issues:
            print("Validation issues found:")
            for issue in issues:
                print(f"  - {issue}")
            sys.exit(1)
        else:
            print("Reference file is valid")
    
    elif args.command == 'batch-template':
        with open(args.births) as f:
            births = json.load(f)
        
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for i, bd_dict in enumerate(births):
            bd = BirthData.from_dict(bd_dict)
            name_slug = bd.name.lower().replace(' ', '_') if bd.name else f"chart_{i+1}"
            output_path = output_dir / f"jhora_ref_{name_slug}.json"
            create_manual_template(bd, output_path)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
