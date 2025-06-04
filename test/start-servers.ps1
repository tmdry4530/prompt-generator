# AI Prompt Optimization Tool - Integrated Server Launcher
# PowerShell script for running both frontend and backend servers

param(
    [string]$Mode = "dev",           # dev, prod, build
    [string]$Frontend = "true",      # true, false
    [string]$Backend = "true",       # true, false
    [int]$FrontendPort = 5173,       # Vite default port
    [int]$BackendPort = 5001,        # Flask default port (changed from 5000 to avoid conflicts)
    [switch]$Verbose,
    [switch]$Watch,                  # Watch mode for frontend
    [switch]$Help
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

# Global variables for process management
$Global:FrontendProcess = $null
$Global:BackendProcess = $null
$Global:StartTime = Get-Date

# Set console and environment encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Cleanup function for graceful shutdown
function Cleanup {
    Write-Header "Shutting down servers..."
    
    if ($Global:FrontendProcess -and !$Global:FrontendProcess.HasExited) {
        Write-Info "Stopping frontend server..."
        try {
            $Global:FrontendProcess.Kill()
            $Global:FrontendProcess.WaitForExit(5000)
            Write-Success "Frontend server stopped"
        } catch {
            Write-Error "Failed to stop frontend server: $($_.Exception.Message)"
        }
    }
    
    if ($Global:BackendProcess -and !$Global:BackendProcess.HasExited) {
        Write-Info "Stopping backend server..."
        try {
            $Global:BackendProcess.Kill()
            $Global:BackendProcess.WaitForExit(5000)
            Write-Success "Backend server stopped"
        } catch {
            Write-Error "Failed to stop backend server: $($_.Exception.Message)"
        }
    }
    
    $endTime = Get-Date
    $duration = $endTime - $Global:StartTime
    Write-Info "Total runtime: $($duration.TotalMinutes.ToString("F1")) minutes"
    Write-Success "Cleanup completed"
}

# Register cleanup on script exit
Register-EngineEvent PowerShell.Exiting -Action { Cleanup }

# Trap Ctrl+C
$null = Register-ObjectEvent -InputObject ([Console]) -EventName CancelKeyPress -Action {
    Write-Info "Ctrl+C detected. Initiating shutdown..."
    Cleanup
    [Environment]::Exit(0)
}

# Show usage information
function Show-Usage {
    Write-Host "AI Prompt Optimization Tool - Integrated Server Launcher" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor White
    Write-Host "  .\start-servers.ps1 [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Parameters:" -ForegroundColor White
    Write-Host "  -Mode <dev|prod|build>    Server mode (default: dev)" -ForegroundColor Gray
    Write-Host "  -Frontend <true|false>    Start frontend server (default: true)" -ForegroundColor Gray
    Write-Host "  -Backend <true|false>     Start backend server (default: true)" -ForegroundColor Gray
    Write-Host "  -FrontendPort <port>      Frontend port (default: 5173)" -ForegroundColor Gray
    Write-Host "  -BackendPort <port>       Backend port (default: 5001)" -ForegroundColor Gray
    Write-Host "  -Verbose                  Enable verbose output" -ForegroundColor Gray
    Write-Host "  -Watch                    Enable watch mode for frontend" -ForegroundColor Gray
    Write-Host "  -Help                     Show this help message" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor White
    Write-Host "  .\start-servers.ps1                    # Start both servers in dev mode" -ForegroundColor Yellow
    Write-Host "  .\start-servers.ps1 -Mode prod         # Start in production mode" -ForegroundColor Yellow
    Write-Host "  .\start-servers.ps1 -Backend false     # Start frontend only" -ForegroundColor Yellow
    Write-Host "  .\start-servers.ps1 -Mode build        # Build frontend and start backend" -ForegroundColor Yellow
}

# Check if port is available
function Test-Port {
    param([int]$Port)
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, $Port)
        $listener.Start()
        $listener.Stop()
        return $true
    } catch {
        return $false
    }
}

# Wait for server to be ready
function Wait-ForServer {
    param(
        [string]$Url,
        [int]$TimeoutSeconds = 60,
        [string]$ServerName = "Server"
    )
    
    Write-Info "Waiting for $ServerName to be ready at $Url..."
    $timeout = (Get-Date).AddSeconds($TimeoutSeconds)
    $checkInterval = 2
    
    while ((Get-Date) -lt $timeout) {
        try {
            $uri = [Uri]$Url
            
            # 프론트엔드의 경우 단순히 포트 연결 확인
            if ($ServerName -eq "Frontend") {
                $tcpClient = New-Object System.Net.Sockets.TcpClient
                try {
                    $tcpClient.Connect($uri.Host, $uri.Port)
                    if ($tcpClient.Connected) {
                        Write-Success "$ServerName is ready!"
                        return $true
                    }
                } catch {
                    # 연결 실패는 정상 (아직 준비되지 않음)
                } finally {
                    if ($tcpClient) { $tcpClient.Close() }
                }
            }
            # 백엔드의 경우 HTTP 요청으로 Health Check
            else {
                try {
                    $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
                    if ($response.StatusCode -eq 200) {
                        Write-Success "$ServerName is ready!"
                        return $true
                    }
                } catch {
                    # HTTP 요청 실패는 정상 (아직 준비되지 않음)
                    Write-Debug "Backend health check failed: $($_.Exception.Message)"
                }
            }
        } catch {
            Write-Debug "Server check failed: $($_.Exception.Message)"
        }
        
        Start-Sleep -Seconds $checkInterval
    }
    
    Write-Error "$ServerName failed to start within $TimeoutSeconds seconds"
    return $false
}

# Check environment requirements
function Test-Requirements {
    Write-Header "Checking Environment Requirements"
    
    $allRequirementsMet = $true
    
    # Check Node.js (for frontend)
    if ($Frontend -eq "true") {
        try {
            $nodeVersion = node --version 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Node.js installed: $nodeVersion"
            } else {
                Write-Error "Node.js not installed (required for frontend)"
                $allRequirementsMet = $false
            }
        } catch {
            Write-Error "Node.js not installed (required for frontend)"
            $allRequirementsMet = $false
        }
        
        # Check npm
        try {
            $npmVersion = npm --version 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Success "npm installed: $npmVersion"
            } else {
                Write-Error "npm not installed (required for frontend)"
                $allRequirementsMet = $false
            }
        } catch {
            Write-Error "npm not installed (required for frontend)"
            $allRequirementsMet = $false
        }
    }
    
    # Check Python (for backend)
    if ($Backend -eq "true") {
        try {
            $pythonVersion = python --version 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Python installed: $pythonVersion"
            } else {
                Write-Error "Python not installed (required for backend)"
                $allRequirementsMet = $false
            }
        } catch {
            Write-Error "Python not installed (required for backend)"
            $allRequirementsMet = $false
        }
    }
    
    # Check port availability
    if ($Frontend -eq "true" -and !(Test-Port $FrontendPort)) {
        Write-Error "Frontend port $FrontendPort is already in use"
        $allRequirementsMet = $false
    }
    
    if ($Backend -eq "true" -and !(Test-Port $BackendPort)) {
        Write-Error "Backend port $BackendPort is already in use"
        $allRequirementsMet = $false
    }
    
    return $allRequirementsMet
}

# Start frontend server
function Start-FrontendServer {
    Write-Header "Starting Frontend Server"
    
    if (!(Test-Path "frontend")) {
        Write-Error "Frontend directory not found"
        return $false
    }
    
    Push-Location "frontend"
    
    try {
        # Install dependencies if needed
        if (!(Test-Path "node_modules")) {
            Write-Info "Installing frontend dependencies..."
            npm install
            if ($LASTEXITCODE -ne 0) {
                Write-Error "Failed to install frontend dependencies"
                return $false
            }
        }
        
        # Determine command based on mode
        $command = switch ($Mode) {
            "dev" {
                if ($Watch) { "npm run dev -- -H 0.0.0.0 -p $FrontendPort" }
                else { "npm run dev -- -H 0.0.0.0 -p $FrontendPort" }
            }
            "build" { "npm run build" }
            "prod" {
                # Build first, then serve
                Write-Info "Building frontend for production..."
                npm run build
                if ($LASTEXITCODE -ne 0) {
                    Write-Error "Frontend build failed"
                    return $false
                }
                "npm run start -- -H 0.0.0.0 -p $FrontendPort"
            }
            default { "npm run dev -- -H 0.0.0.0 -p $FrontendPort" }
        }
        
        if ($Mode -eq "build") {
            # Build only mode
            Write-Info "Building frontend..."
            Invoke-Expression $command
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Frontend build completed"
                return $true
            } else {
                Write-Error "Frontend build failed"
                return $false
            }
        } else {
            # Start server
            Write-Info "Starting frontend server with command: $command"
            $Global:FrontendProcess = Start-Process -FilePath "powershell" -ArgumentList "-Command", $command -NoNewWindow -PassThru
            
            if ($Global:FrontendProcess) {
                Write-Success "Frontend server started (PID: $($Global:FrontendProcess.Id))"
                Write-Info "Frontend URL: http://localhost:$FrontendPort"
                return $true
            } else {
                Write-Error "Failed to start frontend server"
                return $false
            }
        }
    } catch {
        Write-Error "Error starting frontend server: $($_.Exception.Message)"
        return $false
    } finally {
        Pop-Location
    }
}

# Start backend server
function Start-BackendServer {
    Write-Header "Starting Backend Server"
    
    if (!(Test-Path "backend")) {
        Write-Error "Backend directory not found"
        return $false
    }
    
    Push-Location "backend"
    
    try {
        # Activate virtual environment if exists
        if (Test-Path ".venv/Scripts/Activate.ps1") {
            Write-Info "Activating Python virtual environment..."
            & .\.venv\Scripts\Activate.ps1
        }
        
        # Install dependencies if needed
        if (Test-Path "requirements.txt") {
            Write-Info "Installing/updating backend dependencies..."
            python -m pip install -r requirements.txt --quiet
        }
        
        # Set environment variables
        $env:FLASK_ENV = if ($Mode -eq "prod") { "production" } else { "development" }
        $env:PORT = $BackendPort
        
        Write-Debug "Environment: FLASK_ENV=$env:FLASK_ENV, PORT=$env:PORT"
        
        # Start backend server
        $command = "python -m src.main"
        Write-Info "Starting backend server with command: $command"
        
        $Global:BackendProcess = Start-Process -FilePath "python" -ArgumentList "-m", "src.main" -NoNewWindow -PassThru
        
        if ($Global:BackendProcess) {
            Write-Success "Backend server started (PID: $($Global:BackendProcess.Id))"
            Write-Info "Backend URL: http://localhost:$BackendPort"
            return $true
        } else {
            Write-Error "Failed to start backend server"
            return $false
        }
    } catch {
        Write-Error "Error starting backend server: $($_.Exception.Message)"
        return $false
    } finally {
        Pop-Location
    }
}

# Monitor servers
function Monitor-Servers {
    Write-Header "Monitoring Servers"
    
    # Wait for servers to be ready
    $serversReady = $true
    
    if ($Frontend -eq "true" -and $Mode -ne "build") {
        if (!(Wait-ForServer "http://localhost:$FrontendPort" 30 "Frontend")) {
            $serversReady = $false
        }
    }
    
    if ($Backend -eq "true") {
        if (!(Wait-ForServer "http://localhost:$BackendPort/api/health" 30 "Backend")) {
            $serversReady = $false
        }
    }
    
    if (!$serversReady) {
        Write-Error "One or more servers failed to start properly"
        return $false
    }
    
    # Display server information
    Write-Success "All servers are running successfully!"
    Write-Host ""
    Write-Host "Server Information:" -ForegroundColor White
    Write-Host "==================" -ForegroundColor White
    
    if ($Frontend -eq "true" -and $Mode -ne "build") {
        Write-Host "Frontend (${Mode}): http://localhost:$FrontendPort" -ForegroundColor Green
    }
    
    if ($Backend -eq "true") {
        Write-Host "Backend (${Mode}):  http://localhost:$BackendPort" -ForegroundColor Green
        Write-Host "API Health:         http://localhost:$BackendPort/api/health" -ForegroundColor Green
        Write-Host "API Models:         http://localhost:$BackendPort/api/models" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "Press Ctrl+C to stop all servers" -ForegroundColor Yellow
    
    # Keep monitoring
    while ($true) {
        Start-Sleep -Seconds 5
        
        # Check if processes are still running
        if ($Global:FrontendProcess -and $Global:FrontendProcess.HasExited) {
            Write-Error "Frontend server has stopped unexpectedly"
            break
        }
        
        if ($Global:BackendProcess -and $Global:BackendProcess.HasExited) {
            Write-Error "Backend server has stopped unexpectedly"
            break
        }
    }
    
    return $true
}

# Main execution function
function Main {
    Write-Header "AI Prompt Optimization Tool - Integrated Server Launcher"
    Write-Info "Mode: $Mode | Frontend: $Frontend | Backend: $Backend"
    Write-Info "Frontend Port: $FrontendPort | Backend Port: $BackendPort"
    Write-Info "Start Time: $(Get-Date)"
    
    # Validate parameters
    if ($Mode -notin @("dev", "prod", "build")) {
        Write-Error "Invalid mode: $Mode. Use 'dev', 'prod', or 'build'"
        return 1
    }
    
    if ($Frontend -notin @("true", "false")) {
        Write-Error "Invalid frontend setting: $Frontend. Use 'true' or 'false'"
        return 1
    }
    
    if ($Backend -notin @("true", "false")) {
        Write-Error "Invalid backend setting: $Backend. Use 'true' or 'false'"
        return 1
    }
    
    if ($Frontend -eq "false" -and $Backend -eq "false") {
        Write-Error "At least one server (frontend or backend) must be enabled"
        return 1
    }
    
    # Check requirements
    if (!(Test-Requirements)) {
        Write-Error "Environment requirements not met"
        return 1
    }
    
    # Start servers
    $success = $true
    
    if ($Backend -eq "true") {
        if (!(Start-BackendServer)) {
            $success = $false
        }
    }
    
    if ($Frontend -eq "true" -and $success) {
        if (!(Start-FrontendServer)) {
            $success = $false
        }
    }
    
    if (!$success) {
        Write-Error "Failed to start one or more servers"
        Cleanup
        return 1
    }
    
    # Monitor servers (unless in build-only mode)
    if ($Mode -ne "build" -or ($Mode -eq "build" -and $Backend -eq "true")) {
        Monitor-Servers
    }
    
    Cleanup
    return 0
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
    Cleanup
    exit 1
} 