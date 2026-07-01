import React, { useEffect } from 'react'
import { useWellStore } from '../store/wellStore'

const cardStyle: React.CSSProperties = {
  background: '#111827',
  border: '1px solid #1f2937',
  borderRadius: 10,
  padding: '20px 24px',
  textAlign: 'center',
}

const labelStyle: React.CSSProperties = { color: '#9ca3af', fontSize: 13, marginBottom: 6 }
const valueStyle: React.CSSProperties = { color: '#f9fafb', fontSize: 28, fontWeight: 700 }
const accent = '#0891b2'

export default function StatsCards() {
  const { stats, fetchStats } = useWellStore()

  useEffect(() => { fetchStats() }, [])

  const cards = [
    { label: 'Total Wells', value: stats?.total_wells ?? 0, color: accent },
    { label: 'Active Wells', value: stats?.active_wells ?? 0, color: '#22c55e' },
    { label: 'Critical Alerts', value: stats?.critical_alerts ?? 0, color: '#ef4444' },
    { label: 'Avg Integrity', value: stats ? `${stats.avg_integrity_score}%` : '0%', color: '#eab308' },
  ]

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16, marginBottom: 24 }}>
      {cards.map((c) => (
        <div key={c.label} style={cardStyle}>
          <div style={labelStyle}>{c.label}</div>
          <div style={{ ...valueStyle, color: c.color }}>{c.value}</div>
        </div>
      ))}
    </div>
  )
}
