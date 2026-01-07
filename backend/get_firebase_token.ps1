# Get Firebase Authentication Token for API Testing
$FIREBASE_API_KEY = "AIzaSyBx0wXKdaX9HRUSTIS8tIQnfaR97IwrKi8"

Write-Host "Creating Firebase test user..." -ForegroundColor Cyan

$randomId = -join ((65..90) + (97..122) | Get-Random -Count 8 | ForEach-Object {[char]$_})
$testEmail = "test_${randomId}@example.com"
$testPassword = "TestPass123!"

Write-Host "Email: $testEmail" -ForegroundColor Yellow

$signUpBody = @{
    email = $testEmail
    password = $testPassword
    returnSecureToken = $true
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=$FIREBASE_API_KEY" -Method Post -Body $signUpBody -ContentType "application/json"
    
    Write-Host ""
    Write-Host "User created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your Firebase ID Token:" -ForegroundColor Cyan
    Write-Host $response.idToken -ForegroundColor White
    Write-Host ""
    Write-Host "Token saved to firebase_token.txt" -ForegroundColor Green
    
    $response.idToken | Out-File -FilePath "firebase_token.txt" -NoNewline -Encoding UTF8
    
    Write-Host ""
    Write-Host "Test the API with:" -ForegroundColor Cyan
    Write-Host '  $token = Get-Content firebase_token.txt' -ForegroundColor White
    Write-Host '  curl -H "Authorization: Bearer $token" http://localhost:8080/api/projects' -ForegroundColor White
    Write-Host ""
    Write-Host "User ID: $($response.localId)"
    
} catch {
    Write-Host ""
    Write-Host "Error creating user:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}
