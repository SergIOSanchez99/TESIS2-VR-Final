import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'

const TerapiaUsarCubiertos = ({ ejercicioId, onComplete }) => {
  const [foodItems, setFoodItems] = useState([])
  const [completed, setCompleted] = useState(0)
  const [startTime, setStartTime] = useState(null)
  const [isActive, setIsActive] = useState(false)
  const [selectedUtensil, setSelectedUtensil] = useState(null)
  const [draggedItem, setDraggedItem] = useState(null)
  const gameContainerRef = useRef(null)

  const foodData = [
    { id: 0, name: 'Manzana', emoji: '🍎', utensil: 'fork', x: 20, y: 30 },
    { id: 1, name: 'Pasta', emoji: '🍝', utensil: 'fork', x: 20, y: 50 },
    { id: 2, name: 'Carne', emoji: '🥩', utensil: 'knife', x: 20, y: 70 }
  ]

  useEffect(() => {
    initializeGame()
  }, [])

  const initializeGame = () => {
    setFoodItems(foodData.map(item => ({ ...item, completed: false })))
    setCompleted(0)
    setIsActive(false)
    setSelectedUtensil(null)
  }

  const startGame = () => {
    setIsActive(true)
    setStartTime(Date.now())
  }

  const handleUtensilSelect = (utensil) => {
    if (!isActive) {
      startGame()
    }
    setSelectedUtensil(utensil)
  }

  const handleFoodClick = (food) => {
    if (!selectedUtensil || food.completed) return

    if (food.utensil === selectedUtensil) {
      const newFoodItems = foodItems.map(item =>
        item.id === food.id ? { ...item, completed: true } : item
      )
      setFoodItems(newFoodItems)
      setCompleted(prev => {
        const newCompleted = prev + 1
        if (newCompleted === foodData.length) {
          handleComplete()
        }
        return newCompleted
      })
    }
  }

  const handleComplete = async () => {
    const tiempoEjecucion = startTime ? (Date.now() - startTime) / 1000 : 0
    
    try {
      await axios.post(
        '/api/ejercicios/resultado',
        {
          ejercicio_id: ejercicioId,
          nivel: 2,
          exito: true,
          tiempo_ejecucion: tiempoEjecucion,
          puntuacion: 100,
          observaciones: `Ejercicio completado en ${tiempoEjecucion.toFixed(1)} segundos`
        },
        { withCredentials: true }
      )
    } catch (error) {
      console.error('Error al registrar resultado:', error)
    }

    if (onComplete) {
      onComplete({ tiempoEjecucion, completed: foodData.length })
    }
  }

  return (
    <div className="text-center">
      <div className="mb-4">
        <h4 className="text-primary mb-3">
          <i className="fas fa-utensils me-2"></i>
          Ejercicio: Usar Cubiertos
        </h4>
        <p className="text-muted">
          Selecciona el cubierto correcto y haz clic en el alimento correspondiente.
          Este ejercicio mejora la coordinación y habilidades de alimentación independiente.
        </p>
      </div>

      <div
        ref={gameContainerRef}
        style={{
          position: 'relative',
          height: '550px',
          background: 'linear-gradient(135deg, #fff9e6 0%, #ffe0b2 100%)',
          borderRadius: '15px',
          margin: '0 auto',
          maxWidth: '700px',
          boxShadow: '0 8px 16px rgba(0, 0, 0, 0.1)',
          border: '3px solid #03a9f4',
          overflow: 'hidden'
        }}
      >
        {/* Mesa */}
        <div
          style={{
            position: 'absolute',
            bottom: '0',
            left: '0',
            right: '0',
            height: '150px',
            background: 'linear-gradient(135deg, #8d6e63 0%, #6d4c41 100%)',
            borderTop: '8px solid #5d4037',
            boxShadow: 'inset 0 4px 8px rgba(0, 0, 0, 0.3)'
          }}
        >
          {/* Textura de madera */}
          <div
            style={{
              position: 'absolute',
              top: '0',
              left: '0',
              right: '0',
              bottom: '0',
              backgroundImage: 'repeating-linear-gradient(90deg, transparent, transparent 50px, rgba(0,0,0,0.1) 50px, rgba(0,0,0,0.1) 52px)',
              opacity: 0.3
            }}
          />
        </div>

        {/* Platos con alimentos */}
        <div style={{ position: 'relative', height: '100%', padding: '40px' }}>
          {foodItems.map((food) => (
            <div
              key={food.id}
              onClick={() => handleFoodClick(food)}
              style={{
                position: 'absolute',
                left: `${food.x}%`,
                top: `${food.y}%`,
                transform: 'translate(-50%, -50%)',
                width: '120px',
                height: '120px',
                background: food.completed
                  ? 'linear-gradient(135deg, #43a047 0%, #2e7d32 100%)'
                  : 'linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%)',
                borderRadius: '50%',
                border: `4px solid ${food.completed ? '#43a047' : '#03a9f4'}`,
                boxShadow: food.completed
                  ? '0 4px 8px rgba(67, 160, 71, 0.3)'
                  : '0 6px 12px rgba(0, 0, 0, 0.2)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: food.completed ? 'default' : 'pointer',
                transition: 'all 0.3s ease',
                transform: `translate(-50%, -50%) ${food.completed ? 'scale(0.9)' : 'scale(1)'}`,
                opacity: food.completed ? 0.7 : 1
              }}
              onMouseEnter={(e) => {
                if (!food.completed) {
                  e.currentTarget.style.transform = 'translate(-50%, -50%) scale(1.1)'
                  e.currentTarget.style.boxShadow = '0 8px 16px rgba(3, 169, 244, 0.4)'
                }
              }}
              onMouseLeave={(e) => {
                if (!food.completed) {
                  e.currentTarget.style.transform = 'translate(-50%, -50%) scale(1)'
                  e.currentTarget.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.2)'
                }
              }}
            >
              <div style={{ fontSize: '50px', marginBottom: '5px' }}>
                {food.emoji}
              </div>
              <div style={{ fontSize: '12px', fontWeight: 'bold', color: '#333' }}>
                {food.name}
              </div>
              {food.completed && (
                <div style={{
                  position: 'absolute',
                  top: '5px',
                  right: '5px',
                  width: '30px',
                  height: '30px',
                  background: '#43a047',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white'
                }}>
                  <i className="fas fa-check"></i>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Cubiertos */}
        <div style={{
          position: 'absolute',
          bottom: '20px',
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          gap: '30px',
          zIndex: 10
        }}>
          {/* Tenedor */}
          <div
            onClick={() => handleUtensilSelect('fork')}
            style={{
              width: '80px',
              height: '80px',
              background: selectedUtensil === 'fork'
                ? 'linear-gradient(135deg, #03a9f4 0%, #0277bd 100%)'
                : 'linear-gradient(135deg, #b0bec5 0%, #90a4ae 100%)',
              borderRadius: '15px',
              border: `4px solid ${selectedUtensil === 'fork' ? '#0277bd' : '#78909c'}`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              boxShadow: selectedUtensil === 'fork'
                ? '0 6px 12px rgba(3, 169, 244, 0.4)'
                : '0 4px 8px rgba(0, 0, 0, 0.2)',
              transition: 'all 0.3s ease',
              transform: selectedUtensil === 'fork' ? 'scale(1.1)' : 'scale(1)'
            }}
            onMouseEnter={(e) => {
              if (selectedUtensil !== 'fork') {
                e.currentTarget.style.transform = 'scale(1.05)'
              }
            }}
            onMouseLeave={(e) => {
              if (selectedUtensil !== 'fork') {
                e.currentTarget.style.transform = 'scale(1)'
              }
            }}
          >
            <i className="fas fa-utensils fa-2x text-white"></i>
          </div>

          {/* Cuchillo */}
          <div
            onClick={() => handleUtensilSelect('knife')}
            style={{
              width: '80px',
              height: '80px',
              background: selectedUtensil === 'knife'
                ? 'linear-gradient(135deg, #03a9f4 0%, #0277bd 100%)'
                : 'linear-gradient(135deg, #b0bec5 0%, #90a4ae 100%)',
              borderRadius: '15px',
              border: `4px solid ${selectedUtensil === 'knife' ? '#0277bd' : '#78909c'}`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              boxShadow: selectedUtensil === 'knife'
                ? '0 6px 12px rgba(3, 169, 244, 0.4)'
                : '0 4px 8px rgba(0, 0, 0, 0.2)',
              transition: 'all 0.3s ease',
              transform: selectedUtensil === 'knife' ? 'scale(1.1)' : 'scale(1)'
            }}
            onMouseEnter={(e) => {
              if (selectedUtensil !== 'knife') {
                e.currentTarget.style.transform = 'scale(1.05)'
              }
            }}
            onMouseLeave={(e) => {
              if (selectedUtensil !== 'knife') {
                e.currentTarget.style.transform = 'scale(1)'
              }
            }}
          >
            <i className="fas fa-utensils fa-2x text-white" style={{ transform: 'rotate(90deg)' }}></i>
          </div>
        </div>

        {/* Indicador de progreso */}
        <div
          style={{
            position: 'absolute',
            top: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            width: '80%',
            height: '10px',
            background: '#e0e0e0',
            borderRadius: '10px',
            overflow: 'hidden',
            boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.1)'
          }}
        >
          <div
            style={{
              width: `${(completed / foodData.length) * 100}%`,
              height: '100%',
              background: 'linear-gradient(90deg, #43a047 0%, #66bb6a 100%)',
              transition: 'width 0.5s ease',
              borderRadius: '10px'
            }}
          />
        </div>
      </div>

      <div className="mt-4">
        <div className="row">
          <div className="col-md-6">
            <div className="card">
              <div className="card-body">
                <h6 className="text-muted mb-1">Progreso</h6>
                <h4 className="text-success mb-0">
                  {completed} / {foodData.length}
                </h4>
              </div>
            </div>
          </div>
          <div className="col-md-6">
            <div className="card">
              <div className="card-body">
                <h6 className="text-muted mb-1">Tiempo</h6>
                <h4 className="text-primary mb-0">
                  {startTime ? ((Date.now() - startTime) / 1000).toFixed(1) : '0.0'}s
                </h4>
              </div>
            </div>
          </div>
        </div>
      </div>

      {!isActive && (
        <div className="alert alert-info mt-3">
          <strong><i className="fas fa-info-circle me-2"></i>Instrucciones:</strong>
          <br />
          Selecciona un cubierto (tenedor o cuchillo) y luego haz clic en el alimento que corresponde.
        </div>
      )}

      {completed === foodData.length && (
        <div className="alert alert-success mt-3">
          <strong><i className="fas fa-check-circle me-2"></i>¡Ejercicio completado!</strong>
          <br />
          Has usado los cubiertos correctamente en {startTime ? ((Date.now() - startTime) / 1000).toFixed(1) : '0.0'} segundos.
        </div>
      )}
    </div>
  )
}

export default TerapiaUsarCubiertos

