import React, { useState } from 'react'
import { useWellStore } from '../store/wellStore'

const inputStyle: React.CSSProperties = {
  width: '100%', padding: '10px 12px', borderRadius: 6, border: '1px solid #374151',
  background: '#1f2937', color: '#f9fafb', fontSize: 14, boxSizing: 'border-box',
}

export default function WellForm() {
  const { submitWell } = useWellStore()
  const [form, setForm] = useState({ well_name: '', well_type: 'oil', depth: '', pressure: '', temperature: '', flow_rate: '' })
  const [loading, setLoading] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      await submitWell({
        well_name: form.well_name,
        well_type: form.well_type,
        depth: parseFloat(form.depth) || 0,
        pressure: parseFloat(form.pressure) || 0,
        temperature: parseFloat(form.temperature) || 0,
        flow_rate: parseFloat(form.flow_rate) || 0,
      })
      setForm({ well_name: '', well_type: 'oil', depth: '', pressure: '', temperature: '', flow_rate: '' })
    } catch {}
    setLoading(false)
  }

  return (
    <form onSubmit={handleSubmit} style={{ background: '#111827', border: '1px solid #1f2937', borderRadius: 10, padding: 20, marginBottom: 24 }}>
      <h3 style={{ color: '#f9fafb', margin: '0 0 16px', fontSize: 16 }}>Register Well</h3>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
        <input name="well_name" placeholder="Well name" value={form.well_name} onChange={handleChange} required style={inputStyle} />
        <select name="well_type" value={form.well_type} onChange={handleChange} style={inputStyle}>
          <option value="oil">Oil</option>
          <option value="gas">Gas</option>
          <option value="injection">Injection</option>
        </select>
        <input name="depth" placeholder="Depth (ft)" type="number" value={form.depth} onChange={handleChange} style={inputStyle} />
        <input name="pressure" placeholder="Pressure (psi)" type="number" value={form.pressure} onChange={handleChange} style={inputStyle} />
        <input name="temperature" placeholder="Temperature (°C)" type="number" value={form.temperature} onChange={handleChange} style={inputStyle} />
        <input name="flow_rate" placeholder="Flow rate" type="number" value={form.flow_rate} onChange={handleChange} style={inputStyle} />
      </div>
      <button type="submit" disabled={loading} style={{
        marginTop: 16, width: '100%', padding: '10px', borderRadius: 6,
        border: 'none', background: '#0891b2', color: '#fff', fontSize: 14, fontWeight: 600, cursor: 'pointer',
      }}>
        {loading ? 'Submitting...' : 'Add Well'}
      </button>
    </form>
  )
}
