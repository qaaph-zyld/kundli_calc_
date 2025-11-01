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

try {
  Log-Header -title 'Health'
  Invoke-RestMethod -Uri 'http://127.0.0.1:8099/api/v1/health' -Method Get |
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
  Invoke-RestMethod -Uri 'http://127.0.0.1:8099/api/v1/ayanamsa/calculate' -Method Post -ContentType 'application/json' -Body $ay |
    ConvertTo-Json -Depth 8 | Tee-Object -FilePath $log -Append
}
catch { $_ | Out-String | Tee-Object -FilePath $log -Append; Log-ErrorBody $_ }

try {
  Log-Header -title 'Panchang'
  $p = @'
{ "date_time": "1990-10-09T07:10:00Z" }
'@
  Invoke-RestMethod -Uri 'http://127.0.0.1:8099/api/v1/panchang/calculate' -Method Post -ContentType 'application/json' -Body $p |
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
  Invoke-RestMethod -Uri 'http://127.0.0.1:8099/api/v1/charts/calculate' -Method Post -ContentType 'application/json' -Body $json |
    ConvertTo-Json -Depth 12 | Tee-Object -FilePath $log -Append
}
catch { $_ | Out-String | Tee-Object -FilePath $log -Append; Log-ErrorBody $_ }
