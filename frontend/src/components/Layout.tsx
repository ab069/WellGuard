import React from 'react'
import { useAuthStore } from '../store/authStore'
import { useWsStore } from '../store/wsStore'
import { useNavigate } from 'react-router-dom'

const styles: Record<string, React.CSSProperties> = {
  header: {
    background: '#111827',
    borderBottom: '1px solid #1f2937',
    padding: '12px 24px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  logo: { color: '#0891b2', fontSize: 22, fontWeight: 700, letterSpacing: 1 },
  right: { display: 'flex', alignItems: 'center', gap: 16 },
  userName: { color: '#9ca3af', fontSize: 14 },
  badge: { width: 8, height: 8, borderRadius: '50%', display: 'inline-block' },
  btn: {
    background: 'transparent',
    border: '1px solid #374151',
    color: '#d1d5db',
    padding: '6px 14px',
    borderRadius: 6,
    cursor: 'pointer',
    fontSize: 13,
  },
}

export default function Layout({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuthStore()
  const { connected } = useWsStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div style={{ minHeight: '100vh', background: '#0b0f1a' }}>
      <header style={styles.header}>
        <span style={styles.logo}>WellGuard</span>
        <div style={styles.right}>
          <span style={{ ...styles.badge, background: connected ? '#22c55e' : '#ef4444' }} />
          <span style={styles.userName}>{user?.name}</span>
          <button style={styles.btn} onClick={handleLogout}>Logout</button>
        </div>
      </header>
      <main style={{ padding: 24, maxWidth: 1280, margin: '0 auto' }}>{children}</main>
    </div>
  )
}
