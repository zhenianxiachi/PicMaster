export interface HistoryState {
  id: string
  timestamp: number
  params: Record<string, number>
  description: string
  thumbnail?: string
}

export class HistoryManager {
  private history: HistoryState[] = []
  private currentIndex: number = -1
  private maxHistory: number = 100

  constructor(maxHistory: number = 100) {
    this.maxHistory = maxHistory
  }

  pushState(params: Record<string, number>, description: string, thumbnail?: string): void {
    const state: HistoryState = {
      id: `history_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now(),
      params: JSON.parse(JSON.stringify(params)),
      description,
      thumbnail
    }

    if (this.currentIndex < this.history.length - 1) {
      this.history = this.history.slice(0, this.currentIndex + 1)
    }

    this.history.push(state)

    if (this.history.length > this.maxHistory) {
      this.history.shift()
    } else {
      this.currentIndex++
    }
  }

  undo(): HistoryState | null {
    if (!this.canUndo()) return null
    this.currentIndex--
    return this.history[this.currentIndex] ?? null
  }

  redo(): HistoryState | null {
    if (!this.canRedo()) return null
    this.currentIndex++
    return this.history[this.currentIndex] ?? null
  }

  canUndo(): boolean {
    return this.currentIndex > 0
  }

  canRedo(): boolean {
    return this.currentIndex < this.history.length - 1
  }

  getCurrentState(): HistoryState | null {
    if (this.currentIndex >= 0 && this.currentIndex < this.history.length) {
      return this.history[this.currentIndex]
    }
    return null
  }

  getHistory(): HistoryState[] {
    return this.history
  }

  getCurrentIndex(): number {
    return this.currentIndex
  }

  jumpToState(index: number): HistoryState | null {
    if (index >= 0 && index < this.history.length) {
      this.currentIndex = index
      return this.history[index] ?? null
    }
    return null
  }

  clear(): void {
    this.history = []
    this.currentIndex = -1
  }

  getHistoryLength(): number {
    return this.history.length
  }
}

export const historyManager = new HistoryManager(100)
