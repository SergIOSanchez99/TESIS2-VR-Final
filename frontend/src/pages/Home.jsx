import React from 'react'
import { Link } from 'react-router-dom'

const Home = () => {
  return (
    <>
      <section className="hero-section bg-primary text-white py-5">
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
              <img 
                src="https://images.unsplash.com/photo-1593508512255-86ab42a8e620?w=600&h=600&fit=crop&q=80" 
                alt="Realidad Virtual para Rehabilitación" 
                className="img-fluid rounded-3 shadow-lg"
                style={{ maxWidth: '100%', height: 'auto', borderRadius: '15px' }}
                onError={(e) => {
                  // Si la imagen falla, usar un placeholder
                  e.target.src = 'https://via.placeholder.com/600x400/667eea/ffffff?text=VR+Rehabilitación'
                }}
              />
            </div>
          </div>
        </div>
      </section>

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
    </>
  )
}

export default Home

