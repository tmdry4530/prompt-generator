/**
 * MSW (Mock Service Worker) 서버 설정
 * API 요청을 모킹하여 테스트에서 사용합니다.
 */

import { setupServer } from "msw/node";
import { handlers } from "./handlers";

// 서버 설정 생성
export const server = setupServer(...handlers);

// 개별 핸들러 내보내기 (테스트에서 직접 사용할 수 있도록)
export { handlers };
