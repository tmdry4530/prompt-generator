# AI Prompt Optimization Tool - Server Termination Script
# 모든 개발 서버를 안전하게 종료하는 PowerShell 스크립트

# 콘솔 인코딩 설정
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 색상 출력 함수
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

# 헤더 출력
Write-Host "======================================" -ForegroundColor Blue
Write-Host "AI Prompt Optimization Tool - Server Termination" -ForegroundColor Blue
Write-Host "======================================" -ForegroundColor Blue
Write-Host ""

# 포트 검사 및 종료
Write-Info "Checking ports: 5001, 5173, 3000, 8000, 8080"
$ports = @(5001, 5173, 3000, 8000, 8080)
$anyProcessTerminatedInPortCheck = $false

foreach ($port in $ports) {
    $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    
    if ($connections) {
        foreach ($connection in $connections) {
            $processId = $connection.OwningProcess
            $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
            
            if ($process) {
                Write-Info "Port $port in use: $($process.ProcessName) (PID: $($process.Id))"
                if ($process.Id -eq 0) {
                    Write-Info "Skipping termination of System Idle Process (PID: 0) on port $port."
                    continue # PID 0은 종료하지 않음
                }

                $terminatedSuccessfully = $false
                try {
                    Stop-Process -Id $process.Id -Force -ErrorAction Stop
                    Write-Success "Process terminated: $($process.ProcessName) (PID: $($process.Id))"
                    $terminatedSuccessfully = $true
                    $anyProcessTerminatedInPortCheck = $true
                } catch [Microsoft.PowerShell.Commands.ProcessCommandException] {
                    $errMsg = $_.Exception.Message
                    if ($_.FullyQualifiedErrorId -eq "NoProcessFoundForGivenId,Microsoft.PowerShell.Commands.StopProcessCommand") {
                        Write-Info ("Process {0} (PID: {1}) was already terminated." -f $process.ProcessName, $process.Id)
                        # 이미 종료된 경우도 성공으로 간주할 수 있음 (선택 사항)
                        $terminatedSuccessfully = $true 
                    } else {
                        Write-Error ("Failed to terminate process {0} (PID: {1}) on port {2}: {3}" -f $process.ProcessName, $process.Id, $port, $errMsg)
                    }
                } catch {
                    $errMsg = $_.Exception.Message
                    Write-Error ("An unexpected error occurred while terminating process {0} (PID: {1}) on port {2}: {3}" -f $process.ProcessName, $process.Id, $port, $errMsg)
                }
            } else {
                Write-Info "Process with PID $processId (on port $port) not found or already terminated."
            }
        }
    } else {
        Write-Info "No process running on port $port"
    }
}

# 개발 서버 프로세스 이름으로 종료
Write-Info "Terminating development server processes by name..."
$serverProcessNames = @("node", "python", "flask", "npm", "uvicorn", "fastapi") # 와일드카드 없이 정확한 이름 사용 권장 또는 패턴 사용 시 주의
$anyProcessTerminatedByName = $false

foreach ($procNamePattern in $serverProcessNames) {
    # Get-Process는 -Name에 와일드카드를 직접 지원하므로 *procNamePattern* 형태로 사용
    $processesToKill = Get-Process -Name "*$procNamePattern*" -ErrorAction SilentlyContinue
    
    if ($processesToKill) {
        Write-Info "Found $($processesToKill.Count) processes matching '*$procNamePattern*'"
        
        foreach ($process in $processesToKill) {
            # 포트 검사에서 이미 종료된 프로세스는 여기서 다시 시도하지 않도록 할 수 있으나,
            # 여기서는 포트와 무관하게 이름으로 한 번 더 확인하여 종료
            if ($process.Id -eq 0) { # 혹시 모를 PID 0 체크
                Write-Info "Skipping termination of System Idle Process (PID: 0) found by name."
                continue
            }
            $terminatedSuccessfullyByName = $false
            try {
                # 프로세스가 여전히 실행 중인지 확인 (선택 사항, Stop-Process가 어차피 처리함)
                # Get-Process -Id $process.Id -ErrorAction Stop > $null 

                Stop-Process -Id $process.Id -Force -ErrorAction Stop
                Write-Success "Process terminated: $($process.ProcessName) (PID: $($process.Id))"
                $terminatedSuccessfullyByName = $true
                $anyProcessTerminatedByName = $true
            } catch [Microsoft.PowerShell.Commands.ProcessCommandException] {
                 $errMsg = $_.Exception.Message
                 if ($_.FullyQualifiedErrorId -eq "NoProcessFoundForGivenId,Microsoft.PowerShell.Commands.StopProcessCommand" -or $errMsg -match "Cannot find a process with the process identifier") {
                    Write-Info ("Process {0} (PID: {1}) matching name '{2}' was already terminated." -f $process.ProcessName, $process.Id, $procNamePattern)
                    $terminatedSuccessfullyByName = $true # 이미 종료된 경우
                } else {
                    Write-Error ("Failed to terminate process {0} (PID: {1}) matching name '{2}': {3}" -f $process.ProcessName, $process.Id, $procNamePattern, $errMsg)
                }
            } catch {
                $errMsg = $_.Exception.Message
                Write-Error ("An unexpected error occurred while terminating process {0} (PID: {1}) matching name '{2}': {3}" -f $process.ProcessName, $process.Id, $procNamePattern, $errMsg)
            }
        }
    } else {
        Write-Info "No processes found matching name '*$procNamePattern*'"
    }
}

# 종료 확인
Write-Info "Final check for remaining server processes..."
$remainingProcesses = Get-Process -Name "*node*", "*python*", "*flask*", "*npm*", "*uvicorn*", "*fastapi*" -ErrorAction SilentlyContinue

# PID 0은 남은 프로세스 목록에서 제외
$remainingUserProcesses = $remainingProcesses | Where-Object {$_.Id -ne 0}

if ($remainingUserProcesses) {
    Write-Error "Some server processes might still be running:"
    foreach ($process in $remainingUserProcesses) {
        Write-Host "  - $($process.ProcessName) (PID: $($process.Id))" -ForegroundColor Red
    }
} else {
    Write-Success "All targeted server processes appear to have been successfully terminated."
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Blue
Write-Host "Server Termination Complete" -ForegroundColor Blue
Write-Host "======================================" -ForegroundColor Blue

