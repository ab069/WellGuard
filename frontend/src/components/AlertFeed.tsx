import React from 'react'
import { useWsStore } from '../store/wsStore'

const severityColors: Record<string, string> = {
  critical: '#ef4444',
  high: '#f97316',
  medium: '#eab308',
  low: '#22c55e',
}

export default function AlertFeed() {
  const { alerts } = useWsStore()

  return (
    <div style={{ background: '#111827', border: '1px solid #1f2937', borderRadius: 10, padding: 20, marginBottom: 24 }}>
      <h3 style={{ color: '#f9fafb', margin: '0 0 12px', fontSize: 16 }}>Real-Time Alerts</h3>
      {alerts.length === 0 && <p style={{ color: '#6b7280', fontSize: 13 }}>No alerts yet</p>}
      {alerts.map((a: any, i: number) => (
        <div key={i} style={{ padding: '10px 0', borderBottom: '1px solid #1f2937', display: 'flex', alignItems: 'center', gap: 12 }}>
          <span style={{
            padding: '2px 8px', borderRadius: 4, fontSize: 11, fontWeight: 600,
            background: severityColors[a.severity] || '#6b7280', color: '#fff',
          }}>
            {a.severity.toUpperCase()}
          </span>
          <span style={{ color: '#d1d5db', fontSize: 13, flex: 1 }}>{a.title}</span>
          <span style={{ color: '#6b7280', fontSize: 11 }}>{a.status}</span>
        </div>
      ))}
    </div>
  )
}
