// Panel principal - Dashboard

// static/js/panel.js - CORREGIDO Y OPTIMIZADO

// ========================================
// FUNCIONES DE UTILIDAD SEGURAS
// ========================================

function obtenerElementoSeguro(id) {
    const elemento = document.getElementById(id);
    if (!elemento) {
        console.warn(`⚠️ Elemento con ID '${id}' no encontrado`);
    }
    return elemento;
}

function setElementText(id, texto) {
    const elemento = obtenerElementoSeguro(id);
    if (elemento) {
        elemento.innerText = texto;
    }
}

// ========================================
// RELOJ EN TIEMPO REAL
// ========================================

function actualizarReloj() {
    try {
        const ahora = new Date();
        const opciones = {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        };
        const horaLocal = ahora.toLocaleTimeString('es-AR', opciones);
        setElementText('reloj', horaLocal);
    } catch (e) {
        console.error('Error actualizando reloj:', e);
    }
}

// ========================================
// NOTIFICACIONES VÍA AJAX
// ========================================

function cargarNotificaciones() {
    try {
        fetch('/api/notificaciones')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const contador = obtenerElementoSeguro('notificaciones-contador');
                if (contador && data.total > 0) {
                    contador.innerText = data.total;
                    contador.style.display = 'inline';
                } else if (contador) {
                    contador.style.display = 'none';
                }
            })
            .catch(error => {
                console.warn('⚠️ Error cargando notificaciones (no crítico):', error);
                // No mostrar alerta al usuario, es solo informativo
            });
    } catch (e) {
        console.error('Error en cargarNotificaciones:', e);
    }
}

// ========================================
// ACTUALIZACIÓN DE ESTADÍSTICAS
// ========================================

function actualizarEstadisticas() {
    try {
        // Esta función puede llamarse periódicamente si es necesario
        console.log('📊 Estadísticas actualizadas');
    } catch (e) {
        console.error('Error actualizando estadísticas:', e);
    }
}

// ========================================
// CARGA DE GRÁFICOS (si los hay)
// ========================================

function inicializarGraficos() {
    try {
        // Aquí iría código de gráficos si existieran
        console.log('📈 Inicializando gráficos...');
    } catch (e) {
        console.error('Error inicializando gráficos:', e);
    }
}

// ========================================
// INICIALIZACIÓN
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    try {
        console.log('🚀 Inicializando panel de control...');
        
        // Iniciar reloj
        actualizarReloj();
        setInterval(() => {
            try {
                actualizarReloj();
            } catch (e) {
                console.error('Error en intervalo del reloj:', e);
            }
        }, 1000);
        
        // Cargar notificaciones
        setTimeout(() => {
            try {
                cargarNotificaciones();
            } catch (e) {
                console.error('Error cargando notificaciones:', e);
            }
        }, 500);
        
        // Actualizar estadísticas cada 30 segundos
        setInterval(() => {
            try {
                actualizarEstadisticas();
            } catch (e) {
                console.error('Error actualizando estadísticas:', e);
            }
        }, 30000);
        
        // Inicializar gráficos si existen
        inicializarGraficos();
        
        console.log('✅ Panel de control inicializado correctamente');
        
    } catch (e) {
        console.error('❌ Error en inicialización del panel:', e);
    }
});

// ========================================
// FUNCIONES PARA TARJETAS DEL DASHBOARD
// ========================================

function irALegajo(legajoId) {
    try {
        if (legajoId) {
            window.location.href = `/legajo/${legajoId}`;
        }
    } catch (e) {
        console.error('Error navegando a legajo:', e);
    }
}

function refrescarDashboard() {
    try {
        location.reload();
    } catch (e) {
        console.error('Error refrescando dashboard:', e);
    }
}

console.log('📊 Módulo de panel cargado correctamente');