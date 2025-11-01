$ErrorActionPreference = 'Stop'
$log = Join-Path $PSScriptRoot 'terminal.md'

function Log-Header {
  param([string]$title)
  Write-Output ("=== {0} {1} ===" -f (Get-Date -Format o), $title) | Tee-Object -FilePath $log -Append
}

function Log-ErrorBody {
  param($err)
  try {
    if ($err.Exception -and $err.Exception.Response) {
      $stream = $err.Exception.Response.GetResponseStream()
      if ($stream) {
        $reader = New-Object System.IO.StreamReader($stream)
        $body = $reader.ReadToEnd()
        $reader.Dispose()
        if ($body) { $body | Tee-Object -FilePath $log -Append }
      }
    }
  } catch {}
}

# Determine API base URL (prefer local dev 8099, fallback to Docker 8000)
$BaseUrl = 'http://127.0.0.1:8099'
try {
  Invoke-RestMethod -Uri "$BaseUrl/api/v1/health" -Method Get | Out-Null
} catch {
  $BaseUrl = 'http://127.0.0.1:8000'
}
Log-Header -title "BaseUrl: $BaseUrl"

try {
  Log-Header -title 'Health'
  Invoke-RestMethod -Uri "$BaseUrl/api/v1/health" -Method Get |
    ConvertTo-Json -Depth 8 | Tee-Object -FilePath $log -Append
}
catch { $_ | Out-String | Tee-Object -FilePath $log -Append; Log-ErrorBody $_ }

# Divisional - D9 Navamsa
try {
  Log-Header -title 'Divisional - D9'
  $d9 = @'
{
  "date_time": "1990-10-09T07:10:00Z",
  "latitude": 44.531346,
  "longitude": 19.206766,
  "altitude": 0,
  "division": 9
}
'@
  Invoke-RestMethod -Uri "$BaseUrl/api/v1/divisional/calculate" -Method Post -ContentType 'application/json' -Body $d9 |
    ConvertTo-Json -Depth 8 | Tee-Object -FilePath $log -Append
}
catch { $_ | Out-String | Tee-Object -FilePath $log -Append; Log-ErrorBody $_ }

try {
  Log-Header -title 'Sun Times'
  $sun = @'
{
  "date": "1990-10-09T00:00:00Z",
  "latitude": 44.531346,
  "longitude": 19.206766
}
'@
  Invoke-RestMethod -Uri "$BaseUrl/api/v1/panchang/sun_times" -Method Post -ContentType 'application/json' -Body $sun |
    ConvertTo-Json -Depth 8 | Tee-Object -FilePath $log -Append
}
catch { $_ | Out-String | Tee-Object -FilePath $log -Append; Log-ErrorBody $_ }

try {
  Log-Header -title 'Ayanamsa'
  $ay = @'
{
  "date": "1990-10-09T07:10:00Z",
  "ayanamsa_type": "lahiri"
}
'@
  Invoke-RestMethod -Uri "$BaseUrl/api/v1/ayanamsa/calculate" -Method Post -ContentType 'application/json' -Body $ay |
    ConvertTo-Json -Depth 8 | Tee-Object -FilePath $log -Append
}
catch { $_ | Out-String | Tee-Object -FilePath $log -Append; Log-ErrorBody $_ }

try {
  Log-Header -title 'Panchang'
  $p = @'
{ "date_time": "1990-10-09T07:10:00Z" }
'@
  Invoke-RestMethod -Uri "$BaseUrl/api/v1/panchang/calculate" -Method Post -ContentType 'application/json' -Body $p |
    ConvertTo-Json -Depth 8 | Tee-Object -FilePath $log -Append
}
catch { $_ | Out-String | Tee-Object -FilePath $log -Append; Log-ErrorBody $_ }

try {
  Log-Header -title 'Charts'
  $json = @'
{
  "date_time": "1990-10-09T07:10:00Z",
  "latitude": 44.531346,
  "longitude": 19.206766,
  "altitude": 0,
  "ayanamsa": 1,
  "house_system": "P"
}
'@
  Invoke-RestMethod -Uri "$BaseUrl/api/v1/charts/calculate" -Method Post -ContentType 'application/json' -Body $json |
    ConvertTo-Json -Depth 12 | Tee-Object -FilePath $log -Append
}
catch { $_ | Out-String | Tee-Object -FilePath $log -Append; Log-ErrorBody $_ }

# Dasha - Vimshottari
try {
  Log-Header -title 'Dasha - Vimshottari'
  $dasha = @'
{
  "birth_date": "1990-10-09T07:10:00Z",
  "moon_longitude": 81.46558689539434
}
'@
  Invoke-RestMethod -Uri "$BaseUrl/api/v1/dasha/vimshottari" -Method Post -ContentType 'application/json' -Body $dasha |
    ConvertTo-Json -Depth 6 | Tee-Object -FilePath $log -Append
}
catch { $_ | Out-String | Tee-Object -FilePath $log -Append; Log-ErrorBody $_ }
