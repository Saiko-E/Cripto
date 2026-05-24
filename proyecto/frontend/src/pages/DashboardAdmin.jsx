import { useState, useEffect } from "react"
import { TopBar, NavBar, UserBar, SectionTitle } from './Header'

const API = "http://localhost:8000"

const FORM_EMPRESA_VACIO = { nombre: "", direccion: "", telefono: "", correo: "", folioRegistro: "" }
const FORM_ALUMNO_VACIO = {
  matricula: "", usuario: "", contrasena: "", nombre: "",
  apellidoPaterno: "", apellidoMaterno: "", carrera: "", semestre: "", empresaId: "",
}

const NAV = [
  { id: "resumen", label: "Resumen" },
  { id: "alumnos", label: "Alumnos" },
  { id: "empresas", label: "Empresas" },
]

export default function DashboardAdmin({ usuario, onLogout }) {
  const [tab, setTab] = useState("resumen")
  const [alumnos, setAlumnos] = useState([])
  const [empresas, setEmpresas] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState("")
  const [exito, setExito] = useState("")
  const [formEmpresa, setFormEmpresa] = useState(FORM_EMPRESA_VACIO)
  const [formAlumno, setFormAlumno] = useState(FORM_ALUMNO_VACIO)
  const [enviandoEmpresa, setEnviandoEmpresa] = useState(false)
  const [enviandoAlumno, setEnviandoAlumno] = useState(false)
  const [mostrarFormAlumno, setMostrarFormAlumno] = useState(false)

  useEffect(() => { cargarDatos() }, [])

  async function cargarDatos() {
    setCargando(true)
    try {
      const [resA, resE] = await Promise.all([fetch(`${API}/alumnos/`), fetch(`${API}/empresas/`)])
      setAlumnos((await resA.json()).alumnos)
      setEmpresas((await resE.json()).empresas)
    } catch { setError("Error al cargar los datos") }
    finally { setCargando(false) }
  }

  async function darDeBaja(alumnoId, nombre) {
    if (!confirm(`¿Dar de baja a ${nombre}? Se eliminará también su contrato.`)) return
    try {
      const res = await fetch(`${API}/alumnos/${alumnoId}`, { method: "DELETE" })
      if (res.ok) { setAlumnos(prev => prev.filter(a => a.alumnoId !== alumnoId)); mostrarMsg("Alumno dado de baja") }
    } catch { setError("Error al dar de baja") }
  }

  async function registrarEmpresa(e) {
    e.preventDefault(); setEnviandoEmpresa(true); setError("")
    try {
      const res = await fetch(`${API}/empresas/`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(formEmpresa) })
      const data = await res.json()
      if (!res.ok) setError(data.detail || "Error al registrar empresa")
      else { setFormEmpresa(FORM_EMPRESA_VACIO); mostrarMsg("Empresa registrada"); cargarDatos() }
    } catch { setError("Error de conexión") }
    finally { setEnviandoEmpresa(false) }
  }

  async function registrarAlumno(e) {
    e.preventDefault(); setEnviandoAlumno(true); setError("")
    try {
      const body = { ...formAlumno, semestre: parseInt(formAlumno.semestre), empresaId: formAlumno.empresaId ? parseInt(formAlumno.empresaId) : null }
      const res = await fetch(`${API}/alumnos/`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) })
      const data = await res.json()
      if (!res.ok) setError(data.detail || "Error al registrar alumno")
      else { setFormAlumno(FORM_ALUMNO_VACIO); setMostrarFormAlumno(false); mostrarMsg("Alumno registrado"); cargarDatos() }
    } catch { setError("Error de conexión") }
    finally { setEnviandoAlumno(false) }
  }

  function mostrarMsg(msg) { setExito(msg); setTimeout(() => setExito(""), 3500) }

  const porCarrera = alumnos.reduce((acc, a) => { acc[a.carrera] = (acc[a.carrera] || 0) + 1; return acc }, {})
  const maxCarrera = Math.max(...Object.values(porCarrera), 1)

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
      <UserBar identificador={usuario.usuario} onLogout={onLogout} />

      <main className="fi-main">
        <SectionTitle>Panel de Administración</SectionTitle>

        {exito && <div className="fi-banner ok">{exito}</div>}
        {error && <div className="fi-banner error">{error}</div>}

        {/* ---------- RESUMEN ---------- */}
        {tab === "resumen" && (
          <div className="fi-stack">
            <div className="stats-row">
              <StatNum titulo="Total alumnos" valor={alumnos.length} />
              <StatNum titulo="Total empresas" valor={empresas.length} />
              <StatNum titulo="Alumnos asignados" valor={alumnos.filter(a => a.empresa).length} />
            </div>

            <section className="fi-panel">
              <div className="fi-panel-head">Alumnos por Carrera</div>
              <div className="fi-panel-body">
                {Object.keys(porCarrera).length === 0 ? <p className="muted">Sin datos aún.</p> : (
                  <div className="barras">
                    {Object.entries(porCarrera).sort((a, b) => b[1] - a[1]).map(([carrera, total]) => (
                      <div key={carrera}>
                        <div className="barra-lbl">
                          <span>{carrera}</span>
                          <span style={{ fontWeight: 700 }}>{total}</span>
                        </div>
                        <div className="fi-bar-track"><div className="fi-bar-fill" style={{ width: `${(total / maxCarrera) * 100}%` }} /></div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </section>

            <section className="fi-panel">
              <div className="fi-panel-head">Estado de Asignación</div>
              <div className="fi-panel-body">
                <div className="barras">
                  {[{ label: "Con empresa", valor: alumnos.filter(a => a.empresa).length }].map(({ label, valor }) => (
                    <div key={label}>
                      <div className="barra-lbl">
                        <span>{label}</span>
                        <span style={{ fontWeight: 700 }}>{valor}</span>
                      </div>
                      <div className="fi-bar-track">
                        <div className="fi-bar-fill" style={{ width: alumnos.length ? `${(valor / alumnos.length) * 100}%` : "0%", background: "var(--ok)" }} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </section>
          </div>
        )}

        {/* ---------- ALUMNOS ---------- */}
        {tab === "alumnos" && (
          <div className="fi-stack">
            <div style={{ display: "flex", justifyContent: "flex-end" }}>
              <button className="fi-btn" onClick={() => setMostrarFormAlumno(v => !v)}>
                {mostrarFormAlumno ? "Cancelar" : "+ Registrar alumno"}
              </button>
            </div>

            {mostrarFormAlumno && (
              <section className="fi-panel">
                <div className="fi-panel-head">Nuevo Alumno</div>
                <div className="fi-panel-body">
                  <form onSubmit={registrarAlumno} className="form-stack">
                    <div className="fi-form-grid">
                      <Campo label="Matrícula" value={formAlumno.matricula} onChange={v => setFormAlumno(f => ({ ...f, matricula: v }))} />
                      <Campo label="Usuario" value={formAlumno.usuario} onChange={v => setFormAlumno(f => ({ ...f, usuario: v }))} />
                      <Campo label="Contraseña" type="password" value={formAlumno.contrasena} onChange={v => setFormAlumno(f => ({ ...f, contrasena: v }))} />
                      <Campo label="Nombre" value={formAlumno.nombre} onChange={v => setFormAlumno(f => ({ ...f, nombre: v }))} />
                      <Campo label="Apellido paterno" value={formAlumno.apellidoPaterno} onChange={v => setFormAlumno(f => ({ ...f, apellidoPaterno: v }))} />
                      <Campo label="Apellido materno (opcional)" value={formAlumno.apellidoMaterno} onChange={v => setFormAlumno(f => ({ ...f, apellidoMaterno: v }))} required={false} />
                      <Campo label="Carrera" value={formAlumno.carrera} onChange={v => setFormAlumno(f => ({ ...f, carrera: v }))} />
                      <Campo label="Semestre" type="number" value={formAlumno.semestre} onChange={v => setFormAlumno(f => ({ ...f, semestre: v }))} />
                      <div className="fi-field">
                        <label>Empresa (opcional)</label>
                        <select value={formAlumno.empresaId} onChange={e => setFormAlumno(f => ({ ...f, empresaId: e.target.value }))} className="fi-select">
                          <option value="">Sin asignar</option>
                          {empresas.map(emp => <option key={emp.empresaId} value={emp.empresaId}>{emp.nombre}</option>)}
                        </select>
                      </div>
                    </div>
                    <button className="fi-btn" type="submit" disabled={enviandoAlumno} style={{ alignSelf: "flex-start" }}>
                      {enviandoAlumno ? "Registrando…" : "Registrar alumno"}
                    </button>
                  </form>
                </div>
              </section>
            )}

            <section className="fi-panel">
              <div className="fi-panel-head">Lista de Alumnos ({alumnos.length})</div>
              <div className="fi-panel-body">
                {alumnos.length === 0 ? <p className="muted">No hay alumnos registrados.</p> : (
                  <div style={{ overflowX: "auto" }}>
                    <table className="fi-table">
                      <thead><tr>{["Matrícula", "Nombre", "Carrera", "Semestre", "Empresa", "Acción"].map(h => <th key={h}>{h}</th>)}</tr></thead>
                      <tbody>
                        {alumnos.map(a => (
                          <tr key={a.alumnoId}>
                            <td><code>{a.matricula}</code></td>
                            <td>{a.nombre} {a.apellidoPaterno}</td>
                            <td>{a.carrera}</td>
                            <td>{a.semestre}</td>
                            <td>{a.empresa ?? <span style={{ color: "var(--warn)", fontWeight: 600 }}>Sin asignar</span>}</td>
                            <td><button className="fi-btn-danger" onClick={() => darDeBaja(a.alumnoId, `${a.nombre} ${a.apellidoPaterno}`)}>Dar de baja</button></td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </section>
          </div>
        )}

        {/* ---------- EMPRESAS ---------- */}
        {tab === "empresas" && (
          <div className="fi-stack">
            <section className="fi-panel">
              <div className="fi-panel-head">Registrar Nueva Empresa</div>
              <div className="fi-panel-body">
                <form onSubmit={registrarEmpresa} className="form-stack">
                  <div className="fi-form-grid">
                    <Campo label="Nombre" value={formEmpresa.nombre} onChange={v => setFormEmpresa(f => ({ ...f, nombre: v }))} />
                    <Campo label="Dirección" value={formEmpresa.direccion} onChange={v => setFormEmpresa(f => ({ ...f, direccion: v }))} />
                    <Campo label="Teléfono" value={formEmpresa.telefono} onChange={v => setFormEmpresa(f => ({ ...f, telefono: v }))} />
                    <Campo label="Correo" type="email" value={formEmpresa.correo} onChange={v => setFormEmpresa(f => ({ ...f, correo: v }))} />
                    <Campo label="Folio de registro" value={formEmpresa.folioRegistro} onChange={v => setFormEmpresa(f => ({ ...f, folioRegistro: v }))} />
                  </div>
                  <button className="fi-btn" type="submit" disabled={enviandoEmpresa} style={{ alignSelf: "flex-start" }}>
                    {enviandoEmpresa ? "Registrando…" : "Registrar empresa"}
                  </button>
                </form>
              </div>
            </section>

            <section className="fi-panel">
              <div className="fi-panel-head">Empresas Registradas ({empresas.length})</div>
              <div className="fi-panel-body">
                {empresas.length === 0 ? <p className="muted">No hay empresas.</p> : (
                  <div className="fi-grid-cards">
                    {empresas.map(emp => (
                      <div key={emp.empresaId} className="fi-mini-card">
                        <strong style={{ color: "var(--text-h)", display: "block", marginBottom: 6 }}>{emp.nombre}</strong>
                        <p className="muted">{emp.direccion}</p>
                        <p className="muted">{emp.telefono}</p>
                        <p className="muted">{emp.correo}</p>
                        <p className="muted" style={{ fontFamily: "var(--mono)", fontSize: "0.72rem", marginTop: 6 }}>{emp.folioRegistro}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </section>
          </div>
        )}
      </main>

      <style>{`
        .stats-row { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 16px; }
        .barras { display: flex; flex-direction: column; gap: 16px; }
        .barra-lbl { display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 0.9rem; color: var(--text-h); }
        .form-stack { display: flex; flex-direction: column; gap: 18px; }
        .muted { color: var(--text-muted); font-size: 0.9rem; margin: 3px 0; }
      `}</style>
    </div>
  )
}

function StatNum({ titulo, valor }) {
  return (
    <div className="fi-stat">
      <div className="num">{valor}</div>
      <div className="lbl">{titulo}</div>
    </div>
  )
}

function Campo({ label, value, onChange, type = "text", required = true }) {
  return (
    <div className="fi-field">
      <label>{label}</label>
      <input type={type} value={value} onChange={e => onChange(e.target.value)} required={required} className="fi-input" />
    </div>
  )
}
