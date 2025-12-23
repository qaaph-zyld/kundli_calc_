# Swiss Ephemeris Data Directory

This directory contains the Swiss Ephemeris data files required for astronomical calculations.

## Required Files

The application requires the following ephemeris files:

### Essential Files (Planets)
- `sepl_18.se1` - Main planetary ephemeris (1800-2400)
- `semo_18.se1` - Moon ephemeris (1800-2400)

### Optional Files (Extended Range)
- `sepl_*.se1` - Extended planetary data for other centuries
- `semo_*.se1` - Extended moon data

### Asteroid/Special Files (Optional)
- `seas_18.se1` - Asteroid ephemeris
- `sefstars.txt` - Fixed stars catalog

## Download Instructions

### Option 1: Direct Download
Download from the official Swiss Ephemeris website:
https://www.astro.com/ftp/swisseph/ephe/

Required files:
```bash
wget https://www.astro.com/ftp/swisseph/ephe/sepl_18.se1
wget https://www.astro.com/ftp/swisseph/ephe/semo_18.se1
```

### Option 2: Via pyswisseph Package
The pyswisseph package includes basic ephemeris data. If EPHE_PATH is not set or empty, Swiss Ephemeris will use the bundled data.

### Option 3: Docker Build
For production deployment, add ephemeris files during Docker image build:

```dockerfile
# In Dockerfile
RUN mkdir -p /app/ephemeris
COPY ephemeris/*.se1 /app/ephemeris/
```

## Configuration

Set the ephemeris path via environment variable:

```bash
export EPHE_PATH=/path/to/ephemeris
```

Or in `.env`:
```
EPHE_PATH=/app/ephemeris
```

## Verification

Test that ephemeris is correctly configured:

```python
import swisseph as swe
from app.core.config import settings

swe.set_ephe_path(settings.EPHE_PATH)
jd = swe.julday(2000, 1, 1, 12.0)
result = swe.calc_ut(jd, swe.SUN)
print(f"Sun position on J2000: {result[0][0]:.4f}°")
```

Expected output: Sun position ≈ 280.46°

## License

Swiss Ephemeris is dual-licensed:
- **GPL v2+**: Free for open-source projects
- **Swiss Ephemeris Professional**: Commercial license available

This project uses Swiss Ephemeris under GPL v2+.

For more information: https://www.astro.com/swisseph/
