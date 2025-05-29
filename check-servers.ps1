# AI Prompt Optimization Tool - Server Status Checker
# PowerShell script for checking server status

param(
    [int]$FrontendPort = 5173,    # Vite default port
    [int]$BackendPort = 5001,     # Flask default port (updated to 5001)
    [switch]$Verbose,
    [switch]$Help,
    [switch]$Detailed             # Show detailed information
)

# Color output functions
function Write-Header {
    param([string]$Message)
    Write-Host "======================================" -ForegroundColor Blue
    Write-Host $Message -ForegroundColor Blue
    Write-Host "======================================" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Yellow
}

function Write-Debug {
    param([string]$Message)
    if ($Verbose) {
        Write-Host "[DEBUG] $Message" -ForegroundColor Cyan
    }
}

# Show usage information
function Show-Usage {
    Write-Host "AI Prompt Optimization Tool - Server Status Checker" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor White
    Write-Host "  .\check-servers.ps1 [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor White
    Write-Host "  -FrontendPort <port>      Frontend port to check (default: 5173)" -ForegroundColor Gray
    Write-Host "  -BackendPort <port>       Backend port to check (default: 5001)" -ForegroundColor Gray
    Write-Host "  -Verbose                  Enable verbose output" -ForegroundColor Gray
    Write-Host "  -Help                     Show this help message" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor White
    Write-Host "  .\check-servers.ps1                    # Check default ports" -ForegroundColor Yellow
    Write-Host "  .\check-servers.ps1 -FrontendPort 3000 # Check custom frontend port" -ForegroundColor Yellow
}

# Check if port is responding
function Test-ServerPort {
    param(
        [string]$Hostname = "localhost",
        [int]$Port,
        [int]$TimeoutMs = 3000
    )
    
    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $asyncResult = $tcpClient.BeginConnect($Hostname, $Port, $null, $null)
        $wait = $asyncResult.AsyncWaitHandle.WaitOne($TimeoutMs, $false)
        
        if ($wait) {
            try {
                $tcpClient.EndConnect($asyncResult)
                $connected = $tcpClient.Connected
                $tcpClient.Close()
                return $connected
            } catch {
                return $false
            }
        } else {
            return $false
        }
    } catch {
        return $false
    }
}

# Check HTTP endpoint
function Test-HttpEndpoint {
    param(
        [string]$Url,
        [int]$TimeoutSec = 5
    )
    
    try {
        $response = Invoke-WebRequest -Uri $Url -TimeoutSec $TimeoutSec -ErrorAction SilentlyContinue
        return @{
            Success = $true
            StatusCode = $response.StatusCode
            ResponseTime = $null
            Error = $null
        }
    } catch {
        return @{
            Success = $false
            StatusCode = $null
            ResponseTime = $null
            Error = $_.Exception.Message
        }
    }
}

# Get process information for a port
function Get-ProcessOnPort {
    param([int]$Port)
    
    try {
        $netstat = netstat -ano | Select-String ":$Port "
        if ($netstat) {
            $line = $netstat[0].ToString().Trim()
            $parts = $line -split '\s+'
            $processId = $parts[-1]
            
            if ($processId -and $processId -ne "0") {
                $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
                if ($process) {
                    return @{
                        PID = $processId
                        ProcessName = $process.ProcessName
                        StartTime = $process.StartTime
                    }
                }
            }
        }
        return $null
    } catch {
        return $null
    }
}

# Check frontend server
function Check-Frontend {
    Write-Header "Checking Frontend Server"
    
    $frontendUrl = "http://localhost:$FrontendPort"
    
    # Check if port is open
    $portOpen = Test-ServerPort -Port $FrontendPort
    Write-Debug "Frontend port $FrontendPort open: $portOpen"
    
    if ($portOpen) {
        Write-Success "Frontend port $FrontendPort is open"
        
        # Get process information
        $processInfo = Get-ProcessOnPort -Port $FrontendPort
        if ($processInfo) {
            Write-Info "Process: $($processInfo.ProcessName) (PID: $($processInfo.PID))"
            if ($processInfo.StartTime) {
                Write-Info "Started: $($processInfo.StartTime)"
            }
        }
        
        # Check HTTP response
        Write-Info "Testing HTTP endpoint: $frontendUrl"
        $httpResult = Test-HttpEndpoint -Url $frontendUrl
        
        if ($httpResult.Success) {
            Write-Success "Frontend server is responding (HTTP $($httpResult.StatusCode))"
        } else {
            Write-Error "Frontend server is not responding: $($httpResult.Error)"
        }
        
        return $httpResult.Success
    } else {
        Write-Error "Frontend server is not running on port $FrontendPort"
        return $false
    }
}

# Check backend server
function Check-Backend {
    Write-Header "Checking Backend Server"
    
    $backendUrl = "http://localhost:$BackendPort"
    $healthUrl = "$backendUrl/api/health"
    
    # Check if port is open
    $portOpen = Test-ServerPort -Port $BackendPort
    Write-Debug "Backend port $BackendPort open: $portOpen"
    
    if ($portOpen) {
        Write-Success "Backend port $BackendPort is open"
        
        # Get process information
        $processInfo = Get-ProcessOnPort -Port $BackendPort
        if ($processInfo) {
            Write-Info "Process: $($processInfo.ProcessName) (PID: $($processInfo.PID))"
            if ($processInfo.StartTime) {
                Write-Info "Started: $($processInfo.StartTime)"
            }
        }
        
        # Check health endpoint
        Write-Info "Testing health endpoint: $healthUrl"
        $healthResult = Test-HttpEndpoint -Url $healthUrl
        
        if ($healthResult.Success) {
            Write-Success "Backend server is healthy (HTTP $($healthResult.StatusCode))"
            
            # Try to get detailed health info
            try {
                $healthResponse = Invoke-RestMethod -Uri $healthUrl -TimeoutSec 3
                if ($healthResponse.status) {
                    Write-Info "Health status: $($healthResponse.status)"
                }
                if ($healthResponse.version) {
                    Write-Info "API version: $($healthResponse.version)"
                }
            } catch {
                Write-Debug "Could not parse health response"
            }
        } else {
            Write-Error "Backend health check failed: $($healthResult.Error)"
        }
        
        # Check main endpoint
        Write-Info "Testing main endpoint: $backendUrl"
        $mainResult = Test-HttpEndpoint -Url $backendUrl
        
        if ($mainResult.Success) {
            Write-Success "Backend main endpoint is responding (HTTP $($mainResult.StatusCode))"
        } else {
            Write-Info "Backend main endpoint check: $($mainResult.Error)"
        }
        
        return $healthResult.Success
    } else {
        Write-Error "Backend server is not running on port $BackendPort"
        return $false
    }
}

# Get system information
function Get-SystemInfo {
    Write-Header "System Information"
    
    # CPU and Memory
    $cpu = Get-WmiObject -Class Win32_Processor | Select-Object -First 1
    $memory = Get-WmiObject -Class Win32_ComputerSystem
    $os = Get-WmiObject -Class Win32_OperatingSystem
    
    Write-Info "OS: $($os.Caption) $($os.Version)"
    Write-Info "CPU: $($cpu.Name)"
    Write-Info "Total RAM: $([math]::Round($memory.TotalPhysicalMemory / 1GB, 2)) GB"
    Write-Info "Available RAM: $([math]::Round($os.FreePhysicalMemory / 1MB, 2)) MB"
    
    # PowerShell version
    Write-Info "PowerShell: $($PSVersionTable.PSVersion)"
    
    # Check Node.js
    try {
        $nodeVersion = node --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Info "Node.js: $nodeVersion"
        }
    } catch {
        Write-Info "Node.js: Not installed"
    }
    
    # Check Python
    try {
        $pythonVersion = python --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Info "Python: $pythonVersion"
        }
    } catch {
        Write-Info "Python: Not installed"
    }
}

# Main function
function Main {
    Write-Header "AI Prompt Optimization Tool - Server Status Check"
    Write-Info "Check time: $(Get-Date)"
    
    if ($Verbose) {
        Get-SystemInfo
    }
    
    $frontendStatus = Check-Frontend
    $backendStatus = Check-Backend
    
    # Summary
    Write-Header "Status Summary"
    
    Write-Host "Frontend Server: " -NoNewline
    if ($frontendStatus) {
        Write-Host "✅ RUNNING" -ForegroundColor Green
        Write-Host "  URL: http://localhost:$FrontendPort" -ForegroundColor Cyan
    } else {
        Write-Host "❌ NOT RUNNING" -ForegroundColor Red
    }
    
    Write-Host "Backend Server:  " -NoNewline
    if ($backendStatus) {
        Write-Host "✅ RUNNING" -ForegroundColor Green
        Write-Host "  URL: http://localhost:$BackendPort" -ForegroundColor Cyan
        Write-Host "  Health: http://localhost:$BackendPort/api/health" -ForegroundColor Cyan
    } else {
        Write-Host "❌ NOT RUNNING" -ForegroundColor Red
    }
    
    if (!$frontendStatus -and !$backendStatus) {
        Write-Host ""
        Write-Info "No servers are running. To start servers:"
        Write-Host "  .\start-servers.ps1" -ForegroundColor Yellow
    }
    
    if ($frontendStatus -or $backendStatus) {
        return 0
    } else {
        return 1
    }
}

# Show help if requested
if ($Help) {
    Show-Usage
    exit 0
}

# Execute main function
try {
    $exitCode = Main
    exit $exitCode
} catch {
    Write-Error "Unexpected error: $($_.Exception.Message)"
    exit 1
} 