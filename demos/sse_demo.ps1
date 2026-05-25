$BaseUrl = if ($env:TITANIC_API_URL) { $env:TITANIC_API_URL } else { "http://127.0.0.1:8000" }

Write-Host "Streaming TITANIC agent reasoning for 4 seconds..." -ForegroundColor Cyan
curl.exe -N --max-time 4 "$BaseUrl/events/incident/INC-4821"
Write-Host "`nSSE sample complete. Curl timeout is expected because event streams stay open." -ForegroundColor Green
