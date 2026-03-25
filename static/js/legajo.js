// static/js/legajo.js - VERSIÓN CORREGIDA Y OPTIMIZADA

// ========================================
// FUNCIONES DE UTILIDAD SEGURAS
// ========================================

// Función segura para obtener elemento por ID
function obtenerElementoSeguro(id) {
    const elemento = document.getElementById(id);
    if (!elemento) {
        console.warn(`Elemento con ID '${id}' no encontrado`);
    }
    return elemento;
}

// Función segura para mostrar/ocultar elementos
function setElementDisplay(id, display) {
    const elemento = obtenerElementoSeguro(id);
    if (elemento) {
        elemento.style.display = display;
    }
}

// Función segura para establecer texto
function setElementText(id, texto) {
    const elemento = obtenerElementoSeguro(id);
    if (elemento) {
        elemento.innerText = texto;
    }
}

// Función segura para establecer valor
function setElementValue(id, valor) {
    const elemento = obtenerElementoSeguro(id);
    if (elemento) {
        elemento.value = valor;
    }
}

// ========================================
// MODAL DE SUBIDA DE DOCUMENTOS
// ========================================

function mostrarModalSubida(tipo, nombre) {
    try {
        setElementValue('campoTipo', tipo);
        setElementText('tipoSeleccionado', nombre);
        setElementText('modalTitulo', 'Subir ' + nombre);
        setElementDisplay('modalSubida', 'block');
        document.body.style.overflow = 'hidden';
    } catch (e) {
        console.error('Error mostrando modal:', e);
        alert('Error al abrir el modal. Intente nuevamente.');
    }
}

function cerrarModal() {
    try {
        setElementDisplay('modalSubida', 'none');
        document.body.style.overflow = 'auto';
    } catch (e) {
        console.error('Error cerrando modal:', e);
    }
}

// ========================================
// MODAL DE ANULACIÓN DE DOCUMENTOS
// ========================================

function anularDocumento(docId, docNombre) {
    try {
        if (confirm(`¿Está seguro de anular el documento "${docNombre}"?\n\nEsta acción no se puede deshacer.`)) {
            setElementValue('docIdAnular', docId);
            setElementText('docNombreAnular', docNombre);
            setElementDisplay('modalAnular', 'block');
            document.body.style.overflow = 'hidden';
        }
    } catch (e) {
        console.error('Error en anulación:', e);
        alert('Error al procesar la anulación');
    }
}

function confirmarAnulacion() {
    try {
        const motivo = document.getElementById('motivoAnulacion')?.value;
        
        if (!motivo || !motivo.trim()) {
            alert('Debe ingresar un motivo de anulación');
            return;
        }
        
        const formAnular = document.getElementById('formAnular');
        if (formAnular) {
            formAnular.submit();
        } else {
            alert('Error: Formulario de anulación no encontrado');
        }
    } catch (e) {
        console.error('Error confirmando anulación:', e);
        alert('Error al confirmar la anulación');
    }
}

function cerrarModalAnular() {
    try {
        setElementDisplay('modalAnular', 'none');
        document.body.style.overflow = 'auto';
    } catch (e) {
        console.error('Error cerrando modal de anulación:', e);
    }
}

// ========================================
// IMPRESIÓN DE DOCUMENTOS
// ========================================

function imprimirDocumento(url) {
    try {
        const ventana = window.open(url, '_blank');
        if (ventana) {
            ventana.onload = function() {
                setTimeout(() => {
                    ventana.print();
                }, 500);
            };
        } else {
            alert('Por favor, permita ventanas emergentes para imprimir');
        }
    } catch (e) {
        console.error('Error imprimiendo documento:', e);
        alert('Error al imprimir el documento');
    }
}

// ========================================
// PROGRESO DE SUBIDA
// ========================================

function mostrarProgreso(porcentaje, estado) {
    try {
        setElementDisplay('progresoSubida', 'block');
        const barra = document.getElementById('barraProgreso');
        if (barra) {
            barra.style.width = porcentaje + '%';
        }
        setElementText('estadoSubida', estado);
    } catch (e) {
        console.error('Error mostrando progreso:', e);
    }
}

// ========================================
// SUBIDA DE DOCUMENTOS CON AJAX
// ========================================

function subirDocumento(event) {
    event.preventDefault();
    
    try {
        const formSubida = document.getElementById('formSubida');
        if (!formSubida) {
            alert('Error: Formulario no encontrado');
            return false;
        }
        
        const formData = new FormData(formSubida);
        const xhr = new XMLHttpRequest();
        
        xhr.upload.addEventListener('progress', function(e) {
            try {
                if (e.lengthComputable) {
                    const porcentaje = Math.round((e.loaded / e.total) * 100);
                    mostrarProgreso(porcentaje, 'Subiendo...');
                }
            } catch (error) {
                console.error('Error en progreso:', error);
            }
        });
        
        xhr.addEventListener('load', function() {
            try {
                if (xhr.status === 200) {
                    const respuesta = JSON.parse(xhr.responseText);
                    if (respuesta.success) {
                        mostrarProgreso(100, '¡Completado!');
                        setTimeout(() => {
                            cerrarModal();
                            location.reload();
                        }, 1000);
                    } else {
                        alert('Error: ' + (respuesta.error || 'Error desconocido'));
                        cerrarModal();
                    }
                } else {
                    alert('Error en la subida del documento (Código: ' + xhr.status + ')');
                    cerrarModal();
                }
            } catch (error) {
                console.error('Error procesando respuesta:', error);
                alert('Error al procesar la respuesta del servidor');
                cerrarModal();
            }
        });
        
        xhr.addEventListener('error', function() {
            alert('Error de conexión al subir el documento');
            cerrarModal();
        });
        
        xhr.open('POST', formSubida.action, true);
        xhr.send(formData);
        
    } catch (e) {
        console.error('Error en subida:', e);
        alert('Error al iniciar la subida del documento');
    }
    
    return false;
}

// ========================================
// CIERRE DE MODALES CON TECLA ESCAPE
// ========================================

function manejarTeclaEscape(e) {
    if (e.key === 'Escape') {
        cerrarModal();
        cerrarModalAnular();
    }
}

// ========================================
// CIERRE DE MODALES CLIC FUERA
// ========================================

function manejarClickFuera(event) {
    try {
        const modalSubida = document.getElementById('modalSubida');
        const modalAnular = document.getElementById('modalAnular');
        
        if (modalSubida && event.target === modalSubida) {
            cerrarModal();
        }
        if (modalAnular && event.target === modalAnular) {
            cerrarModalAnular();
        }
    } catch (e) {
        console.error('Error manejando click fuera:', e);
    }
}

// ========================================
// INICIALIZACIÓN
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    try {
        // Event listener para tecla Escape
        document.addEventListener('keydown', manejarTeclaEscape);
        
        // Event listener para click fuera del modal
        window.onclick = manejarClickFuera;
        
        // Inicializar formulario de subida
        const formSubida = document.getElementById('formSubida');
        if (formSubida) {
            // Remover event listeners anteriores para evitar duplicados
            formSubida.onsubmit = null;
            // Agregar nuevo event listener
            formSubida.addEventListener('submit', subirDocumento);
        }
        
        console.log('✅ Sistema de documentos inicializado correctamente');
        
    } catch (e) {
        console.error('Error en inicialización:', e);
    }
});

// ========================================
// FUNCIONES ADICIONALES DE SEGURIDAD
// ========================================

// Limpiar formularios al cerrar modales
function limpiarFormularioSubida() {
    try {
        const form = document.getElementById('formSubida');
        if (form) {
            form.reset();
        }
        setElementDisplay('progresoSubida', 'none');
        const barra = document.getElementById('barraProgreso');
        if (barra) {
            barra.style.width = '0%';
        }
    } catch (e) {
        console.error('Error limpiando formulario:', e);
    }
}

// Sobrescribir cerrarModal para incluir limpieza
const cerrarModalOriginal = cerrarModal;
cerrarModal = function() {
    limpiarFormularioSubida();
    cerrarModalOriginal();
};

// ========================================
// EXPORTAR FUNCIONES PARA USO GLOBAL
// ========================================

// Las funciones ya están en el ámbito global
console.log('📁 Módulo de gestión de documentos cargado');