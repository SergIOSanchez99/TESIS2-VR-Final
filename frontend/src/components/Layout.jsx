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
    <div className="min-vh-100 d-flex flex-column">
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
        <div className="container">
          <Link className="navbar-brand" to="/">
            <i className="fas fa-dumbbell me-2"></i>
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
              {user && (
                <li className="nav-item">
                  <button className="btn btn-outline-light btn-sm" onClick={handleLogout}>
                    Cerrar Sesión
                  </button>
                </li>
              )}
            </ul>
          </div>
        </div>
      </nav>
      <main className="flex-grow-1">
        {children}
      </main>
      <footer className="bg-dark text-light py-4 mt-auto">
        <div className="container text-center">
          <p className="mb-0">&copy; 2024 RehaVR - Sistema de Rehabilitación Motora</p>
        </div>
      </footer>
    </div>
  )
}

export default Layout

