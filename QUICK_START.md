# Quick Start Guide - Kundli Calc

## Prerequisites
- Python 3.10 or 3.11 (Python 3.13 has limited package compatibility)
- Git

## Step 1: Activate Virtual Environment

```powershell
.\.venv\Scripts\activate
```

You should see `(.venv)` in your prompt.

## Step 2: Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**If pyswisseph fails:** This is expected on Python 3.13. The backend will still start but calculations may be limited. For full functionality, use Python 3.10/3.11.

## Step 3: Start Backend (Terminal 1)

```powershell
python -m uvicorn backend.app.main:app --reload --port 8000
```

**Success indicators:**
- No `ModuleNotFoundError`
- Message: `Uvicorn running on http://127.0.0.1:8000`
- Can open: http://127.0.0.1:8000/api/v1/docs

**Leave this terminal running.**

## Step 4: Run Tests (Terminal 2)

In a new terminal, activate venv again and run:

```powershell
.\.venv\Scripts\activate
python test_user_complete.py
```

## Step 5: Review Results

Check the file: `kundli_validation_report.txt`

Look for lines like:
- `D1: ✅ match` (good)
- `D9: mismatches=2` (needs investigation)

## Step 6: Commit Changes

```powershell
git add .
git commit -m "Fix: Add pyyaml and update swisseph package name"
git push origin main
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'yaml'`
**Fix:** Make sure you ran `pip install -r requirements.txt` after updating requirements.txt

### Issue: `pyswisseph` won't install
**Fix:** 
1. Try: `python -m pip install pyswisseph`
2. If still fails, use Python 3.10 or 3.11
3. Create new venv: 
   ```powershell
   python -m venv .venv_py311
   .\.venv_py311\Scripts\activate
   pip install -r requirements.txt
   ```

### Issue: Backend starts but test fails
**Check:**
1. Is backend running on port 8000? (Check terminal 1)
2. Can you access http://127.0.0.1:8000/api/v1/health in browser?
3. Are you in the correct directory when running test?

## Files Updated This Session

1. `requirements.txt` - Added `pyyaml`, fixed package name to `pyswisseph`
2. `SETUP_FIX_2025-11-16.md` - Detailed fix documentation
3. `QUICK_START.md` - This file
4. `setup_and_test.ps1` - Automated setup script (optional)

## What's Next?

See `NEXT_STEPS_PLAN_2025-11-15.md` for the full development roadmap.

## Support

- View roadmap: `ROADMAP_OVERVIEW_2025-11-15.svg`
- API docs: http://127.0.0.1:8000/api/v1/docs (when backend is running)
- Test profile reference: `tests/test_profile/kundli.txt`
