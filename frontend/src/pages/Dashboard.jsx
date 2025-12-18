import React, { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import axios from 'axios'

const Dashboard = () => {
  const navigate = useNavigate()
  const [paciente, setPaciente] = useState(null)
  const [historial, setHistorial] = useState([])
  const [ejercicios, setEjercicios] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [pacienteRes, historialRes, ejerciciosRes] = await Promise.all([
        axios.get('/api/auth/paciente', { withCredentials: true }),
        axios.get('/api/ejercicios/historial', { withCredentials: true }),
        axios.get('/api/ejercicios/', { withCredentials: true })
      ])

      if (pacienteRes.data.success) {
        const pacienteData = pacienteRes.data.paciente?.paciente || pacienteRes.data.paciente
        setPaciente(pacienteData)
      } else {
        navigate('/login')
      }

      if (historialRes.data.success) {
        setHistorial(historialRes.data.historial || [])
      }

      if (ejerciciosRes.data.success) {
        setEjercicios(ejerciciosRes.data.ejercicios || [])
      }
    } catch (error) {
      console.error('Error al cargar datos:', error)
      if (error.response?.status === 401) {
        navigate('/login')
      }
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

  const ejerciciosExitosos = historial.filter(h => h.exito).length
  const porcentajeProgreso = historial.length > 0 
    ? Math.round((ejerciciosExitosos / historial.length) * 100 * 10) / 10 
    : 0

  const handleLogout = async () => {
    try {
      await axios.post('/api/auth/logout', {}, {
        withCredentials: true
      })
      navigate('/')
    } catch (error) {
      console.error('Error al cerrar sesión:', error)
      // Redirigir de todas formas
      navigate('/')
    }
  }

  return (
    <div style={{ 
      background: 'linear-gradient(135deg, #4a90e2 0%, #357abd 25%, #2e5c8a 50%, #357abd 75%, #4a90e2 100%)',
      minHeight: '100vh', 
      paddingTop: '2rem', 
      paddingBottom: '3rem',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Efecto de estrellas decorativo */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundImage: `
          radial-gradient(2px 2px at 20% 30%, rgba(255,255,255,0.8), transparent),
          radial-gradient(2px 2px at 60% 70%, rgba(255,255,255,0.8), transparent),
          radial-gradient(1px 1px at 50% 50%, rgba(255,255,255,0.6), transparent),
          radial-gradient(1px 1px at 80% 10%, rgba(255,255,255,0.7), transparent),
          radial-gradient(2px 2px at 90% 60%, rgba(255,255,255,0.8), transparent),
          radial-gradient(1px 1px at 33% 80%, rgba(255,255,255,0.6), transparent),
          radial-gradient(2px 2px at 10% 50%, rgba(255,255,255,0.7), transparent),
          radial-gradient(1px 1px at 70% 20%, rgba(255,255,255,0.6), transparent),
          radial-gradient(1px 1px at 40% 60%, rgba(255,255,255,0.5), transparent),
          radial-gradient(2px 2px at 15% 80%, rgba(255,255,255,0.7), transparent)
        `,
        backgroundSize: '200% 200%',
        opacity: 0.4,
        animation: 'twinkle 15s ease-in-out infinite',
        pointerEvents: 'none'
      }}></div>
      <div className="container py-4" style={{ position: 'relative', zIndex: 1 }}>
      {/* Header */}
      <div className="row mb-4">
        <div className="col-12">
          <div className="card shadow-lg" style={{ 
            border: 'none', 
            borderRadius: '20px', 
            boxShadow: '0 8px 24px rgba(0, 0, 0, 0.15)',
            background: 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)'
          }}>
            <div className="card-body p-4">
              <div className="row align-items-center">
                <div className="col-md-7">
                  <h2 className="mb-2" style={{ fontSize: '2rem', fontWeight: 'bold', color: '#333' }}>
                    <i className="fas fa-user-circle me-2 text-primary"></i>
                    Bienvenido/a, {paciente?.nombre || 'Usuario'}
                  </h2>
                  {paciente?.edad && (
                    <p className="text-muted mb-0" style={{ fontSize: '1.1rem' }}>
                      <i className="fas fa-birthday-cake me-2"></i>
                      Edad: {paciente.edad} años
                    </p>
                  )}
                </div>
                <div className="col-md-3 text-center">
                  <div className="progress-circle bg-primary shadow-lg" style={{ 
                    width: '110px', 
                    height: '110px', 
                    fontSize: '3rem', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center',
                    margin: '0 auto'
                  }}>
                    <span className="rehavr-logo" style={{ color: 'white', fontSize: '3rem' }}>
                      <span className="logo-icon" style={{ fontSize: '3rem' }}>
                        <span className="logo-h" style={{ color: 'white' }}>H</span>
                      </span>
                    </span>
                  </div>
                </div>
                <div className="col-md-2 text-end">
                  <button
                    onClick={handleLogout}
                    className="btn btn-outline-danger"
                    style={{
                      borderRadius: '25px',
                      padding: '10px 20px',
                      fontWeight: '600',
                      borderWidth: '2px',
                      transition: 'all 0.3s ease'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.transform = 'translateY(-2px)'
                      e.currentTarget.style.boxShadow = '0 4px 8px rgba(220, 53, 69, 0.3)'
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.transform = 'translateY(0)'
                      e.currentTarget.style.boxShadow = 'none'
                    }}
                  >
                    <i className="fas fa-sign-out-alt me-2"></i>
                    Cerrar Sesión
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Statistics */}
      <div className="row mb-5 g-4">
        <div className="col-md-4">
          <div className="card text-center shadow-lg h-100" style={{ 
            border: 'none', 
            borderRadius: '20px', 
            boxShadow: '0 6px 20px rgba(0, 0, 0, 0.12)',
            transition: 'transform 0.3s ease, box-shadow 0.3s ease',
            background: 'white'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-8px)'
            e.currentTarget.style.boxShadow = '0 12px 28px rgba(25, 118, 210, 0.2)'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)'
            e.currentTarget.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.12)'
          }}
          >
            <div className="card-body p-4">
              <div className="mb-3">
                <div style={{
                  width: '70px',
                  height: '70px',
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto',
                  boxShadow: '0 4px 12px rgba(25, 118, 210, 0.3)'
                }}>
                  <i className="fas fa-gamepad fa-2x text-white"></i>
                </div>
              </div>
              <h5 className="card-title mb-2" style={{ fontSize: '1rem', fontWeight: '600', color: '#666' }}>Ejercicios Completados</h5>
              <h3 className="text-primary mb-0" style={{ fontSize: '3rem', fontWeight: 'bold' }}>{historial.length}</h3>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card text-center shadow-lg h-100" style={{ 
            border: 'none', 
            borderRadius: '20px', 
            boxShadow: '0 6px 20px rgba(0, 0, 0, 0.12)',
            transition: 'transform 0.3s ease, box-shadow 0.3s ease',
            background: 'white'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-8px)'
            e.currentTarget.style.boxShadow = '0 12px 28px rgba(67, 160, 71, 0.2)'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)'
            e.currentTarget.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.12)'
          }}
          >
            <div className="card-body p-4">
              <div className="mb-3">
                <div style={{
                  width: '70px',
                  height: '70px',
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #43a047 0%, #2e7d32 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto',
                  boxShadow: '0 4px 12px rgba(67, 160, 71, 0.3)'
                }}>
                  <i className="fas fa-trophy fa-2x text-white"></i>
                </div>
              </div>
              <h5 className="card-title mb-2" style={{ fontSize: '1rem', fontWeight: '600', color: '#666' }}>Éxitos</h5>
              <h3 className="text-success mb-0" style={{ fontSize: '3rem', fontWeight: 'bold' }}>{ejerciciosExitosos}</h3>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card text-center shadow-lg h-100" style={{ 
            border: 'none', 
            borderRadius: '20px', 
            boxShadow: '0 6px 20px rgba(0, 0, 0, 0.12)',
            transition: 'transform 0.3s ease, box-shadow 0.3s ease',
            background: 'white'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-8px)'
            e.currentTarget.style.boxShadow = '0 12px 28px rgba(3, 169, 244, 0.2)'
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)'
            e.currentTarget.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.12)'
          }}
          >
            <div className="card-body p-4">
              <div className="mb-3">
                <div style={{
                  width: '70px',
                  height: '70px',
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #03a9f4 0%, #0277bd 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto',
                  boxShadow: '0 4px 12px rgba(3, 169, 244, 0.3)'
                }}>
                  <i className="fas fa-chart-line fa-2x text-white"></i>
                </div>
              </div>
              <h5 className="card-title mb-2" style={{ fontSize: '1rem', fontWeight: '600', color: '#666' }}>Progreso</h5>
              <h3 className="text-info mb-0" style={{ fontSize: '3rem', fontWeight: 'bold' }}>{porcentajeProgreso}%</h3>
            </div>
          </div>
        </div>
      </div>

      {/* Exercise Options - Rehabilitación */}
      {ejercicios.filter(e => e.tipo === 'rehabilitacion').length > 0 && (
        <div className="row mb-5">
          <div className="col-12">
            <div className="mb-4">
              <h3 className="text-white mb-3" style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>
                <i className="fas fa-dumbbell me-2"></i>Ejercicios de Rehabilitación
              </h3>
            </div>
            <div className="row g-4">
              {ejercicios
                .filter(e => e.tipo === 'rehabilitacion')
                .sort((a, b) => a.nivel - b.nivel)
                .map((ejercicio) => {
                  const nivelNum = ejercicio.nivel || 1
                  const iconos = {
                    1: 'fa-bullseye',
                    2: 'fa-running',
                    3: 'fa-bolt'
                  }
                  const descripciones = {
                    1: 'Objetivo estático - Ideal para principiantes',
                    2: 'Objetivo se mueve lento - Nivel intermedio',
                    3: 'Objetivo se mueve rápido - Nivel avanzado'
                  }
                  return (
                    <div key={ejercicio.id} className="col-md-4">
                      <div className="card h-100 shadow-lg" style={{ 
                        border: 'none', 
                        borderRadius: '20px', 
                        boxShadow: '0 6px 20px rgba(0, 0, 0, 0.12)',
                        transition: 'transform 0.3s ease, box-shadow 0.3s ease',
                        cursor: 'pointer',
                        background: 'white'
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'translateY(-10px)'
                        e.currentTarget.style.boxShadow = '0 12px 32px rgba(25, 118, 210, 0.25)'
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'translateY(0)'
                        e.currentTarget.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.12)'
                      }}
                      >
                        <div className="card-body p-4">
                          <div className="mb-3">
                            <div style={{
                              width: '60px',
                              height: '60px',
                              borderRadius: '15px',
                              background: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              boxShadow: '0 4px 12px rgba(25, 118, 210, 0.3)'
                            }}>
                              <i className={`fas ${iconos[nivelNum] || 'fa-gamepad'} fa-2x text-white`}></i>
                            </div>
                          </div>
                          <h5 className="text-primary mb-3" style={{ fontSize: '1.3rem', fontWeight: 'bold' }}>
                            Nivel {nivelNum}
                          </h5>
                          <p className="text-muted mb-4" style={{ fontSize: '1rem', minHeight: '50px' }}>
                            {descripciones[nivelNum] || ejercicio.descripcion}
                          </p>
                          <Link 
                            to={`/ejercicio/${ejercicio.id}`} 
                            className="btn btn-primary w-100"
                            style={{ borderRadius: '25px', padding: '12px', fontWeight: '600', fontSize: '1rem' }}
                          >
                            <i className="fas fa-play me-2"></i>Comenzar
                          </Link>
                        </div>
                      </div>
                    </div>
                  )
                })}
            </div>
          </div>
        </div>
      )}

      {/* Exercise Options - Terapia Ocupacional */}
      <div className="row mb-5">
        <div className="col-12">
          <div className="mb-4">
            <h3 className="text-white mb-3" style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>
              <i className="fas fa-hands-helping me-2"></i>Terapia Ocupacional
            </h3>
          </div>
          <div className="row">
            <div className="col-md-4">
              <Link to="/terapia-ocupacional" style={{ textDecoration: 'none' }}>
                <div className="card h-100 shadow-lg" style={{ 
                  border: 'none', 
                  borderRadius: '20px', 
                  boxShadow: '0 6px 20px rgba(0, 0, 0, 0.12)',
                  transition: 'transform 0.3s ease, box-shadow 0.3s ease',
                  cursor: 'pointer',
                  background: 'white'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-10px)'
                  e.currentTarget.style.boxShadow = '0 12px 32px rgba(255, 152, 0, 0.3)'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)'
                  e.currentTarget.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.12)'
                }}
                >
                  <div className="card-body p-4 text-center">
                    <div className="mb-3">
                      <div style={{
                        width: '80px',
                        height: '80px',
                        borderRadius: '20px',
                        background: 'linear-gradient(135deg, #ff9800 0%, #f57c00 100%)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        margin: '0 auto',
                        boxShadow: '0 4px 16px rgba(255, 152, 0, 0.4)'
                      }}>
                        <i className="fas fa-hands-helping fa-3x text-white"></i>
                      </div>
                    </div>
                    <h5 className="mb-3" style={{ fontSize: '1.4rem', fontWeight: 'bold', color: '#333' }}>
                      Terapia Ocupacional
                    </h5>
                    <p className="text-muted mb-4" style={{ fontSize: '1rem' }}>
                      Ejercicios para actividades diarias
                    </p>
                    <div className="btn w-100"
                      style={{ 
                        backgroundColor: '#ff9800', 
                        color: 'white',
                        border: 'none',
                        borderRadius: '25px', 
                        padding: '12px', 
                        fontWeight: '600',
                        fontSize: '1rem'
                      }}
                    >
                      <i className="fas fa-arrow-right me-2"></i>Ver Ejercicios
                    </div>
                  </div>
                </div>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      {historial.length > 0 && (
        <div className="row">
          <div className="col-12">
            <div className="mb-4">
              <h3 className="text-white mb-3" style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>
                <i className="fas fa-history me-2"></i>Actividad Reciente
              </h3>
            </div>
            <div className="card shadow-lg" style={{ border: 'none', borderRadius: '20px' }}>
              <div className="card-body p-4">
                <div className="table-responsive">
                  <table className="table table-hover mb-0">
                    <thead>
                      <tr style={{ background: 'transparent' }}>
                        <th style={{ border: 'none', padding: '15px', color: '#666', fontWeight: '600' }}>Fecha</th>
                        <th style={{ border: 'none', padding: '15px', color: '#666', fontWeight: '600' }}>Ejercicio</th>
                        <th style={{ border: 'none', padding: '15px', color: '#666', fontWeight: '600' }}>Resultado</th>
                      </tr>
                    </thead>
                    <tbody>
                      {historial.slice(-5).reverse().map((actividad, index) => (
                        <tr key={index} style={{ borderBottom: '1px solid #f0f0f0' }}>
                          <td style={{ padding: '15px', verticalAlign: 'middle' }}>
                            {new Date(actividad.fecha_ejercicio || actividad.fecha).toLocaleDateString('es-ES', {
                              day: '2-digit',
                              month: 'short',
                              year: 'numeric'
                            })}
                          </td>
                          <td style={{ padding: '15px', verticalAlign: 'middle', fontWeight: '500' }}>
                            {actividad.nivel || actividad.ejercicio || 'N/A'}
                          </td>
                          <td style={{ padding: '15px', verticalAlign: 'middle' }}>
                            {actividad.exito ? (
                              <span className="badge" style={{ 
                                backgroundColor: '#43a047', 
                                padding: '8px 16px',
                                borderRadius: '20px',
                                fontSize: '0.9rem'
                              }}>
                                <i className="fas fa-check me-1"></i>Éxito
                              </span>
                            ) : (
                              <span className="badge" style={{ 
                                backgroundColor: '#ff9800', 
                                padding: '8px 16px',
                                borderRadius: '20px',
                                fontSize: '0.9rem'
                              }}>
                                <i className="fas fa-times me-1"></i>Necesita práctica
                              </span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
      </div>
    </div>
  )
}

export default Dashboard

