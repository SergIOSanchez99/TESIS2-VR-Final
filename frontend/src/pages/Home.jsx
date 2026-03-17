import React from 'react'
import { Link } from 'react-router-dom'

const createSvgDataUri = (svg) => `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`

const heroIllustration = createSvgDataUri(`
  <svg width="720" height="520" viewBox="0 0 720 520" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="720" height="520" rx="36" fill="#F4FBFF"/>
    <circle cx="118" cy="104" r="64" fill="#D8F3FF"/>
    <circle cx="608" cy="92" r="54" fill="#E9F9F2"/>
    <rect x="72" y="108" width="576" height="320" rx="28" fill="white"/>
    <rect x="72" y="108" width="576" height="320" rx="28" stroke="#D7EAF5" stroke-width="4"/>
    <rect x="108" y="150" width="180" height="230" rx="22" fill="#E7F7FF"/>
    <circle cx="198" cy="214" r="44" fill="#9ADCF7"/>
    <path d="M154 317C154 285.52 179.52 260 211 260H214C245.48 260 271 285.52 271 317V334H154V317Z" fill="#4FAFD1"/>
    <rect x="330" y="154" width="270" height="42" rx="18" fill="#F3F9FC"/>
    <rect x="330" y="216" width="232" height="18" rx="9" fill="#DAEEF8"/>
    <rect x="330" y="250" width="195" height="18" rx="9" fill="#DAEEF8"/>
    <rect x="330" y="284" width="248" height="18" rx="9" fill="#DAEEF8"/>
    <rect x="330" y="330" width="118" height="48" rx="18" fill="#37C98B"/>
    <rect x="466" y="330" width="118" height="48" rx="18" fill="#0EB7DA"/>
    <path d="M461 436C520.095 436 568 388.095 568 329C568 269.905 520.095 222 461 222C401.905 222 354 269.905 354 329C354 388.095 401.905 436 461 436Z" fill="#F7FBFD"/>
    <path d="M460 407C503.078 407 538 372.078 538 329C538 285.922 503.078 251 460 251C416.922 251 382 285.922 382 329C382 372.078 416.922 407 460 407Z" stroke="#BFE2F1" stroke-width="22"/>
    <path d="M460 407C503.078 407 538 372.078 538 329" stroke="#0EB7DA" stroke-width="22" stroke-linecap="round"/>
    <circle cx="461" cy="329" r="16" fill="#0A6C88"/>
    <path d="M575 155L593 173L626 140" stroke="#37C98B" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
`)

const calmIllustration = createSvgDataUri(`
  <svg width="520" height="360" viewBox="0 0 520 360" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="520" height="360" rx="28" fill="#F7FCFF"/>
    <rect x="44" y="44" width="432" height="272" rx="24" fill="white" stroke="#DDECF4" stroke-width="3"/>
    <circle cx="142" cy="133" r="46" fill="#CDEFFF"/>
    <path d="M96 226C96 197.281 119.281 174 148 174H152C180.719 174 204 197.281 204 226V244H96V226Z" fill="#58B4D7"/>
    <rect x="244" y="92" width="182" height="22" rx="11" fill="#D7EEF9"/>
    <rect x="244" y="130" width="156" height="18" rx="9" fill="#E7F5FB"/>
    <rect x="244" y="160" width="130" height="18" rx="9" fill="#E7F5FB"/>
    <rect x="244" y="212" width="148" height="52" rx="18" fill="#EBFFF6"/>
    <path d="M281 238L303 259L355 209" stroke="#39C58C" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
`)

const progressIllustration = createSvgDataUri(`
  <svg width="520" height="360" viewBox="0 0 520 360" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="520" height="360" rx="28" fill="#F8FCFF"/>
    <rect x="48" y="52" width="424" height="256" rx="22" fill="white" stroke="#DDECF4" stroke-width="3"/>
    <path d="M106 246H414" stroke="#DCECF5" stroke-width="10" stroke-linecap="round"/>
    <path d="M106 206H414" stroke="#EDF6FB" stroke-width="10" stroke-linecap="round"/>
    <path d="M106 166H414" stroke="#EDF6FB" stroke-width="10" stroke-linecap="round"/>
    <path d="M122 233L190 184L248 198L324 126L390 150" stroke="#0EB7DA" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="190" cy="184" r="14" fill="#39C58C"/>
    <circle cx="324" cy="126" r="14" fill="#39C58C"/>
    <rect x="118" y="96" width="120" height="36" rx="14" fill="#E8F8FF"/>
    <rect x="256" y="96" width="108" height="36" rx="14" fill="#ECFFF6"/>
    <rect x="376" y="96" width="46" height="36" rx="14" fill="#FFF3D6"/>
  </svg>
`)

const therapyIllustration = createSvgDataUri(`
  <svg width="520" height="360" viewBox="0 0 520 360" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="520" height="360" rx="28" fill="#F7FCFE"/>
    <circle cx="380" cy="102" r="60" fill="#DDF7EC"/>
    <rect x="50" y="56" width="420" height="248" rx="24" fill="white" stroke="#D9ECF4" stroke-width="3"/>
    <rect x="86" y="108" width="148" height="148" rx="26" fill="#E9F7FF"/>
    <path d="M129 160C129 142.327 143.327 128 161 128H162C179.673 128 194 142.327 194 160V172H129V160Z" fill="#54B0D4"/>
    <rect x="273" y="110" width="154" height="22" rx="11" fill="#D6EEF8"/>
    <rect x="273" y="146" width="116" height="18" rx="9" fill="#E7F5FB"/>
    <rect x="273" y="178" width="132" height="18" rx="9" fill="#E7F5FB"/>
    <rect x="273" y="218" width="118" height="44" rx="16" fill="#0EB7DA"/>
    <path d="M340 202C369.823 202 394 177.823 394 148C394 118.177 369.823 94 340 94C310.177 94 286 118.177 286 148C286 177.823 310.177 202 340 202Z" stroke="#BDE4F3" stroke-width="18"/>
    <path d="M340 202C369.823 202 394 177.823 394 148" stroke="#39C58C" stroke-width="18" stroke-linecap="round"/>
  </svg>
`)

const heroStats = [
  { value: 'Simple', label: 'Interfaz clara y sin saturacion' },
  { value: 'Guiada', label: 'Pasos faciles de seguir' },
  { value: 'Motivadora', label: 'Progreso visible en cada sesion' },
]

const imageCards = [
  {
    image: calmIllustration,
    title: 'Ambiente visual tranquilo',
    description: 'Colores suaves, bloques claros y una navegacion pensada para reducir la carga visual y transmitir confianza.',
  },
  {
    image: therapyIllustration,
    title: 'Ejercicios que se sienten cercanos',
    description: 'La plataforma acompana al paciente con mensajes sencillos y accesos rapidos a sus actividades de rehabilitacion.',
  },
  {
    image: progressIllustration,
    title: 'Avances faciles de entender',
    description: 'El progreso se presenta de forma amigable para que cada usuario vea su mejora sin complicaciones.',
  },
]

const benefits = [
  {
    icon: 'fas fa-heart',
    title: 'Diseno amable para pacientes',
    description: 'Cada seccion prioriza claridad, tranquilidad y una lectura comoda para personas de distintas edades.',
  },
  {
    icon: 'fas fa-hand-pointer',
    title: 'Interaccion intuitiva',
    description: 'Botones grandes, jerarquia visual limpia y acciones principales visibles desde el primer momento.',
  },
  {
    icon: 'fas fa-chart-line',
    title: 'Motivacion constante',
    description: 'Los elementos visuales ayudan a reforzar la sensacion de avance y a mantener el interes en la terapia.',
  },
  {
    icon: 'fas fa-hands-helping',
    title: 'Confianza y acompanamiento',
    description: 'La interfaz transmite cercania y apoyo para que el paciente se sienta guiado durante su proceso.',
  },
]

const steps = [
  {
    number: '1',
    title: 'Crea tu cuenta',
    description: 'Ingresa al sistema de forma rapida y segura para comenzar tu seguimiento personalizado.',
  },
  {
    number: '2',
    title: 'Explora tus ejercicios',
    description: 'Encuentra rutinas adaptadas a tus necesidades en una pantalla simple y facil de recorrer.',
  },
  {
    number: '3',
    title: 'Realiza tu sesion',
    description: 'Sigue las indicaciones visuales y completa cada actividad con una experiencia mas agradable.',
  },
  {
    number: '4',
    title: 'Revisa tu avance',
    description: 'Observa tus logros y mantente motivado con una vista de progreso limpia y entendible.',
  },
]

const Home = () => {
  return (
    <div className="patient-home">
        <section className="patient-home__hero">
          <div className="container">
            <div className="row align-items-center g-5">
              <div className="col-lg-6">
                <span className="patient-home__eyebrow rehavr-anim-fadein">
                  <i className="fas fa-heartbeat"></i>
                  Rehabilitacion con una experiencia mas humana
                </span>

                <h1 className="patient-home__title">
                  Un espacio claro, calido y motivador para avanzar en tu recuperacion
                </h1>

                <p className="patient-home__subtitle">
                  Nuestro sistema de rehabilitacion motora combina ejercicios interactivos,
                  acompanamiento visual y seguimiento de progreso en una interfaz minimalista
                  y agradable para pacientes.
                </p>

                <div className="patient-home__actions">
                  <Link to="/registro" className="btn btn-primary btn-lg">
                    <i className="fas fa-user-plus me-2"></i>
                    Crear cuenta
                  </Link>

                  <Link to="/login" className="btn patient-home__secondary-btn btn-lg">
                    <i className="fas fa-sign-in-alt me-2"></i>
                    Iniciar sesion
                  </Link>
                </div>

                <div className="row g-3">
                  {heroStats.map(({ value, label }) => (
                    <div key={label} className="col-md-4 col-sm-6">
                      <div className="patient-home__stat">
                        <span className="patient-home__stat-value">{value}</span>
                        <span className="patient-home__stat-label">{label}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="col-lg-6">
                <div className="patient-home__visual">
                  <div className="patient-home__glow"></div>
                  <img
                    src={heroIllustration}
                    alt="Ilustracion de seguimiento y rehabilitacion"
                    className="patient-home__main-image"
                  />

                  <div className="patient-home__floating-card patient-home__floating-card--progress">
                    <span className="patient-home__floating-icon">
                      <i className="fas fa-chart-line"></i>
                    </span>
                    <span>
                      <span className="patient-home__floating-title">Progreso visible</span>
                      <span className="patient-home__floating-copy">Indicadores simples y faciles de entender</span>
                    </span>
                  </div>

                  <div className="patient-home__floating-card patient-home__floating-card--support">
                    <span className="patient-home__floating-icon">
                      <i className="fas fa-hands-helping"></i>
                    </span>
                    <span>
                      <span className="patient-home__floating-title">Experiencia cercana</span>
                      <span className="patient-home__floating-copy">Pensada para dar confianza en cada sesion</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="py-5">
          <div className="container">
            <div className="patient-home__section-heading text-center">
              <h2>Una portada mas amable para comenzar</h2>
              <p>
                Esta interfaz busca que el paciente sienta orden, calma y cercania desde
                el primer vistazo, con imagenes relacionadas al proceso de rehabilitacion
                y detalles visuales modernos.
              </p>
            </div>

            <div className="row g-4">
              {imageCards.map(({ image, title, description }) => (
                <div key={title} className="col-lg-4">
                  <article className="patient-home__image-card">
                    <img src={image} alt={title} className="patient-home__image" />
                    <div className="patient-home__image-card-body">
                      <span className="patient-home__kicker">
                        <i className="fas fa-star"></i>
                        Experiencia visual
                      </span>
                      <h3 className="h4 mb-3">{title}</h3>
                      <p className="mb-0">{description}</p>
                    </div>
                  </article>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="pb-5">
          <div className="container">
            <div className="patient-home__section-heading text-center">
              <h2>Beneficios de una interfaz mas clara</h2>
              <p>
                El objetivo no es solo que se vea moderna, sino que ayude a los pacientes
                a sentirse comodos usando el sistema todos los dias.
              </p>
            </div>

            <div className="row g-4">
              {benefits.map(({ icon, title, description }) => (
                <div key={title} className="col-md-6 col-xl-3">
                  <article className="patient-home__benefit">
                    <span className="patient-home__benefit-icon">
                      <i className={icon}></i>
                    </span>
                    <h3 className="h5 mb-3">{title}</h3>
                    <p className="mb-0">{description}</p>
                  </article>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="patient-home__steps-section py-5">
          <div className="container">
            <div className="patient-home__section-heading text-center">
              <h2>Comenzar es muy sencillo</h2>
              <p>
                La experiencia esta organizada en pasos claros para que cualquier paciente
                pueda ubicarse rapidamente dentro del sistema.
              </p>
            </div>

            <div className="row g-4">
              {steps.map(({ number, title, description }) => (
                <div key={number} className="col-md-6 col-xl-3">
                  <article className="patient-home__step">
                    <span className="patient-home__step-number">{number}</span>
                    <h3 className="h5 mb-3">{title}</h3>
                    <p className="mb-0">{description}</p>
                  </article>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="py-5">
          <div className="container">
            <div className="patient-home__cta">
              <div className="row align-items-center g-4">
                <div className="col-lg-7">
                  <span className="patient-home__kicker">
                    <i className="fas fa-play-circle"></i>
                    Empieza hoy
                  </span>
                  <h2 className="display-6 mb-3">
                    Una experiencia sencilla para concentrarte en lo importante: tu recuperacion
                  </h2>
                  <p className="mb-4">
                    Crea tu cuenta, explora tus actividades y vive un proceso de rehabilitacion
                    con una interfaz moderna, ligera y agradable de usar.
                  </p>
                  <div className="d-flex flex-wrap gap-3">
                    <Link to="/registro" className="btn btn-primary btn-lg">
                      <i className="fas fa-rocket me-2"></i>
                      Comenzar ahora
                    </Link>
                    <Link to="/login" className="btn patient-home__secondary-btn btn-lg">
                      <i className="fas fa-arrow-right me-2"></i>
                      Ya tengo cuenta
                    </Link>
                  </div>
                </div>

                <div className="col-lg-5">
                  <img
                    src={progressIllustration}
                    alt="Panel visual de avance del paciente"
                    className="patient-home__cta-image"
                  />
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
  )
}

export default Home

