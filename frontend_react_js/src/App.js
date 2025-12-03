import React, { useEffect, useState } from 'react';

const apiBase = process.env.REACT_APP_API_BASE || process.env.REACT_APP_BACKEND_URL || '';

export default function App() {
  const [status, setStatus] = useState('Checking backend...');
  useEffect(() => {
    let cancelled = false;
    async function check() {
      try {
        if (!apiBase) {
          setStatus('No backend configured');
          return;
        }
        const res = await fetch(apiBase + '/');
        if (!cancelled) {
          if (res.ok) {
            const data = await res.json().catch(() => ({}));
            setStatus(`Backend OK: ${data.message || res.status}`);
          } else {
            setStatus(`Backend error: ${res.status}`);
          }
        }
      } catch (e) {
        if (!cancelled) setStatus(`Backend unreachable: ${e.message}`);
      }
    }
    check();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div style={{ fontFamily: 'system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif', background: '#F3F4F6', minHeight: '100vh' }}>
      <header style={{ background: '#1E3A8A', color: '#FFFFFF', padding: '16px 24px', boxShadow: '0 2px 6px rgba(0,0,0,0.1)' }}>
        <h1 style={{ margin: 0, fontSize: 20 }}>VizAI Animal Behavior Analytics</h1>
      </header>
      <main style={{ padding: 24 }}>
        <section style={{ background: '#FFFFFF', borderRadius: 8, padding: 16, boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
          <h2 style={{ marginTop: 0 }}>Environment</h2>
          <ul>
            <li><strong>API Base:</strong> {apiBase || '(not set)'}</li>
            <li><strong>WebSocket:</strong> {process.env.REACT_APP_WS_URL || '(not set)'}</li>
            <li><strong>Frontend URL:</strong> {process.env.REACT_APP_FRONTEND_URL || '(not set)'}</li>
          </ul>
          <p><strong>Health:</strong> {status}</p>
        </section>
      </main>
      <footer style={{ padding: 16, textAlign: 'center', color: '#111827' }}>
        <small>Ocean Professional theme</small>
      </footer>
    </div>
  );
}
