import { useEffect, useRef } from 'react'
import { useAuthStore } from '../store/authStore'
import { useWsStore } from '../store/wsStore'

export function useWebSocket() {
  const { user } = useAuthStore()
  const { setConnected, addAlert, setLastEvent } = useWsStore()
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    if (!user) return

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    const url = `${protocol}//${host}/ws/${user.id}`

    function connect() {
      const ws = new WebSocket(url)
      wsRef.current = ws

      ws.onopen = () => setConnected(true)
      ws.onclose = () => {
        setConnected(false)
        setTimeout(connect, 3000)
      }
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          setLastEvent(data)
          if (data.type === 'alert') addAlert(data.alert)
        } catch {}
      }
    }

    connect()

    return () => {
      wsRef.current?.close()
    }
  }, [user?.id])

  const sendMessage = (msg: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(msg))
    }
  }

  return { sendMessage }
}
