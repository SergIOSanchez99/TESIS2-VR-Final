import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

const Configuracion = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [guardando, setGuardando] = useState(false)
  const [config, setConfig] = useState(null)
  const [tabActiva, setTabActiva] = useState('calibracion')

  useEffect(() => {
    cargarConfiguracion()
  }, [])

  const cargarConfiguracion = async () => {
    try {
      const response = await axios.get('/api/configuracion', { withCredentials: true })
      if (response.data.success) {
        setConfig(response.data.configuracion)
      }
    } catch (error) {
      console.error('Error al cargar configuración:', error)
      if (error.response?.status === 401) {
        navigate('/login')
      }
    } finally {
      setLoading(false)
    }
  }

  const guardarCalibracion = async (e) => {
    e.preventDefault()
    setGuardando(true)
    
    try {
      const response = await axios.put(
        '/api/configuracion/calibracion',
        config.calibracion,
        { withCredentials: true }
      )
      
      if (response.data.success) {
        alert('Calibración actualizada correctamente')
      }
    } catch (error) {
      console.error('Error al guardar:', error)
      alert('Error al guardar la configuración')
    } finally {
      setGuardando(false)
    }
  }

  const guardarAccesibilidad = async (e) => {
    e.preventDefault()
    setGuardando(true)
    
    try {
      const response = await axios.put(
        '/api/configuracion/accesibilidad',
        config.accesibilidad,
        { withCredentials: true }
      )
      
      if (response.data.success) {
        alert('Configuración de accesibilidad actualizada')
      }
    } catch (error) {
      console.error('Error al guardar:', error)
      alert('Error al guardar la configuración')
    } finally {
      setGuardando(false)
    }
  }

  const guardarSeguridad = async (e) => {
    e.preventDefault()
    setGuardando(true)
    
    try {
      const response = await axios.put(
        '/api/configuracion/seguridad',
        config.seguridad,
        { withCredentials: true }
      )
      
      if (response.data.success) {
        alert('Configuración de seguridad actualizada')
      }
    } catch (error) {
      console.error('Error al guardar:', error)
      alert('Error al guardar la configuración')
    } finally {
      setGuardando(false)
    }
  }

  const aplicarPreset = async (preset) => {
    try {
      const response = await axios.post(
        `/api/configuracion/preset/${preset}`,
        {},
        { withCredentials: true }
      )
      
      if (response.data.success) {
        alert(`Preset "${preset}" aplicado correctamente`)
        await cargarConfiguracion()
      }
    } catch (error) {
      console.error('Error al aplicar preset:', error)
      alert('Error al aplicar el preset')
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

  if (!config) return null

  return (
    <div style={{ 
      background: 'linear-gradient(135deg, #4a90e2 0%, #357abd 50%, #2e5c8a 100%)',
      minHeight: '100vh', 
      paddingTop: '2rem', 
      paddingBottom: '3rem'
    }}>
      <div className="container">
        <div className="row mb-4">
          <div className="col-12">
            <div className="card shadow-lg">
              <div className="card-body">
                <h2 className="mb-0">
                  <i className="fas fa-cog me-2 text-primary"></i>
                  Configuración
                </h2>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="row mb-4">
          <div className="col-12">
            <ul className="nav nav-pills nav-fill" style={{ backgroundColor: 'white', borderRadius: '10px', padding: '10px' }}>
              <li className="nav-item">
                <button
                  className={`nav-link ${tabActiva === 'calibracion' ? 'active' : ''}`}
                  onClick={() => setTabActiva('calibracion')}
                >
                  <i className="fas fa-ruler me-2"></i>Calibración
                </button>
              </li>
              <li className="nav-item">
                <button
                  className={`nav-link ${tabActiva === 'accesibilidad' ? 'active' : ''}`}
                  onClick={() => setTabActiva('accesibilidad')}
                >
                  <i className="fas fa-universal-access me-2"></i>Accesibilidad
                </button>
              </li>
              <li className="nav-item">
                <button
                  className={`nav-link ${tabActiva === 'seguridad' ? 'active' : ''}`}
                  onClick={() => setTabActiva('seguridad')}
                >
                  <i className="fas fa-shield-alt me-2"></i>Seguridad
                </button>
              </li>
              <li className="nav-item">
                <button
                  className={`nav-link ${tabActiva === 'presets' ? 'active' : ''}`}
                  onClick={() => setTabActiva('presets')}
                >
                  <i className="fas fa-magic me-2"></i>Presets
                </button>
              </li>
            </ul>
          </div>
        </div>

        {/* Contenido Tabs */}
        <div className="row">
          <div className="col-12">
            <div className="card shadow-lg">
              <div className="card-body">
                
                {/* Tab Calibración */}
                {tabActiva === 'calibracion' && (
                  <form onSubmit={guardarCalibracion}>
                    <h4 className="mb-4">Calibración Física</h4>
                    
                    <div className="row">
                      <div className="col-md-6 mb-3">
                        <label className="form-label">Altura (cm)</label>
                        <input
                          type="number"
                          className="form-control"
                          value={config.calibracion.altura_cm || ''}
                          onChange={(e) => setConfig({
                            ...config,
                            calibracion: { ...config.calibracion, altura_cm: parseInt(e.target.value) }
                          })}
                          min="100"
                          max="250"
                        />
                      </div>
                      
                      <div className="col-md-6 mb-3">
                        <label className="form-label">Rango Movimiento Hombro (grados)</label>
                        <input
                          type="number"
                          className="form-control"
                          value={config.calibracion.rango_movimiento_hombro}
                          onChange={(e) => setConfig({
                            ...config,
                            calibracion: { ...config.calibracion, rango_movimiento_hombro: parseInt(e.target.value) }
                          })}
                          min="0"
                          max="180"
                        />
                        <small className="text-muted">Normal: 180°</small>
                      </div>
                      
                      <div className="col-md-6 mb-3">
                        <label className="form-label">Rango Movimiento Codo (grados)</label>
                        <input
                          type="number"
                          className="form-control"
                          value={config.calibracion.rango_movimiento_codo}
                          onChange={(e) => setConfig({
                            ...config,
                            calibracion: { ...config.calibracion, rango_movimiento_codo: parseInt(e.target.value) }
                          })}
                          min="0"
                          max="150"
                        />
                        <small className="text-muted">Normal: 150°</small>
                      </div>
                      
                      <div className="col-md-6 mb-3">
                        <label className="form-label">Rango Movimiento Muñeca (grados)</label>
                        <input
                          type="number"
                          className="form-control"
                          value={config.calibracion.rango_movimiento_muneca}
                          onChange={(e) => setConfig({
                            ...config,
                            calibracion: { ...config.calibracion, rango_movimiento_muneca: parseInt(e.target.value) }
                          })}
                          min="0"
                          max="90"
                        />
                        <small className="text-muted">Normal: 90°</small>
                      </div>
                    </div>
                    
                    <button type="submit" className="btn btn-primary" disabled={guardando}>
                      {guardando ? 'Guardando...' : 'Guardar Calibración'}
                    </button>
                  </form>
                )}

                {/* Tab Accesibilidad */}
                {tabActiva === 'accesibilidad' && (
                  <form onSubmit={guardarAccesibilidad}>
                    <h4 className="mb-4">Configuración de Accesibilidad</h4>
                    
                    <div className="row">
                      <div className="col-md-6 mb-3">
                        <label className="form-label">Modo de Juego</label>
                        <select
                          className="form-select"
                          value={config.accesibilidad.modo_accesibilidad}
                          onChange={(e) => setConfig({
                            ...config,
                            accesibilidad: { ...config.accesibilidad, modo_accesibilidad: e.target.value }
                          })}
                        >
                          <option value="sentado">Sentado</option>
                          <option value="pie">De Pie</option>
                          <option value="ambos">Ambos</option>
                        </select>
                      </div>
                      
                      <div className="col-md-6 mb-3">
                        <label className="form-label">Manos Habilitadas</label>
                        <select
                          className="form-select"
                          value={config.accesibilidad.manos_habilitadas}
                          onChange={(e) => setConfig({
                            ...config,
                            accesibilidad: { ...config.accesibilidad, manos_habilitadas: e.target.value }
                          })}
                        >
                          <option value="izquierda">Izquierda</option>
                          <option value="derecha">Derecha</option>
                          <option value="ambas">Ambas</option>
                        </select>
                      </div>
                      
                      <div className="col-md-6 mb-3">
                        <label className="form-label">Velocidad del Juego: {config.accesibilidad.velocidad_juego}x</label>
                        <input
                          type="range"
                          className="form-range"
                          min="0.5"
                          max="2.0"
                          step="0.1"
                          value={config.accesibilidad.velocidad_juego}
                          onChange={(e) => setConfig({
                            ...config,
                            accesibilidad: { ...config.accesibilidad, velocidad_juego: parseFloat(e.target.value) }
                          })}
                        />
                      </div>
                      
                      <div className="col-md-6 mb-3">
                        <label className="form-label">Tamaño de Objetivos</label>
                        <select
                          className="form-select"
                          value={config.accesibilidad.tamano_objetivos}
                          onChange={(e) => setConfig({
                            ...config,
                            accesibilidad: { ...config.accesibilidad, tamano_objetivos: e.target.value }
                          })}
                        >
                          <option value="pequeno">Pequeño</option>
                          <option value="mediano">Mediano</option>
                          <option value="grande">Grande</option>
                        </select>
                      </div>
                      
                      <div className="col-12 mb-3">
                        <div className="form-check">
                          <input
                            type="checkbox"
                            className="form-check-input"
                            id="dificultad_adaptativa"
                            checked={config.accesibilidad.dificultad_adaptativa}
                            onChange={(e) => setConfig({
                              ...config,
                              accesibilidad: { ...config.accesibilidad, dificultad_adaptativa: e.target.checked }
                            })}
                          />
                          <label className="form-check-label" htmlFor="dificultad_adaptativa">
                            Dificultad Adaptativa (ajusta automáticamente según tu desempeño)
                          </label>
                        </div>
                      </div>
                      
                      <div className="col-12 mb-3">
                        <div className="form-check">
                          <input
                            type="checkbox"
                            className="form-check-input"
                            id="controles_simplificados"
                            checked={config.accesibilidad.controles_simplificados}
                            onChange={(e) => setConfig({
                              ...config,
                              accesibilidad: { ...config.accesibilidad, controles_simplificados: e.target.checked }
                            })}
                          />
                          <label className="form-check-label" htmlFor="controles_simplificados">
                            Controles Simplificados
                          </label>
                        </div>
                      </div>
                      
                      <div className="col-12 mb-3">
                        <div className="form-check">
                          <input
                            type="checkbox"
                            className="form-check-input"
                            id="texto_grande"
                            checked={config.accesibilidad.texto_grande}
                            onChange={(e) => setConfig({
                              ...config,
                              accesibilidad: { ...config.accesibilidad, texto_grande: e.target.checked }
                            })}
                          />
                          <label className="form-check-label" htmlFor="texto_grande">
                            Texto Grande
                          </label>
                        </div>
                      </div>
                      
                      <div className="col-12 mb-3">
                        <div className="form-check">
                          <input
                            type="checkbox"
                            className="form-check-input"
                            id="alto_contraste"
                            checked={config.accesibilidad.alto_contraste}
                            onChange={(e) => setConfig({
                              ...config,
                              accesibilidad: { ...config.accesibilidad, alto_contraste: e.target.checked }
                            })}
                          />
                          <label className="form-check-label" htmlFor="alto_contraste">
                            Alto Contraste
                          </label>
                        </div>
                      </div>
                    </div>
                    
                    <button type="submit" className="btn btn-primary" disabled={guardando}>
                      {guardando ? 'Guardando...' : 'Guardar Accesibilidad'}
                    </button>
                  </form>
                )}

                {/* Tab Seguridad */}
                {tabActiva === 'seguridad' && (
                  <form onSubmit={guardarSeguridad}>
                    <h4 className="mb-4">Configuración de Seguridad</h4>
                    
                    <div className="row">
                      <div className="col-md-6 mb-3">
                        <label className="form-label">Límite de Tiempo de Sesión (minutos)</label>
                        <input
                          type="number"
                          className="form-control"
                          value={config.seguridad.limite_tiempo_sesion}
                          onChange={(e) => setConfig({
                            ...config,
                            seguridad: { ...config.seguridad, limite_tiempo_sesion: parseInt(e.target.value) }
                          })}
                          min="5"
                          max="60"
                        />
                      </div>
                      
                      <div className="col-md-6 mb-3">
                        <label className="form-label">Intervalo de Descanso (minutos)</label>
                        <input
                          type="number"
                          className="form-control"
                          value={config.seguridad.intervalo_descanso}
                          onChange={(e) => setConfig({
                            ...config,
                            seguridad: { ...config.seguridad, intervalo_descanso: parseInt(e.target.value) }
                          })}
                          min="5"
                          max="30"
                        />
                      </div>
                      
                      <div className="col-md-6 mb-3">
                        <label className="form-label">Duración de Descanso (minutos)</label>
                        <input
                          type="number"
                          className="form-control"
                          value={config.seguridad.duracion_descanso}
                          onChange={(e) => setConfig({
                            ...config,
                            seguridad: { ...config.seguridad, duracion_descanso: parseInt(e.target.value) }
                          })}
                          min="1"
                          max="10"
                        />
                      </div>
                      
                      <div className="col-md-6 mb-3">
                        <label className="form-label">Tiempo de Inactividad (segundos)</label>
                        <input
                          type="number"
                          className="form-control"
                          value={config.seguridad.tiempo_inactividad}
                          onChange={(e) => setConfig({
                            ...config,
                            seguridad: { ...config.seguridad, tiempo_inactividad: parseInt(e.target.value) }
                          })}
                          min="10"
                          max="120"
                        />
                      </div>
                      
                      <div className="col-12 mb-3">
                        <div className="form-check">
                          <input
                            type="checkbox"
                            className="form-check-input"
                            id="alerta_movimientos"
                            checked={config.seguridad.alerta_movimientos_bruscos}
                            onChange={(e) => setConfig({
                              ...config,
                              seguridad: { ...config.seguridad, alerta_movimientos_bruscos: e.target.checked }
                            })}
                          />
                          <label className="form-check-label" htmlFor="alerta_movimientos">
                            Alerta de Movimientos Bruscos
                          </label>
                        </div>
                      </div>
                      
                      <div className="col-12 mb-3">
                        <div className="form-check">
                          <input
                            type="checkbox"
                            className="form-check-input"
                            id="pausa_auto"
                            checked={config.seguridad.pausa_automatica_inactividad}
                            onChange={(e) => setConfig({
                              ...config,
                              seguridad: { ...config.seguridad, pausa_automatica_inactividad: e.target.checked }
                            })}
                          />
                          <label className="form-check-label" htmlFor="pausa_auto">
                            Pausa Automática por Inactividad
                          </label>
                        </div>
                      </div>
                      
                      <div className="col-12 mb-3">
                        <div className="form-check">
                          <input
                            type="checkbox"
                            className="form-check-input"
                            id="zona_delimitada"
                            checked={config.seguridad.zona_juego_delimitada}
                            onChange={(e) => setConfig({
                              ...config,
                              seguridad: { ...config.seguridad, zona_juego_delimitada: e.target.checked }
                            })}
                          />
                          <label className="form-check-label" htmlFor="zona_delimitada">
                            Zona de Juego Delimitada
                          </label>
                        </div>
                      </div>
                      
                      <div className="col-12 mb-3">
                        <div className="form-check">
                          <input
                            type="checkbox"
                            className="form-check-input"
                            id="antimareo"
                            checked={config.seguridad.sistema_antimareo}
                            onChange={(e) => setConfig({
                              ...config,
                              seguridad: { ...config.seguridad, sistema_antimareo: e.target.checked }
                            })}
                          />
                          <label className="form-check-label" htmlFor="antimareo">
                            Sistema Anti-Mareo (viñetas)
                          </label>
                        </div>
                      </div>
                    </div>
                    
                    <button type="submit" className="btn btn-primary" disabled={guardando}>
                      {guardando ? 'Guardando...' : 'Guardar Seguridad'}
                    </button>
                  </form>
                )}

                {/* Tab Presets */}
                {tabActiva === 'presets' && (
                  <div>
                    <h4 className="mb-4">Presets de Configuración</h4>
                    <p className="text-muted">Selecciona un preset para aplicar configuraciones predefinidas</p>
                    
                    <div className="row g-3">
                      <div className="col-md-4">
                        <div className="card h-100">
                          <div className="card-body">
                            <h5 className="card-title">
                              <i className="fas fa-star text-warning me-2"></i>
                              Principiante
                            </h5>
                            <p className="card-text">
                              Velocidad reducida, objetivos grandes, controles simplificados.
                            </p>
                            <button 
                              className="btn btn-outline-primary"
                              onClick={() => aplicarPreset('principiante')}
                            >
                              Aplicar
                            </button>
                          </div>
                        </div>
                      </div>
                      
                      <div className="col-md-4">
                        <div className="card h-100">
                          <div className="card-body">
                            <h5 className="card-title">
                              <i className="fas fa-check-circle text-primary me-2"></i>
                              Intermedio
                            </h5>
                            <p className="card-text">
                              Configuración balanceada, velocidad normal, dificultad adaptativa.
                            </p>
                            <button 
                              className="btn btn-outline-primary"
                              onClick={() => aplicarPreset('intermedio')}
                            >
                              Aplicar
                            </button>
                          </div>
                        </div>
                      </div>
                      
                      <div className="col-md-4">
                        <div className="card h-100">
                          <div className="card-body">
                            <h5 className="card-title">
                              <i className="fas fa-trophy text-success me-2"></i>
                              Avanzado
                            </h5>
                            <p className="card-text">
                              Mayor velocidad, objetivos pequeños, máximo desafío.
                            </p>
                            <button 
                              className="btn btn-outline-primary"
                              onClick={() => aplicarPreset('avanzado')}
                            >
                              Aplicar
                            </button>
                          </div>
                        </div>
                      </div>
                      
                      <div className="col-md-6">
                        <div className="card h-100">
                          <div className="card-body">
                            <h5 className="card-title">
                              <i className="fas fa-wheelchair text-info me-2"></i>
                              Movilidad Limitada
                            </h5>
                            <p className="card-text">
                              Modo sentado, velocidad lenta, objetivos grandes, adaptado para movilidad reducida.
                            </p>
                            <button 
                              className="btn btn-outline-primary"
                              onClick={() => aplicarPreset('movilidad_limitada')}
                            >
                              Aplicar
                            </button>
                          </div>
                        </div>
                      </div>
                      
                      <div className="col-md-6">
                        <div className="card h-100">
                          <div className="card-body">
                            <h5 className="card-title">
                              <i className="fas fa-eye text-secondary me-2"></i>
                              Visión Reducida
                            </h5>
                            <p className="card-text">
                              Objetivos grandes, texto grande, alto contraste, optimizado para baja visión.
                            </p>
                            <button 
                              className="btn btn-outline-primary"
                              onClick={() => aplicarPreset('vision_reducida')}
                            >
                              Aplicar
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="row mt-4">
          <div className="col-12">
            <button 
              className="btn btn-secondary"
              onClick={() => navigate('/dashboard')}
            >
              <i className="fas fa-arrow-left me-2"></i>
              Volver al Dashboard
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Configuracion

