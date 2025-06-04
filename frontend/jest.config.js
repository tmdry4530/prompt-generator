const nextJest = require("next/jest");

const createJestConfig = nextJest({
  // Next.js 앱 경로
  dir: "./",
});

// Jest에 전달할 사용자 정의 설정
const customJestConfig = {
  setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],
  testEnvironment: "jest-environment-jsdom",
  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/src/$1",
  },
  testPathIgnorePatterns: ["<rootDir>/node_modules/", "<rootDir>/.next/"],
};

// createJestConfig를 내보내 Next.js의 요구사항을 감지하게 함
module.exports = createJestConfig(customJestConfig);
