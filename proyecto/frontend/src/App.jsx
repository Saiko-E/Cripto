import { useState } from 'react'
import Login from './pages/Login'
import VistaAlumno from './pages/VistaAlumno'
import DashboardAdmin from './pages/DashboardAdmin'

function App() {
  const [usuario, setUsuario] = useState(null)

  if (!usuario) return <Login onLogin={setUsuario} />

  if (usuario.rol === 'Alumno')
    return <VistaAlumno usuario={usuario} onLogout={() => setUsuario(null)} />

  return <DashboardAdmin usuario={usuario} onLogout={() => setUsuario(null)} />
}

export default App
