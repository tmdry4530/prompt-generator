// 이 파일은 toast 기능을 위한 훅을 제공합니다
import { toast } from "sonner"

export interface ToasterToast {
  id: string
  description?: React.ReactNode
  action?: React.ReactNode
  duration?: number
}

export const useToast = () => {
  return {
    toast: (message: string, options?: any) => {
      return toast(message, options)
    },
    dismiss: (toastId?: string) => {
      if (toastId) {
        toast.dismiss(toastId)
      }
    },
    success: (message: string, options?: any) => {
      return toast.success(message, options)
    },
    error: (message: string, options?: any) => {
      return toast.error(message, options)
    },
    warning: (message: string, options?: any) => {
      return toast(message, {
        ...options,
        className: "bg-yellow-500 text-white",
      })
    },
    info: (message: string, options?: any) => {
      return toast(message, {
        ...options,
        className: "bg-blue-500 text-white",
      })
    }
  }
}
