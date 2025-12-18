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
      <section className="py-5 bg-light">
        <div className="container">
          <div className="row text-center mb-5">
            <div className="col-12">
              <h2 className="display-5 fw-bold text-primary">¿Cómo Funciona?</h2>
              <p className="lead text-muted">
                Sigue estos simples pasos para comenzar tu rehabilitación
              </p>
            </div>
          </div>

          <div className="row g-4">
            <div className="col-md-3 text-center">
              <div className="mb-3">
                <div className="progress-circle bg-primary">1</div>
              </div>
              <h5>Regístrate</h5>
              <p className="text-muted">
                Crea tu cuenta de paciente de forma rápida y segura
              </p>
            </div>

            <div className="col-md-3 text-center">
              <div className="mb-3">
                <div className="progress-circle bg-primary">2</div>
              </div>
              <h5>Selecciona Ejercicios</h5>
              <p className="text-muted">
                Elige el nivel de dificultad que mejor se adapte a ti
              </p>
            </div>

            <div className="col-md-3 text-center">
              <div className="mb-3">
                <div className="progress-circle bg-primary">3</div>
              </div>
              <h5>Realiza Ejercicios</h5>
              <p className="text-muted">
                Completa los ejercicios interactivos con tu mouse
              </p>
            </div>

            <div className="col-md-3 text-center">
              <div className="mb-3">
                <div className="progress-circle bg-primary">4</div>
              </div>
              <h5>Monitorea Progreso</h5>
              <p className="text-muted">Revisa tu evolución y mejora continua</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-5">
        <div className="container">
          <div className="row justify-content-center">
            <div className="col-lg-8 text-center">
              <h2 className="display-6 fw-bold text-primary mb-4">
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

