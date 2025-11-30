// Funcionalidades JavaScript para el Sistema de Rehabilitación

document.addEventListener("DOMContentLoaded", function () {
  // Inicializar tooltips de Bootstrap
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Inicializar popovers de Bootstrap
  var popoverTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="popover"]')
  );
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });

  // Animaciones de entrada
  animateElements();

  // Configurar formularios
  setupForms();

  // Configurar notificaciones
  setupNotifications();
});

// Función para animar elementos al cargar la página
function animateElements() {
  const elements = document.querySelectorAll(
    ".card, .exercise-card, .therapy-exercise"
  );
  elements.forEach((element, index) => {
    setTimeout(() => {
      element.classList.add("fade-in");
    }, index * 100);
  });
}

// Configurar formularios con validación mejorada
function setupForms() {
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.innerHTML = '<span class="loading"></span> Procesando...';
        submitBtn.disabled = true;
      }
    });
  });
}

// Sistema de notificaciones
// Definir funciones globales primero
window.showSuccess = function (message) {
  showNotification(message, "success");
};

window.showError = function (message) {
  showNotification(message, "danger");
};

window.showInfo = function (message) {
  showNotification(message, "info");
};

function setupNotifications() {
  // Las funciones ya están definidas globalmente arriba
}

// Función para mostrar notificaciones
function showNotification(message, type = "info") {
  const notification = document.createElement("div");
  notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
  notification.style.cssText =
    "top: 20px; right: 20px; z-index: 9999; min-width: 300px;";
  notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

  document.body.appendChild(notification);

  // Auto-remover después de 5 segundos
  setTimeout(() => {
    if (notification.parentNode) {
      notification.remove();
    }
  }, 5000);
}

// Función para actualizar estadísticas en tiempo real
function updateStats() {
  const statsElements = document.querySelectorAll("[data-stat]");
  statsElements.forEach((element) => {
    const statType = element.getAttribute("data-stat");
    const currentValue = parseInt(element.textContent) || 0;

    // Simular actualización de estadísticas
    if (statType === "ejercicios") {
      element.textContent = currentValue + Math.floor(Math.random() * 3);
    } else if (statType === "tiempo") {
      element.textContent = currentValue + Math.floor(Math.random() * 10);
    }
  });
}

// Función para manejar el progreso de ejercicios
function updateProgress(progress) {
  const progressBars = document.querySelectorAll(".progress-bar");
  progressBars.forEach((bar) => {
    bar.style.width = progress + "%";
    bar.setAttribute("aria-valuenow", progress);
    bar.textContent = progress + "%";
  });
}

// Función para guardar preferencias del usuario
function saveUserPreferences() {
  const preferences = {
    theme: document.body.getAttribute("data-theme") || "light",
    fontSize: document.body.getAttribute("data-font-size") || "medium",
    soundEnabled: localStorage.getItem("soundEnabled") === "true",
  };

  localStorage.setItem("userPreferences", JSON.stringify(preferences));
}

// Función para cargar preferencias del usuario
function loadUserPreferences() {
  const preferences = JSON.parse(
    localStorage.getItem("userPreferences") || "{}"
  );

  if (preferences.theme) {
    document.body.setAttribute("data-theme", preferences.theme);
  }

  if (preferences.fontSize) {
    document.body.setAttribute("data-font-size", preferences.fontSize);
  }
}

// Función para manejar el modo oscuro/claro
function toggleTheme() {
  const currentTheme = document.body.getAttribute("data-theme") || "light";
  const newTheme = currentTheme === "light" ? "dark" : "light";

  document.body.setAttribute("data-theme", newTheme);
  saveUserPreferences();

  showNotification(
    `Modo ${newTheme === "dark" ? "oscuro" : "claro"} activado`,
    "info"
  );
}

// Función para manejar el tamaño de fuente
function changeFontSize(size) {
  document.body.setAttribute("data-font-size", size);
  saveUserPreferences();

  const sizeNames = {
    small: "pequeño",
    medium: "mediano",
    large: "grande",
  };

  showNotification(`Tamaño de fuente cambiado a ${sizeNames[size]}`, "info");
}

// Función para exportar datos del usuario
function exportUserData() {
  const userData = {
    timestamp: new Date().toISOString(),
    user: sessionStorage.getItem("currentUser"),
    preferences: JSON.parse(localStorage.getItem("userPreferences") || "{}"),
  };

  const dataStr = JSON.stringify(userData, null, 2);
  const dataBlob = new Blob([dataStr], { type: "application/json" });

  const link = document.createElement("a");
  link.href = URL.createObjectURL(dataBlob);
  link.download = "user_data.json";
  link.click();

  showNotification("Datos exportados correctamente", "success");
}

// Función para manejar la accesibilidad
function setupAccessibility() {
  // Agregar navegación por teclado
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      // Cerrar modales o popovers
      const modals = document.querySelectorAll(".modal.show");
      modals.forEach((modal) => {
        const modalInstance = bootstrap.Modal.getInstance(modal);
        if (modalInstance) {
          modalInstance.hide();
        }
      });
    }
  });

  // Mejorar contraste para usuarios con problemas de visión
  const highContrastBtn = document.getElementById("high-contrast");
  if (highContrastBtn) {
    highContrastBtn.addEventListener("click", function () {
      document.body.classList.toggle("high-contrast");
      showNotification(
        "Modo alto contraste " +
          (document.body.classList.contains("high-contrast")
            ? "activado"
            : "desactivado"),
        "info"
      );
    });
  }
}

// Función para manejar el tiempo de sesión
function setupSessionTimer() {
  let sessionTime = 0;
  const sessionTimer = setInterval(() => {
    sessionTime++;
    const hours = Math.floor(sessionTime / 3600);
    const minutes = Math.floor((sessionTime % 3600) / 60);
    const seconds = sessionTime % 60;

    const timeDisplay = document.getElementById("session-time");
    if (timeDisplay) {
      timeDisplay.textContent = `${hours.toString().padStart(2, "0")}:${minutes
        .toString()
        .padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
    }
  }, 1000);

  return sessionTimer;
}

// Inicializar funcionalidades adicionales
document.addEventListener("DOMContentLoaded", function () {
  loadUserPreferences();
  setupAccessibility();

  // Configurar botones de tema si existen
  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", toggleTheme);
  }

  // Configurar botones de tamaño de fuente
  const fontSizeBtns = document.querySelectorAll("[data-font-size]");
  fontSizeBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      changeFontSize(this.getAttribute("data-font-size"));
    });
  });

  // Configurar exportación de datos
  const exportBtn = document.getElementById("export-data");
  if (exportBtn) {
    exportBtn.addEventListener("click", exportUserData);
  }

  // Iniciar temporizador de sesión en el dashboard
  if (window.location.pathname === "/dashboard") {
    setupSessionTimer();
  }

  // Exportar funciones para uso global después de que todo esté inicializado
  window.RehabSystem = {
    showSuccess: window.showSuccess,
    showError: window.showError,
    showInfo: window.showInfo,
    updateStats,
    updateProgress,
    toggleTheme,
    changeFontSize,
    exportUserData,
  };
});
