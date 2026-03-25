// static/js/nuevo_legajo.js - CORREGIDO Y OPTIMIZADO

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

// ========================================
// INICIALIZACIÓN
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    try {
        console.log('📝 Inicializando formulario de nuevo legajo...');
        
        const form = obtenerElementoSeguro('formLegajo');
        
        if (form) {
            form.addEventListener('submit', function(e) {
                try {
                    validarFormulario(e);
                } catch (error) {
                    console.error('Error en validación:', error);
                    e.preventDefault();
                    alert('Error al validar el formulario');
                }
            });
        }
        
        // Auto-formatear DNI
        const dniInput = obtenerElementoSeguro('dni');
        if (dniInput) {
            dniInput.addEventListener('input', function(e) {
                try {
                    this.value = this.value.replace(/\D/g, '');
                } catch (error) {
                    console.error('Error formateando DNI:', error);
                }
            });
        }
        
        // Auto-formatear teléfono
        const telefonoInput = obtenerElementoSeguro('telefono');
        if (telefonoInput) {
            telefonoInput.addEventListener('input', function(e) {
                try {
                    this.value = this.value.replace(/\D/g, '');
                } catch (error) {
                    console.error('Error formateando teléfono:', error);
                }
            });
        }
        
        // Validar legajo único
        const legajoInput = obtenerElementoSeguro('legajo_id');
        if (legajoInput) {
            legajoInput.addEventListener('blur', function() {
                try {
                    verificarLegajoUnico.call(this);
                } catch (error) {
                    console.error('Error verificando legajo:', error);
                }
            });
        }
        
        console.log('✅ Formulario de nuevo legajo inicializado');
        
    } catch (e) {
        console.error('❌ Error en inicialización:', e);
    }
});

// ========================================
// VALIDACIÓN DE FORMULARIO
// ========================================

function validarFormulario(e) {
    try {
        const legajo = obtenerElementoSeguro('legajo_id');
        const apellido = obtenerElementoSeguro('apellido');
        const nombre = obtenerElementoSeguro('nombre');
        const dni = obtenerElementoSeguro('dni');
        
        let errores = [];
        
        if (!legajo || !legajo.value.trim()) {
            errores.push('El número de legajo es obligatorio');
            if (legajo) legajo.classList.add('error');
        }
        
        if (!apellido || !apellido.value.trim()) {
            errores.push('El apellido es obligatorio');
            if (apellido) apellido.classList.add('error');
        }
        
        if (!nombre || !nombre.value.trim()) {
            errores.push('El nombre es obligatorio');
            if (nombre) nombre.classList.add('error');
        }
        
        if (dni && dni.value && !/^\d{7,8}$/.test(dni.value)) {
            errores.push('El DNI debe tener 7 u 8 dígitos');
            dni.classList.add('error');
        }
        
        if (errores.length > 0) {
            e.preventDefault();
            alert('Errores:\n• ' + errores.join('\n• '));
        }
        
    } catch (error) {
        console.error('Error en validación:', error);
        e.preventDefault();
        alert('Error al validar el formulario');
    }
}

// ========================================
// VERIFICAR LEGAJO ÚNICO
// ========================================

function verificarLegajoUnico() {
    try {
        const legajo = this.value;
        if (!legajo) return;
        
        // Usar fetch API para verificar
        fetch(`/api/verificar-legajo/${legajo}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.existe) {
                    this.classList.add('error');
                    alert('Este número de legajo ya existe');
                } else {
                    this.classList.remove('error');
                }
            })
            .catch(error => {
                console.warn('⚠️ Error verificando legajo (no crítico):', error);
                // No mostrar error al usuario, es solo informativo
            });
            
    } catch (e) {
        console.error('Error en verificarLegajoUnico:', e);
    }
}

// ========================================
// LIMPIAR ERRORES DEL FORMULARIO
// ========================================

function limpiarErrores() {
    try {
        document.querySelectorAll('.error').forEach(el => {
            el.classList.remove('error');
        });
    } catch (e) {
        console.error('Error limpiando errores:', e);
    }
}

console.log('📝 Módulo de nuevo legajo cargado correctamente');