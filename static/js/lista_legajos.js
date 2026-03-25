// static/js/lista_legajos.js - CORREGIDO Y OPTIMIZADO

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
// VARIABLES GLOBALES DEL MÓDULO
// ========================================

let datosFiltrados = [];
let tabla = null;
let buscador = null;
let filtroEstado = null;
let ordenarPor = null;
let resultadosSpan = null;

// ========================================
// INICIALIZACIÓN
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    try {
        console.log('🔍 Inicializando lista de legajos...');
        
        // Obtener referencias a elementos
        tabla = obtenerElementoSeguro('tabla-legajos');
        buscador = obtenerElementoSeguro('buscador');
        filtroEstado = obtenerElementoSeguro('filtroEstado');
        ordenarPor = obtenerElementoSeguro('ordenarPor');
        resultadosSpan = obtenerElementoSeguro('resultados');
        
        if (!tabla) {
            console.warn('⚠️ Tabla de legajos no encontrada');
            return;
        }
        
        // Inicializar datos
        inicializarDatos();
        
        // Agregar event listeners
        if (buscador) {
            buscador.addEventListener('keyup', function(e) {
                try {
                    filtrar();
                } catch (error) {
                    console.error('Error en filtro por búsqueda:', error);
                }
            });
        }
        
        if (filtroEstado) {
            filtroEstado.addEventListener('change', function(e) {
                try {
                    filtrar();
                } catch (error) {
                    console.error('Error en filtro por estado:', error);
                }
            });
        }
        
        if (ordenarPor) {
            ordenarPor.addEventListener('change', function(e) {
                try {
                    ordenar();
                } catch (error) {
                    console.error('Error en ordenamiento:', error);
                }
            });
        }
        
        console.log('✅ Lista de legajos inicializada');
        
    } catch (e) {
        console.error('❌ Error en inicialización:', e);
    }
});

// ========================================
// INICIALIZAR DATOS DE LA TABLA
// ========================================

function inicializarDatos() {
    try {
        if (!tabla) return;
        
        const filas = tabla.querySelectorAll('tbody tr');
        datosFiltrados = [];
        
        filas.forEach((fila, index) => {
            try {
                const celdas = fila.querySelectorAll('td');
                if (celdas.length < 3) return;
                
                datosFiltrados.push({
                    elemento: fila,
                    legajo: celdas[0]?.innerText || '',
                    apellido: fila.dataset.apellido || (celdas[1]?.innerText || ''),
                    nombre: fila.dataset.nombre || (celdas[2]?.innerText || ''),
                    estado: fila.dataset.estado || '',
                    html: fila
                });
            } catch (error) {
                console.error('Error procesando fila:', error);
            }
        });
        
        actualizarContador();
        
    } catch (e) {
        console.error('Error inicializando datos:', e);
    }
}

// ========================================
// FILTRAR LEGAJOS
// ========================================

function filtrar() {
    try {
        if (!datosFiltrados.length) return;
        
        const texto = buscador ? buscador.value.toLowerCase() : '';
        const estado = filtroEstado ? filtroEstado.value : 'todos';
        
        datosFiltrados.forEach(item => {
            try {
                if (!item.elemento) return;
                
                const matchesTexto = texto === '' || 
                    item.legajo.toLowerCase().includes(texto) ||
                    item.apellido.toLowerCase().includes(texto) ||
                    item.nombre.toLowerCase().includes(texto);
                
                const matchesEstado = estado === 'todos' || item.estado === estado;
                
                item.elemento.style.display = matchesTexto && matchesEstado ? '' : 'none';
                
            } catch (error) {
                console.error('Error filtrando item:', error);
            }
        });
        
        actualizarContador();
        
    } catch (e) {
        console.error('Error en filtrado:', e);
    }
}

// ========================================
// ORDENAR LEGAJOS
// ========================================

function ordenar() {
    try {
        if (!tabla || !datosFiltrados.length) return;
        
        const criterio = ordenarPor ? ordenarPor.value : 'legajo';
        
        datosFiltrados.sort((a, b) => {
            try {
                if (criterio === 'legajo') {
                    return (parseInt(a.legajo) || 0) - (parseInt(b.legajo) || 0);
                } else if (criterio === 'apellido') {
                    return (a.apellido || '').localeCompare(b.apellido || '');
                } else if (criterio === 'fecha') {
                    return 0; // Implementar si hay fecha
                }
            } catch (error) {
                console.error('Error comparando items:', error);
            }
            return 0;
        });
        
        const tbody = tabla.querySelector('tbody');
        if (tbody) {
            datosFiltrados.forEach(item => {
                if (item.elemento) {
                    tbody.appendChild(item.elemento);
                }
            });
        }
        
    } catch (e) {
        console.error('Error en ordenamiento:', e);
    }
}

// ========================================
// ACTUALIZAR CONTADOR DE RESULTADOS
// ========================================

function actualizarContador() {
    try {
        if (!resultadosSpan) return;
        
        const visibles = datosFiltrados.filter(item => 
            item.elemento && item.elemento.style.display !== 'none'
        ).length;
        
        resultadosSpan.innerText = `Mostrando ${visibles} de ${datosFiltrados.length} legajos`;
        
    } catch (e) {
        console.error('Error actualizando contador:', e);
    }
}

// ========================================
// MODAL DE ELIMINACIÓN
// ========================================

let legajoAEliminar = null;

function confirmarEliminacion(legajoId) {
    try {
        legajoAEliminar = legajoId;
        const spanLegajo = obtenerElementoSeguro('legajoEliminar');
        if (spanLegajo) {
            spanLegajo.innerText = legajoId;
        }
        
        const modal = obtenerElementoSeguro('modalEliminar');
        if (modal) {
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        }
    } catch (e) {
        console.error('Error confirmando eliminación:', e);
        alert('Error al preparar eliminación');
    }
}

function cerrarModalEliminar() {
    try {
        const modal = obtenerElementoSeguro('modalEliminar');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
        legajoAEliminar = null;
    } catch (e) {
        console.error('Error cerrando modal:', e);
    }
}

function eliminarLegajo() {
    try {
        if (!legajoAEliminar) {
            alert('No hay legajo seleccionado');
            cerrarModalEliminar();
            return;
        }
        
        // Aquí iría la llamada AJAX para eliminar
        if (confirm(`¿Está seguro de eliminar el legajo ${legajoAEliminar}?`)) {
            // Implementar eliminación
            console.log('Eliminar legajo:', legajoAEliminar);
            cerrarModalEliminar();
            location.reload();
        }
    } catch (e) {
        console.error('Error eliminando legajo:', e);
        alert('Error al eliminar el legajo');
        cerrarModalEliminar();
    }
}

// ========================================
// MANEJADOR DE TECLA ESCAPE
// ========================================

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        cerrarModalEliminar();
    }
});

// ========================================
// CIERRE DE MODAL AL HACER CLIC FUERA
// ========================================

window.addEventListener('click', function(event) {
    try {
        const modal = obtenerElementoSeguro('modalEliminar');
        if (modal && event.target === modal) {
            cerrarModalEliminar();
        }
    } catch (e) {
        console.error('Error en click fuera:', e);
    }
});

console.log('📋 Módulo de lista de legajos cargado correctamente');