import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'

const TerapiaRompecabezas = ({ ejercicioId, onComplete }) => {
  const [pieces, setPieces] = useState([])
  const [completed, setCompleted] = useState(0)
  const [startTime, setStartTime] = useState(null)
  const [isActive, setIsActive] = useState(false)
  const [draggedPiece, setDraggedPiece] = useState(null)
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 })
  const gameContainerRef = useRef(null)

  const gridSize = 3
  const pieceSize = 80

  useEffect(() => {
    initializeGame()
  }, [])

  const initializeGame = () => {
    const newPieces = []
    const positions = []
    
    // Crear posiciones objetivo
    for (let row = 0; row < gridSize; row++) {
      for (let col = 0; col < gridSize; col++) {
        positions.push({
          row,
          col,
          targetX: 60 + col * (pieceSize + 10),
          targetY: 150 + row * (pieceSize + 10)
        })
      }
    }

    // Crear piezas con posiciones iniciales aleatorias
    positions.forEach((pos, index) => {
      newPieces.push({
        id: index,
        row: pos.row,
        col: pos.col,
        targetX: pos.targetX,
        targetY: pos.targetY,
        currentX: 50 + (index % 3) * 100,
        currentY: 400 + Math.floor(index / 3) * 100,
        completed: false,
        number: index + 1
      })
    })

    // Mezclar las piezas
    const shuffled = newPieces.sort(() => Math.random() - 0.5)
    setPieces(shuffled)
    setCompleted(0)
    setIsActive(false)
  }

  const startGame = () => {
    setIsActive(true)
    setStartTime(Date.now())
  }

  const handleMouseDown = (e, piece) => {
    if (!isActive) {
      startGame()
    }
    if (piece.completed) return

    const rect = gameContainerRef.current.getBoundingClientRect()
    setDraggedPiece(piece)
    setDragOffset({
      x: e.clientX - rect.left - piece.currentX,
      y: e.clientY - rect.top - piece.currentY
    })
  }

  const handleMouseMove = (e) => {
    if (!draggedPiece) return

    const rect = gameContainerRef.current.getBoundingClientRect()
    const newX = e.clientX - rect.left - dragOffset.x
    const newY = e.clientY - rect.top - dragOffset.y

    setPieces(prev => prev.map(p =>
      p.id === draggedPiece.id
        ? { ...p, currentX: Math.max(0, Math.min(rect.width - pieceSize, newX)), currentY: Math.max(0, Math.min(rect.height - pieceSize, newY)) }
        : p
    ))
  }

  const handleMouseUp = () => {
    if (!draggedPiece) return

    const piece = pieces.find(p => p.id === draggedPiece.id)
    const tolerance = 30

    if (
      Math.abs(piece.currentX - piece.targetX) < tolerance &&
      Math.abs(piece.currentY - piece.targetY) < tolerance
    ) {
      const newPieces = pieces.map(p =>
        p.id === piece.id
          ? { ...p, completed: true, currentX: p.targetX, currentY: p.targetY }
          : p
      )
      setPieces(newPieces)
      setCompleted(prev => {
        const newCompleted = prev + 1
        if (newCompleted === gridSize * gridSize) {
          handleComplete()
        }
        return newCompleted
      })
    }

    setDraggedPiece(null)
  }

  useEffect(() => {
    if (draggedPiece) {
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
      return () => {
        document.removeEventListener('mousemove', handleMouseMove)
        document.removeEventListener('mouseup', handleMouseUp)
      }
    }
  }, [draggedPiece, dragOffset, pieces])

  const handleComplete = async () => {
    const tiempoEjecucion = startTime ? (Date.now() - startTime) / 1000 : 0
    
    try {
      await axios.post(
        '/api/ejercicios/resultado',
        {
          ejercicio_id: ejercicioId,
          nivel: 3,
          exito: true,
          tiempo_ejecucion: tiempoEjecucion,
          puntuacion: 100,
          observaciones: `Rompecabezas completado en ${tiempoEjecucion.toFixed(1)} segundos`
        },
        { withCredentials: true }
      )
    } catch (error) {
      console.error('Error al registrar resultado:', error)
    }

    if (onComplete) {
      onComplete({ tiempoEjecucion, completed: gridSize * gridSize })
    }
  }

  return (
    <div className="text-center">
      <div className="mb-4">
        <h4 className="text-primary mb-3">
          <i className="fas fa-puzzle-piece me-2"></i>
          Ejercicio: Rompecabezas
        </h4>
        <p className="text-muted">
          Arrastra las piezas a su posición correcta para completar el rompecabezas.
          Este ejercicio mejora la organización espacial y resolución de problemas.
        </p>
      </div>

      <div
        ref={gameContainerRef}
        style={{
          position: 'relative',
          height: '600px',
          background: 'linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%)',
          borderRadius: '15px',
          margin: '0 auto',
          maxWidth: '800px',
          boxShadow: '0 8px 16px rgba(0, 0, 0, 0.1)',
          border: '3px solid #e91e63',
          overflow: 'hidden'
        }}
      >
        {/* Área objetivo del rompecabezas */}
        <div
          style={{
            position: 'absolute',
            top: '100px',
            left: '50%',
            transform: 'translateX(-50%)',
            width: gridSize * (pieceSize + 10) - 10,
            height: gridSize * (pieceSize + 10) - 10,
            border: '4px dashed #e91e63',
            borderRadius: '10px',
            background: 'rgba(233, 30, 99, 0.1)',
            display: 'grid',
            gridTemplateColumns: `repeat(${gridSize}, ${pieceSize}px)`,
            gridTemplateRows: `repeat(${gridSize}, ${pieceSize}px)`,
            gap: '10px',
            padding: '10px'
          }}
        >
          {/* Espacios vacíos para guía */}
          {Array.from({ length: gridSize * gridSize }).map((_, index) => {
            const row = Math.floor(index / gridSize)
            const col = index % gridSize
            const piece = pieces.find(p => p.row === row && p.col === col && p.completed)
            return (
              <div
                key={index}
                style={{
                  width: pieceSize,
                  height: pieceSize,
                  background: piece ? 'transparent' : 'rgba(233, 30, 99, 0.2)',
                  borderRadius: '8px',
                  border: piece ? 'none' : '2px dashed #e91e63'
                }}
              />
            )
          })}
        </div>

        {/* Piezas del rompecabezas */}
        {pieces.map((piece) => (
          <div
            key={piece.id}
            onMouseDown={(e) => handleMouseDown(e, piece)}
            style={{
              position: 'absolute',
              left: `${piece.currentX}px`,
              top: `${piece.currentY}px`,
              width: pieceSize,
              height: pieceSize,
              background: piece.completed
                ? 'linear-gradient(135deg, #43a047 0%, #2e7d32 100%)'
                : 'linear-gradient(135deg, #e91e63 0%, #c2185b 100%)',
              borderRadius: '10px',
              border: `4px solid ${piece.completed ? '#43a047' : '#ffffff'}`,
              cursor: piece.completed ? 'default' : draggedPiece?.id === piece.id ? 'grabbing' : 'grab',
              boxShadow: piece.completed
                ? '0 2px 4px rgba(0, 0, 0, 0.2)'
                : draggedPiece?.id === piece.id
                ? '0 8px 16px rgba(233, 30, 99, 0.4)'
                : '0 4px 8px rgba(0, 0, 0, 0.3)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '2rem',
              fontWeight: 'bold',
              color: 'white',
              transition: piece.completed ? 'all 0.5s ease' : 'box-shadow 0.2s ease',
              transform: draggedPiece?.id === piece.id ? 'scale(1.1) rotate(5deg)' : 'scale(1)',
              zIndex: draggedPiece?.id === piece.id ? 1000 : piece.completed ? 1 : 10,
              opacity: piece.completed ? 0.8 : 1
            }}
          >
            {piece.number}
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
              width: `${(completed / (gridSize * gridSize)) * 100}%`,
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
                  {completed} / {gridSize * gridSize}
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
          Arrastra cada pieza a su posición correcta según el número. Comienza arrastrando la primera pieza.
        </div>
      )}

      {completed === gridSize * gridSize && (
        <div className="alert alert-success mt-3">
          <strong><i className="fas fa-check-circle me-2"></i>¡Rompecabezas completado!</strong>
          <br />
          Has completado el rompecabezas en {startTime ? ((Date.now() - startTime) / 1000).toFixed(1) : '0.0'} segundos.
        </div>
      )}
    </div>
  )
}

export default TerapiaRompecabezas

