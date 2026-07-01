import React, { useEffect, useState } from 'react'
import { useWellStore } from '../store/wellStore'
import { useWebSocket } from '../hooks/useWebSocket'

function integrityColor(score: number): string {
  if (score >= 70) return '#22c55e'
  if (score >= 40) return '#eab308'
  return '#ef4444'
}

export default function WellList() {
  const { wells, fetchWells } = useWellStore()
  const { sendMessage } = useWebSocket()
  const [expanded, setExpanded] = useState<string | null>(null)
  const [analyzing, setAnalyzing] = useState<string | null>(null)

  useEffect(() => { fetchWells() }, [])

  const handleAnalyze = (wellId: string) => {
    setAnalyzing(wellId)
    sendMessage({ action: 'analyze', well_id: wellId })
    setTimeout(() => setAnalyzing(null), 2000)
  }

  return (
    <div>
      <h3 style={{ color: '#f9fafb', margin: '0 0 12px', fontSize: 16 }}>Wells</h3>
      {wells.map((w) => (
        <div key={w.id} style={{
          background: '#111827', border: '1px solid #1f2937', borderRadius: 8, marginBottom: 8, overflow: 'hidden',
        }}>
          <div
            onClick={() => setExpanded(expanded === w.id ? null : w.id)}
            style={{ padding: '14px 18px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', cursor: 'pointer' }}
          >
            <div>
              <span style={{ color: '#f9fafb', fontWeight: 600, fontSize: 14 }}>{w.well_name}</span>
              <span style={{ color: '#6b7280', fontSize: 12, marginLeft: 10 }}>{w.well_type}</span>
              <span style={{ color: '#9ca3af', fontSize: 12, marginLeft: 10 }}>{w.status}</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <span style={{ color: integrityColor(w.integrity_score), fontWeight: 700, fontSize: 18 }}>{w.integrity_score}</span>
              <span style={{ color: '#6b7280', fontSize: 11 }}>/100</span>
            </div>
          </div>
          {expanded === w.id && (
            <div style={{ padding: '0 18px 14px', borderTop: '1px solid #1f2937', paddingTop: 12 }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, color: '#d1d5db', fontSize: 13, marginBottom: 12 }}>
                <div>Depth: <strong>{w.depth} ft</strong></div>
                <div>Pressure: <strong>{w.pressure} psi</strong></div>
                <div>Temperature: <strong>{w.temperature} °C</strong></div>
                <div>Flow Rate: <strong>{w.flow_rate}</strong></div>
              </div>
              <button
                onClick={() => handleAnalyze(w.id)}
                disabled={analyzing === w.id}
                style={{
                  padding: '8px 16px', borderRadius: 6, border: 'none',
                  background: analyzing === w.id ? '#374151' : '#0891b2',
                  color: '#fff', fontSize: 13, cursor: 'pointer',
                }}
              >
                {analyzing === w.id ? 'Analyzing...' : 'Analyze Integrity'}
              </button>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
