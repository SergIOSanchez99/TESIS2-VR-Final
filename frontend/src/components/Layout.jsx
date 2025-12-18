import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import axios from 'axios'

const Layout = ({ children }) => {
  const navigate = useNavigate()
  const [user, setUser] = React.useState(null)

  React.useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    try {
      const response = await axios.get('/api/auth/paciente', {
        withCredentials: true
      })
      if (response.data.success) {
        setUser(response.data.paciente)
      }
    } catch (error) {
      setUser(null)
    }
  }

  const handleLogout = async () => {
    try {
      await axios.post('/api/auth/logout', {}, {
        withCredentials: true
      })
      setUser(null)
      navigate('/')
    } catch (error) {
      console.error('Error al cerrar sesión:', error)
    }
  }

  return (
    <>
      {/* Navbar */}
      <nav className="navbar navbar-expand-lg navbar-light bg-white shadow-sm" style={{ backgroundColor: 'white !important' }}>
        <div className="container">
          <Link className="navbar-brand rehavr-logo" to="/">
            <span className="logo-icon">
              <span className="logo-h">H</span>
            </span>
            RehaVR
          </Link>

          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              {user ? (
                <>
                  <li className="nav-item">
                    <span className="nav-link">
                      <i className="fas fa-user me-1"></i>{user.nombre}
                    </span>
                  </li>
                  <li className="nav-item">
                    <Link className="nav-link" to="/dashboard">
                      <i className="fas fa-tachometer-alt me-1"></i>Dashboard
                    </Link>
                  </li>
                  <li className="nav-item">
                    <button className="nav-link btn btn-link text-decoration-none p-0" onClick={handleLogout}>
                      <i className="fas fa-sign-out-alt me-1"></i>Cerrar Sesión
                    </button>
                  </li>
                </>
              ) : null}
            </ul>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main>{children}</main>

      {/* Footer */}
      <footer className="bg-dark text-white text-center py-4 mt-5">
        <div className="container">
          <p className="mb-0">
            <i className="fas fa-heartbeat me-2"></i>
            Sistema de Rehabilitación Motora - RehaVR
          </p>
        </div>
      </footer>
    </>
  )
}

export default Layout

