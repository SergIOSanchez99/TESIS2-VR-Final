import React, { useRef, useEffect, useState } from 'react'
import axios from 'axios'

const EjercicioCanvas = ({ ejercicioId, nivel, onComplete }) => {
  const canvasRef = useRef(null)
  const [gameState, setGameState] = useState('ready') // ready, playing, completed
  const [score, setScore] = useState(0)
  const [hits, setHits] = useState(0)
  const [misses, setMisses] = useState(0)
  const [combo, setCombo] = useState(0)
  const [maxCombo, setMaxCombo] = useState(0)
  const [timeLeft, setTimeLeft] = useState(60)
  const [precision, setPrecision] = useState(0)
  const [startTime, setStartTime] = useState(null)
  
  // Posiciones y estados del juego - Tamaños más grandes para VR
  const targetRef = useRef({ x: 500, y: 300, vx: 0, vy: 0, size: nivel === 1 ? 60 : nivel === 2 ? 55 : 50, pulse: 0, color: '#1976d2', alpha: 1.0 })
  const particlesRef = useRef([])
  const animationFrameRef = useRef(null)
  const timerIntervalRef = useRef(null)
  const lastHitTimeRef = useRef(0)
  
  // Métricas avanzadas
  const metricsRef = useRef({
    totalClicks: 0,
    totalDistance: 0,
    reactionTimes: [],
    movementHistory: [],
    lastClickPos: { x: 0, y: 0 },
    startTime: 0,
    minX: Infinity,
    maxX: -Infinity,
    minY: Infinity,
    maxY: -Infinity
  })

  // Configurar velocidad según nivel
  useEffect(() => {
    if (nivel === 1) {
      targetRef.current.vx = 0
      targetRef.current.vy = 0
    } else if (nivel === 2) {
      targetRef.current.vx = (Math.random() - 0.5) * 2
      targetRef.current.vy = (Math.random() - 0.5) * 2
    } else if (nivel === 3) {
      targetRef.current.vx = (Math.random() - 0.5) * 5
      targetRef.current.vy = (Math.random() - 0.5) * 5
    }
    targetRef.current.x = 500
    targetRef.current.y = 300
  }, [nivel])

  // Timer
  useEffect(() => {
    if (gameState === 'playing') {
      timerIntervalRef.current = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            handleGameComplete()
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

  const createParticles = (x, y, color) => {
    for (let i = 0; i < 15; i++) {
      particlesRef.current.push({
        x: x,
        y: y,
        vx: (Math.random() - 0.5) * 8,
        vy: (Math.random() - 0.5) * 8,
        size: Math.random() * 5 + 2,
        life: 1,
        color: color
      })
    }
  }

  const moveTarget = () => {
    const target = targetRef.current
    if (nivel === 1) return

    const margin = target.size
    const bounceDamping = 0.8

    target.x += target.vx
    target.y += target.vy

    if (target.x <= margin || target.x >= 1000 - margin) {
      target.vx *= -bounceDamping
      target.x = Math.max(margin, Math.min(1000 - margin, target.x))
      if (nivel === 3) {
        target.vy += (Math.random() - 0.5) * 2
      }
    }

    if (target.y <= margin || target.y >= 600 - margin) {
      target.vy *= -bounceDamping
      target.y = Math.max(margin, Math.min(600 - margin, target.y))
      if (nivel === 3) {
        target.vx += (Math.random() - 0.5) * 2
      }
    }

    if (nivel === 3) {
      if (Math.random() < 0.02) {
        target.vx += (Math.random() - 0.5) * 3
        target.vy += (Math.random() - 0.5) * 3
      }
      const maxSpeed = 8
      const speed = Math.sqrt(target.vx * target.vx + target.vy * target.vy)
      if (speed > maxSpeed) {
        target.vx = (target.vx / speed) * maxSpeed
        target.vy = (target.vy / speed) * maxSpeed
      }
    }

    metricsRef.current.minX = Math.min(metricsRef.current.minX, target.x)
    metricsRef.current.maxX = Math.max(metricsRef.current.maxX, target.x)
    metricsRef.current.minY = Math.min(metricsRef.current.minY, target.y)
    metricsRef.current.maxY = Math.max(metricsRef.current.maxY, target.y)
  }

  const checkHit = (mouseX, mouseY, currentCombo) => {
    const target = targetRef.current
    const metrics = metricsRef.current
    
    metrics.totalClicks++
    const distance = Math.sqrt(
      Math.pow(mouseX - target.x, 2) + Math.pow(mouseY - target.y, 2)
    )

    const clickDistance = Math.sqrt(
      Math.pow(mouseX - metrics.lastClickPos.x, 2) +
      Math.pow(mouseY - metrics.lastClickPos.y, 2)
    )
    metrics.totalDistance += clickDistance
    metrics.lastClickPos = { x: mouseX, y: mouseY }
    metrics.movementHistory.push({ x: mouseX, y: mouseY })
    if (metrics.movementHistory.length > 50) {
      metrics.movementHistory.shift()
    }

    if (distance <= target.size) {
      const newCombo = currentCombo + 1
      setCombo(newCombo)
      setMaxCombo(prevMax => Math.max(prevMax, newCombo))

      const currentTime = Date.now()
      if (lastHitTimeRef.current > 0) {
        const reactionTime = currentTime - lastHitTimeRef.current
        metrics.reactionTimes.push(reactionTime)
      }
      lastHitTimeRef.current = currentTime

      const baseScore = nivel * 10
      const comboMultiplier = 1 + (newCombo * 0.1)
      setScore(prev => prev + Math.floor(baseScore * comboMultiplier))

      createParticles(target.x, target.y, '#43a047')
      target.color = '#43a047'
      setTimeout(() => {
        target.color = '#1976d2'
      }, 200)

      target.x = Math.random() * (1000 - 2 * target.size) + target.size
      target.y = Math.random() * (600 - 2 * target.size) + target.size

      if (nivel === 2) {
        target.vx = (Math.random() - 0.5) * 2
        target.vy = (Math.random() - 0.5) * 2
      } else if (nivel === 3) {
        target.vx = (Math.random() - 0.5) * 5
        target.vy = (Math.random() - 0.5) * 5
      }

      return true
    } else {
      setCombo(0)
      createParticles(mouseX, mouseY, '#dc3545')
      return false
    }
  }

  const handleGameComplete = async () => {
    setGameState('completed')
    const metrics = metricsRef.current
    const tiempoEjecucion = startTime ? (Date.now() - startTime) / 1000 : 60
    
    const totalAttempts = hits + misses
    const precisionValue = totalAttempts > 0 ? (hits / totalAttempts) * 100 : 0
    const success = precisionValue >= (nivel === 1 ? 60 : nivel === 2 ? 50 : 40) && hits >= (nivel * 3)

    const elapsed = (Date.now() - metrics.startTime) / 1000
    const avgSpeed = elapsed > 0 ? metrics.totalDistance / elapsed : 0
    const movementRange = Math.max(
      metrics.maxX !== -Infinity ? metrics.maxX - metrics.minX : 0,
      metrics.maxY !== -Infinity ? metrics.maxY - metrics.minY : 0
    )
    const avgReactionTime = metrics.reactionTimes.length > 0
      ? metrics.reactionTimes.reduce((a, b) => a + b, 0) / metrics.reactionTimes.length
      : 0
    const consistency = metrics.reactionTimes.length > 1
      ? 100 - (Math.sqrt(metrics.reactionTimes.reduce((sum, rt) => {
          const avg = metrics.reactionTimes.reduce((a, b) => a + b, 0) / metrics.reactionTimes.length
          return sum + Math.pow(rt - avg, 2)
        }, 0) / metrics.reactionTimes.length) / avgReactionTime * 100)
      : 100

    const observaciones = JSON.stringify({
      precision: precisionValue.toFixed(2),
      avgSpeed: avgSpeed.toFixed(1),
      movementRange: movementRange.toFixed(0),
      avgReactionTime: avgReactionTime.toFixed(0),
      hitRate: (hits / totalAttempts * 100).toFixed(2),
      consistency: consistency.toFixed(1),
      maxCombo: maxCombo
    })

    try {
      await axios.post(
        '/api/ejercicios/resultado',
        {
          ejercicio_id: ejercicioId,
          nivel: nivel,
          exito: success,
          tiempo_ejecucion: tiempoEjecucion,
          puntuacion: score,
          observaciones: observaciones,
          precision: precisionValue,
          velocidad_promedio: avgSpeed,
          rango_movimiento: movementRange,
          tiempo_reaccion_promedio: avgReactionTime,
          tasa_aciertos: hits / totalAttempts * 100,
          consistencia: consistency,
          combo_maximo: maxCombo,
          aciertos: hits,
          fallos: misses
        },
        { withCredentials: true }
      )
    } catch (error) {
      console.error('Error al registrar resultado:', error)
    }

    if (onComplete) {
      onComplete({ score, hits, tiempoEjecucion, precision: precisionValue })
    }
  }

  const startGame = () => {
    if (gameState !== 'ready') return
    setGameState('playing')
    setStartTime(Date.now())
    metricsRef.current.startTime = Date.now()
  }

  // Manejo de clics
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const handleClick = (e) => {
      if (gameState === 'ready') {
        startGame()
        return
      }

      if (gameState !== 'playing') return

      const rect = canvas.getBoundingClientRect()
      const mouseX = e.clientX - rect.left
      const mouseY = e.clientY - rect.top

      const wasHit = checkHit(mouseX, mouseY, combo)
      
      if (wasHit) {
        setHits(prev => prev + 1)
      } else {
        setMisses(prev => prev + 1)
      }
    }

    canvas.addEventListener('click', handleClick)
    return () => {
      canvas.removeEventListener('click', handleClick)
    }
  }, [gameState, nivel, combo])

  // Actualizar precisión cuando cambian hits o misses
  useEffect(() => {
    const totalAttempts = hits + misses
    if (totalAttempts > 0) {
      setPrecision((hits / totalAttempts) * 100)
    }
  }, [hits, misses])

  // Loop de animación
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    const width = canvas.width
    const height = canvas.height

    const draw = () => {
      // Fondo más realista y amigable para VR - Colores suaves y profesionales
      const gradient = ctx.createLinearGradient(0, 0, width, height)
      gradient.addColorStop(0, '#e8f4f8')
      gradient.addColorStop(0.5, '#f0f8ff')
      gradient.addColorStop(1, '#e6f2ff')
      ctx.fillStyle = gradient
      ctx.fillRect(0, 0, width, height)

      // Cuadrícula más sutil para no distraer en VR
      ctx.strokeStyle = 'rgba(200, 220, 240, 0.3)'
      ctx.lineWidth = 1
      for (let i = 0; i < width; i += 80) {
        ctx.beginPath()
        ctx.moveTo(i, 0)
        ctx.lineTo(i, height)
        ctx.stroke()
      }
      for (let i = 0; i < height; i += 80) {
        ctx.beginPath()
        ctx.moveTo(0, i)
        ctx.lineTo(width, i)
        ctx.stroke()
      }

      if (gameState === 'ready') {
        ctx.fillStyle = '#333'
        ctx.font = '30px Arial'
        ctx.textAlign = 'center'
        ctx.fillText('Haz clic para comenzar', width / 2, height / 2)
        
        // Dibujar objetivo incluso antes de empezar - Sin parpadeo, diseño realista
        const target = targetRef.current
        
        // Glow suave y constante (sin parpadeo)
        const glowGradient = ctx.createRadialGradient(
          target.x, target.y, 0,
          target.x, target.y, target.size + 15
        )
        glowGradient.addColorStop(0, 'rgba(25, 118, 210, 0.4)')
        glowGradient.addColorStop(0.5, 'rgba(25, 118, 210, 0.2)')
        glowGradient.addColorStop(1, 'rgba(25, 118, 210, 0)')
        ctx.fillStyle = glowGradient
        ctx.beginPath()
        ctx.arc(target.x, target.y, target.size + 15, 0, 2 * Math.PI)
        ctx.fill()

        // Círculo exterior con sombra suave
        ctx.shadowBlur = 15
        ctx.shadowColor = 'rgba(25, 118, 210, 0.5)'
        ctx.fillStyle = target.color
        ctx.beginPath()
        ctx.arc(target.x, target.y, target.size, 0, 2 * Math.PI)
        ctx.fill()
        ctx.shadowBlur = 0

        // Borde blanco grueso para mejor visibilidad en VR
        ctx.strokeStyle = '#ffffff'
        ctx.lineWidth = 5
        ctx.beginPath()
        ctx.arc(target.x, target.y, target.size, 0, 2 * Math.PI)
        ctx.stroke()

        // Círculo interior para profundidad
        ctx.strokeStyle = '#1976d2'
        ctx.lineWidth = 3
        ctx.beginPath()
        ctx.arc(target.x, target.y, target.size * 0.7, 0, 2 * Math.PI)
        ctx.stroke()

        // Centro sólido y visible
        ctx.fillStyle = '#ffffff'
        ctx.beginPath()
        ctx.arc(target.x, target.y, target.size * 0.3, 0, 2 * Math.PI)
        ctx.fill()

        animationFrameRef.current = requestAnimationFrame(draw)
        return
      }

      if (gameState === 'playing') {
        moveTarget()

        const target = targetRef.current

        // Glow suave y constante (sin parpadeo) - Diseño realista para VR
        const glowGradient = ctx.createRadialGradient(
          target.x, target.y, 0,
          target.x, target.y, target.size + 15
        )
        glowGradient.addColorStop(0, 'rgba(25, 118, 210, 0.4)')
        glowGradient.addColorStop(0.5, 'rgba(25, 118, 210, 0.2)')
        glowGradient.addColorStop(1, 'rgba(25, 118, 210, 0)')
        ctx.fillStyle = glowGradient
        ctx.beginPath()
        ctx.arc(target.x, target.y, target.size + 15, 0, 2 * Math.PI)
        ctx.fill()

        // Círculo principal con sombra suave para profundidad realista
        ctx.shadowBlur = 15
        ctx.shadowColor = 'rgba(25, 118, 210, 0.5)'
        ctx.fillStyle = target.color
        ctx.beginPath()
        ctx.arc(target.x, target.y, target.size, 0, 2 * Math.PI)
        ctx.fill()
        ctx.shadowBlur = 0

        // Borde blanco grueso para mejor visibilidad en VR
        ctx.strokeStyle = '#ffffff'
        ctx.lineWidth = 5
        ctx.beginPath()
        ctx.arc(target.x, target.y, target.size, 0, 2 * Math.PI)
        ctx.stroke()

        // Círculo interior para dar profundidad visual
        ctx.strokeStyle = '#1976d2'
        ctx.lineWidth = 3
        ctx.beginPath()
        ctx.arc(target.x, target.y, target.size * 0.7, 0, 2 * Math.PI)
        ctx.stroke()

        // Centro sólido y visible - más grande para VR
        ctx.fillStyle = '#ffffff'
        ctx.beginPath()
        ctx.arc(target.x, target.y, target.size * 0.3, 0, 2 * Math.PI)
        ctx.fill()

        // Dibujar partículas
        particlesRef.current = particlesRef.current.filter(particle => {
          particle.x += particle.vx
          particle.y += particle.vy
          particle.life -= 0.02
          particle.size *= 0.98

          if (particle.life <= 0) return false

          ctx.save()
          ctx.globalAlpha = particle.life
          ctx.fillStyle = particle.color
          ctx.beginPath()
          ctx.arc(particle.x, particle.y, particle.size, 0, 2 * Math.PI)
          ctx.fill()
          ctx.restore()

          return true
        })

        // Dibujar trail del cursor más sutil para VR
        const metrics = metricsRef.current
        if (metrics.movementHistory.length > 0) {
          ctx.strokeStyle = 'rgba(25, 118, 210, 0.2)'
          ctx.lineWidth = 3
          ctx.lineCap = 'round'
          ctx.lineJoin = 'round'
          ctx.beginPath()
          ctx.moveTo(metrics.movementHistory[0].x, metrics.movementHistory[0].y)
          for (let i = 1; i < metrics.movementHistory.length; i++) {
            ctx.lineTo(metrics.movementHistory[i].x, metrics.movementHistory[i].y)
          }
          ctx.stroke()
        }
      }

      if (gameState === 'completed') {
        ctx.fillStyle = '#27ae60'
        ctx.font = '40px Arial'
        ctx.textAlign = 'center'
        ctx.fillText('¡Ejercicio Completado!', width / 2, height / 2 - 40)
        ctx.font = '24px Arial'
        ctx.fillText(`Puntuación: ${score}`, width / 2, height / 2)
        ctx.fillText(`Aciertos: ${hits}`, width / 2, height / 2 + 40)
        ctx.fillText(`Precisión: ${precision.toFixed(1)}%`, width / 2, height / 2 + 80)
      }
    }

    const animate = () => {
      draw()
      if (gameState === 'playing' || gameState === 'ready') {
        animationFrameRef.current = requestAnimationFrame(animate)
      }
    }

    animate()

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
    }
  }, [gameState, nivel, score, hits, precision])

  const totalAttempts = hits + misses
  const avgSpeed = startTime && gameState === 'playing' 
    ? ((Date.now() - startTime) / 1000 > 0 ? metricsRef.current.totalDistance / ((Date.now() - startTime) / 1000) : 0).toFixed(1)
    : 0
  const movementRange = Math.max(
    metricsRef.current.maxX !== -Infinity ? metricsRef.current.maxX - metricsRef.current.minX : 0,
    metricsRef.current.maxY !== -Infinity ? metricsRef.current.maxY - metricsRef.current.minY : 0
  ).toFixed(0)
  const avgReactionTime = metricsRef.current.reactionTimes.length > 0
    ? (metricsRef.current.reactionTimes.reduce((a, b) => a + b, 0) / metricsRef.current.reactionTimes.length).toFixed(0)
    : 0
  const hitRate = totalAttempts > 0 ? ((hits / totalAttempts) * 100).toFixed(1) : 0
  const consistency = metricsRef.current.reactionTimes.length > 1
    ? (100 - (Math.sqrt(metricsRef.current.reactionTimes.reduce((sum, rt) => {
        const avg = metricsRef.current.reactionTimes.reduce((a, b) => a + b, 0) / metricsRef.current.reactionTimes.length
        return sum + Math.pow(rt - avg, 2)
      }, 0) / metricsRef.current.reactionTimes.length) / (metricsRef.current.reactionTimes.reduce((a, b) => a + b, 0) / metricsRef.current.reactionTimes.length) * 100)).toFixed(1)
    : 100

  return (
    <div className="text-center">
      <div className="mb-3">
        <div className="row">
          <div className="col-md-3">
            <div className="card">
              <div className="card-body">
                <h6 className="text-muted mb-1">Tiempo</h6>
                <h4 className="text-primary mb-0">{timeLeft}s</h4>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card">
              <div className="card-body">
                <h6 className="text-muted mb-1">Puntuación</h6>
                <h4 className="text-success mb-0">{score}</h4>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card">
              <div className="card-body">
                <h6 className="text-muted mb-1">Aciertos</h6>
                <h4 className="text-info mb-0">{hits}</h4>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card">
              <div className="card-body">
                <h6 className="text-muted mb-1">Precisión</h6>
                <h4 className="text-warning mb-0">{precision.toFixed(1)}%</h4>
              </div>
            </div>
          </div>
        </div>
      </div>

      {combo > 2 && (
        <div className="alert alert-warning mb-3">
          <strong>Combo x{combo}!</strong>
        </div>
      )}
      
      <canvas
        ref={canvasRef}
        width={1000}
        height={600}
        style={{
          border: '4px solid #1976d2',
          borderRadius: '15px',
          cursor: 'crosshair',
          backgroundColor: '#f0f8ff',
          boxShadow: '0 8px 16px rgba(0, 0, 0, 0.1)',
          maxWidth: '100%',
          height: 'auto'
        }}
      />
      
      <div className="mt-3">
        <div className="card">
          <div className="card-header bg-light">
            <h5 className="mb-0">
              <i className="fas fa-chart-line me-2"></i>Métricas de Rehabilitación
            </h5>
          </div>
          <div className="card-body">
            <div className="row">
              <div className="col-md-6">
                <div className="d-flex justify-content-between mb-2">
                  <span className="fw-bold">Velocidad Promedio:</span>
                  <span className="text-primary">{avgSpeed} px/s</span>
                </div>
                <div className="d-flex justify-content-between mb-2">
                  <span className="fw-bold">Rango de Movimiento:</span>
                  <span className="text-primary">{movementRange} px</span>
                </div>
                <div className="d-flex justify-content-between mb-2">
                  <span className="fw-bold">Tiempo de Reacción:</span>
                  <span className="text-primary">{avgReactionTime} ms</span>
                </div>
              </div>
              <div className="col-md-6">
                <div className="d-flex justify-content-between mb-2">
                  <span className="fw-bold">Tasa de Aciertos:</span>
                  <span className="text-primary">{hitRate}%</span>
                </div>
                <div className="d-flex justify-content-between mb-2">
                  <span className="fw-bold">Consistencia:</span>
                  <span className="text-primary">{consistency}%</span>
                </div>
                <div className="d-flex justify-content-between mb-2">
                  <span className="fw-bold">Combo Máximo:</span>
                  <span className="text-primary">{maxCombo}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-3">
        {gameState === 'ready' && (
          <div className="alert alert-info" style={{ fontSize: '1.1rem', padding: '1rem' }}>
            <strong><i className="fas fa-info-circle me-2"></i>Instrucciones del Ejercicio:</strong>
            <br />
            {nivel === 1 && '• Nivel Principiante: El objetivo permanece estático. Toca el círculo azul con precisión.'}
            {nivel === 2 && '• Nivel Intermedio: El objetivo se mueve lentamente. Sigue el movimiento y toca el círculo azul.'}
            {nivel === 3 && '• Nivel Avanzado: El objetivo se mueve rápidamente. Requiere máxima concentración y precisión.'}
            <br />
            <strong>Haz clic en cualquier parte del área de juego para comenzar el ejercicio de rehabilitación.</strong>
          </div>
        )}
        {gameState === 'playing' && (
          <div className="alert alert-success" style={{ fontSize: '1rem', padding: '0.75rem' }}>
            <strong><i className="fas fa-hand-pointer me-2"></i>Ejercicio en curso:</strong> Toca el objetivo azul con precisión para completar el ejercicio de rehabilitación motora.
          </div>
        )}
        {gameState === 'completed' && (
          <div className="alert alert-success">
            <strong>¡Ejercicio completado!</strong> Puntuación: {score} | Aciertos: {hits} | Precisión: {precision.toFixed(1)}%
          </div>
        )}
      </div>
    </div>
  )
}

export default EjercicioCanvas
