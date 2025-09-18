import { useState } from 'react'
import { Room } from 'livekit-client'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:3001'

export default function MinimalLivekitTest() {
  const [log, setLog] = useState<string>('idle')

  async function run() {
    setLog('fetching token...')
    const identity = `tester_${Math.floor(Math.random() * 1e6)}`
    const room = 'default'
    try {
      const r = await fetch(`${BACKEND_URL}/token?identity=${encodeURIComponent(identity)}&room=${encodeURIComponent(room)}`)
      const { token, wsUrl } = await r.json()
      setLog(`connecting to ${wsUrl} as ${identity}`)

      const lk = new Room()
      try {
        await lk.connect(wsUrl, token, { rtcConfig: { iceTransportPolicy: 'relay' }, autoSubscribe: true })
        setLog('connected!')
      } catch (e) {
        setLog('primary failed, retry alt... ' + (e as Error).message)
        const alt = wsUrl.endsWith('/rtc') ? wsUrl.replace(/\/rtc$/, '') : `${wsUrl.replace(/\/$/, '')}/rtc`
        await lk.connect(alt, token, { rtcConfig: { iceTransportPolicy: 'relay' }, autoSubscribe: true })
        setLog('connected via alt!')
      }
    } catch (e) {
      setLog('error: ' + (e as Error).message)
    }
  }

  return (
    <div style={{ padding: 24 }}>
      <h2>Minimal LiveKit Test</h2>
      <button onClick={run}>Run</button>
      <pre style={{ whiteSpace: 'pre-wrap' }}>{log}</pre>
    </div>
  )
}


