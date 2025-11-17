# Git Commit Script for Dependency Fixes
# Run from project root: .\commit_fixes.ps1

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Committing Dependency Fixes to GitHub" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in a git repository
if (-Not (Test-Path ".git")) {
    Write-Host "ERROR: Not in a git repository root" -ForegroundColor Red
    Write-Host "Please run this script from the project root directory" -ForegroundColor Yellow
    exit 1
}

# Check git status
Write-Host "Current git status:" -ForegroundColor Green
git status --short

Write-Host ""
Write-Host "Files to be committed:" -ForegroundColor Yellow
Write-Host "- requirements.txt (dependency fixes)" -ForegroundColor White
Write-Host "- SETUP_FIX_2025-11-16.md (setup documentation)" -ForegroundColor White
Write-Host "- QUICK_START.md (quick start guide)" -ForegroundColor White
Write-Host "- setup_and_test.ps1 (automated setup script)" -ForegroundColor White
Write-Host "- CHANGES_2025-11-16.md (changelog)" -ForegroundColor White
Write-Host "- commit_fixes.ps1 (this script)" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Continue with commit? (y/N)"

if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Commit cancelled" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Staging files..." -ForegroundColor Green

# Stage specific files
git add requirements.txt
git add SETUP_FIX_2025-11-16.md
git add QUICK_START.md
git add setup_and_test.ps1
git add CHANGES_2025-11-16.md
git add commit_fixes.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to stage files" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Files staged" -ForegroundColor Green
Write-Host ""

# Commit
Write-Host "Creating commit..." -ForegroundColor Green

$commitMessage = @"
Fix: Resolve dependency issues blocking backend startup

- Add pyyaml to requirements.txt (needed by main.py for OpenAPI)
- Fix Swiss Ephemeris package name: swisseph -> pyswisseph  
- Add comprehensive setup documentation and quick start guide
- Create automated setup/test PowerShell script

These changes enable backend to start without ModuleNotFoundError
and prepare system for divisional chart validation tests.

Closes: Dependency blocking issues
Next: Run validation tests for 09 Oct 1990 Loznica profile
"@

git commit -m $commitMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Commit failed" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Commit created" -ForegroundColor Green
Write-Host ""

# Push
Write-Host "Pushing to origin/main..." -ForegroundColor Green
git push origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "WARNING: Push failed" -ForegroundColor Yellow
    Write-Host "You may need to pull first or resolve conflicts" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Try:" -ForegroundColor Cyan
    Write-Host "  git pull origin main" -ForegroundColor White
    Write-Host "  git push origin main" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "✓ Pushed to GitHub" -ForegroundColor Green
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Success! All changes committed and pushed" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Install dependencies: pip install -r requirements.txt" -ForegroundColor White
Write-Host "2. Start backend: python -m uvicorn backend.app.main:app --reload --port 8000" -ForegroundColor White
Write-Host "3. Run tests: python test_user_complete.py" -ForegroundColor White
Write-Host "4. Review: kundli_validation_report.txt" -ForegroundColor White
Write-Host ""
