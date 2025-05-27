/**
 * 유틸리티 함수 모음
 */

import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * 클래스명을 병합하는 유틸리티 함수
 * Tailwind CSS와 함께 사용하기 위한 함수입니다.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * 날짜를 포맷팅하는 유틸리티 함수
 */
export function formatDate(date: Date): string {
  return date.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  })
}

/**
 * 숫자에 천 단위 구분자를 추가하는 유틸리티 함수
 */
export function formatNumber(num: number): string {
  return num.toLocaleString("ko-KR")
}

/**
 * 문자열을 특정 길이로 자르는 유틸리티 함수
 */
export function truncateString(str: string, length: number): string {
  if (str.length <= length) return str
  return str.slice(0, length) + "..."
}

/**
 * 랜덤 ID를 생성하는 유틸리티 함수
 */
export function generateId(): string {
  return Math.random().toString(36).substring(2, 9)
}
