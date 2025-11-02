$sun = @'
{
  "date": "1990-10-09T00:00:00Z",
  "latitude": 44.531346,
  "longitude": 19.206766
}
'@

Write-Host "Testing Sun Times endpoint..."
Invoke-RestMethod -Uri "http://127.0.0.1:8099/api/v1/panchang/sun_times" -Method Post -ContentType 'application/json' -Body $sun | ConvertTo-Json -Depth 8
