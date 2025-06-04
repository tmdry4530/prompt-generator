import { Loader2 } from "lucide-react"

export default function Loading() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-theme(space.14))]">
      <Loader2 className="h-16 w-16 animate-spin text-zinc-900 dark:text-zinc-50" />
      <p className="mt-4 text-lg text-zinc-500 dark:text-zinc-400">Loading Prompt Optimizer...</p>
    </div>
  )
}
