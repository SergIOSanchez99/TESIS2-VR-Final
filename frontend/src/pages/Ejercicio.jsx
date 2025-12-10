import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'
import EjercicioCanvas from '../components/EjercicioCanvas'

const Ejercicio = () => {
  const { nivel } = useParams()
  const navigate = useNavigate()
  const [ejercicio, setEjercicio] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadEjercicio()
  }, [nivel])

  const loadEjercicio = async () => {
    try {
      // Mapear nivel a ejercicio_id
      const ejercicioMap = {
        '1': 'rehabilitacion_nivel_1',
        '2': 'rehabilitacion_nivel_2',
        '3': 'rehabilitacion_nivel_3'
      }

      const ejercicioId = ejercicioMap[nivel]
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

  return (
    <div className="container py-5">
      <div className="card shadow">
        <div className="card-header bg-primary text-white">
          <h2 className="mb-0">
            <i className="fas fa-gamepad me-2"></i>
            {ejercicio.nombre}
          </h2>
        </div>
        <div className="card-body">
          <p className="lead">{ejercicio.descripcion}</p>
          
          {ejercicio.instrucciones && ejercicio.instrucciones.length > 0 && (
            <div className="alert alert-info">
              <h5 className="alert-heading">Instrucciones:</h5>
              <ul className="mb-0">
                {ejercicio.instrucciones.map((inst, index) => (
                  <li key={index}>{inst}</li>
                ))}
              </ul>
            </div>
          )}

          <EjercicioCanvas
            ejercicioId={ejercicio.id}
            nivel={parseInt(nivel)}
            onComplete={handleComplete}
          />

          <div className="mt-4 text-center">
            <button
              className="btn btn-secondary"
              onClick={() => navigate('/dashboard')}
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

