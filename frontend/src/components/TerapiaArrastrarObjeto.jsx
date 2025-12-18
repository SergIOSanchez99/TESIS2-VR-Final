import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'

const TerapiaArrastrarObjeto = ({ ejercicioId, onComplete }) => {
  const [objects, setObjects] = useState([])
  const [completed, setCompleted] = useState(0)
  const [startTime, setStartTime] = useState(null)
  const [isActive, setIsActive] = useState(false)
  const [draggedObject, setDraggedObject] = useState(null)
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 })
  const gameContainerRef = useRef(null)

  const objectsData = [
    { id: 0, emoji: '🥄', name: 'Cuchara', color: '#ff9800', x: 80, y: 80 },
    { id: 1, emoji: '🍴', name: 'Tenedor', color: '#2196f3', x: 80, y: 180 },
    { id: 2, emoji: '🔑', name: 'Llave', color: '#ffc107', x: 80, y: 280 },
    { id: 3, emoji: '✏️', name: 'Lápiz', color: '#9c27b0', x: 80, y: 380 }
  ]

  useEffect(() => {
    initializeGame()
  }, [])

  const initializeGame = () => {
    setObjects(objectsData.map(obj => ({ ...obj, completed: false })))
    setCompleted(0)
    setIsActive(false)
  }

  const startGame = () => {
    setIsActive(true)
    setStartTime(Date.now())
  }

  const handleMouseDown = (e, object) => {
    if (!isActive) {
      startGame()
    }
    if (object.completed) return

    const rect = gameContainerRef.current.getBoundingClientRect()
    setDraggedObject(object)
    setDragOffset({
      x: e.clientX - rect.left - object.x,
      y: e.clientY - rect.top - object.y
    })
  }

  const handleMouseMove = (e) => {
    if (!draggedObject) return

    const rect = gameContainerRef.current.getBoundingClientRect()
    const newX = e.clientX - rect.left - dragOffset.x
    const newY = e.clientY - rect.top - dragOffset.y

    setObjects(prev => prev.map(obj => 
      obj.id === draggedObject.id 
        ? { ...obj, x: Math.max(0, Math.min(rect.width - 80, newX)), y: Math.max(0, Math.min(rect.height - 80, newY)) }
        : obj
    ))
  }

  const handleMouseUp = () => {
    if (!draggedObject) return

    const object = objects.find(obj => obj.id === draggedObject.id)
    if (!object || object.completed) {
      setDraggedObject(null)
      return
    }

    // Verificar si está sobre el área objetivo correspondiente
    const targetX = 600
    const targetY = object.id * 100 + 80
    const tolerance = 60

    if (
      Math.abs(object.x - targetX) < tolerance &&
      Math.abs(object.y - targetY) < tolerance
    ) {
      const newObjects = objects.map(obj =>
        obj.id === object.id
          ? { ...obj, completed: true, x: targetX, y: targetY }
          : obj
      )
      setObjects(newObjects)
      setCompleted(prev => {
        const newCompleted = prev + 1
        if (newCompleted === objectsData.length) {
          handleComplete()
        }
        return newCompleted
      })
    }

    setDraggedObject(null)
  }

  useEffect(() => {
    if (draggedObject) {
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
      return () => {
        document.removeEventListener('mousemove', handleMouseMove)
        document.removeEventListener('mouseup', handleMouseUp)
      }
    }
  }, [draggedObject, dragOffset, objects])

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
      onComplete({ tiempoEjecucion, completed: objectsData.length })
    }
  }

  return (
    <div className="text-center">
      <div className="mb-4">
        <h4 className="text-primary mb-3">
          <i className="fas fa-hand-paper me-2"></i>
          Ejercicio: Arrastrar y Soltar Objetos
        </h4>
        <p className="text-muted">
          Arrastra cada objeto a su área de destino correspondiente. 
          Este ejercicio mejora la coordinación mano-ojo y la precisión en el posicionamiento.
        </p>
      </div>

      <div
        ref={gameContainerRef}
        style={{
          position: 'relative',
          height: '500px',
          background: 'linear-gradient(135deg, #f5f7fa 0%, #e8f0f5 100%)',
          borderRadius: '15px',
          margin: '0 auto',
          maxWidth: '900px',
          boxShadow: '0 8px 16px rgba(0, 0, 0, 0.1)',
          border: '3px solid #1976d2',
          overflow: 'hidden'
        }}
      >
        {/* Áreas objetivo */}
        {objectsData.map((objData, index) => {
          const obj = objects.find(o => o.id === objData.id)
          const isHovered = draggedObject && draggedObject.id === objData.id && 
            Math.abs(obj.x - 600) < 60 && Math.abs(obj.y - (index * 100 + 80)) < 60

          return (
            <div
              key={`target-${objData.id}`}
              style={{
                position: 'absolute',
                right: '50px',
                top: `${index * 100 + 50}px`,
                width: '120px',
                height: '100px',
                background: obj?.completed 
                  ? `${objData.color}40`
                  : isHovered
                  ? `${objData.color}30`
                  : `${objData.color}15`,
                border: `3px ${obj?.completed ? 'solid' : 'dashed'} ${objData.color}`,
                borderRadius: '15px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                transition: 'all 0.3s ease',
                transform: isHovered ? 'scale(1.05)' : 'scale(1)',
                boxShadow: obj?.completed 
                  ? `0 4px 8px ${objData.color}40`
                  : '0 2px 4px rgba(0, 0, 0, 0.1)'
              }}
            >
              <div style={{ fontSize: '32px', marginBottom: '5px' }}>
                {objData.emoji}
              </div>
              <div style={{ 
                fontSize: '12px', 
                fontWeight: 'bold', 
                color: objData.color,
                textAlign: 'center'
              }}>
                {objData.name}
              </div>
            </div>
          )
        })}

        {/* Objetos arrastrables */}
        {objects.map((obj) => (
          <div
            key={obj.id}
            onMouseDown={(e) => handleMouseDown(e, obj)}
            style={{
              position: 'absolute',
              left: `${obj.x}px`,
              top: `${obj.y}px`,
              width: '80px',
              height: '80px',
              background: obj.completed
                ? `${obj.color}80`
                : `linear-gradient(135deg, ${obj.color} 0%, ${obj.color}dd 100%)`,
              borderRadius: '15px',
              cursor: obj.completed ? 'default' : draggedObject?.id === obj.id ? 'grabbing' : 'grab',
              border: `4px solid ${obj.completed ? '#43a047' : '#ffffff'}`,
              boxShadow: obj.completed
                ? '0 2px 4px rgba(0, 0, 0, 0.2)'
                : draggedObject?.id === obj.id
                ? '0 8px 16px rgba(0, 0, 0, 0.4)'
                : '0 4px 8px rgba(0, 0, 0, 0.3)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '40px',
              transition: obj.completed ? 'all 0.5s ease' : 'box-shadow 0.2s ease',
              transform: draggedObject?.id === obj.id ? 'scale(1.1) rotate(5deg)' : 'scale(1)',
              zIndex: draggedObject?.id === obj.id ? 1000 : obj.completed ? 1 : 10,
              opacity: obj.completed ? 0.7 : 1
            }}
          >
            {/* Sombra del objeto para efecto 3D */}
            {!obj.completed && (
              <div
                style={{
                  position: 'absolute',
                  bottom: '-5px',
                  left: '10%',
                  width: '80%',
                  height: '10px',
                  background: 'rgba(0, 0, 0, 0.2)',
                  borderRadius: '50%',
                  filter: 'blur(5px)'
                }}
              />
            )}
          </div>
        ))}

        {/* Indicador de progreso */}
        <div
          style={{
            position: 'absolute',
            bottom: '20px',
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
              width: `${(completed / objectsData.length) * 100}%`,
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
                  {completed} / {objectsData.length}
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
          Haz clic y arrastra cada objeto a su área de destino correspondiente. 
          Comienza arrastrando el primer objeto.
        </div>
      )}

      {completed === objectsData.length && (
        <div className="alert alert-success mt-3">
          <strong><i className="fas fa-check-circle me-2"></i>¡Ejercicio completado!</strong>
          <br />
          Has colocado todos los objetos correctamente en {startTime ? ((Date.now() - startTime) / 1000).toFixed(1) : '0.0'} segundos.
        </div>
      )}
    </div>
  )
}

export default TerapiaArrastrarObjeto

