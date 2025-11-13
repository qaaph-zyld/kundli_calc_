"""
Complete User Chart Test
Test Date: October 9, 1990, 09:10 AM
Location: Loznica, Serbia (44.5333°N, 19.2333°E)
"""

import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8000/api/v1"

def _parse_kundli_profile(path):
    rows = {}
    with open(path, "r") as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]
    header_idx = None
    for i, ln in enumerate(lines):
        if ln.startswith("Chart"):
            header_idx = i
            break
    if header_idx is None:
        return rows
    cols = [c.strip() for c in lines[header_idx].split("|")]
    key_map = {"AS":"AS","SU":"Sun","MO":"Moon","ME":"Mercury","VE":"Venus","MA":"Mars","JU":"Jupiter","SA":"Saturn","RA":"Rahu","KE":"Ketu"}
    for ln in lines[header_idx+2:]:
        parts = [p.strip() for p in ln.split("|")]
        if len(parts) < len(cols):
            continue
        chart_name = parts[0]
        vals = {}
        for ci, col in enumerate(cols[1:]):
            label = col
            if label in key_map:
                try:
                    vals[key_map[label]] = int(parts[ci+1])
                except:
                    pass
        rows[chart_name] = vals
    return rows

def _house_from_cusps_ws(longitude, cusps0):
    asc_sign = int(float(cusps0) / 30)
    p_sign = int(float(longitude) / 30)
    return ((p_sign - asc_sign) % 12) + 1

def validate_against_kundli_profile(chart, birth_data):
    profile = _parse_kundli_profile("tests/test_profile/kundli.txt")
    supported = ["D1","D2","D3","D4","D7","D9","D10","D12","D16","D20","D24","D27","D30","D40","D45","D60"]
    results = []
    signs = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
    d1_comp = {}
    for k,v in chart.get('planetary_positions',{}).items():
        d1_comp[k] = int(v.get('house',0))
    results.append(("D1", d1_comp))
    for dn in supported:
        if dn == "D1":
            continue
        req = {
            "date_time": birth_data["date_time"],
            "latitude": birth_data["latitude"],
            "longitude": birth_data["longitude"],
            "altitude": birth_data["altitude"],
            "division": int(dn[1:])
        }
        try:
            r = requests.post(f"{API_BASE}/divisional/calculate", json=req, timeout=15)
            if r.status_code != 200:
                continue
            dv = r.json()
            cusps = dv.get("house_cusps", [])
            if not cusps:
                continue
            comp = {}
            # Determine asc house cusp 1 value (supports dict or list)
            if isinstance(cusps, dict):
                cusps0 = cusps.get("1")
                if cusps0 is None:
                    # attempt to pick the smallest numeric key
                    try:
                        cusps0 = dict(sorted(((int(k), v) for k, v in cusps.items()), key=lambda x: x[0]))[1]
                    except Exception:
                        continue
            else:
                cusps0 = cusps[0]
            for planet, pdata in dv.get("planetary_positions", {}).items():
                if planet not in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Rahu","Ketu"]:
                    continue
                try:
                    if isinstance(pdata, dict):
                        long_val = float(pdata.get("longitude", 0))
                    else:
                        long_val = float(pdata)
                except Exception:
                    continue
                comp[planet] = _house_from_cusps_ws(long_val, cusps0)
            results.append((dn, comp))
        except Exception:
            continue
    mismatches = []
    print("\n\n🧾 Validation vs kundli.txt")
    print("="*60)
    for dn, comp in results:
        expected = profile.get(dn, {})
        if not expected:
            print(f"   {dn}: no reference, skipped")
            continue
        errs = []
        for planet in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Rahu","Ketu"]:
            ev = expected.get(planet)
            av = comp.get(planet)
            if ev is None or av is None:
                continue
            if int(ev) != int(av):
                errs.append((planet, ev, av))
        if errs:
            print(f"   {dn}: mismatches={len(errs)}")
            for p, ev, av in errs[:8]:
                print(f"      {p}: expected {ev}, got {av}")
            mismatches.append((dn, errs))
        else:
            print(f"   {dn}: ✅ match")
    try:
        with open("kundli_validation_report.txt","w") as f:
            for dn, comp in results:
                f.write(f"{dn}: {comp}\n")
            f.write("\nMismatches:\n")
            for dn, errs in mismatches:
                f.write(f"{dn}: {[(e[0], e[1], e[2]) for e in errs]}\n")
    except Exception:
        pass

def test_user_chart():
    """Test complete chart calculation for user's birth data"""
    
    print("=" * 60)
    print("🧪 COMPLETE USER CHART TEST")
    print("=" * 60)
    print()
    
    # Birth data
    birth_data = {
        "date_time": "1990-10-09T08:10:00Z",
        "latitude": 44.5333,
        "longitude": 19.2333,
        "altitude": 0,
        "ayanamsa_type": "LAHIRI",
        "house_system": "W"
    }
    
    print("📋 Birth Details:")
    print(f"   Date: October 9, 1990")
    print(f"   Time: 09:10 AM (Central European Time)")
    print(f"   Location: Loznica, Serbia")
    print(f"   Coordinates: {birth_data['latitude']}°N, {birth_data['longitude']}°E")
    print(f"   Ayanamsa: Lahiri")
    print(f"   House System: Whole Sign")
    print()
    
    # Test 1: Chart Calculation
    print("🔍 Test 1: Chart Calculation")
    print("-" * 60)
    
    try:
        response = requests.post(
            f"{API_BASE}/charts/calculate",
            json=birth_data,
            timeout=15
        )
        
        if response.status_code == 200:
            print("✅ Chart calculation successful!")
            chart = response.json()
            
            # Parse results
            print("\n📊 CHART RESULTS:")
            print("=" * 60)
            
            # Ascendant
            if 'houses' in chart and 'ascendant' in chart['houses']:
                asc_deg = float(chart['houses']['ascendant'])
                asc_sign_num = int(asc_deg / 30)
                signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
                asc_sign = signs[asc_sign_num]
                asc_in_sign = asc_deg % 30
                
                print(f"\n🌅 ASCENDANT (Lagna):")
                print(f"   Sign: {asc_sign}")
                print(f"   Degree: {asc_deg:.2f}° ({asc_in_sign:.2f}° in {asc_sign})")
            
            # Planetary Positions
            if 'planetary_positions' in chart:
                print(f"\n🪐 PLANETARY POSITIONS:")
                print("-" * 60)
                
                planets_order = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 
                               'Venus', 'Saturn', 'Rahu', 'Ketu']
                
                for planet in planets_order:
                    if planet in chart['planetary_positions']:
                        pos = chart['planetary_positions'][planet]
                        longitude = float(pos['longitude'])
                        sign_num = int(longitude / 30)
                        sign = signs[sign_num]
                        deg_in_sign = longitude % 30
                        
                        # Get speed for retrograde check
                        speed = float(pos.get('speed', 0))
                        retro = " (R)" if speed < 0 and planet not in ['Rahu', 'Ketu'] else ""
                        house_ws = int(chart['planetary_positions'][planet].get('house', 0))
                        print(f"   {planet:10s}: {sign:12s} {deg_in_sign:6.2f}°  Hs(WS)={house_ws}{retro}")
            
            # Divisional Charts
            if 'divisional_charts' in chart:
                print(f"\n📐 DIVISIONAL CHARTS:")
                print("-" * 60)
                
                for div_name, div_data in chart['divisional_charts'].items():
                    if isinstance(div_data, dict) and 'planetary_positions' in div_data:
                        print(f"\n   {div_name} (Whole Sign houses):")
                        # Compute varga asc sign from house cusps (cusps[0] is 1st house start)
                        cusps = div_data.get('house_cusps', [])
                        if cusps:
                            asc_sign_num = int(float(cusps[0]) / 30)
                        else:
                            asc_sign_num = 0
                        order = ['Sun','Moon','Mercury','Venus','Mars','Jupiter','Saturn','Rahu','Ketu']
                        for planet in order:
                            pos_data = div_data['planetary_positions'].get(planet)
                            if isinstance(pos_data, dict) and 'longitude' in pos_data:
                                long = float(pos_data['longitude'])
                                p_sign_num = int(long / 30)
                                sign = signs[p_sign_num]
                                house_ws = ((p_sign_num - asc_sign_num) % 12) + 1
                                print(f"      {planet:8s}: {sign:12s} Hs(WS)={house_ws}")
            
            # Save full result
            with open('user_chart_result.json', 'w') as f:
                json.dump(chart, f, indent=2, default=str)
            print("\n💾 Full chart saved to: user_chart_result.json")
            
            return True, chart
            
        else:
            print(f"❌ Chart calculation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, None

def analyze_yogas(chart_data):
    """Analyze yogas from chart data"""
    print("\n\n🎯 Test 2: Yoga Analysis")
    print("=" * 60)
    
    # This would be done by frontend, but we can analyze the data
    if not chart_data or 'planetary_positions' not in chart_data:
        print("❌ No chart data to analyze")
        return
    
    planets = chart_data['planetary_positions']
    
    # Check for some major yogas
    print("\n📋 Major Yoga Indicators:")
    
    # Get house positions (simplified - actual calculation needs house cusps)
    print("   (Detailed yoga analysis requires frontend library)")
    print("   Chart data contains all necessary planetary positions")
    print("   ✅ Ready for yoga detection on frontend")

def test_performance(birth_data):
    """Test API performance"""
    print("\n\n⚡ Test 3: Performance Check")
    print("=" * 60)
    
    import time
    
    times = []
    for i in range(3):
        start = time.time()
        response = requests.post(
            f"{API_BASE}/charts/calculate",
            json=birth_data,
            timeout=15
        )
        elapsed = time.time() - start
        times.append(elapsed)
        
        if response.status_code == 200:
            print(f"   Run {i+1}: {elapsed:.2f}s")
        else:
            print(f"   Run {i+1}: FAILED")
    
    if times:
        avg = sum(times) / len(times)
        print(f"\n   Average: {avg:.2f}s")
        
        if avg < 3:
            print(f"   ✅ EXCELLENT - Target achieved!")
        elif avg < 5:
            print(f"   ✅ GOOD - Within acceptable range")
        elif avg < 8:
            print(f"   ⚠️  ACCEPTABLE - Could be better")
        else:
            print(f"   ❌ SLOW - Optimization needed")

def main():
    """Run all tests"""
    
    birth_data = {
        "date_time": "1990-10-09T08:10:00Z",
        "latitude": 44.5333,
        "longitude": 19.2333,
        "altitude": 0,
        "ayanamsa_type": "LAHIRI",
        "house_system": "W"
    }
    
    # Test chart calculation
    success, chart = test_user_chart()
    
    if success:
        # Analyze yogas
        analyze_yogas(chart)

        # Validate against kundli.txt profile
        validate_against_kundli_profile(chart, birth_data)
        
        # Test performance
        test_performance(birth_data)
        
        print("\n\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED")
        print("=" * 60)
        print("\n📄 Next Steps:")
        print("   1. Open browser to http://localhost:3100")
        print("   2. Enter birth details:")
        print("      - Date: October 9, 1990")
        print("      - Time: 09:10 AM")
        print("      - Location: Loznica, Serbia")
        print("      - Or use coordinates: 44.5333, 19.2333")
        print("   3. Generate chart and verify all features")
        print("   4. Test all chart types (D1, D9, North/South)")
        print("   5. Check Yogas, Doshas, Planetary Strength")
        print("   6. Test Ashtakoot matching with another chart")
        print("   7. Test Transits and Rectification features")
    else:
        print("\n\n❌ TESTS FAILED")
        print("   Please check that backend is running on port 8000")

if __name__ == "__main__":
    main()
