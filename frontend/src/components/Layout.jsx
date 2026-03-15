import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import axios from 'axios'
import { useTheme } from '../context/ThemeContext'

const Layout = ({ children }) => {
  const navigate = useNavigate()
  const { theme, toggle } = useTheme()
  const [user, setUser] = React.useState(null)

  React.useEffect(() => { checkAuth() }, [])

  const checkAuth = async () => {
    try {
      const res = await axios.get('/api/auth/paciente', { withCredentials: true })
      if (res.data.success) setUser(res.data.paciente)
    } catch {
      setUser(null)
    }
  }

  const handleLogout = async () => {
    try {
      await axios.post('/api/auth/logout', {}, { withCredentials: true })
      setUser(null)
      navigate('/')
    } catch (err) {
      console.error('Error al cerrar sesión:', err)
    }
  }

  return (
    <>
      {/* ─── Navbar ─── */}
      <nav className="navbar navbar-expand-lg layout-navbar">
        <div className="container">
          {/* Logo */}
          <Link className="navbar-brand rehavr-logo" to="/">
            <span style={{ marginRight: 8, fontSize: '1.4rem' }}>⚕</span>
            RehaVR
          </Link>

          {/* Hamburguesa (mobile) */}
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto align-items-center gap-1">

              {user && (
                <>
                  <li className="nav-item">
                    <span className="nav-link" style={{ fontWeight: 600 }}>
                      <i className="fas fa-user-circle me-1" style={{ color: 'var(--rv-cyan)' }}></i>
                      {user.nombre || user.paciente?.nombre || 'Paciente'}
                    </span>
                  </li>

                  <li className="nav-item">
                    <Link className="nav-link" to="/dashboard">
                      <i className="fas fa-th-large me-1"></i>Dashboard
                    </Link>
                  </li>

                  <li className="nav-item">
                    <button
                      className="nav-link btn btn-link text-decoration-none p-0"
                      onClick={handleLogout}
                      style={{ border: 'none', background: 'none' }}
                    >
                      <i className="fas fa-sign-out-alt me-1"></i>Salir
                    </button>
                  </li>
                </>
              )}

              {/* ─── Toggle de tema ─── */}
              <li className="nav-item ms-2">
                <button
                  className="rv-theme-toggle"
                  onClick={toggle}
                  title={theme === 'dark' ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'}
                  aria-label="Cambiar tema"
                >
                  {theme === 'dark'
                    ? <i className="fas fa-sun"></i>
                    : <i className="fas fa-moon"></i>
                  }
                </button>
              </li>

            </ul>
          </div>
        </div>
      </nav>

      {/* ─── Contenido principal ─── */}
      <main>{children}</main>

      {/* ─── Footer ─── */}
      <footer className="layout-footer text-center py-4 mt-5">
        <div className="container">
          <p className="mb-0" style={{ fontSize: '0.85rem' }}>
            <i className="fas fa-heartbeat me-2" style={{ color: 'var(--rv-cyan)' }}></i>
            RehaVR — Sistema de Rehabilitación Motora Virtual
          </p>
        </div>
      </footer>
    </>
  )
}

export default Layout
