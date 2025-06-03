# AI Prompt Optimization Tool - Environment Setup Script
# PowerShell script for setting up development environment

param(
    [switch]$Frontend,
    [switch]$Backend,
    [switch]$All,
    [switch]$Verbose,
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

# Show usage information
function Show-Usage {
    Write-Host "AI Prompt Optimization Tool - Environment Setup" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor White
    Write-Host "  .\setup-environment.ps1 [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor White
    Write-Host "  -Frontend         Setup frontend environment only" -ForegroundColor Gray
    Write-Host "  -Backend          Setup backend environment only" -ForegroundColor Gray
    Write-Host "  -All              Setup both frontend and backend (default)" -ForegroundColor Gray
    Write-Host "  -Verbose          Enable verbose output" -ForegroundColor Gray
    Write-Host "  -Help             Show this help message" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor White
    Write-Host "  .\setup-environment.ps1 -All         # Setup complete environment" -ForegroundColor Yellow
    Write-Host "  .\setup-environment.ps1 -Frontend    # Setup frontend only" -ForegroundColor Yellow
    Write-Host "  .\setup-environment.ps1 -Backend     # Setup backend only" -ForegroundColor Yellow
}

# Check if running as administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]$currentUser
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Install Node.js using winget
function Install-NodeJS {
    Write-Info "Installing Node.js..."
    
    try {
        # Check if winget is available
        if (Get-Command winget -ErrorAction SilentlyContinue) {
            winget install -e --id OpenJS.NodeJS
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Node.js installed successfully"
                return $true
            }
        }
        
        # Fallback: Manual download instructions
        Write-Info "Please install Node.js manually from https://nodejs.org/"
        Write-Info "Download the LTS version and run the installer"
        return $false
    } catch {
        Write-Error "Failed to install Node.js: $($_.Exception.Message)"
        return $false
    }
}

# Install Python using winget
function Install-Python {
    Write-Info "Installing Python..."
    
    try {
        # Check if winget is available
        if (Get-Command winget -ErrorAction SilentlyContinue) {
            winget install -e --id Python.Python.3.11
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Python installed successfully"
                return $true
            }
        }
        
        # Fallback: Manual download instructions
        Write-Info "Please install Python manually from https://python.org/"
        Write-Info "Download Python 3.11+ and run the installer"
        Write-Info "Make sure to check 'Add Python to PATH' during installation"
        return $false
    } catch {
        Write-Error "Failed to install Python: $($_.Exception.Message)"
        return $false
    }
}

# Setup frontend environment
function Setup-Frontend {
    Write-Header "Setting up Frontend Environment"
    
    # Check Node.js
    try {
        $nodeVersion = node --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Node.js already installed: $nodeVersion"
        } else {
            if (!(Install-NodeJS)) {
                return $false
            }
        }
    } catch {
        if (!(Install-NodeJS)) {
            return $false
        }
    }
    
    # Check npm
    try {
        $npmVersion = npm --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "npm available: $npmVersion"
        } else {
            Write-Error "npm not available after Node.js installation"
            return $false
        }
    } catch {
        Write-Error "npm not available"
        return $false
    }
    
    # Navigate to frontend directory and install dependencies
    if (Test-Path "frontend") {
        Write-Info "Installing frontend dependencies..."
        Push-Location "frontend"
        
        try {
            npm install
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Frontend dependencies installed successfully"
            } else {
                Write-Error "Failed to install frontend dependencies"
                return $false
            }
        } catch {
            Write-Error "Error installing frontend dependencies: $($_.Exception.Message)"
            return $false
        } finally {
            Pop-Location
        }
    } else {
        Write-Error "Frontend directory not found"
        return $false
    }
    
    return $true
}

# Setup backend environment
function Setup-Backend {
    Write-Header "Setting up Backend Environment"
    
    # Check Python
    try {
        $pythonVersion = python --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Python already installed: $pythonVersion"
        } else {
            if (!(Install-Python)) {
                return $false
            }
        }
    } catch {
        if (!(Install-Python)) {
            return $false
        }
    }
    
    # Navigate to backend directory
    if (Test-Path "backend") {
        Push-Location "backend"
        
        try {
            # Create virtual environment
            if (!(Test-Path ".venv")) {
                Write-Info "Creating Python virtual environment..."
                python -m venv .venv
                if ($LASTEXITCODE -ne 0) {
                    Write-Error "Failed to create virtual environment"
                    return $false
                }
                Write-Success "Virtual environment created"
            } else {
                Write-Info "Virtual environment already exists"
            }
            
            # Activate virtual environment
            Write-Info "Activating virtual environment..."
            if (Test-Path ".venv/Scripts/Activate.ps1") {
                & .\.venv\Scripts\Activate.ps1
                Write-Success "Virtual environment activated"
            } else {
                Write-Error "Virtual environment activation script not found"
                return $false
            }
            
            # Upgrade pip
            Write-Info "Upgrading pip..."
            python -m pip install --upgrade pip
            
            # Install dependencies
            if (Test-Path "requirements.txt") {
                Write-Info "Installing backend dependencies..."
                python -m pip install -r requirements.txt
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "Backend dependencies installed successfully"
                } else {
                    Write-Error "Failed to install backend dependencies"
                    return $false
                }
            } else {
                Write-Info "requirements.txt not found, skipping dependency installation"
            }
            
        } catch {
            Write-Error "Error setting up backend environment: $($_.Exception.Message)"
            return $false
        } finally {
            Pop-Location
        }
    } else {
        Write-Error "Backend directory not found"
        return $false
    }
    
    return $true
}

# Main setup function
function Main {
    Write-Header "AI Prompt Optimization Tool - Environment Setup"
    
    # Default to all if no specific option is provided
    if (!$Frontend -and !$Backend -and !$All) {
        $All = $true
    }
    
    $success = $true
    
    # Setup frontend
    if ($Frontend -or $All) {
        if (!(Setup-Frontend)) {
            $success = $false
        }
    }
    
    # Setup backend
    if ($Backend -or $All) {
        if (!(Setup-Backend)) {
            $success = $false
        }
    }
    
    # Summary
    Write-Header "Setup Summary"
    
    if ($success) {
        Write-Success "Environment setup completed successfully!"
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor White
        Write-Host "1. Run: .\start-servers.ps1               # Start both servers" -ForegroundColor Cyan
        Write-Host "2. Run: .\start-servers.ps1 -Frontend false   # Start backend only" -ForegroundColor Cyan
        Write-Host "3. Run: .\start-servers.ps1 -Backend false    # Start frontend only" -ForegroundColor Cyan
        Write-Host "4. Run: .\start-servers.ps1 -Mode prod        # Start in production mode" -ForegroundColor Cyan
    } else {
        Write-Error "Environment setup failed"
        Write-Info "Please check the error messages above and try again"
        return 1
    }
    
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
    exit 1
} 