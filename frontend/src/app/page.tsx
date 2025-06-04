import PromptGenerator from "@/components/prompt-generator";

export default function Home() {
  return (
    <main className="min-h-screen p-4 md:p-8 lg:p-12">
      <div className="container mx-auto max-w-6xl">
        <h1 className="text-3xl font-bold text-center mb-8">
          모델 최적화 프롬프트 생성기
        </h1>
        <PromptGenerator />
      </div>
    </main>
  );
}
