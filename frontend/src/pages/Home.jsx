import React from 'react'
import { Link } from 'react-router-dom'

const Home = () => {
  return (
    <>
      {/* Hero Section */}
      <section className="hero-section">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-lg-6">
              <h1 className="display-4 fw-bold mb-4">
                <i className="fas fa-dumbbell me-3"></i>
                Sistema de Rehabilitación Motora
              </h1>
              <p className="lead mb-4">
                Plataforma innovadora para ejercicios de rehabilitación motora con
                tecnología de realidad virtual y seguimiento personalizado.
              </p>
              <div className="d-flex gap-3">
                <Link to="/registro" className="btn btn-light btn-lg">
                  <i className="fas fa-user-plus me-2"></i>Registrarse
                </Link>
                <Link to="/login" className="btn btn-outline-light btn-lg">
                  <i className="fas fa-sign-in-alt me-2"></i>Iniciar Sesión
                </Link>
              </div>
            </div>
            <div className="col-lg-6 text-center">
              <div className="progress-circle bg-success">
                <i className="fas fa-heartbeat"></i>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-5">
        <div className="container">
          <div className="row text-center mb-5">
            <div className="col-12">
              <h2 className="display-5 fw-bold text-primary">
                Características Principales
              </h2>
              <p className="lead text-muted">
                Descubre las herramientas que te ayudarán en tu rehabilitación
              </p>
            </div>
          </div>

          <div className="row g-4">
            <div className="col-md-4">
              <div className="card feature-card h-100">
                <div className="card-body text-center">
                  <div className="mb-3">
                    <i className="fas fa-gamepad fa-3x text-primary"></i>
                  </div>
                  <h5 className="card-title">Ejercicios Interactivos</h5>
                  <p className="card-text">
                    Ejercicios gamificados con diferentes niveles de dificultad para
                    mejorar la coordinación y movilidad.
                  </p>
                </div>
              </div>
            </div>

            <div className="col-md-4">
              <div className="card feature-card h-100">
                <div className="card-body text-center">
                  <div className="mb-3">
                    <i className="fas fa-chart-line fa-3x text-success"></i>
                  </div>
                  <h5 className="card-title">Seguimiento de Progreso</h5>
                  <p className="card-text">
                    Monitorea tu evolución con gráficos detallados y estadísticas de
                    rendimiento personalizadas.
                  </p>
                </div>
              </div>
            </div>

            <div className="col-md-4">
              <div className="card feature-card h-100">
                <div className="card-body text-center">
                  <div className="mb-3">
                    <i className="fas fa-hands-helping fa-3x text-accent"></i>
                  </div>
                  <h5 className="card-title">Terapia Ocupacional</h5>
                  <p className="card-text">
                    Ejercicios específicos para actividades de la vida diaria y mejora
                    de la independencia funcional.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How it Works Section */}
      <section className="py-5" style={{ background: 'var(--rv-bg-2)' }}>
        <div className="container">
          <div className="row text-center mb-5">
            <div className="col-12">
              <h2 className="display-5 fw-bold" style={{ color: 'var(--rv-cyan)' }}>¿Cómo Funciona?</h2>
              <p className="lead" style={{ color: 'var(--rv-text-muted)' }}>
                Sigue estos simples pasos para comenzar tu rehabilitación
              </p>
            </div>
          </div>

          <div className="row g-4">
            {[
              { num: '1', titulo: 'Regístrate',          desc: 'Crea tu cuenta de paciente de forma rápida y segura' },
              { num: '2', titulo: 'Selecciona Ejercicios', desc: 'Elige el nivel de dificultad que mejor se adapte a ti' },
              { num: '3', titulo: 'Realiza Ejercicios',   desc: 'Completa los ejercicios interactivos con tu mouse' },
              { num: '4', titulo: 'Monitorea Progreso',   desc: 'Revisa tu evolución y mejora continua' },
            ].map(({ num, titulo, desc }) => (
              <div key={num} className="col-md-3 text-center">
                <div className="mb-3">
                  <div
                    className="progress-circle"
                    style={{
                      background: 'linear-gradient(135deg, var(--rv-cyan), #0077a8)',
                      boxShadow: '0 0 20px var(--rv-cyan-glow)',
                      color: '#fff',
                      fontSize: '1.4rem',
                      fontWeight: 800,
                    }}
                  >
                    {num}
                  </div>
                </div>
                <h5 style={{ color: 'var(--rv-text)', fontWeight: 700 }}>{titulo}</h5>
                <p style={{ color: 'var(--rv-text-muted)' }}>{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-5">
        <div className="container">
          <div className="row justify-content-center">
            <div className="col-lg-8 text-center">
              <h2 className="display-6 fw-bold mb-4" style={{ color: 'var(--rv-text)' }}>
                ¿Listo para comenzar tu rehabilitación?
              </h2>
              <p className="lead mb-4">
                Únete a nuestra comunidad de pacientes y comienza tu camino hacia la
                recuperación
              </p>
              <Link to="/registro" className="btn btn-primary btn-lg">
                <i className="fas fa-rocket me-2"></i>Comenzar Ahora
              </Link>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}

export default Home

