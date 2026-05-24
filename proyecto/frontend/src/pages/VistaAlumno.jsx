import { useState, useEffect } from 'react'
import { TopBar, NavBar, UserBar, SectionTitle, CheckMark } from './Header'

const API = 'http://localhost:8000'

const NAV = [
  { id: 'perfil', label: 'Mi Perfil' },
  { id: 'contrato', label: 'Contrato' },
  { id: 'empresas', label: 'Empresas' },
]

export default function VistaAlumno({ usuario, onLogout }) {
  const [alumno, setAlumno] = useState(null)
  const [contrato, setContrato] = useState(null)
  const [empresas, setEmpresas] = useState([])
  const [cargando, setCargando] = useState(true)
  const [generando, setGenerando] = useState(false)
  const [error, setError] = useState('')
  const [tab, setTab] = useState('perfil')

  useEffect(() => {
    async function cargarDatos() {
      try {
        const [resAlumno, resEmpresas] = await Promise.all([
          fetch(`${API}/alumnos/${usuario.id}`),
          fetch(`${API}/empresas/`),
        ])
        const dataAlumno = await resAlumno.json()
        const dataEmpresas = await resEmpresas.json()

        setAlumno(dataAlumno.alumno)
        setEmpresas(dataEmpresas.empresas)

        // Intentar cargar contrato existente
        const resContrato = await fetch(`${API}/contratos/alumno/${usuario.id}`)
        if (resContrato.ok) {
          const dataContrato = await resContrato.json()
          setContrato(dataContrato.contrato)
        }
      } catch {
        setError('Error al cargar los datos')
      } finally {
        setCargando(false)
      }
    }
    cargarDatos()
  }, [usuario.id])

  async function generarContrato() {
    setGenerando(true)
    setError('')
    try {
      const res = await fetch(`${API}/contratos/generar/${usuario.id}`, { method: 'POST' })
      const data = await res.json()
      if (!res.ok) {
        setError(data.detail)
      } else {
        setContrato(data.contrato)
      }
    } catch {
      setError('Error al generar el contrato')
    } finally {
      setGenerando(false)
    }
  }

  if (cargando) {
    return (
      <div style={{ minHeight: '100vh', background: 'var(--bg-soft)' }}>
        <TopBar />
        <div className="fi-center">Cargando…</div>
      </div>
    )
  }

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-soft)' }}>
      <TopBar />
      <NavBar items={NAV} activo={tab} onSelect={setTab} />
      <UserBar identificador={alumno?.matricula ?? usuario.usuario} onLogout={onLogout} />

      <main className="fi-main">
        <SectionTitle>Proceso de Servicio Social</SectionTitle>

        <div className="fi-stack">
          {/* ---------- Mi perfil ---------- */}
          {tab === 'perfil' && alumno && (
            <section className="fi-panel">
              <div className="fi-panel-head">Mi Perfil</div>
              <div className="fi-panel-body">
                <div className="perfil-grid">
                  <div>
                    <div className="fi-row"><span className="lbl">Nombre</span><span className="val">{`${alumno.nombre} ${alumno.apellidoPaterno} ${alumno.apellidoMaterno}`}</span></div>
                    <div className="fi-row"><span className="lbl">Matrícula</span><span className="val"><code>{alumno.matricula}</code></span></div>
                    <div className="fi-row"><span className="lbl">Carrera</span><span className="val">{alumno.carrera}</span></div>
                    <div className="fi-row"><span className="lbl">Semestre</span><span className="val">{alumno.semestre}</span></div>
                    <div className="fi-row">
                      <span className="lbl">Empresa</span>
                      <span className="val">
                        {alumno.empresa
                          ? <span className="fi-badge ok"><CheckMark />{alumno.empresa}</span>
                          : <span className="fi-badge warn">Sin asignar</span>}
                      </span>
                    </div>
                  </div>
                  <div className="qr-box">
                    <p className="qr-title">QR de matrícula cifrado</p>
                    {alumno.qrCode
                      ? <img src={alumno.qrCode} alt="QR cifrado" className="qr-img" />
                      : <p className="muted">No disponible</p>}
                  </div>
                </div>
              </div>
            </section>
          )}

          {/* ---------- Contrato ---------- */}
          {tab === 'contrato' && (
            <section className="fi-panel">
              <div className="fi-panel-head">Contrato de Servicio Social</div>
              <div className="fi-panel-body">
                {contrato ? (
                  <div>
                    <pre className="contrato-cuerpo">{contrato.contenido}</pre>
                    <div className="firma-estado">
                      <span className="fi-badge ok">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 1 3 5v6c0 5.5 3.8 10.7 9 12 5.2-1.3 9-6.5 9-12V5z"/></svg>
                        Firma PQC: <strong style={{ marginLeft: 4 }}>{contrato.estadoFirma}</strong>
                      </span>
                    </div>
                  </div>
                ) : (
                  <div>
                    <p className="muted" style={{ marginBottom: 14 }}>No tienes contrato generado todavía.</p>
                    {error && <p className="fi-banner error">{error}</p>}
                    <button className="fi-btn" onClick={generarContrato} disabled={generando}>
                      {generando ? 'Generando…' : 'Generar contrato'}
                    </button>
                  </div>
                )}
              </div>
            </section>
          )}

          {/* ---------- Catálogo de empresas ---------- */}
          {tab === 'empresas' && (
            <section className="fi-panel">
              <div className="fi-panel-head">Catálogo de Empresas Disponibles</div>
              <div className="fi-panel-body">
                {empresas.length === 0 ? (
                  <p className="muted">No hay empresas registradas aún.</p>
                ) : (
                  <div className="fi-grid-cards">
                    {empresas.map(emp => (
                      <div key={emp.empresaId} className="fi-mini-card">
                        <strong style={{ color: 'var(--text-h)', display: 'block', marginBottom: 6 }}>{emp.nombre}</strong>
                        <p className="muted">{emp.direccion}</p>
                        <p className="muted">Tel. {emp.telefono}</p>
                        <p className="muted">{emp.correo}</p>
                        <p className="muted" style={{ fontFamily: 'var(--mono)', fontSize: '0.72rem', marginTop: 6 }}>
                          Folio: {emp.folioRegistro}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </section>
          )}
        </div>
      </main>

      <style>{`
        .perfil-grid { display: flex; gap: 32px; flex-wrap: wrap; }
        .perfil-grid > div:first-child { flex: 1; min-width: 240px; }
        .qr-box { display: flex; flex-direction: column; align-items: center; gap: 8px; }
        .qr-title { font-size: 0.82rem; color: var(--text-muted); font-weight: 700; }
        .qr-img { width: 170px; height: 170px; border-radius: 8px; border: 1px solid var(--border); background: #fff; padding: 6px; }
        .muted { color: var(--text-muted); font-size: 0.9rem; margin: 3px 0; }
        .contrato-cuerpo {
          background: var(--bg-soft); border: 1px solid var(--border); border-radius: 8px;
          padding: 18px; white-space: pre-wrap; font-size: 0.85rem; color: var(--text-h);
          line-height: 1.6; font-family: var(--mono); max-height: 420px; overflow: auto;
        }
        .firma-estado { margin-top: 14px; }
      `}</style>
    </div>
  )
}
