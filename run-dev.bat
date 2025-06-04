@echo off
REM AI 프롬프트 최적화 도구 - 개발 서버 실행 배치 파일
title AI 프롬프트 최적화 도구 - 서버 실행

REM 관리자 권한 확인 없이 실행
echo AI 프롬프트 최적화 도구 - 개발 서버 시작 중...

REM PowerShell 스크립트 실행
powershell.exe -ExecutionPolicy Bypass -File "%~dp0start-servers.ps1"

REM 스크립트 종료 시 5초 대기
timeout /t 5 