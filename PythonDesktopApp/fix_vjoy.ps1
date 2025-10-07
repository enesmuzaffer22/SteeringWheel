# vJoy Quick Fix Script
# This script attempts to fix common vJoy Device busy issues

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "vJoy Device Quick Fix Tool" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check for joy.cpl processes
Write-Host "Step 1: Checking for Game Controllers panel..." -ForegroundColor Yellow
$joyProcesses = Get-Process -Name "joy" -ErrorAction SilentlyContinue
if ($joyProcesses) {
    Write-Host "   [FOUND] Game Controllers panel is running" -ForegroundColor Red
    Write-Host "   Closing it..." -ForegroundColor Yellow
    Stop-Process -Name "joy" -Force -ErrorAction SilentlyContinue
    Write-Host "   Done!" -ForegroundColor Green
} else {
    Write-Host "   [OK] Not running" -ForegroundColor Green
}
Write-Host ""

# Step 2: Check for vJoyConf processes
Write-Host "Step 2: Checking for Configure vJoy..." -ForegroundColor Yellow
$vjoyConfProcesses = Get-Process -Name "vJoyConf*" -ErrorAction SilentlyContinue
if ($vjoyConfProcesses) {
    Write-Host "   [FOUND] Configure vJoy is running" -ForegroundColor Red
    Write-Host "   Closing it..." -ForegroundColor Yellow
    Stop-Process -Name "vJoyConf*" -Force -ErrorAction SilentlyContinue
    Write-Host "   Done!" -ForegroundColor Green
} else {
    Write-Host "   [OK] Not running" -ForegroundColor Green
}
Write-Host ""

# Step 3: Check for old Python processes
Write-Host "Step 3: Checking for old Python processes..." -ForegroundColor Yellow
$pythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "   [WARNING] Found $($pythonProcesses.Count) Python process(es)" -ForegroundColor Yellow
    Write-Host "   These might be using vJoy. Kill them? (y/n)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq "y") {
        Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue
        Write-Host "   Killed all Python processes" -ForegroundColor Green
    }
} else {
    Write-Host "   [OK] No Python processes running" -ForegroundColor Green
}
Write-Host ""

# Step 4: Wait a bit
Write-Host "Step 4: Waiting for cleanup..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
Write-Host "   Done!" -ForegroundColor Green
Write-Host ""

# Step 5: Test vJoy
Write-Host "Step 5: Testing vJoy Device..." -ForegroundColor Yellow
$testResult = python -c "import pyvjoy; j = pyvjoy.VJoyDevice(1); print('SUCCESS')" 2>&1

if ($testResult -like "*SUCCESS*") {
    Write-Host "   SUCCESS! vJoy Device is now available!" -ForegroundColor Green
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host "vJoy is ready! You can now run:" -ForegroundColor Green
    Write-Host "   python main.py" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Green
} else {
    Write-Host "   FAILED! vJoy Device is still busy" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error details:" -ForegroundColor Yellow
    Write-Host $testResult
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host "SOLUTION: Restart your computer" -ForegroundColor Yellow
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "After restart:" -ForegroundColor Yellow
    Write-Host "1. Open 'Configure vJoy' from Start Menu" -ForegroundColor White
    Write-Host "2. Enable Device 1" -ForegroundColor White
    Write-Host "3. Enable X, Y, Z axes" -ForegroundColor White
    Write-Host "4. Click Apply" -ForegroundColor White
    Write-Host "5. Run: python main.py" -ForegroundColor White
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
