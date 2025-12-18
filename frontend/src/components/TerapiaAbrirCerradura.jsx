import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'

const TerapiaAbrirCerradura = ({ ejercicioId, onComplete }) => {
  const [keyPosition, setKeyPosition] = useState({ x: 50, y: 50 })
  const [lockPosition, setLockPosition] = useState({ x: 50, y: 50 })
  const [isInserted, setIsInserted] = useState(false)
  const [rotation, setRotation] = useState(0)
  const [isUnlocked, setIsUnlocked] = useState(false)
  const [startTime, setStartTime] = useState(null)
  const [isActive, setIsActive] = useState(false)
  const [dragging, setDragging] = useState(false)
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 })
  const gameContainerRef = useRef(null)

  useEffect(() => {
    initializeGame()
  }, [])

  const initializeGame = () => {
    setKeyPosition({ x: 20, y: 60 })
    setLockPosition({ x: 80, y: 50 })
    setIsInserted(false)
    setRotation(0)
    setIsUnlocked(false)
    setIsActive(false)
  }

  const startGame = () => {
    setIsActive(true)
    setStartTime(Date.now())
  }

  const handleMouseDown = (e) => {
    if (!isActive) {
      startGame()
    }
    if (isUnlocked) return

    const rect = gameContainerRef.current.getBoundingClientRect()
    const x = ((e.clientX - rect.left) / rect.width) * 100
    const y = ((e.clientY - rect.top) / rect.height) * 100

    // Verificar si se está haciendo clic en la llave
    const keyRadius = 8
    if (
      Math.abs(x - keyPosition.x) < keyRadius &&
      Math.abs(y - keyPosition.y) < keyRadius
    ) {
      setDragging(true)
      setDragOffset({
        x: x - keyPosition.x,
        y: y - keyPosition.y
      })
    }
  }

  const handleMouseMove = (e) => {
    if (!dragging || isUnlocked) return

    const rect = gameContainerRef.current.getBoundingClientRect()
    const x = ((e.clientX - rect.left) / rect.width) * 100
    const y = ((e.clientY - rect.top) / rect.height) * 100

    const newX = Math.max(5, Math.min(95, x - dragOffset.x))
    const newY = Math.max(5, Math.min(95, y - dragOffset.y))

    setKeyPosition({ x: newX, y: newY })

    // Verificar si la llave está cerca de la cerradura
    const lockRadius = 12
    if (
      Math.abs(newX - lockPosition.x) < lockRadius &&
      Math.abs(newY - lockPosition.y) < lockRadius &&
      !isInserted
    ) {
      setIsInserted(true)
      setKeyPosition({ x: lockPosition.x, y: lockPosition.y })
    }
  }

  const handleMouseUp = () => {
    setDragging(false)
  }

  const handleKeyRotate = (direction) => {
    if (!isInserted || isUnlocked) return

    const newRotation = direction === 'left' ? rotation - 15 : rotation + 15
    setRotation(newRotation)

    // Verificar si se ha girado lo suficiente (90 grados)
    if (Math.abs(newRotation) >= 90) {
      setIsUnlocked(true)
      handleComplete()
    }
  }

  useEffect(() => {
    if (dragging) {
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
      return () => {
        document.removeEventListener('mousemove', handleMouseMove)
        document.removeEventListener('mouseup', handleMouseUp)
      }
    }
  }, [dragging, keyPosition, lockPosition, isInserted])

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
          observaciones: `Cerradura abierta en ${tiempoEjecucion.toFixed(1)} segundos`
        },
        { withCredentials: true }
      )
    } catch (error) {
      console.error('Error al registrar resultado:', error)
    }

    if (onComplete) {
      onComplete({ tiempoEjecucion, unlocked: true })
    }
  }

  return (
    <div className="text-center">
      <div className="mb-4">
        <h4 className="text-primary mb-3">
          <i className="fas fa-key me-2"></i>
          Ejercicio: Abrir Cerradura
        </h4>
        <p className="text-muted">
          Arrastra la llave hacia la cerradura, luego gírala para abrirla.
          Este ejercicio mejora la motricidad fina y la destreza en tareas de precisión.
        </p>
      </div>

      <div
        ref={gameContainerRef}
        style={{
          position: 'relative',
          height: '500px',
          background: 'linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%)',
          borderRadius: '15px',
          margin: '0 auto',
          maxWidth: '600px',
          boxShadow: '0 8px 16px rgba(0, 0, 0, 0.1)',
          border: '3px solid #ffc107',
          overflow: 'hidden'
        }}
        onMouseDown={handleMouseDown}
      >
        {/* Puerta */}
        <div
          style={{
            position: 'absolute',
            top: '20%',
            left: '50%',
            transform: 'translateX(-50%)',
            width: '200px',
            height: '300px',
            background: 'linear-gradient(135deg, #8d6e63 0%, #6d4c41 100%)',
            borderRadius: '10px',
            boxShadow: 'inset 0 4px 8px rgba(0, 0, 0, 0.3), 0 6px 12px rgba(0, 0, 0, 0.2)',
            border: '4px solid #5d4037'
          }}
        >
          {/* Cerradura */}
          <div
            style={{
              position: 'absolute',
              top: '60%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              width: '80px',
              height: '80px',
              background: isUnlocked
                ? 'linear-gradient(135deg, #43a047 0%, #2e7d32 100%)'
                : 'linear-gradient(135deg, #ffc107 0%, #f57c00 100%)',
              borderRadius: '50%',
              border: '6px solid #ffffff',
              boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'all 0.5s ease',
              transform: `translate(-50%, -50%) rotate(${rotation}deg)`
            }}
          >
            {/* Agujero de la cerradura */}
            <div
              style={{
                width: '20px',
                height: '40px',
                background: '#424242',
                borderRadius: '10px',
                boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.5)'
              }}
            />
          </div>

          {/* Detalles de la puerta */}
          <div
            style={{
              position: 'absolute',
              top: '20px',
              left: '50%',
              transform: 'translateX(-50%)',
              width: '60px',
              height: '8px',
              background: '#5d4037',
              borderRadius: '4px',
              boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.3)'
            }}
          />
        </div>

        {/* Llave */}
        {!isUnlocked && (
          <div
            style={{
              position: 'absolute',
              left: `${keyPosition.x}%`,
              top: `${keyPosition.y}%`,
              transform: `translate(-50%, -50%) rotate(${isInserted ? rotation : 0}deg)`,
              width: '60px',
              height: '120px',
              cursor: dragging ? 'grabbing' : 'grab',
              transition: isInserted ? 'all 0.3s ease' : 'none',
              zIndex: 10
            }}
          >
            {/* Cabeza de la llave */}
            <div
              style={{
                width: '40px',
                height: '40px',
                background: 'linear-gradient(135deg, #ffc107 0%, #f57c00 100%)',
                borderRadius: '50%',
                border: '4px solid #ffffff',
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)',
                margin: '0 auto',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <div
                style={{
                  width: '12px',
                  height: '12px',
                  background: '#424242',
                  borderRadius: '50%'
                }}
              />
            </div>
            {/* Cuerpo de la llave */}
            <div
              style={{
                width: '12px',
                height: '80px',
                background: 'linear-gradient(135deg, #ffc107 0%, #f57c00 100%)',
                margin: '0 auto',
                borderRadius: '6px',
                boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)'
              }}
            />
            {/* Dientes de la llave */}
            <div
              style={{
                width: '20px',
                height: '20px',
                background: 'linear-gradient(135deg, #ffc107 0%, #f57c00 100%)',
                margin: '0 auto',
                borderRadius: '10px 10px 0 0',
                boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)'
              }}
            />
          </div>
        )}

        {/* Instrucciones flotantes */}
        {!isInserted && (
          <div
            style={{
              position: 'absolute',
              bottom: '20px',
              left: '50%',
              transform: 'translateX(-50%)',
              background: 'rgba(255, 193, 7, 0.9)',
              padding: '15px 25px',
              borderRadius: '25px',
              color: '#333',
              fontWeight: 'bold',
              boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)'
            }}
          >
            <i className="fas fa-hand-paper me-2"></i>
            Arrastra la llave hacia la cerradura
          </div>
        )}

        {isInserted && !isUnlocked && (
          <div
            style={{
              position: 'absolute',
              bottom: '20px',
              left: '50%',
              transform: 'translateX(-50%)',
              background: 'rgba(255, 193, 7, 0.9)',
              padding: '15px 25px',
              borderRadius: '25px',
              color: '#333',
              fontWeight: 'bold',
              boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)'
            }}
          >
            <div className="d-flex gap-3 justify-content-center">
              <button
                className="btn btn-warning"
                onClick={() => handleKeyRotate('left')}
                style={{ borderRadius: '50%', width: '50px', height: '50px' }}
              >
                <i className="fas fa-undo"></i>
              </button>
              <span className="align-self-center">Gira la llave</span>
              <button
                className="btn btn-warning"
                onClick={() => handleKeyRotate('right')}
                style={{ borderRadius: '50%', width: '50px', height: '50px' }}
              >
                <i className="fas fa-redo"></i>
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="mt-4">
        <div className="row">
          <div className="col-md-6">
            <div className="card">
              <div className="card-body">
                <h6 className="text-muted mb-1">Estado</h6>
                <h4 className={isUnlocked ? 'text-success' : 'text-warning'} style={{ marginBottom: 0 }}>
                  {isUnlocked ? (
                    <>
                      <i className="fas fa-unlock me-2"></i>Abierta
                    </>
                  ) : isInserted ? (
                    <>
                      <i className="fas fa-lock me-2"></i>Insertada
                    </>
                  ) : (
                    <>
                      <i className="fas fa-key me-2"></i>En proceso
                    </>
                  )}
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

      {isUnlocked && (
        <div className="alert alert-success mt-3">
          <strong><i className="fas fa-check-circle me-2"></i>¡Cerradura abierta!</strong>
          <br />
          Has completado el ejercicio en {startTime ? ((Date.now() - startTime) / 1000).toFixed(1) : '0.0'} segundos.
        </div>
      )}
    </div>
  )
}

export default TerapiaAbrirCerradura

