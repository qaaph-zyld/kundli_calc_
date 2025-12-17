"""
Navamsa (D9) Verification for New Chart
"""

# Chart data from JHora (convert to absolute longitude)
rasi = {
    'Sun': 90 + 18 + 25/60,      # Cancer 18°25'
    'Moon': 150 + 14 + 59/60,    # Virgo 14°59'  
    'Mercury': 0 + 23 + 11/60,   # Aries 23°11'
    'Venus': 30 + 24 + 22/60,    # Taurus 24°22'
    'Mars': 60 + 29 + 6/60,      # Gemini 29°06'
    'Jupiter': 210 + 22 + 32/60, # Scorpio 22°32'
    'Saturn': 210 + 16 + 41/60,  # Scorpio 16°41'
    'Rahu': 330 + 28 + 29/60,    # Pisces 28°29'
    'Asc': 60 + 20 + 15/60,      # Gemini 20°15'
}

SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo',
         'Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']

def calc_navamsa(longitude):
    """
    Calculate D9 Navamsa position using traditional method.
    
    Navamsa Rule:
    - Each sign is divided into 9 parts of 3°20' (3.333°) each
    - The starting sign for counting depends on the element:
      * Fire signs (Ari, Leo, Sag): count from Aries
      * Earth signs (Tau, Vir, Cap): count from Capricorn  
      * Air signs (Gem, Lib, Aqu): count from Libra
      * Water signs (Can, Sco, Pis): count from Cancer
    """
    sign_num = int(longitude / 30)
    deg_in_sign = longitude % 30
    navamsa_span = 30 / 9  # 3.333... degrees
    navamsa_num = int(deg_in_sign / navamsa_span)
    
    # Starting navamsa depends on element of rasi sign
    element = sign_num % 4
    if element == 0:    # Fire (Aries=0, Leo=4, Sag=8)
        start = 0       # Start from Aries
    elif element == 1:  # Earth (Taurus=1, Virgo=5, Cap=9)
        start = 9       # Start from Capricorn
    elif element == 2:  # Air (Gemini=2, Libra=6, Aqua=10)
        start = 6       # Start from Libra
    else:               # Water (Cancer=3, Scorpio=7, Pisces=11)
        start = 3       # Start from Cancer
    
    navamsa_sign = (start + navamsa_num) % 12
    return navamsa_sign, SIGNS[navamsa_sign]

print("=" * 65)
print("NAVAMSA (D9) CALCULATION - Manual Verification")
print("=" * 65)
print(f"{'Planet':<10} {'Rasi Position':<22} {'Navamsa Sign':<15}")
print("-" * 65)

for planet, lon in rasi.items():
    rasi_sign = SIGNS[int(lon/30)]
    rasi_deg = lon % 30
    deg = int(rasi_deg)
    mins = int((rasi_deg - deg) * 60)
    nav_num, nav_sign = calc_navamsa(lon)
    print(f"{planet:<10} {rasi_sign:<12} {deg:02d}°{mins:02d}'     ->  {nav_sign}")

print("=" * 65)

# Now let's call our backend API and compare
import requests

# We need birth datetime for this chart - assuming a test date
# Since we don't have the actual birth data, let's just verify the formula
print("\nNAVAMSA INTERPRETATION GUIDE:")
print("-" * 65)
print("""
The Navamsa (D9) chart is the most important divisional chart after Rasi.

KEY PRINCIPLES:
1. Navamsa shows the FRUIT of the Rasi chart
2. A planet strong in Rasi but weak in Navamsa = initial promise, poor results
3. A planet weak in Rasi but strong in Navamsa = delayed but eventual success
4. Vargottama (same sign in D1 & D9) = extremely strong planet

NAVAMSA USES:
- Marriage & spouse characteristics (7th house, Venus, Jupiter)
- Dharma & spiritual path (9th house from Navamsa lagna)
- True strength of planets (pushkara navamsa, vargottama)
- Timing of results (dasha lord's navamsa position)

THIS CHART'S NAVAMSA HIGHLIGHTS:
""")

# Check for Vargottama
for planet, lon in rasi.items():
    rasi_sign_num = int(lon/30)
    nav_num, nav_sign = calc_navamsa(lon)
    if rasi_sign_num == nav_num:
        print(f"  ★ {planet} is VARGOTTAMA ({SIGNS[rasi_sign_num]}) - Very Strong!")

print("\n" + "=" * 65)
