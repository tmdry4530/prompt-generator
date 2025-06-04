import Link from "next/link"
import { ModeToggle } from "./mode-toggle"
import { BotMessageSquareIcon } from "lucide-react"

export default function AppHeader() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-zinc-200/40 bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60 dark:border-zinc-800/40 dark:bg-zinc-950/95 dark:supports-[backdrop-filter]:bg-zinc-950/60">
      <div className="container flex h-14 max-w-screen-2xl items-center">
        <Link href="/" className="mr-6 flex items-center space-x-2">
          <BotMessageSquareIcon className="h-6 w-6" />
          <span className="font-bold sm:inline-block">AI Prompt Optimizer</span>
        </Link>
        <div className="flex flex-1 items-center justify-end space-x-2">
          <ModeToggle />
        </div>
      </div>
    </header>
  )
}
