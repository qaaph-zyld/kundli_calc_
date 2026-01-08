from backend.app.core.knowledge.sources.bphs_planets_in_houses import BPHS_PLANETS_IN_HOUSES

total = sum(len(h) for h in BPHS_PLANETS_IN_HOUSES.values())
print(f'✓ Total: {total} interpretations')
for p, h in BPHS_PLANETS_IN_HOUSES.items():
    print(f'  {p}: {len(h)}/12 houses')
