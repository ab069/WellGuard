import { create } from 'zustand'

interface WsState {
  connected: boolean
  lastEvent: any
  alerts: any[]
  setConnected: (v: boolean) => void
  addAlert: (alert: any) => void
  setLastEvent: (event: any) => void
}

export const useWsStore = create<WsState>((set) => ({
  connected: false,
  lastEvent: null,
  alerts: [],
  setConnected: (v) => set({ connected: v }),
  addAlert: (alert) => set((s) => ({ alerts: [alert, ...s.alerts].slice(0, 50) })),
  setLastEvent: (event) => set({ lastEvent: event }),
}))
