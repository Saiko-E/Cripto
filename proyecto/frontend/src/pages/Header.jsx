import escudoUNAM from '../assets/escudoUNAM.png'
import escudoFI from '../assets/escudoFI.png'

// Encabezado institucional reutilizable (estilo Facultad de Ingeniería)
export function TopBar() {
  return (
    <header className="fi-topbar">
      <div className="fi-brand">
        <div className="escudos">
          <img src={escudoUNAM} alt="Escudo UNAM" className="escudo" />
          <img src={escudoFI} alt="Escudo Facultad de Ingeniería" className="escudo" />
        </div>
        <div className="brand-text">
          <div className="linea1">Facultad de</div>
          <div className="linea2">Ingeniería</div>
        </div>
      </div>

      <div className="fi-sysname">
        <div className="l1">Sistema de</div>
        <div className="l2">Servicio Social</div>
      </div>
    </header>
  )
}

// Barra de navegación con pestañas. `items` = [{ id, label }], `activo`, `onSelect`.
export function NavBar({ items = [], activo, onSelect }) {
  return (
    <nav className="fi-nav">
      <button className="nav-home" title="Inicio" onClick={() => items[0] && onSelect(items[0].id)}>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 3 2 12h3v8h6v-5h2v5h6v-8h3z" />
        </svg>
      </button>
      {items.map(it => (
        <button
          key={it.id}
          className={activo === it.id ? 'activo' : ''}
          onClick={() => onSelect(it.id)}
        >
          {it.label}
        </button>
      ))}
    </nav>
  )
}

// Barra de usuario: matrícula/usuario + botón cerrar sesión
export function UserBar({ identificador, onLogout }) {
  return (
    <div className="fi-userbar">
      <span className="uid">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 12a5 5 0 1 0 0-10 5 5 0 0 0 0 10Zm0 2c-5 0-9 2.5-9 5.5V22h18v-2.5c0-3-4-5.5-9-5.5Z" />
        </svg>
        {identificador}
      </span>
      <button className="btn-cerrar" onClick={onLogout}>Cerrar Sesión</button>
    </div>
  )
}

// Título de sección centrado con regla roja (como "Proceso de inscripción 2026-2")
export function SectionTitle({ children }) {
  return (
    <>
      <h1 className="fi-section-title">{children}</h1>
      <hr className="fi-rule" />
    </>
  )
}

// Verificación verde (paloma de "Realizado")
export function CheckMark() {
  return (
    <span className="fi-check">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
        <path d="M5 13l4 4L19 7" />
      </svg>
    </span>
  )
}
