import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'

const TerapiaAbotonarCamisa = ({ ejercicioId, onComplete }) => {
  const [buttons, setButtons] = useState([])
  const [completed, setCompleted] = useState(0)
  const [startTime, setStartTime] = useState(null)
  const [isActive, setIsActive] = useState(false)
  const gameContainerRef = useRef(null)
  const buttonCount = 6

  useEffect(() => {
    initializeGame()
  }, [])

  const initializeGame = () => {
    const newButtons = []
    for (let i = 0; i < buttonCount; i++) {
      newButtons.push({
        id: i,
        completed: false,
        top: 90 + i * 45
      })
    }
    setButtons(newButtons)
    setCompleted(0)
    setIsActive(false)
  }

  const startGame = () => {
    setIsActive(true)
    setStartTime(Date.now())
  }

  const handleButtonClick = async (buttonId) => {
    if (!isActive) {
      startGame()
      return
    }

    if (buttons[buttonId].completed) return

    const newButtons = [...buttons]
    newButtons[buttonId].completed = true
    setButtons(newButtons)
    setCompleted(prev => {
      const newCompleted = prev + 1
      
      if (newCompleted === buttonCount) {
        handleComplete()
      }
      return newCompleted
    })
  }

  const handleComplete = async () => {
    const tiempoEjecucion = startTime ? (Date.now() - startTime) / 1000 : 0
    
    try {
      await axios.post(
        '/api/ejercicios/resultado',
        {
          ejercicio_id: ejercicioId,
          nivel: 1,
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
      onComplete({ tiempoEjecucion, completed: buttonCount })
    }
  }

  return (
    <div className="text-center">
      <div className="mb-4">
        <h4 className="text-primary mb-3">
          <i className="fas fa-tshirt me-2"></i>
          Ejercicio: Abotonar Camisa
        </h4>
        <p className="text-muted">
          Haz clic en los botones en orden de arriba hacia abajo para abotonar la camisa.
          Este ejercicio mejora la coordinación fina y la destreza manual.
        </p>
      </div>

      <div 
        ref={gameContainerRef}
        style={{
          position: 'relative',
          height: '450px',
          background: 'linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%)',
          borderRadius: '15px',
          margin: '0 auto',
          maxWidth: '350px',
          boxShadow: '0 8px 16px rgba(0, 0, 0, 0.1)',
          border: '3px solid #1976d2'
        }}
      >
        {/* Camisa realista */}
        <div
          style={{
            position: 'absolute',
            top: '30px',
            left: '50%',
            transform: 'translateX(-50%)',
            width: '280px',
            height: '380px',
            background: 'linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%)',
            border: '4px solid #1976d2',
            borderRadius: '20px',
            boxShadow: '0 6px 12px rgba(0, 0, 0, 0.15)',
            overflow: 'hidden'
          }}
        >
          {/* Cuello de la camisa */}
          <div
            style={{
              position: 'absolute',
              top: '-15px',
              left: '50%',
              transform: 'translateX(-50%)',
              width: '220px',
              height: '50px',
              background: '#1976d2',
              borderRadius: '25px 25px 0 0',
              boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)'
            }}
          >
            {/* Detalles del cuello */}
            <div
              style={{
                position: 'absolute',
                top: '10px',
                left: '50%',
                transform: 'translateX(-50%)',
                width: '180px',
                height: '30px',
                background: '#1565c0',
                borderRadius: '15px'
              }}
            />
          </div>

          {/* Botones y ojales */}
          {buttons.map((button, index) => (
            <React.Fragment key={button.id}>
              {/* Ojal */}
              <div
                style={{
                  position: 'absolute',
                  left: '48%',
                  width: button.completed ? '0px' : '30px',
                  height: '10px',
                  background: '#424242',
                  borderRadius: '5px',
                  top: `${button.top}px`,
                  transition: 'all 0.6s ease',
                  boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.3)'
                }}
              />

              {/* Botón */}
              <div
                onClick={() => handleButtonClick(button.id)}
                style={{
                  position: 'absolute',
                  left: button.completed ? '48%' : '52%',
                  transform: 'translateX(-50%)',
                  width: '42px',
                  height: '42px',
                  background: button.completed 
                    ? 'linear-gradient(135deg, #43a047 0%, #2e7d32 100%)'
                    : 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)',
                  borderRadius: '50%',
                  cursor: button.completed ? 'default' : 'pointer',
                  border: '4px solid #ffffff',
                  boxShadow: button.completed
                    ? '0 2px 4px rgba(0, 0, 0, 0.2)'
                    : '0 4px 8px rgba(0, 0, 0, 0.3)',
                  transition: 'all 0.6s ease',
                  top: `${button.top - 5}px`,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  zIndex: 10
                }}
                onMouseEnter={(e) => {
                  if (!button.completed) {
                    e.currentTarget.style.transform = 'translateX(-50%) scale(1.15)'
                    e.currentTarget.style.boxShadow = '0 6px 12px rgba(0, 0, 0, 0.4)'
                  }
                }}
                onMouseLeave={(e) => {
                  if (!button.completed) {
                    e.currentTarget.style.transform = 'translateX(-50%) scale(1)'
                    e.currentTarget.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.3)'
                  }
                }}
              >
                {/* Centro del botón con efecto 3D */}
                <div
                  style={{
                    width: '16px',
                    height: '16px',
                    background: 'rgba(255, 255, 255, 0.4)',
                    borderRadius: '50%',
                    boxShadow: 'inset 0 1px 2px rgba(0, 0, 0, 0.2)'
                  }}
                />
              </div>
            </React.Fragment>
          ))}

          {/* Detalles de la camisa - costuras */}
          <div
            style={{
              position: 'absolute',
              left: '50%',
              transform: 'translateX(-50%)',
              width: '2px',
              height: '350px',
              top: '40px',
              background: 'rgba(25, 118, 210, 0.2)',
              boxShadow: '0 0 2px rgba(25, 118, 210, 0.3)'
            }}
          />
        </div>

        {/* Indicador de progreso visual */}
        <div
          style={{
            position: 'absolute',
            bottom: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            width: '90%',
            height: '8px',
            background: '#e0e0e0',
            borderRadius: '10px',
            overflow: 'hidden',
            boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.1)'
          }}
        >
          <div
            style={{
              width: `${(completed / buttonCount) * 100}%`,
              height: '100%',
              background: 'linear-gradient(90deg, #43a047 0%, #66bb6a 100%)',
              transition: 'width 0.6s ease',
              borderRadius: '10px',
              boxShadow: '0 2px 4px rgba(67, 160, 71, 0.3)'
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
                  {completed} / {buttonCount}
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
          Haz clic en el primer botón para comenzar. Luego continúa abotonando de arriba hacia abajo.
        </div>
      )}

      {completed === buttonCount && (
        <div className="alert alert-success mt-3">
          <strong><i className="fas fa-check-circle me-2"></i>¡Ejercicio completado!</strong>
          <br />
          Has abotonado la camisa correctamente en {startTime ? ((Date.now() - startTime) / 1000).toFixed(1) : '0.0'} segundos.
        </div>
      )}
    </div>
  )
}

export default TerapiaAbotonarCamisa

