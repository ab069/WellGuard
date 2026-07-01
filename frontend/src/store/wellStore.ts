import { create } from 'zustand'
import axios from 'axios'
import { useAuthStore } from './authStore'

interface Well {
  id: string
  well_name: string
  well_type: string
  status: string
  depth: number
  pressure: number
  temperature: number
  flow_rate: number
  integrity_score: number
  created_at: string
}

interface WellStats {
  total_wells: number
  active_wells: number
  critical_alerts: number
  avg_integrity_score: number
}

interface WellState {
  wells: Well[]
  stats: WellStats | null
  loading: boolean
  fetchWells: () => Promise<void>
  fetchStats: () => Promise<void>
  submitWell: (data: any) => Promise<void>
}

const api = axios.create({ baseURL: '/api' })

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export const useWellStore = create<WellState>((set) => ({
  wells: [],
  stats: null,
  loading: false,
  fetchWells: async () => {
    set({ loading: true })
    try {
      const { data } = await api.get('/wells')
      set({ wells: data, loading: false })
    } catch {
      set({ loading: false })
    }
  },
  fetchStats: async () => {
    try {
      const { data } = await api.get('/wells/stats')
      set({ stats: data })
    } catch {}
  },
  submitWell: async (wellData) => {
    await api.post('/wells', wellData)
    await Promise.all([
      useWellStore.getState().fetchWells(),
      useWellStore.getState().fetchStats(),
    ])
  },
}))
