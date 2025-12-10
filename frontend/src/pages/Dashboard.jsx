import React, { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import axios from 'axios'

const Dashboard = () => {
  const navigate = useNavigate()
  const [paciente, setPaciente] = useState(null)
  const [ejercicios, setEjercicios] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [pacienteRes, ejerciciosRes] = await Promise.all([
        axios.get('/api/auth/paciente', { withCredentials: true }),
        axios.get('/api/ejercicios/', { withCredentials: true })
      ])

      if (pacienteRes.data.success) {
        // La respuesta viene con estructura: { paciente: { paciente: {...}, ejercicios: {...} } }
        const pacienteData = pacienteRes.data.paciente?.paciente || pacienteRes.data.paciente
        setPaciente(pacienteData)
      } else {
        navigate('/login')
      }

      if (ejerciciosRes.data.success) {
        setEjercicios(ejerciciosRes.data.ejercicios || [])
      }
    } catch (error) {
      console.error('Error al cargar datos:', error)
      navigate('/login')
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

  return (
    <div className="container py-5">
      <h1 className="mb-4">
        <i className="fas fa-tachometer-alt me-2"></i>Dashboard
      </h1>
      
      {paciente && paciente.nombre && (
        <div className="card mb-4">
          <div className="card-body">
            <h5 className="card-title">Bienvenido, {paciente.nombre}</h5>
          </div>
        </div>
      )}

      <div className="row g-4">
        {ejercicios.map((ejercicio) => (
          <div key={ejercicio.id} className="col-md-4">
            <div className="card h-100">
              <div className="card-body">
                <h5 className="card-title">{ejercicio.nombre}</h5>
                <p className="card-text">{ejercicio.descripcion}</p>
                <p className="card-text">
                  <small className="text-muted">Nivel: {ejercicio.nivel}</small>
                </p>
                <Link
                  to={`/ejercicio/${ejercicio.nivel}`}
                  className="btn btn-primary"
                >
                  Comenzar Ejercicio
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Dashboard

