import React, { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import axios from 'axios'
import { useTheme } from '../context/ThemeContext'

/* Configuración visual por nivel de dificultad */
const LEVEL_CONFIG = {
  1: {
    icon: 'fa-crosshairs',
    label: 'Principiante',
    color: '#00b4d8',
    glow: 'rgba(0,180,216,0.4)',
    desc: 'Objetivo estático — Ideal para comenzar tu proceso de recuperación motora.',
  },
  2: {
    icon: 'fa-circle-notch',
    label: 'Intermedio',
    color: '#f9c74f',
    glow: 'rgba(249,199,79,0.4)',
    desc: 'Objetivo en movimiento lento — Incrementa tu coordinación y seguimiento visual.',
  },
  3: {
    icon: 'fa-bolt',
    label: 'Avanzado',
    color: '#f94144',
    glow: 'rgba(249,65,68,0.4)',
    desc: 'Objetivo rápido — Maximiza tu velocidad de reacción y precisión motora.',
  },
}

const OCC_ICONS = [
  'fa-tshirt', 'fa-utensils', 'fa-puzzle-piece',
  'fa-hand-paper', 'fa-lock', 'fa-sort-amount-up',
]

/* ── Subcomponente: Anillo de progreso SVG ── */
function StatRing({ value, max = 100, color }) {
  const pct = Math.min(Math.round((value / max) * 100), 100)
  return (
    <div className="rehavr-stat-ring">
      <svg viewBox="0 0 36 36">
        <path
          d="M18 2 a16 16 0 0 1 0 32 a16 16 0 0 1 0 -32"
          fill="none"
          stroke={`${color}22`}
          strokeWidth="3"
        />
        <path
          className="rehavr-ring-fill"
          d="M18 2 a16 16 0 0 1 0 32 a16 16 0 0 1 0 -32"
          fill="none"
          stroke={color}
          strokeWidth="3"
          strokeDasharray={`${pct} 100`}
          strokeLinecap="round"
        />
      </svg>
    </div>
  )
}

/* ── Subcomponente: Card de estadística ── */
function StatCard({ icon, value, label, iconBg, iconColor, ringColor, ringMax, delay }) {
  return (
    <div className="rehavr-stat-card rehavr-anim-fadein" style={{ animationDelay: delay }}>
      <div className="rehavr-stat-icon" style={{ background: iconBg, color: iconColor }}>
        <i className={`fas ${icon}`}></i>
      </div>
      <div className="rehavr-stat-content">
        <div className="rehavr-stat-value">{value}</div>
        <div className="rehavr-stat-label">{label}</div>
      </div>
      <StatRing value={Number(value) || 0} max={ringMax} color={ringColor} />
    </div>
  )
}

/* ── Subcomponente: Card de ejercicio de rehabilitación ── */
function RehabCard({ ejercicio, delay }) {
  const nivelNum = ejercicio.nivel || 1
  const cfg = LEVEL_CONFIG[nivelNum] || LEVEL_CONFIG[1]

  return (
    <div
      className="rehavr-exercise-card rehavr-anim-fadein"
      style={{ animationDelay: delay }}
    >
      <div className="rehavr-card-accent" style={{ background: cfg.color }} />
      <div className="rehavr-card-header">
        <div
          className="rehavr-card-icon"
          style={{
            color: cfg.color,
            boxShadow: `0 0 20px ${cfg.glow}`,
            border: `1px solid ${cfg.color}30`,
          }}
        >
          <i className={`fas ${cfg.icon}`}></i>
        </div>
        <span
          className="rehavr-level-badge"
          style={{
            background: `${cfg.color}20`,
            color: cfg.color,
            border: `1px solid ${cfg.color}50`,
          }}
        >
          {cfg.label}
        </span>
      </div>

      <h3 className="rehavr-card-title">Nivel {nivelNum}</h3>
      <p className="rehavr-card-desc">{cfg.desc}</p>

      <div className="rehavr-card-meta">
        <span><i className="fas fa-clock"></i> ~15 min</span>
        <span><i className="fas fa-redo"></i> Repetible</span>
      </div>

      <Link
        to={`/ejercicio/${ejercicio.id}`}
        className="rehavr-btn-primary"
        style={{ '--btn-color': cfg.color, '--btn-glow': cfg.glow }}
      >
        <i className="fas fa-play-circle"></i>
        Iniciar Sesión
      </Link>
    </div>
  )
}

/* ════════════════════════════════════════
   COMPONENTE PRINCIPAL — Dashboard
   ════════════════════════════════════════ */
export default function Dashboard() {
  const navigate = useNavigate()
  const { theme, toggle } = useTheme()
  const [paciente, setPaciente]   = useState(null)
  const [historial, setHistorial] = useState([])
  const [ejercicios, setEjercicios] = useState([])
  const [loading, setLoading]     = useState(true)
  const [currentTime, setCurrentTime] = useState(new Date())

  /* Reloj en tiempo real */
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000)
    return () => clearInterval(timer)
  }, [])

  useEffect(() => { loadData() }, [])

  const loadData = async () => {
    try {
      const [pacienteRes, historialRes, ejerciciosRes] = await Promise.all([
        axios.get('/api/auth/paciente',      { withCredentials: true }),
        axios.get('/api/ejercicios/historial', { withCredentials: true }),
        axios.get('/api/ejercicios/',          { withCredentials: true }),
      ])

      if (pacienteRes.data.success) {
        setPaciente(pacienteRes.data.paciente?.paciente || pacienteRes.data.paciente)
      } else {
        navigate('/login')
      }

      if (historialRes.data.success)  setHistorial(historialRes.data.historial  || [])
      if (ejerciciosRes.data.success) setEjercicios(ejerciciosRes.data.ejercicios || [])
    } catch (err) {
      if (err.response?.status === 401) navigate('/login')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    try {
      await axios.post('/api/auth/logout', {}, { withCredentials: true })
    } finally {
      navigate('/')
    }
  }

  /* ── Loading ── */
  if (loading) {
    return (
      <div style={{
        background: '#0a1628',
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
        gap: '1rem',
      }}>
        <div className="rehavr-spinner" />
        <p style={{ color: '#00b4d8', fontWeight: 600, fontSize: '0.9rem', letterSpacing: 1 }}>
          CARGANDO SISTEMA…
        </p>
      </div>
    )
  }

  /* ── Métricas calculadas ── */
  const totalSesiones     = historial.length
  const exitosos          = historial.filter(h => h.exito).length
  const porcentajeProgreso = totalSesiones > 0
    ? Math.round((exitosos / totalSesiones) * 100)
    : 0

  const iniciales = paciente?.nombre
    ? paciente.nombre.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    : 'P'

  const ejerciciosRehab = ejercicios
    .filter(e => e.tipo === 'rehabilitacion')
    .sort((a, b) => (a.nivel || 1) - (b.nivel || 1))

  /* ── Render ── */
  return (
    <div className="rehavr-dashboard">
      {/* Fondo de cuadrícula decorativa */}
      <div className="rehavr-grid-bg" />

      {/* ─── HEADER ─── */}
      <header className="rehavr-header">
        <div className="rehavr-header-inner">

          {/* Marca */}
          <div className="rehavr-brand">
            <div className="rehavr-logo-mark">
              <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
                <circle cx="16" cy="16" r="14" stroke="#00b4d8" strokeWidth="2" />
                <path d="M9 10 L9 22 M9 16 L16 16 M16 10 L16 22"
                  stroke="#00b4d8" strokeWidth="2.5" strokeLinecap="round" />
                <circle cx="23" cy="16" r="3.5" stroke="#00c6fb" strokeWidth="2" />
                <ellipse cx="23" cy="16" rx="1.5" ry="3" fill="#00c6fb" opacity="0.7" />
              </svg>
            </div>
            <div>
              <span className="rehavr-brand-name">RehaVR</span>
              <span className="rehavr-brand-sub">Sistema de Rehabilitación</span>
            </div>
          </div>

          {/* Reloj */}
          <div className="rehavr-clock">
            <div className="rehavr-clock-time">
              {currentTime.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
            </div>
            <div className="rehavr-clock-date">
              {currentTime.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })}
            </div>
          </div>

          {/* Acciones */}
          <div className="rehavr-header-actions">
            <div className="rehavr-patient-badge">
              <div className="rehavr-avatar">{iniciales}</div>
              <div>
                <div className="rehavr-patient-name">{paciente?.nombre || 'Paciente'}</div>
                <div className="rehavr-patient-status">
                  <span className="rehavr-status-dot" />Sesión activa
                </div>
              </div>
            </div>

            <Link to="/configuracion" className="rehavr-btn-icon" title="Configuración">
              <i className="fas fa-sliders-h"></i>
            </Link>

            <button
              className="rehavr-btn-icon"
              onClick={toggle}
              title={theme === 'dark' ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'}
              aria-label="Cambiar tema"
            >
              {theme === 'dark'
                ? <i className="fas fa-sun"></i>
                : <i className="fas fa-moon"></i>
              }
            </button>

            <button onClick={handleLogout} className="rehavr-btn-logout">
              <i className="fas fa-power-off"></i>
              <span>Salir</span>
            </button>
          </div>
        </div>
      </header>

      {/* ─── MAIN ─── */}
      <main className="rehavr-main">

        {/* ── Stats ── */}
        <div className="rehavr-stats-row">
          <StatCard
            icon="fa-dumbbell"
            value={totalSesiones}
            label="Sesiones Completadas"
            iconBg="rgba(0,180,216,0.14)"
            iconColor="#00b4d8"
            ringColor="#00b4d8"
            ringMax={20}
            delay="0.1s"
          />
          <StatCard
            icon="fa-check-circle"
            value={exitosos}
            label="Ejercicios Exitosos"
            iconBg="rgba(67,211,130,0.14)"
            iconColor="#43d382"
            ringColor="#43d382"
            ringMax={20}
            delay="0.2s"
          />
          <StatCard
            icon="fa-chart-line"
            value={`${porcentajeProgreso}%`}
            label="Tasa de Progreso"
            iconBg="rgba(249,199,79,0.14)"
            iconColor="#f9c74f"
            ringColor="#f9c74f"
            ringMax={100}
            delay="0.3s"
          />
          <StatCard
            icon="fa-user-injured"
            value={paciente?.edad ?? '--'}
            label="Años del paciente"
            iconBg="rgba(157,78,221,0.14)"
            iconColor="#9d4edd"
            ringColor="#9d4edd"
            ringMax={100}
            delay="0.4s"
          />
        </div>

        {/* ── Sección: Rehabilitación Motora ── */}
        {ejerciciosRehab.length > 0 && (
          <section className="rehavr-section rehavr-anim-fadein" style={{ animationDelay: '0.5s' }}>
            <div className="rehavr-section-header">
              <div className="rehavr-section-icon">
                <i className="fas fa-brain"></i>
              </div>
              <div>
                <h2 className="rehavr-section-title">Rehabilitación Motora</h2>
                <p className="rehavr-section-sub">
                  Ejercicios progresivos de recuperación de movimiento
                </p>
              </div>
              <div className="rehavr-section-badge">
                {ejerciciosRehab.length} módulos
              </div>
            </div>

            <div className="rehavr-cards-grid">
              {ejerciciosRehab.map((ej, i) => (
                <RehabCard
                  key={ej.id}
                  ejercicio={ej}
                  delay={`${0.55 + i * 0.1}s`}
                />
              ))}
            </div>
          </section>
        )}

        {/* ── Sección: Terapia Ocupacional ── */}
        <section className="rehavr-section rehavr-anim-fadein" style={{ animationDelay: '0.7s' }}>
          <div className="rehavr-section-header">
            <div className="rehavr-section-icon" style={{ background: 'rgba(255,152,0,0.12)', color: '#ff9800', borderColor: 'rgba(255,152,0,0.2)' }}>
              <i className="fas fa-hands"></i>
            </div>
            <div>
              <h2 className="rehavr-section-title">Terapia Ocupacional</h2>
              <p className="rehavr-section-sub">
                Actividades de vida diaria y recuperación de motricidad fina
              </p>
            </div>
            <div className="rehavr-section-badge" style={{ background: 'rgba(255,152,0,0.1)', color: '#ff9800', border: '1px solid rgba(255,152,0,0.25)' }}>
              6 ejercicios
            </div>
          </div>

          <div className="rehavr-occ-card">
            {/* Iconos animados */}
            <div className="rehavr-occ-visual">
              <div className="rehavr-occ-icons">
                {OCC_ICONS.map((ic, i) => (
                  <div key={i} className="rehavr-occ-icon" style={{ animationDelay: `${i * 0.3}s` }}>
                    <i className={`fas ${ic}`}></i>
                  </div>
                ))}
              </div>
            </div>

            {/* Descripción + acceso */}
            <div className="rehavr-occ-content">
              <h3>Módulo de Actividades Diarias</h3>
              <p>
                Ejercicios diseñados para recuperar la independencia funcional:
                abotonar ropa, usar cubiertos, manipular objetos, cerradura,
                clasificación y rompecabezas.
              </p>
              <div className="rehavr-occ-tags">
                <span>Motricidad fina</span>
                <span>Coordinación</span>
                <span>Precisión</span>
                <span>Memoria motora</span>
              </div>
              <Link
                to="/terapia-ocupacional"
                className="rehavr-btn-primary"
                style={{ '--btn-color': '#ff9800', '--btn-glow': 'rgba(255,152,0,0.4)' }}
              >
                <i className="fas fa-arrow-right"></i>
                Acceder al Módulo
              </Link>
            </div>
          </div>
        </section>

        {/* ── Sección: Historial de actividad ── */}
        {historial.length > 0 && (
          <section className="rehavr-section rehavr-anim-fadein" style={{ animationDelay: '0.9s' }}>
            <div className="rehavr-section-header">
              <div className="rehavr-section-icon" style={{ background: 'rgba(0,180,216,0.1)', color: '#00b4d8' }}>
                <i className="fas fa-history"></i>
              </div>
              <div>
                <h2 className="rehavr-section-title">Historial de Actividad</h2>
                <p className="rehavr-section-sub">
                  Últimas sesiones de terapia registradas
                </p>
              </div>
              <div className="rehavr-section-badge">
                {historial.length} registros
              </div>
            </div>

            <div className="rehavr-table-wrap">
              <table className="rehavr-table">
                <thead>
                  <tr>
                    <th><i className="fas fa-calendar-alt"></i> Fecha</th>
                    <th><i className="fas fa-clipboard-list"></i> Ejercicio</th>
                    <th><i className="fas fa-star"></i> Puntuación</th>
                    <th><i className="fas fa-flag"></i> Resultado</th>
                  </tr>
                </thead>
                <tbody>
                  {historial.slice(-8).reverse().map((act, i) => {
                    const fecha = new Date(act.fecha_ejercicio || act.fecha)
                    const nombre = act.tipo_ejercicio || act.nivel || act.ejercicio || 'N/A'
                    return (
                      <tr key={i} className="rehavr-table-row">
                        <td>
                          {isNaN(fecha)
                            ? '—'
                            : fecha.toLocaleDateString('es-ES', {
                                day: '2-digit', month: 'short', year: 'numeric',
                              })}
                        </td>
                        <td><span className="rehavr-exercise-name">{nombre}</span></td>
                        <td><span className="rehavr-score">{act.puntuacion ?? '—'}</span></td>
                        <td>
                          {act.exito ? (
                            <span className="rehavr-badge rehavr-badge-success">
                              <i className="fas fa-check"></i> Completado
                            </span>
                          ) : (
                            <span className="rehavr-badge rehavr-badge-warn">
                              <i className="fas fa-redo"></i> En progreso
                            </span>
                          )}
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {/* Mensaje si no hay historial */}
        {historial.length === 0 && (
          <div
            className="rehavr-anim-fadein"
            style={{
              textAlign: 'center',
              padding: '3rem',
              color: 'rgba(122,143,166,0.7)',
              animationDelay: '0.9s',
            }}
          >
            <i className="fas fa-heartbeat" style={{ fontSize: '2.5rem', marginBottom: '1rem', display: 'block', color: 'rgba(0,180,216,0.3)' }}></i>
            <p style={{ margin: 0, fontWeight: 600 }}>
              Aún no hay sesiones registradas. ¡Comienza tu primer ejercicio!
            </p>
          </div>
        )}
      </main>
    </div>
  )
}
