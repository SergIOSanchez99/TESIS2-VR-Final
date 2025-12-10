import React, { useRef, useEffect, useState } from 'react'
import axios from 'axios'

const EjercicioCanvas = ({ ejercicioId, nivel, onComplete }) => {
  const canvasRef = useRef(null)
  const [gameState, setGameState] = useState('ready') // ready, playing, completed
  const [score, setScore] = useState(0)
  const [hits, setHits] = useState(0)
  const [timeLeft, setTimeLeft] = useState(60)
  const [startTime, setStartTime] = useState(null)
  
  // Posiciones y estados del juego
  const handPosRef = useRef({ x: 300, y: 200 })
  const targetPosRef = useRef({ x: 400, y: 200 })
  const targetVelocityRef = useRef({ x: 0, y: 0 })
  const keysRef = useRef({})
  const animationFrameRef = useRef(null)
  const timerIntervalRef = useRef(null)

  // Configurar velocidad según nivel
  useEffect(() => {
    if (nivel === 1) {
      targetVelocityRef.current = { x: 0, y: 0 } // Estático
    } else if (nivel === 2) {
      targetVelocityRef.current = { x: 2, y: 1.5 } // Movimiento lento
    } else if (nivel === 3) {
      targetVelocityRef.current = { x: 5, y: 4 } // Movimiento rápido
    }
  }, [nivel])

  // Manejo de teclado
  useEffect(() => {
    const handleKeyDown = (e) => {
      keysRef.current[e.key] = true
    }

    const handleKeyUp = (e) => {
      keysRef.current[e.key] = false
    }

    const handleKeyPress = (e) => {
      if (e.key === ' ' && gameState === 'ready') {
        setGameState('playing')
        setStartTime(Date.now())
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    window.addEventListener('keyup', handleKeyUp)
    window.addEventListener('keypress', handleKeyPress)

    return () => {
      window.removeEventListener('keydown', handleKeyDown)
      window.removeEventListener('keyup', handleKeyUp)
      window.removeEventListener('keypress', handleKeyPress)
    }
  }, [gameState])

  // Timer
  useEffect(() => {
    if (gameState === 'playing') {
      timerIntervalRef.current = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            return 0
          }
          return prev - 1
        })
      }, 1000)
    } else {
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current)
      }
    }

    return () => {
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current)
      }
    }
  }, [gameState])

  // Verificar tiempo agotado
  useEffect(() => {
    if (timeLeft === 0 && gameState === 'playing') {
      handleGameComplete()
    }
  }, [timeLeft, gameState])

  const handleGameComplete = async () => {
    setGameState('completed')
    const tiempoEjecucion = startTime ? (Date.now() - startTime) / 1000 : 0
    
    // Enviar resultado al backend
    try {
      await axios.post(
        '/api/ejercicios/resultado',
        {
          ejercicio_id: ejercicioId,
          exito: hits > 0,
          tiempo_ejecucion: tiempoEjecucion,
          puntuacion: score,
          observaciones: `Nivel ${nivel} completado con ${hits} aciertos`
        },
        { withCredentials: true }
      )
    } catch (error) {
      console.error('Error al registrar resultado:', error)
    }

    if (onComplete) {
      onComplete({ score, hits, tiempoEjecucion })
    }
  }

  // Loop de animación
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    const width = canvas.width
    const height = canvas.height

    const draw = () => {
      // Limpiar canvas
      ctx.fillStyle = '#f0f0f0'
      ctx.fillRect(0, 0, width, height)

      if (gameState === 'ready') {
        // Dibujar pantalla de inicio
        ctx.fillStyle = '#333'
        ctx.font = '30px Arial'
        ctx.textAlign = 'center'
        ctx.fillText('Presiona ESPACIO para comenzar', width / 2, height / 2)
        return
      }

      if (gameState === 'playing') {
        // Actualizar posición de la mano con las teclas
        const speed = 5
        let newX = handPosRef.current.x
        let newY = handPosRef.current.y

        if (keysRef.current['ArrowUp'] || keysRef.current['w'] || keysRef.current['W']) {
          newY = Math.max(20, handPosRef.current.y - speed)
        }
        if (keysRef.current['ArrowDown'] || keysRef.current['s'] || keysRef.current['S']) {
          newY = Math.min(height - 20, handPosRef.current.y + speed)
        }
        if (keysRef.current['ArrowLeft'] || keysRef.current['a'] || keysRef.current['A']) {
          newX = Math.max(20, handPosRef.current.x - speed)
        }
        if (keysRef.current['ArrowRight'] || keysRef.current['d'] || keysRef.current['D']) {
          newX = Math.min(width - 20, handPosRef.current.x + speed)
        }

        handPosRef.current = { x: newX, y: newY }

        // Actualizar posición del objetivo (si se mueve)
        if (nivel > 1) {
          let newTargetX = targetPosRef.current.x + targetVelocityRef.current.x
          let newTargetY = targetPosRef.current.y + targetVelocityRef.current.y

          // Rebotar en los bordes
          if (newTargetX <= 30 || newTargetX >= width - 30) {
            targetVelocityRef.current.x = -targetVelocityRef.current.x
            newTargetX = targetPosRef.current.x
          }
          if (newTargetY <= 30 || newTargetY >= height - 30) {
            targetVelocityRef.current.y = -targetVelocityRef.current.y
            newTargetY = targetPosRef.current.y
          }

          targetPosRef.current = { x: newTargetX, y: newTargetY }
        }

        // Dibujar objetivo (círculo rojo)
        ctx.fillStyle = '#e74c3c'
        ctx.beginPath()
        ctx.arc(targetPosRef.current.x, targetPosRef.current.y, 30, 0, Math.PI * 2)
        ctx.fill()
        ctx.strokeStyle = '#c0392b'
        ctx.lineWidth = 3
        ctx.stroke()

        // Dibujar mano (círculo azul)
        ctx.fillStyle = '#3498db'
        ctx.beginPath()
        ctx.arc(handPosRef.current.x, handPosRef.current.y, 20, 0, Math.PI * 2)
        ctx.fill()
        ctx.strokeStyle = '#2980b9'
        ctx.lineWidth = 2
        ctx.stroke()

        // Verificar colisión
        const distance = Math.sqrt(
          Math.pow(handPosRef.current.x - targetPosRef.current.x, 2) + 
          Math.pow(handPosRef.current.y - targetPosRef.current.y, 2)
        )
        if (distance < 50) {
          // Colisión detectada
          setHits(prev => prev + 1)
          setScore(prev => prev + 10)
          
          // Reposicionar objetivo
          targetPosRef.current = {
            x: Math.random() * (width - 60) + 30,
            y: Math.random() * (height - 60) + 30
          }
        }
      }

      if (gameState === 'completed') {
        // Dibujar pantalla de finalización
        ctx.fillStyle = '#27ae60'
        ctx.font = '40px Arial'
        ctx.textAlign = 'center'
        ctx.fillText('¡Ejercicio Completado!', width / 2, height / 2 - 40)
        ctx.font = '24px Arial'
        ctx.fillText(`Puntuación: ${score}`, width / 2, height / 2)
        ctx.fillText(`Aciertos: ${hits}`, width / 2, height / 2 + 40)
      }
    }

    const animate = () => {
      draw()
      if (gameState === 'playing') {
        animationFrameRef.current = requestAnimationFrame(animate)
      }
    }

    if (gameState === 'playing' || gameState === 'ready' || gameState === 'completed') {
      animate()
    }

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
    }
  }, [gameState, nivel, score, hits])

  return (
    <div className="text-center">
      <div className="mb-3">
        <div className="row">
          <div className="col-md-4">
            <div className="card">
              <div className="card-body">
                <h6 className="text-muted mb-1">Tiempo</h6>
                <h4 className="text-primary mb-0">{timeLeft}s</h4>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card">
              <div className="card-body">
                <h6 className="text-muted mb-1">Puntuación</h6>
                <h4 className="text-success mb-0">{score}</h4>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card">
              <div className="card-body">
                <h6 className="text-muted mb-1">Aciertos</h6>
                <h4 className="text-info mb-0">{hits}</h4>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <canvas
        ref={canvasRef}
        width={800}
        height={500}
        style={{
          border: '3px solid #3498db',
          borderRadius: '10px',
          cursor: 'crosshair',
          backgroundColor: '#f8f9fa'
        }}
      />
      
      <div className="mt-3">
        {gameState === 'ready' && (
          <div className="alert alert-info">
            <strong>Instrucciones:</strong> Usa las flechas del teclado o WASD para mover la mano azul.
            Toca el objetivo rojo para ganar puntos. Presiona ESPACIO para comenzar.
          </div>
        )}
        {gameState === 'playing' && (
          <div className="alert alert-warning">
            <strong>En juego:</strong> Mueve la mano azul (círculo azul) hacia el objetivo rojo (círculo rojo).
          </div>
        )}
        {gameState === 'completed' && (
          <div className="alert alert-success">
            <strong>¡Ejercicio completado!</strong> Puntuación: {score} | Aciertos: {hits}
          </div>
        )}
      </div>
    </div>
  )
}

export default EjercicioCanvas
