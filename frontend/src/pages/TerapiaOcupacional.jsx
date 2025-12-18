import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import axios from 'axios'

const TerapiaOcupacional = () => {
  const navigate = useNavigate()
  const [ejercicios, setEjercicios] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadEjercicios()
  }, [])

  const loadEjercicios = async () => {
    try {
      const response = await axios.get('/api/ejercicios/', { withCredentials: true })
      if (response.data.success) {
        const terapiaEjercicios = response.data.ejercicios.filter(
          e => e.tipo === 'terapia_ocupacional'
        )
        setEjercicios(terapiaEjercicios)
      }
    } catch (error) {
      console.error('Error al cargar ejercicios:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="container py-5 text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
      </div>
    )
  }

  // Configuración de iconos y colores para cada ejercicio
  const ejercicioConfig = {
    'terapia_abotonar_camisa': { icon: 'fa-tshirt', color: '#1976d2', btnColor: '#1976d2' },
    'terapia_arrastrar_objeto': { icon: 'fa-hand-paper', color: '#43a047', btnColor: '#43a047' },
    'terapia_abrir_cerradura': { icon: 'fa-key', color: '#ffc107', btnColor: '#ff9800' },
    'terapia_usar_cubiertos': { icon: 'fa-utensils', color: '#03a9f4', btnColor: '#03a9f4' },
    'terapia_rompecabezas': { icon: 'fa-puzzle-piece', color: '#e91e63', btnColor: '#e91e63' },
    'terapia_clasificar_objetos': { icon: 'fa-layer-group', color: '#9c27b0', btnColor: '#9c27b0' }
  }

  const getEjercicioConfig = (id) => {
    return ejercicioConfig[id] || { icon: 'fa-hands-helping', color: '#666', btnColor: '#666' }
  }

  return (
    <div style={{ backgroundColor: '#9c27b0', minHeight: '100vh', paddingTop: '2rem', paddingBottom: '2rem' }}>
      <div className="container py-4">
        <div className="row mb-4">
          <div className="col-12">
            <div className="card shadow-lg" style={{ borderRadius: '15px', border: 'none' }}>
              <div className="card-body text-center py-4">
                <h2 className="mb-3" style={{ fontSize: '2rem', fontWeight: 'bold', color: '#333' }}>
                  Terapia Ocupacional
                </h2>
                <p className="lead text-muted mb-0" style={{ fontSize: '1.1rem' }}>
                  Ejercicios específicos para mejorar las actividades de la vida
                  diaria y aumentar la independencia funcional.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="row g-4">
          {ejercicios.map((ejercicio) => {
            const config = getEjercicioConfig(ejercicio.id)
            return (
              <div key={ejercicio.id} className="col-md-4">
                <div className="card h-100 shadow-lg" style={{ 
                  borderRadius: '15px', 
                  transition: 'transform 0.3s ease',
                  border: 'none'
                }}
                onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-5px)'}
                onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}
                >
                  <div className="card-body text-center py-4">
                    <div className="mb-3">
                      <i className={`fas ${config.icon} fa-3x`} style={{ color: config.color }}></i>
                    </div>
                    <h5 className="card-title mb-3" style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#333' }}>
                      {ejercicio.nombre}
                    </h5>
                    <p className="card-text text-muted mb-4" style={{ fontSize: '0.95rem', minHeight: '60px' }}>
                      {ejercicio.descripcion}
                    </p>
                    <Link
                      to={`/ejercicio/${ejercicio.id}`}
                      className="btn btn-lg"
                      style={{ 
                        backgroundColor: config.btnColor, 
                        color: 'white',
                        border: 'none',
                        borderRadius: '25px', 
                        padding: '10px 30px',
                        fontWeight: '600'
                      }}
                    >
                      <i className="fas fa-play me-2"></i>Comenzar
                    </Link>
                  </div>
                </div>
              </div>
            )
          })}
        </div>

        <div className="text-center mt-4">
          <Link
            to="/dashboard"
            className="btn btn-outline-light btn-lg"
            style={{ borderRadius: '25px', padding: '10px 30px', borderWidth: '2px' }}
          >
            <i className="fas fa-arrow-left me-2"></i>Volver al Dashboard
          </Link>
        </div>
      </div>
    </div>
  )
}

export default TerapiaOcupacional

