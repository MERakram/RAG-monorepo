// Toast configuration constants
export const TOAST_DURATION = {
  SHORT: 1000,    // 2 seconds
  MEDIUM: 3000,   // 3 seconds (default)
  LONG: 4000,     // 4 seconds
  PERSISTENT: 0   // Never auto-dismiss
} as const

export const DEFAULT_TOAST_DURATION = TOAST_DURATION.SHORT