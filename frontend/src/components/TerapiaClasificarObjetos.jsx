import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'

const TerapiaClasificarObjetos = ({ ejercicioId, onComplete }) => {
  const [objects, setObjects] = useState([])
  const [categories, setCategories] = useState([])
  const [completed, setCompleted] = useState(0)
  const [startTime, setStartTime] = useState(null)
  const [isActive, setIsActive] = useState(false)
  const [draggedObject, setDraggedObject] = useState(null)
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 })
  const gameContainerRef = useRef(null)

  const categoryData = [
    { id: 'frutas', name: 'Frutas', color: '#ff9800', emoji: '🍎' },
    { id: 'herramientas', name: 'Herramientas', color: '#2196f3', emoji: '🔧' },
    { id: 'ropa', name: 'Ropa', color: '#9c27b0', emoji: '👕' }
  ]

  const objectData = [
    { id: 0, name: 'Manzana', emoji: '🍎', category: 'frutas', x: 20, y: 20 },
    { id: 1, name: 'Naranja', emoji: '🍊', category: 'frutas', x: 20, y: 35 },
    { id: 2, name: 'Plátano', emoji: '🍌', category: 'frutas', x: 20, y: 50 },
    { id: 3, name: 'Martillo', emoji: '🔨', category: 'herramientas', x: 20, y: 65 },
    { id: 4, name: 'Llave', emoji: '🔑', category: 'herramientas', x: 20, y: 80 },
    { id: 5, name: 'Destornillador', emoji: '🪛', category: 'herramientas', x: 20, y: 95 },
    { id: 6, name: 'Camisa', emoji: '👕', category: 'ropa', x: 50, y: 20 },
    { id: 7, name: 'Pantalón', emoji: '👖', category: 'ropa', x: 50, y: 35 },
    { id: 8, name: 'Zapato', emoji: '👞', category: 'ropa', x: 50, y: 50 }
  ]

  useEffect(() => {
    initializeGame()
  }, [])

  const initializeGame = () => {
    setObjects(objectData.map(obj => ({ ...obj, completed: false })))
    setCategories(categoryData.map(cat => ({ ...cat, count: 0, total: objectData.filter(o => o.category === cat.id).length })))
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
      x: e.clientX - rect.left - (object.x * rect.width / 100),
      y: e.clientY - rect.top - (object.y * rect.height / 100)
    })
  }

  const handleMouseMove = (e) => {
    if (!draggedObject) return

    const rect = gameContainerRef.current.getBoundingClientRect()
    const newX = ((e.clientX - rect.left - dragOffset.x) / rect.width) * 100
    const newY = ((e.clientY - rect.top - dragOffset.y) / rect.height) * 100

    setObjects(prev => prev.map(obj =>
      obj.id === draggedObject.id
        ? { ...obj, x: Math.max(5, Math.min(95, newX)), y: Math.max(5, Math.min(95, newY)) }
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

    // Verificar si está sobre la categoría correcta
    const category = categories.find(cat => cat.id === object.category)
    const categoryX = category.id === 'frutas' ? 80 : category.id === 'herramientas' ? 80 : 80
    const categoryY = category.id === 'frutas' ? 30 : category.id === 'herramientas' ? 50 : 70
    const tolerance = 15

    if (
      Math.abs(object.x - categoryX) < tolerance &&
      Math.abs(object.y - categoryY) < tolerance
    ) {
      const newObjects = objects.map(obj =>
        obj.id === object.id
          ? { ...obj, completed: true, x: categoryX, y: categoryY }
          : obj
      )
      setObjects(newObjects)

      const newCategories = categories.map(cat =>
        cat.id === object.category
          ? { ...cat, count: cat.count + 1 }
          : cat
      )
      setCategories(newCategories)

      setCompleted(prev => {
        const newCompleted = prev + 1
        if (newCompleted === objectData.length) {
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
  }, [draggedObject, dragOffset, objects, categories])

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
          observaciones: `Objetos clasificados en ${tiempoEjecucion.toFixed(1)} segundos`
        },
        { withCredentials: true }
      )
    } catch (error) {
      console.error('Error al registrar resultado:', error)
    }

    if (onComplete) {
      onComplete({ tiempoEjecucion, completed: objectData.length })
    }
  }

  return (
    <div className="text-center">
      <div className="mb-4">
        <h4 className="text-primary mb-3">
          <i className="fas fa-layer-group me-2"></i>
          Ejercicio: Clasificar Objetos
        </h4>
        <p className="text-muted">
          Arrastra cada objeto a su categoría correspondiente.
          Este ejercicio mejora la organización y habilidades de planificación.
        </p>
      </div>

      <div
        ref={gameContainerRef}
        style={{
          position: 'relative',
          height: '600px',
          background: 'linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)',
          borderRadius: '15px',
          margin: '0 auto',
          maxWidth: '900px',
          boxShadow: '0 8px 16px rgba(0, 0, 0, 0.1)',
          border: '3px solid #9c27b0',
          overflow: 'hidden'
        }}
      >
        {/* Categorías */}
        {categories.map((category) => (
          <div
            key={category.id}
            style={{
              position: 'absolute',
              left: `${category.id === 'frutas' ? 80 : category.id === 'herramientas' ? 80 : 80}%`,
              top: `${category.id === 'frutas' ? 30 : category.id === 'herramientas' ? 50 : 70}%`,
              transform: 'translate(-50%, -50%)',
              width: '150px',
              minHeight: '120px',
              background: `${category.color}40`,
              border: `4px solid ${category.color}`,
              borderRadius: '15px',
              padding: '15px',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)'
            }}
          >
            <div style={{ fontSize: '40px', marginBottom: '10px' }}>
              {category.emoji}
            </div>
            <div style={{ fontWeight: 'bold', color: category.color, marginBottom: '5px' }}>
              {category.name}
            </div>
            <div style={{ fontSize: '14px', color: '#666' }}>
              {category.count} / {category.total}
            </div>
          </div>
        ))}

        {/* Objetos */}
        {objects.map((object) => {
          const category = categories.find(cat => cat.id === object.category)
          const isHovered = draggedObject?.id === object.id &&
            Math.abs(object.x - 80) < 15 &&
            Math.abs(object.y - (object.category === 'frutas' ? 30 : object.category === 'herramientas' ? 50 : 70)) < 15

          return (
            <div
              key={object.id}
              onMouseDown={(e) => handleMouseDown(e, object)}
              style={{
                position: 'absolute',
                left: `${object.x}%`,
                top: `${object.y}%`,
                transform: 'translate(-50%, -50%)',
                width: '70px',
                height: '70px',
                background: object.completed
                  ? `${category.color}80`
                  : `linear-gradient(135deg, ${category.color} 0%, ${category.color}dd 100%)`,
                borderRadius: '15px',
                cursor: object.completed ? 'default' : draggedObject?.id === object.id ? 'grabbing' : 'grab',
                border: `4px solid ${object.completed ? '#43a047' : '#ffffff'}`,
                boxShadow: object.completed
                  ? '0 2px 4px rgba(0, 0, 0, 0.2)'
                  : draggedObject?.id === object.id
                  ? '0 8px 16px rgba(0, 0, 0, 0.4)'
                  : '0 4px 8px rgba(0, 0, 0, 0.3)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '30px',
                transition: object.completed ? 'all 0.5s ease' : 'box-shadow 0.2s ease',
                transform: `translate(-50%, -50%) ${draggedObject?.id === object.id ? 'scale(1.15) rotate(5deg)' : 'scale(1)'}`,
                zIndex: draggedObject?.id === object.id ? 1000 : object.completed ? 1 : 10,
                opacity: object.completed ? 0.7 : 1
              }}
            >
              <div>{object.emoji}</div>
              {object.completed && (
                <div style={{
                  position: 'absolute',
                  top: '-5px',
                  right: '-5px',
                  width: '25px',
                  height: '25px',
                  background: '#43a047',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontSize: '12px'
                }}>
                  <i className="fas fa-check"></i>
                </div>
              )}
            </div>
          )
        })}

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
              width: `${(completed / objectData.length) * 100}%`,
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
                  {completed} / {objectData.length}
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
          Arrastra cada objeto a su categoría correspondiente. Observa las características de cada objeto.
        </div>
      )}

      {completed === objectData.length && (
        <div className="alert alert-success mt-3">
          <strong><i className="fas fa-check-circle me-2"></i>¡Objetos clasificados!</strong>
          <br />
          Has clasificado todos los objetos correctamente en {startTime ? ((Date.now() - startTime) / 1000).toFixed(1) : '0.0'} segundos.
        </div>
      )}
    </div>
  )
}

export default TerapiaClasificarObjetos

