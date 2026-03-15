import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Ejercicio from './pages/Ejercicio'
import TerapiaOcupacional from './pages/TerapiaOcupacional'
import Configuracion from './pages/Configuracion'

function App() {
  return (
    <Router>
      <Routes>
        {/* Páginas sin el Layout (tienen su propio header/footer) */}
        <Route path="/dashboard" element={<Dashboard />} />

        {/* Páginas con Layout (navbar + footer) */}
        <Route path="/*" element={
          <Layout>
            <Routes>
              <Route path="/"                   element={<Home />} />
              <Route path="/login"              element={<Login />} />
              <Route path="/registro"           element={<Register />} />
              <Route path="/ejercicio/:ejercicioId" element={<Ejercicio />} />
              <Route path="/terapia-ocupacional" element={<TerapiaOcupacional />} />
              <Route path="/configuracion"      element={<Configuracion />} />
              <Route path="*"                   element={<Navigate to="/" replace />} />
            </Routes>
          </Layout>
        } />
      </Routes>
    </Router>
  )
}

export default App
