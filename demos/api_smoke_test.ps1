$ErrorActionPreference = "Stop"

$BaseUrl = if ($env:TITANIC_API_URL) { $env:TITANIC_API_URL } else { "http://127.0.0.1:8000" }

function Invoke-DemoRequest {
  param(
    [string] $Name,
    [string] $Method,
    [string] $Url,
    [string] $Body = $null
  )

  $params = @{
    Method = $Method
    Uri = $Url
    UseBasicParsing = $true
    TimeoutSec = 30
  }

  if ($Body) {
    $params.ContentType = "application/json"
    $params.Body = $Body
  }

  $res = Invoke-WebRequest @params
  [pscustomobject]@{
    Name = $Name
    Status = [int] $res.StatusCode
    Bytes = $res.Content.Length
  }
}

$checks = @()
$checks += Invoke-DemoRequest "health" "GET" "$BaseUrl/health"
$checks += Invoke-DemoRequest "system-health" "GET" "$BaseUrl/system/health"
$checks += Invoke-DemoRequest "incidents" "GET" "$BaseUrl/incidents"
$checks += Invoke-DemoRequest "incident-detail" "GET" "$BaseUrl/incidents/INC-4821"
$checks += Invoke-DemoRequest "timeline" "GET" "$BaseUrl/incidents/INC-4821/timeline"
$checks += Invoke-DemoRequest "services" "GET" "$BaseUrl/services"
$checks += Invoke-DemoRequest "metrics" "GET" "$BaseUrl/metrics"
$checks += Invoke-DemoRequest "topology" "GET" "$BaseUrl/topology"
$checks += Invoke-DemoRequest "blast-radius" "GET" "$BaseUrl/topology/blast-radius/db"
$checks += Invoke-DemoRequest "replay" "GET" "$BaseUrl/replay/INC-4821"
$checks += Invoke-DemoRequest "predictions" "GET" "$BaseUrl/ai/predictions"
$checks += Invoke-DemoRequest "memory-similar" "GET" "$BaseUrl/memory/similar?q=payment%20db%20leak"
$checks += Invoke-DemoRequest "ai-analyze" "POST" "$BaseUrl/ai/analyze" '{"incident_id":"INC-4821"}'
$checks += Invoke-DemoRequest "ai-chat" "POST" "$BaseUrl/ai/chat" '{"incident_id":"INC-4821","message":"Should we rollback payment service?"}'
$checks += Invoke-DemoRequest "ai-postmortem" "POST" "$BaseUrl/ai/postmortem" '{"incident_id":"INC-4821"}'
$checks += Invoke-DemoRequest "recovery-plan" "POST" "$BaseUrl/recovery/plan" '{"incident_id":"INC-4821","action":"restart-payment"}'
$checks += Invoke-DemoRequest "recovery-execute-blocked" "POST" "$BaseUrl/recovery/execute" '{"incident_id":"INC-4821","action":"restart-payment"}'
$checks += Invoke-DemoRequest "auth-login" "POST" "$BaseUrl/auth/login" '{"email":"admin@titanic.local","password":"titanic-demo"}'

$checks | Format-Table -AutoSize

if ($checks.Status -contains 500) {
  throw "One or more TITANIC API checks returned HTTP 500."
}

Write-Host "TITANIC API smoke test completed." -ForegroundColor Green

