import React from 'react'
import Layout from '../components/Layout'
import StatsCards from '../components/StatsCards'
import WellForm from '../components/WellForm'
import AlertFeed from '../components/AlertFeed'
import WellList from '../components/WellList'
import { useWebSocket } from '../hooks/useWebSocket'

export default function Dashboard() {
  useWebSocket()

  return (
    <Layout>
      <StatsCards />
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        <div>
          <WellForm />
          <AlertFeed />
        </div>
        <WellList />
      </div>
    </Layout>
  )
}
