"""Check timezone conversion for October 9, 1990"""
from datetime import datetime
try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

# October 9, 1990 - DST ended Sept 30 in Yugoslavia
# So October 9 should be CET (UTC+1), not CEST (UTC+2)

local_time = datetime(1990, 10, 9, 9, 10)  # 09:10 AM local
tz = ZoneInfo('Europe/Belgrade')
local_aware = local_time.replace(tzinfo=tz)
utc_time = local_aware.astimezone(ZoneInfo('UTC'))

print("TIMEZONE ANALYSIS")
print("=" * 50)
print(f"Local Time: {local_time.strftime('%Y-%m-%d %H:%M')} (Loznica, Serbia)")
print(f"Belgrade TZ: {tz}")
print(f"UTC Time:   {utc_time.strftime('%Y-%m-%d %H:%M')}")
print(f"UTC Offset: {local_aware.strftime('%z')}")

# The correct UTC time for October 9, 1990 09:10 AM local
# Should be 08:10 UTC (CET = UTC+1), NOT 07:10 UTC (CEST = UTC+2)
print("\nCONCLUSION:")
print("  DST ended Sept 30, 1990 in Serbia")
print("  October 9 was on CET (UTC+1)")
print("  09:10 AM local = 08:10 UTC")
