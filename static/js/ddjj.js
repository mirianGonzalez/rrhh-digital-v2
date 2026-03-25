// static/js/ddjj.js - CORREGIDO Y OPTIMIZADO

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

function setElementValue(id, valor) {
    const elemento = obtenerElementoSeguro(id);
    if (elemento) {
        elemento.value = valor;
    }
}

// ========================================
// VARIABLES GLOBALES
// ========================================

let pasoActual = 1;
const totalPasos = 9;

// ========================================
// INICIALIZACIÓN
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    try {
        console.log('📄 Inicializando módulo de DDJJ...');
        
        // Inicializar Select2 si existe
        if (typeof $ !== 'undefined' && $.fn && $.fn.select2) {
            try {
                $('.select2').select2({
                    width: '100%'
                });
            } catch (error) {
                console.warn('⚠️ Error inicializando Select2:', error);
            }
        }
        
        // Inicializar autocompletado de edad
        inicializarAutocompletadoEdad();
        
        // Inicializar cálculo de antigüedad
        inicializarCalculoAntiguedad();
        
        console.log('✅ Módulo de DDJJ inicializado');
        
    } catch (e) {
        console.error('❌ Error en inicialización:', e);
    }
});

// ========================================
// NAVEGACIÓN ENTRE PASOS
// ========================================

function cambiarPaso(direccion) {
    try {
        const nuevoPaso = pasoActual + direccion;
        if (nuevoPaso < 1 || nuevoPaso > totalPasos) return;
        
        // Ocultar paso actual
        const pasoActualEl = document.querySelector(`.form-step[data-step="${pasoActual}"]`);
        const stepEl = document.querySelector(`.step[data-step="${pasoActual}"]`);
        
        if (pasoActualEl) pasoActualEl.style.display = 'none';
        if (stepEl) stepEl.classList.remove('active');
        
        // Mostrar nuevo paso
        pasoActual = nuevoPaso;
        const nuevoPasoEl = document.querySelector(`.form-step[data-step="${pasoActual}"]`);
        const nuevoStepEl = document.querySelector(`.step[data-step="${pasoActual}"]`);
        
        if (nuevoPasoEl) nuevoPasoEl.style.display = 'block';
        if (nuevoStepEl) nuevoStepEl.classList.add('active');
        
        // Actualizar barra de progreso
        const progreso = (pasoActual / totalPasos) * 100;
        const barraProgreso = document.querySelector('.progress-bar-fill');
        if (barraProgreso) {
            barraProgreso.style.width = progreso + '%';
        }
        
        // Actualizar botones
        const btnAnterior = obtenerElementoSeguro('btnAnterior');
        if (btnAnterior) {
            btnAnterior.disabled = (pasoActual === 1);
        }
        
        const btnSiguiente = obtenerElementoSeguro('btnSiguiente');
        if (btnSiguiente) {
            btnSiguiente.style.display = (pasoActual === totalPasos) ? 'none' : 'inline-block';
        }
        
        // Scroll al inicio
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
    } catch (e) {
        console.error('Error cambiando paso:', e);
    }
}

// ========================================
// VALIDACIÓN DE FORMULARIO
// ========================================

function validarFormularioDDJJ() {
    try {
        const pasoActualEl = document.querySelector(`.form-step[data-step="${pasoActual}"]`);
        if (!pasoActualEl) return true;
        
        const requireds = pasoActualEl.querySelectorAll('[required]');
        for (let input of requireds) {
            if (!input.value.trim()) {
                alert('Complete todos los campos requeridos (marcados con *)');
                input.focus();
                return false;
            }
        }
        return true;
    } catch (e) {
        console.error('Error validando formulario:', e);
        return true;
    }
}

// ========================================
// CÁLCULO DE EDAD
// ========================================

function calcularEdad(fechaNacimiento) {
    try {
        if (!fechaNacimiento) return '';
        
        const hoy = new Date();
        const nacimiento = new Date(fechaNacimiento);
        let edad = hoy.getFullYear() - nacimiento.getFullYear();
        const mes = hoy.getMonth() - nacimiento.getMonth();
        
        if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
            edad--;
        }
        
        return edad.toString();
    } catch (e) {
        console.error('Error calculando edad:', e);
        return '';
    }
}

function inicializarAutocompletadoEdad() {
    try {
        document.querySelectorAll('[name$="_fecha_nacimiento"]').forEach(input => {
            input.addEventListener('change', function() {
                try {
                    const parent = this.closest('.familiar-card');
                    if (parent) {
                        const edadInput = parent.querySelector('[name$="_edad"]');
                        if (edadInput && this.value) {
                            edadInput.value = calcularEdad(this.value);
                        }
                    }
                } catch (error) {
                    console.error('Error autocompletando edad:', error);
                }
            });
        });
    } catch (e) {
        console.error('Error inicializando autocompletado de edad:', e);
    }
}

// ========================================
// CÁLCULO DE ANTIGÜEDAD
// ========================================

function calcularAntiguedad(fechaIngreso) {
    try {
        if (!fechaIngreso) return '';
        
        const ingreso = new Date(fechaIngreso);
        const hoy = new Date();
        const años = hoy.getFullYear() - ingreso.getFullYear();
        
        return años + ' años';
    } catch (e) {
        console.error('Error calculando antigüedad:', e);
        return '';
    }
}

function inicializarCalculoAntiguedad() {
    try {
        const fechaIngreso = document.querySelector('[name="fecha_ingreso"]');
        if (fechaIngreso) {
            fechaIngreso.addEventListener('change', function() {
                try {
                    if (this.value) {
                        const antiguedadInput = document.querySelector('[name="antiguedad"]');
                        if (antiguedadInput) {
                            antiguedadInput.value = calcularAntiguedad(this.value);
                        }
                    }
                } catch (error) {
                    console.error('Error calculando antigüedad:', error);
                }
            });
        }
    } catch (e) {
        console.error('Error inicializando cálculo de antigüedad:', e);
    }
}

// ========================================
// MODAL DE FINALIZACIÓN
// ========================================

function confirmarFinalizacion() {
    try {
        const aceptoCheck = document.getElementById('aceptoDeclaracion');
        if (!aceptoCheck || !aceptoCheck.checked) {
            alert('Debe aceptar la declaración jurada para finalizar');
            return;
        }
        
        if (!validarFormularioDDJJ()) return;
        
        const modal = obtenerElementoSeguro('modalFinalizar');
        if (modal) {
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        }
    } catch (e) {
        console.error('Error confirmando finalización:', e);
        alert('Error al preparar la finalización');
    }
}

function cerrarModalFinalizar() {
    try {
        const modal = obtenerElementoSeguro('modalFinalizar');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    } catch (e) {
        console.error('Error cerrando modal:', e);
    }
}

// ========================================
// FUNCIONES PARA HISTORIAL DDJJ
// ========================================

function copiarCodigo(codigo) {
    try {
        navigator.clipboard.writeText(codigo).then(function() {
            alert('✅ Código copiado al portapapeles');
        }).catch(function() {
            alert('❌ No se pudo copiar el código');
        });
    } catch (e) {
        console.error('Error copiando código:', e);
        alert('Error al copiar el código');
    }
}

function verQR(codigo) {
    try {
        if (!codigo) {
            alert('Esta DDJJ no tiene código QR generado');
            return;
        }
        
        const modal = obtenerElementoSeguro('modalQR');
        const qrContainer = obtenerElementoSeguro('qrContainer');
        const qrCodigo = obtenerElementoSeguro('qrCodigo');
        
        if (modal && qrContainer && qrCodigo) {
            modal.style.display = 'block';
            qrCodigo.innerText = 'Código: ' + codigo;
            
            // Cargar imagen QR
            qrContainer.innerHTML = `<img src="/static/qr/${codigo}.png" alt="QR" style="max-width: 200px;" onerror="this.onerror=null; this.src='/static/img/qr-placeholder.png';">`;
        }
    } catch (e) {
        console.error('Error mostrando QR:', e);
        alert('Error al mostrar el código QR');
    }
}

function cerrarModalQR() {
    try {
        const modal = obtenerElementoSeguro('modalQR');
        if (modal) {
            modal.style.display = 'none';
        }
    } catch (e) {
        console.error('Error cerrando modal QR:', e);
    }
}

function descargarQR() {
    try {
        const codigo = document.getElementById('qrCodigo')?.innerText.replace('Código: ', '');
        if (codigo) {
            const link = document.createElement('a');
            link.href = `/static/qr/${codigo}.png`;
            link.download = `qr_${codigo}.png`;
            link.click();
        }
    } catch (e) {
        console.error('Error descargando QR:', e);
        alert('Error al descargar el código QR');
    }
}

function verDetalle(ddjjId) {
    try {
        if (ddjjId) {
            window.location.href = `/ddjj/${ddjjId}`;
        }
    } catch (e) {
        console.error('Error viendo detalle:', e);
    }
}

// ========================================
// MANEJADOR DE TECLA ESCAPE
// ========================================

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        cerrarModalFinalizar();
        cerrarModalQR();
    }
});

// ========================================
// CIERRE DE MODALES AL HACER CLIC FUERA
// ========================================

window.addEventListener('click', function(event) {
    try {
        const modalFinalizar = obtenerElementoSeguro('modalFinalizar');
        const modalQR = obtenerElementoSeguro('modalQR');
        
        if (modalFinalizar && event.target === modalFinalizar) {
            cerrarModalFinalizar();
        }
        if (modalQR && event.target === modalQR) {
            cerrarModalQR();
        }
    } catch (e) {
        console.error('Error en click fuera:', e);
    }
});

console.log('📄 Módulo de DDJJ cargado correctamente');