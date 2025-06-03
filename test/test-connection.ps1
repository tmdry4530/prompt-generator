# Connection Test Script for Prompt Generator
# Tests HTTP/HTTPS connections to identify potential issues

param(
    [switch]$Verbose = $false
)

function Write-TestResult {
    param(
        [string]$TestName,
        [bool]$Success,
        [string]$Message = ""
    )
    
    $status = if ($Success) { "✅ PASS" } else { "❌ FAIL" }
    $color = if ($Success) { "Green" } else { "Red" }
    
    Write-Host "$status $TestName" -ForegroundColor $color
    if ($Message) {
        Write-Host "    $Message" -ForegroundColor Gray
    }
}

function Test-BackendHealth {
    Write-Host "`n🔍 Testing Backend Health..." -ForegroundColor Yellow
    
    try {
        # Test HTTP connection to backend health endpoint
        $response = Invoke-RestMethod -Uri "http://localhost:5001/api/health" -Method Get -TimeoutSec 5
        Write-TestResult "Backend Health Check (HTTP)" $true "Status: OK, Version: $($response.version)"
        return $true
    } catch {
        Write-TestResult "Backend Health Check (HTTP)" $false "Error: $($_.Exception.Message)"
        return $false
    }
}

function Test-BackendModels {
    Write-Host "`n🔍 Testing Backend Models API..." -ForegroundColor Yellow
    
    try {
        # Test models endpoint
        $response = Invoke-RestMethod -Uri "http://localhost:5001/api/models" -Method Get -TimeoutSec 5
        $modelCount = if ($response.models) { $response.models.Count } else { 0 }
        Write-TestResult "Backend Models API" $true "Found $modelCount models"
        return $true
    } catch {
        Write-TestResult "Backend Models API" $false "Error: $($_.Exception.Message)"
        return $false
    }
}

function Test-HTTPSConnection {
    Write-Host "`n🔍 Testing HTTPS Connection (should fail)..." -ForegroundColor Yellow
    
    try {
        # This should fail since we're running HTTP server
        $response = Invoke-WebRequest -Uri "https://localhost:5001/api/health" -UseBasicParsing -SkipCertificateCheck -TimeoutSec 3
        Write-TestResult "HTTPS Connection Test" $false "⚠️  HTTPS connection succeeded - this might cause issues!"
        return $false
    } catch {
        Write-TestResult "HTTPS Connection Test" $true "HTTPS correctly rejected (expected)"
        return $true
    }
}

function Test-FrontendServer {
    Write-Host "`n🔍 Testing Frontend Server..." -ForegroundColor Yellow
    
    try {
        # Test if frontend port is accessible
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $tcpClient.Connect("localhost", 5173)
        
        if ($tcpClient.Connected) {
            $tcpClient.Close()
            Write-TestResult "Frontend Port 5173" $true "Port is accessible"
            
            # Try to get the frontend page
            try {
                $response = Invoke-WebRequest -Uri "http://localhost:5173" -UseBasicParsing -TimeoutSec 3
                Write-TestResult "Frontend HTTP Response" $true "Status: $($response.StatusCode)"
                return $true
            } catch {
                Write-TestResult "Frontend HTTP Response" $false "Error: $($_.Exception.Message)"
                return $false
            }
        } else {
            Write-TestResult "Frontend Port 5173" $false "Port not accessible"
            return $false
        }
    } catch {
        Write-TestResult "Frontend Port 5173" $false "Error: $($_.Exception.Message)"
        return $false
    }
}

function Test-CrossOriginRequest {
    Write-Host "`n🔍 Testing CORS Configuration..." -ForegroundColor Yellow
    
    try {
        # Simulate a CORS preflight request
        $headers = @{
            'Origin' = 'http://localhost:5173'
            'Access-Control-Request-Method' = 'GET'
            'Access-Control-Request-Headers' = 'Content-Type'
        }
        
        $response = Invoke-WebRequest -Uri "http://localhost:5001/api/health" -Method OPTIONS -Headers $headers -UseBasicParsing -TimeoutSec 3
        Write-TestResult "CORS Preflight Request" $true "Status: $($response.StatusCode)"
        
        # Check CORS headers
        $corsHeader = $response.Headers['Access-Control-Allow-Origin']
        if ($corsHeader) {
            Write-TestResult "CORS Headers Present" $true "Allow-Origin: $corsHeader"
        } else {
            Write-TestResult "CORS Headers Present" $false "No CORS headers found"
        }
        
        return $true
    } catch {
        Write-TestResult "CORS Configuration Test" $false "Error: $($_.Exception.Message)"
        return $false
    }
}

function Search-HTTPSReferences {
    Write-Host "`n🔍 Searching for HTTPS references in codebase..." -ForegroundColor Yellow
    
    try {
        $httpsRefs = Get-ChildItem -Recurse -Include *.ts,*.tsx,*.js,*.jsx,*.json | 
                     Select-String "https://localhost" | 
                     Select-Object -First 10
        
        if ($httpsRefs) {
            Write-TestResult "HTTPS References Found" $false "Found potential HTTPS references:"
            foreach ($ref in $httpsRefs) {
                Write-Host "    $($ref.Filename):$($ref.LineNumber) - $($ref.Line.Trim())" -ForegroundColor Red
            }
            return $false
        } else {
            Write-TestResult "HTTPS References Check" $true "No HTTPS localhost references found"
            return $true
        }
    } catch {
        Write-TestResult "HTTPS References Check" $false "Error: $($_.Exception.Message)"
        return $false
    }
}

function Test-ProcessStatus {
    Write-Host "`n🔍 Checking Process Status..." -ForegroundColor Yellow
    
    # Check if ports are in use
    $ports = netstat -ano | Select-String "5001|5173"
    
    if ($ports) {
        Write-TestResult "Port Status Check" $true "Ports 5001/5173 are active"
        if ($Verbose) {
            Write-Host "    Active ports:" -ForegroundColor Gray
            $ports | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
        }
    } else {
        Write-TestResult "Port Status Check" $false "Ports 5001/5173 not found"
    }
}

# Main execution
Write-Host "🧪 Prompt Generator Connection Test" -ForegroundColor Blue -BackgroundColor White
Write-Host "====================================" -ForegroundColor Blue

$allTestsPassed = $true

# Run all tests
$allTestsPassed = (Test-ProcessStatus) -and $allTestsPassed
$allTestsPassed = (Test-BackendHealth) -and $allTestsPassed
$allTestsPassed = (Test-BackendModels) -and $allTestsPassed
$allTestsPassed = (Test-HTTPSConnection) -and $allTestsPassed
$allTestsPassed = (Test-FrontendServer) -and $allTestsPassed
$allTestsPassed = (Test-CrossOriginRequest) -and $allTestsPassed
$allTestsPassed = (Search-HTTPSReferences) -and $allTestsPassed

# Summary
Write-Host "`n📊 Test Summary" -ForegroundColor Blue
Write-Host "===============" -ForegroundColor Blue

if ($allTestsPassed) {
    Write-Host "🎉 All tests passed! The connection setup looks good." -ForegroundColor Green
} else {
    Write-Host "⚠️  Some tests failed. Please review the issues above." -ForegroundColor Red
    Write-Host "`n💡 Common solutions:" -ForegroundColor Yellow
    Write-Host "   1. Make sure both servers are running" -ForegroundColor White
    Write-Host "   2. Check for any HTTPS references in your code" -ForegroundColor White
    Write-Host "   3. Verify API base URL is set to http://localhost:5001" -ForegroundColor White
    Write-Host "   4. Clear browser cache and disable service workers" -ForegroundColor White
}

Write-Host "`n🚀 To start servers: .\start-servers.ps1" -ForegroundColor Cyan
Write-Host "🔍 To verify servers: .\verify-servers.ps1" -ForegroundColor Cyan 