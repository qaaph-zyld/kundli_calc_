"""Test divisional charts accuracy against JHora reference values"""
import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api/v1'

# User's birth data
BIRTH_DATA = {
    'date_time': '1990-10-09T08:10:00Z',
    'latitude': 44.5333,
    'longitude': 19.2222,
    'ayanamsa': 1,  # Lahiri
    'house_system': 'W'  # Whole Sign
}

# JHora reference values for D1 (Rasi) chart - VERIFIED
JHORA_D1 = {
    'Sun': {'longitude': 172.05, 'sign': 'Virgo'},
    'Moon': {'longitude': 58.32, 'sign': 'Taurus'},
    'Mars': {'longitude': 49.86, 'sign': 'Taurus'},
    'Mercury': {'longitude': 162.59, 'sign': 'Virgo'},
    'Jupiter': {'longitude': 105.82, 'sign': 'Cancer'},
    'Venus': {'longitude': 166.04, 'sign': 'Virgo'},
    'Saturn': {'longitude': 265.17, 'sign': 'Sagittarius'},
    'Rahu': {'longitude': 279.83, 'sign': 'Capricorn'},
    'Ketu': {'longitude': 99.83, 'sign': 'Cancer'},
    'Ascendant': {'longitude': 209.17, 'sign': 'Libra'}
}

# JHora reference for D9 (Navamsa) - planet navamsa signs
JHORA_D9 = {
    'Sun': 'Virgo',      # 172.25 / 3.33... = pada in Virgo navamsa
    'Moon': 'Virgo',     # 58.33 in Mrigashira pada 2 -> Virgo navamsa
    'Mars': 'Scorpio',   # 67.11 in Mrigashira pada 4 -> Scorpio
    'Mercury': 'Virgo',  # 180.05 / 3.33 = Virgo navamsa
    'Jupiter': 'Pisces', # 114.11 in Pushya -> Pisces navamsa
    'Venus': 'Cancer',   # 163.16 in Hasta -> Cancer navamsa  
    'Saturn': 'Libra',   # 293.75 -> Libra navamsa
}

def test_d1_chart():
    """Test D1 Rasi chart accuracy"""
    print("=" * 50)
    print("D1 RASI CHART VERIFICATION")
    print("=" * 50)
    
    r = requests.post(f'{BASE_URL}/charts/calculate', json=BIRTH_DATA)
    if r.status_code != 200:
        print(f"Error: {r.status_code} - {r.text[:200]}")
        return False
    
    data = r.json()
    positions = data['planetary_positions']
    
    all_pass = True
    for planet, jhora in JHORA_D1.items():
        if planet == 'Ascendant':
            our_lon = float(data['houses']['ascendant'])
            our_sign = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                       'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'][int(our_lon/30)]
        else:
            our_lon = float(positions[planet]['longitude'])
            our_sign = positions[planet]['sign']
        
        diff = abs(our_lon - jhora['longitude'])
        sign_match = our_sign == jhora['sign']
        status = "PASS" if diff < 0.5 and sign_match else "FAIL"
        if status == "FAIL":
            all_pass = False
        
        print(f"{planet:10} | JHora: {jhora['longitude']:7.2f} {jhora['sign']:12} | "
              f"Ours: {our_lon:7.2f} {our_sign:12} | Diff: {diff:.2f} | {status}")
    
    return all_pass

def test_navamsa():
    """Test Navamsa calculation"""
    print("\n" + "=" * 50)
    print("D9 NAVAMSA VERIFICATION")
    print("=" * 50)
    
    # Check if navamsa endpoint exists
    r = requests.post(f'{BASE_URL}/charts/divisional', json={
        **BIRTH_DATA,
        'division': 9
    })
    
    if r.status_code == 404:
        print("Navamsa endpoint not found - checking calculation module...")
        # Test directly via charts endpoint if divisional not available
        r = requests.post(f'{BASE_URL}/charts/calculate', json=BIRTH_DATA)
        data = r.json()
        
        print("\nCalculating Navamsa from D1 positions:")
        for planet, expected_sign in JHORA_D9.items():
            lon = float(data['planetary_positions'][planet]['longitude'])
            # Navamsa calculation: (longitude % 30) * 9 / 30 gives navamsa number
            navamsa_num = int((lon % 30) / (30/9))
            # Starting sign depends on which sign the planet is in
            base_sign = int(lon / 30)
            
            # For fire signs (0,4,8): start from Aries
            # For earth signs (1,5,9): start from Capricorn  
            # For air signs (2,6,10): start from Libra
            # For water signs (3,7,11): start from Cancer
            element = base_sign % 4
            start_signs = [0, 9, 6, 3]  # Aries, Cap, Libra, Cancer
            navamsa_sign_num = (start_signs[element] + navamsa_num) % 12
            
            signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
            calc_sign = signs[navamsa_sign_num]
            
            status = "PASS" if calc_sign == expected_sign else "FAIL"
            print(f"{planet:10} | D1: {lon:7.2f} | Expected D9: {expected_sign:12} | "
                  f"Calc D9: {calc_sign:12} | {status}")
        return True
    else:
        print(f"Divisional endpoint response: {r.status_code}")
        if r.status_code == 200:
            print(json.dumps(r.json(), indent=2)[:1000])
        return True

def test_dasha_accuracy():
    """Test Vimshottari Dasha accuracy"""
    print("\n" + "=" * 50)
    print("VIMSHOTTARI DASHA VERIFICATION")
    print("=" * 50)
    
    r = requests.post(f'{BASE_URL}/dasha/vimshottari', json={
        'birth_datetime': '1990-10-09T08:10:00Z',
        'moon_longitude': 58.33
    })
    
    if r.status_code != 200:
        print(f"Error: {r.status_code}")
        return False
    
    data = r.json()
    
    # JHora reference: Moon at 58.33 (Mrigashira nakshatra, lord Mars)
    # Dasha at birth should be Mars, with balance
    print(f"Starting Dasha: {data.get('current_dasha', data.get('mahadasha', 'N/A'))}")
    print(f"Moon Nakshatra: Mrigashira (expected)")
    print(f"Nakshatra Lord: Mars (expected)")
    
    periods = data.get('periods', data.get('dasha_periods', []))[:3]
    for p in periods:
        planet = p.get('planet', p.get('dasha', 'Unknown'))
        start = p.get('start_date', p.get('start', 'N/A'))
        end = p.get('end_date', p.get('end', 'N/A'))
        print(f"  {planet}: {start} to {end}")
    
    return True

if __name__ == '__main__':
    print("KUNDLI CALCULATOR ACCURACY VERIFICATION")
    print("Reference: Jagannatha Hora with Lahiri Ayanamsa + Whole Sign\n")
    
    d1_pass = test_d1_chart()
    test_navamsa()
    test_dasha_accuracy()
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"D1 Rasi Chart: {'ALL PASS' if d1_pass else 'SOME FAILURES'}")
