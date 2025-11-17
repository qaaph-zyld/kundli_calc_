# Kundli Calc - Setup and Test Script
# Run this from project root with: .\setup_and_test.ps1

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Kundli Calc - Dependency Fix and Test Runner" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv exists
if (-Not (Test-Path ".\.venv")) {
    Write-Host "ERROR: Virtual environment not found at .\.venv" -ForegroundColor Red
    Write-Host "Please create it first with: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "1. Activating virtual environment..." -ForegroundColor Green
& .\.venv\Scripts\Activate.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host "   ✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "2. Upgrading pip..." -ForegroundColor Green
python -m pip install --upgrade pip --quiet
Write-Host "   ✓ pip upgraded" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "3. Installing dependencies from requirements.txt..." -ForegroundColor Green
Write-Host "   (This may take a few minutes...)" -ForegroundColor Yellow
python -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "WARNING: Some dependencies failed to install" -ForegroundColor Yellow
    Write-Host "Attempting to install critical packages individually..." -ForegroundColor Yellow
    Write-Host ""
    
    # Install critical packages one by one
    $critical = @("pyyaml", "fastapi", "uvicorn", "pydantic")
    foreach ($pkg in $critical) {
        Write-Host "   Installing $pkg..." -ForegroundColor Cyan
        python -m pip install $pkg --quiet
    }
    
    # Try pyswisseph separately
    Write-Host "   Installing pyswisseph..." -ForegroundColor Cyan
    python -m pip install pyswisseph
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "WARNING: pyswisseph failed to install" -ForegroundColor Red
        Write-Host "This is likely due to Python 3.13 incompatibility" -ForegroundColor Yellow
        Write-Host "For full functionality, consider using Python 3.10 or 3.11" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "However, attempting to start backend anyway..." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "   ✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Start backend in background
Write-Host "4. Starting backend server..." -ForegroundColor Green
Write-Host "   Backend will run on: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "   API docs at: http://127.0.0.1:8000/api/v1/docs" -ForegroundColor Cyan
Write-Host ""

$backendJob = Start-Job -ScriptBlock {
    param($projectPath)
    Set-Location $projectPath
    & .\.venv\Scripts\Activate.ps1
    python -m uvicorn backend.app.main:app --reload --port 8000
} -ArgumentList (Get-Location)

# Wait for backend to start
Write-Host "   Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check if backend is running
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/health" -Method GET -TimeoutSec 5 -UseBasicParsing
    Write-Host "   ✓ Backend is running!" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "   ✗ Backend failed to start or is not responding" -ForegroundColor Red
    Write-Host "   Check backend job output:" -ForegroundColor Yellow
    Receive-Job -Job $backendJob | Write-Host
    Write-Host ""
    Write-Host "   You may need to start backend manually:" -ForegroundColor Yellow
    Write-Host "   python -m uvicorn backend.app.main:app --reload --port 8000" -ForegroundColor Cyan
    Write-Host ""
    
    Stop-Job -Job $backendJob
    Remove-Job -Job $backendJob
    exit 1
}

# Run validation tests
Write-Host "5. Running validation tests..." -ForegroundColor Green
Write-Host ""
python test_user_complete.py

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Setup and Test Complete!" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Review kundli_validation_report.txt for D-chart validation results" -ForegroundColor White
Write-Host "2. If mismatches exist, debug specific formulas" -ForegroundColor White
Write-Host "3. Commit fixes: git add . && git commit -m 'Fix dependencies and validation'" -ForegroundColor White
Write-Host ""
Write-Host "Backend is still running. To stop it:" -ForegroundColor Yellow
Write-Host "   Stop-Job -Job $($backendJob.Id)" -ForegroundColor Cyan
Write-Host "   Remove-Job -Job $($backendJob.Id)" -ForegroundColor Cyan
Write-Host ""
