import { useState } from 'react'
import { TopBar } from './Header'


const API = 'http://localhost:8000'

export default function Login({ onLogin }) {
  const [usuario, setUsuario] = useState('')
  const [contrasena, setContrasena] = useState('')
  const [error, setError] = useState('')
  const [cargando, setCargando] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setCargando(true)
    try {
      const res = await fetch(`${API}/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ usuario, contrasena }),
      })
      const data = await res.json()
      if (!res.ok) {
        setError(data.detail || 'Credenciales inválidas')
      } else {
        onLogin({ id: data.id, rol: data.rol, usuario })
      }
    } catch {
      setError('No se pudo conectar con el servidor')
    } finally {
      setCargando(false)
    }
  }

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-soft)' }}>
      <TopBar />

      <div className="login-wrap">
        <div className="fi-panel login-card">
          <div className="fi-panel-head">Acceso al Sistema</div>
          <div className="fi-panel-body">
            <div className="login-logo">
              <div>
                <div className="lt">Servicio Social</div>
                <div className="ls">Facultad de Ingeniería · UNAM</div>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="login-form">
              <div className="fi-field">
                <label>Usuario</label>
                <input
                  className="fi-input"
                  type="text"
                  value={usuario}
                  onChange={e => setUsuario(e.target.value)}
                  placeholder="Número de cuenta o usuario"
                  required
                />
              </div>

              <div className="fi-field">
                <label>Contraseña</label>
                <input
                  className="fi-input"
                  type="password"
                  value={contrasena}
                  onChange={e => setContrasena(e.target.value)}
                  placeholder="Ingresa tu contraseña"
                  required
                />
              </div>

              {error && <p className="fi-banner error" style={{ margin: 0 }}>{error}</p>}

              <button className="fi-btn" type="submit" disabled={cargando} style={{ width: '100%' }}>
                {cargando ? 'Iniciando…' : 'Iniciar sesión'}
              </button>
            </form>

            <p className="login-nota">
              Conexión cifrada · Fernet AES-128 + firma Dilithium PQC
            </p>
          </div>
        </div>

        <p className="login-pie">
          Unidad de Servicios de Cómputo Administrativos · Facultad de Ingeniería
        </p>
      </div>

      <style>{`
        .login-wrap {
          max-width: 460px;
          margin: 48px auto;
          padding: 0 20px;
        }
        .login-card { width: 100%; }
        .login-logo {
          display: flex; align-items: center; gap: 14px;
          padding-bottom: 18px; margin-bottom: 18px;
          border-bottom: 1px solid var(--border);
        }
        .login-logo img { height: 52px; }
        .login-logo .lt { font-size: 1.25rem; font-weight: 800; color: var(--unam-red); line-height: 1.1; }
        .login-logo .ls { font-size: 0.82rem; color: var(--text-muted); }
        .login-form { display: flex; flex-direction: column; gap: 16px; }
        .login-nota {
          margin-top: 20px; font-size: 0.75rem; color: var(--text-muted);
          text-align: center; line-height: 1.5;
        }
        .login-pie {
          text-align: center; margin-top: 22px;
          font-size: 0.78rem; color: var(--text-muted);
        }
      `}</style>
    </div>
  )
}
