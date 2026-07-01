import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import axios from 'axios'
import { useAuthStore } from '../store/authStore'

const containerStyle: React.CSSProperties = {
  minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
  background: '#0b0f1a',
}

const cardStyle: React.CSSProperties = {
  background: '#111827', border: '1px solid #1f2937', borderRadius: 12, padding: 40,
  width: 360, maxWidth: '90%',
}

const inputStyle: React.CSSProperties = {
  width: '100%', padding: '10px 12px', borderRadius: 6, border: '1px solid #374151',
  background: '#1f2937', color: '#f9fafb', fontSize: 14, marginBottom: 12, boxSizing: 'border-box',
}

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { setAuth } = useAuthStore()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      const { data } = await axios.post('/api/auth/login', { email, password })
      setAuth(data.access_token, data.user)
      navigate('/')
    } catch {
      setError('Invalid credentials')
    }
  }

  return (
    <div style={containerStyle}>
      <div style={cardStyle}>
        <h1 style={{ color: '#0891b2', textAlign: 'center', margin: '0 0 24px', fontSize: 28 }}>WellGuard</h1>
        <form onSubmit={handleSubmit}>
          <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required style={inputStyle} />
          <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required style={inputStyle} />
          {error && <p style={{ color: '#ef4444', fontSize: 13, margin: '0 0 8px' }}>{error}</p>}
          <button type="submit" style={{
            width: '100%', padding: 10, borderRadius: 6, border: 'none',
            background: '#0891b2', color: '#fff', fontSize: 14, fontWeight: 600, cursor: 'pointer',
          }}>Sign In</button>
        </form>
        <p style={{ color: '#6b7280', fontSize: 13, textAlign: 'center', marginTop: 16 }}>
          No account? <Link to="/register" style={{ color: '#0891b2' }}>Register</Link>
        </p>
      </div>
    </div>
  )
}
