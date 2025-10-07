# Game Controller Test Guide for vJoy
# Instructions for testing vJoy in different scenarios

Write-Host "=" -ForegroundColor Cyan
Write-Host "🎮 vJoy Game Controller Test Guide" -ForegroundColor Cyan  
Write-Host "=" -ForegroundColor Cyan
Write-Host ""

Write-Host "STEP 1: Open Game Controllers Panel" -ForegroundColor Yellow
Write-Host "---------------------------------------" -ForegroundColor Gray
Write-Host "1. Press Windows + R"
Write-Host "2. Type: joy.cpl"
Write-Host "3. Press Enter"
Write-Host ""
Write-Host "You should see 'vJoy Device' in the list"
Write-Host ""
Read-Host "Press Enter when you have joy.cpl open"

Write-Host ""
Write-Host "STEP 2: Open vJoy Properties" -ForegroundColor Yellow
Write-Host "---------------------------------------" -ForegroundColor Gray
Write-Host "1. Select 'vJoy Device'"
Write-Host "2. Click 'Properties' button"
Write-Host "3. Keep this window open"
Write-Host ""
Read-Host "Press Enter when Properties window is open"

Write-Host ""
Write-Host "STEP 3: Testing vJoy Axes" -ForegroundColor Yellow
Write-Host "---------------------------------------" -ForegroundColor Gray
Write-Host "Starting automated axis test..."
Write-Host "Watch the Properties window for movement!"
Write-Host ""

# Run test
python c:\Users\Muzaffer\Documents\GitHub\SteeringWheel\PythonDesktopApp\test_axes.py

Write-Host ""
Write-Host "=" -ForegroundColor Green
Write-Host ""

$response = Read-Host "Did you see the axes moving in joy.cpl? (y/n)"

if ($response -eq "y") {
    Write-Host ""
    Write-Host "✅ GREAT! vJoy is working correctly!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎮 For games to detect vJoy:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "COMMON ISSUE: Some games need specific settings" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "SOLUTIONS:" -ForegroundColor White
    Write-Host ""
    Write-Host "1. RESTART THE GAME after vJoy is configured" -ForegroundColor Yellow
    Write-Host "   Many games only detect controllers at startup"
    Write-Host ""
    Write-Host "2. Check Game Settings → Input/Controls:" -ForegroundColor Yellow
    Write-Host "   • Look for 'Steering Wheel' mode"
    Write-Host "   • Or 'Custom Controller' mode"
    Write-Host "   • Avoid 'Keyboard' or 'Gamepad' modes"
    Write-Host ""
    Write-Host "3. Manual Binding:" -ForegroundColor Yellow
    Write-Host "   • In game controls menu"
    Write-Host "   • Click on 'Steering' → Move phone left/right"
    Write-Host "   • Click on 'Throttle' → Press GAS button"
    Write-Host "   • Click on 'Brake' → Press BRAKE button"
    Write-Host ""
    Write-Host "4. Some games need HidGuardian disabled:" -ForegroundColor Yellow
    Write-Host "   (If vJoy shows in joy.cpl but not in game)"
    Write-Host "   This is rare but possible"
    Write-Host ""
    Write-Host "5. Test in a different game first:" -ForegroundColor Yellow
    Write-Host "   Recommended test games:"
    Write-Host "   • BeamNG.drive (excellent controller support)"
    Write-Host "   • Assetto Corsa (detects all wheels)"
    Write-Host "   • City Car Driving"
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Axes didn't move in joy.cpl" -ForegroundColor Red
    Write-Host ""
    Write-Host "TROUBLESHOOTING:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Make sure joy.cpl Properties window was open during test"
    Write-Host "2. Try closing joy.cpl and opening again"
    Write-Host "3. Restart your computer"
    Write-Host "4. Reinstall vJoy driver"
    Write-Host ""
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
