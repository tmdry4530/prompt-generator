# Simple server verification script

# Set console encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

Write-Host "🚀 AI Prompt Optimization Tool - Server Verification" -ForegroundColor Blue
Write-Host "=" * 60 -ForegroundColor Blue

# Check processes
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
$nodeProcesses = Get-Process node -ErrorAction SilentlyContinue

Write-Host "`n📊 Process Status:" -ForegroundColor Yellow
if ($pythonProcesses) {
    Write-Host "✅ Python processes: $($pythonProcesses.Count)" -ForegroundColor Green
    $pythonProcesses | ForEach-Object { Write-Host "   - PID $($_.Id) started at $($_.StartTime)" -ForegroundColor Gray }
} else {
    Write-Host "❌ No Python processes found" -ForegroundColor Red
}

if ($nodeProcesses) {
    Write-Host "✅ Node.js processes: $($nodeProcesses.Count)" -ForegroundColor Green
    $nodeProcesses | ForEach-Object { Write-Host "   - PID $($_.Id) started at $($_.StartTime)" -ForegroundColor Gray }
} else {
    Write-Host "❌ No Node.js processes found" -ForegroundColor Red
}

# Check ports
Write-Host "`n🌐 Port Status:" -ForegroundColor Yellow
$ports = netstat -ano | Select-String "5001|5173"
if ($ports) {
    Write-Host "✅ Ports 5001/5173 are active:" -ForegroundColor Green
    $ports | ForEach-Object { Write-Host "   $($_.Line.Trim())" -ForegroundColor Gray }
} else {
    Write-Host "❌ Ports 5001/5173 not found" -ForegroundColor Red
}

# Try simple connection test before opening browsers
function Test-HttpConnection {
    param([string]$Url)
    
    try {
        $uri = [Uri]$Url
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $asyncResult = $tcpClient.BeginConnect($uri.Host, $uri.Port, $null, $null)
        $wait = $asyncResult.AsyncWaitHandle.WaitOne(3000, $false)
        
        if ($wait) {
            try {
                $tcpClient.EndConnect($asyncResult)
                if ($tcpClient.Connected) {
                    $tcpClient.Close()
                    return $true
                }
            } catch {}
        }
        $tcpClient.Close()
    } catch {}
    
    return $false
}

# Open browsers
Write-Host "`n🌍 Opening servers in browser..." -ForegroundColor Yellow

$frontendUrl = "http://localhost:5173"
$backendHealthUrl = "http://localhost:5001/api/health"
$backendModelsUrl = "http://localhost:5001/api/models"

Write-Host "✅ Frontend: $frontendUrl" -ForegroundColor Cyan
Write-Host "✅ Backend Health: $backendHealthUrl" -ForegroundColor Cyan
Write-Host "✅ Backend Models: $backendModelsUrl" -ForegroundColor Cyan

if (Test-HttpConnection $frontendUrl) { 
    Start-Process $frontendUrl
    Write-Host "   - Frontend connection successful" -ForegroundColor Green
} else {
    Write-Host "   - Frontend connection failed!" -ForegroundColor Red
}

Start-Sleep -Seconds 1

if (Test-HttpConnection $backendHealthUrl) { 
    Start-Process $backendHealthUrl
    Write-Host "   - Backend health connection successful" -ForegroundColor Green
} else {
    Write-Host "   - Backend health connection failed!" -ForegroundColor Red
}

Start-Sleep -Seconds 1

if (Test-HttpConnection $backendModelsUrl) { 
    Start-Process $backendModelsUrl
    Write-Host "   - Backend models connection successful" -ForegroundColor Green
} else {
    Write-Host "   - Backend models connection failed!" -ForegroundColor Red
}

Write-Host "`n🎉 Server verification completed!" -ForegroundColor Green
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 