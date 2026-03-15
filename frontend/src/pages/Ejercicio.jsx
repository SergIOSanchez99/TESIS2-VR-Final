import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'
import EjercicioCanvas from '../components/EjercicioCanvas'
import TerapiaAbotonarCamisa from '../components/TerapiaAbotonarCamisa'
import TerapiaArrastrarObjeto from '../components/TerapiaArrastrarObjeto'
import TerapiaAbrirCerradura from '../components/TerapiaAbrirCerradura'
import TerapiaUsarCubiertos from '../components/TerapiaUsarCubiertos'
import TerapiaRompecabezas from '../components/TerapiaRompecabezas'
import TerapiaClasificarObjetos from '../components/TerapiaClasificarObjetos'

const Ejercicio = () => {
  const { ejercicioId } = useParams()
  const navigate = useNavigate()
  const [ejercicio, setEjercicio] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadEjercicio()
  }, [ejercicioId])

  const loadEjercicio = async () => {
    try {
      if (!ejercicioId) {
        navigate('/dashboard')
        return
      }

      const response = await axios.get(
        `/api/ejercicios/${ejercicioId}`,
        { withCredentials: true }
      )

      if (response.data.success) {
        setEjercicio(response.data.ejercicio)
      } else {
        navigate('/dashboard')
      }
    } catch (error) {
      console.error('Error al cargar ejercicio:', error)
      navigate('/dashboard')
    } finally {
      setLoading(false)
    }
  }

  const handleComplete = (resultado) => {
    console.log('Ejercicio completado:', resultado)
    // Opcional: redirigir después de un tiempo
    setTimeout(() => {
      navigate('/dashboard')
    }, 3000)
  }

  if (loading) {
    return (
      <div className="container py-5 text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Cargando ejercicio...</span>
        </div>
      </div>
    )
  }

  if (!ejercicio) {
    return (
      <div className="container py-5">
        <div className="alert alert-danger">
          No se pudo cargar el ejercicio
        </div>
      </div>
    )
  }

  // Determinar qué componente usar según el tipo de ejercicio
  const renderEjercicio = () => {
    if (ejercicio.tipo === 'terapia_ocupacional') {
      if (ejercicioId === 'terapia_abotonar_camisa') {
        return (
          <TerapiaAbotonarCamisa
            ejercicioId={ejercicio.id}
            onComplete={handleComplete}
          />
        )
      } else if (ejercicioId === 'terapia_arrastrar_objeto') {
        return (
          <TerapiaArrastrarObjeto
            ejercicioId={ejercicio.id}
            onComplete={handleComplete}
          />
        )
      } else if (ejercicioId === 'terapia_abrir_cerradura') {
        return (
          <TerapiaAbrirCerradura
            ejercicioId={ejercicio.id}
            onComplete={handleComplete}
          />
        )
      } else if (ejercicioId === 'terapia_usar_cubiertos') {
        return (
          <TerapiaUsarCubiertos
            ejercicioId={ejercicio.id}
            onComplete={handleComplete}
          />
        )
      } else if (ejercicioId === 'terapia_rompecabezas') {
        return (
          <TerapiaRompecabezas
            ejercicioId={ejercicio.id}
            onComplete={handleComplete}
          />
        )
      } else if (ejercicioId === 'terapia_clasificar_objetos') {
        return (
          <TerapiaClasificarObjetos
            ejercicioId={ejercicio.id}
            onComplete={handleComplete}
          />
        )
      }
    }
    
    // Ejercicios de rehabilitación
    return (
      <EjercicioCanvas
        ejercicioId={ejercicio.id}
        nivel={ejercicio.nivel || 1}
        onComplete={handleComplete}
      />
    )
  }

  return (
    <div className="container py-5">
      <div className="card shadow-lg" style={{ borderRadius: '15px' }}>
        <div className={`card-header text-white ${ejercicio.tipo === 'terapia_ocupacional' ? 'bg-accent' : 'bg-primary'}`} style={{ 
          backgroundColor: ejercicio.tipo === 'terapia_ocupacional' ? 'var(--accent-color)' : undefined,
          borderRadius: '15px 15px 0 0'
        }}>
          <h2 className="mb-0">
            <i className={`fas ${ejercicio.tipo === 'terapia_ocupacional' ? 'fa-hands-helping' : 'fa-gamepad'} me-2`}></i>
            {ejercicio.nombre}
          </h2>
        </div>
        <div className="card-body">
          <p className="lead">{ejercicio.descripcion}</p>
          
          {ejercicio.instrucciones && ejercicio.instrucciones.length > 0 && (
            <div className="alert alert-info" style={{ borderRadius: '10px' }}>
              <h5 className="alert-heading">
                <i className="fas fa-info-circle me-2"></i>Instrucciones:
              </h5>
              <ul className="mb-0">
                {ejercicio.instrucciones.map((inst, index) => (
                  <li key={index} style={{ marginBottom: '5px' }}>{inst}</li>
                ))}
              </ul>
            </div>
          )}

          {renderEjercicio()}

          <div className="mt-4 text-center">
            <button
              className="btn btn-secondary btn-lg"
              onClick={() => navigate('/dashboard')}
              style={{ borderRadius: '25px', padding: '10px 30px' }}
            >
              <i className="fas fa-arrow-left me-2"></i>Volver al Dashboard
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Ejercicio

