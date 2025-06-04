export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4">
      <h1 className="text-4xl font-bold mb-4">404</h1>
      <h2 className="text-2xl mb-6">페이지를 찾을 수 없습니다</h2>
      <p className="text-gray-600 mb-8">
        요청하신 페이지가 존재하지 않거나 이동되었습니다.
      </p>
      <a
        href="/"
        className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
      >
        홈으로 돌아가기
      </a>
    </div>
  );
}
