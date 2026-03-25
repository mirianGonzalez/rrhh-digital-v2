// static/js/auditoria.js - CORREGIDO Y OPTIMIZADO

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
        console.log('🔍 Inicializando módulo de auditoría...');
        
        inicializarFiltros();
        inicializarDetallesExpandibles();
        
        console.log('✅ Auditoría inicializada');
        
    } catch (e) {
        console.error('❌ Error en inicialización:', e);
    }
});

// ========================================
// FILTROS
// ========================================

function inicializarFiltros() {
    try {
        const filtroUsuario = obtenerElementoSeguro('filtroUsuario');
        const filtroAccion = obtenerElementoSeguro('filtroAccion');
        const fechaDesde = obtenerElementoSeguro('fechaDesde');
        const fechaHasta = obtenerElementoSeguro('fechaHasta');
        
        if (filtroUsuario) filtroUsuario.addEventListener('change', aplicarFiltros);
        if (filtroAccion) filtroAccion.addEventListener('change', aplicarFiltros);
        if (fechaDesde) fechaDesde.addEventListener('change', aplicarFiltros);
        if (fechaHasta) fechaHasta.addEventListener('change', aplicarFiltros);
        
    } catch (e) {
        console.error('Error inicializando filtros:', e);
    }
}

function aplicarFiltros() {
    try {
        const filtroUsuario = obtenerElementoSeguro('filtroUsuario')?.value || 'todos';
        const filtroAccion = obtenerElementoSeguro('filtroAccion')?.value || 'todos';
        const fechaDesde = obtenerElementoSeguro('fechaDesde')?.value;
        const fechaHasta = obtenerElementoSeguro('fechaHasta')?.value;
        
        const filas = document.querySelectorAll('#tablaAuditoria tbody tr');
        
        filas.forEach(fila => {
            try {
                let mostrar = true;
                
                if (filtroUsuario !== 'todos') {
                    const usuario = fila.querySelector('td:nth-child(2)')?.innerText;
                    if (usuario !== filtroUsuario) mostrar = false;
                }
                
                if (filtroAccion !== 'todos' && mostrar) {
                    const badge = fila.querySelector('td:nth-child(4) .badge');
                    if (badge && !badge.innerText.includes(filtroAccion)) mostrar = false;
                }
                
                if (fechaDesde && mostrar) {
                    const fecha = fila.querySelector('td:first-child')?.innerText.split(' ')[0];
                    if (fecha && fecha < fechaDesde) mostrar = false;
                }
                
                if (fechaHasta && mostrar) {
                    const fecha = fila.querySelector('td:first-child')?.innerText.split(' ')[0];
                    if (fecha && fecha > fechaHasta) mostrar = false;
                }
                
                fila.style.display = mostrar ? '' : 'none';
                
            } catch (error) {
                console.error('Error filtrando fila:', error);
            }
        });
        
        actualizarContador();
        
    } catch (e) {
        console.error('Error aplicando filtros:', e);
    }
}

function limpiarFiltros() {
    try {
        const filtroUsuario = obtenerElementoSeguro('filtroUsuario');
        const filtroAccion = obtenerElementoSeguro('filtroAccion');
        const fechaDesde = obtenerElementoSeguro('fechaDesde');
        const fechaHasta = obtenerElementoSeguro('fechaHasta');
        
        if (filtroUsuario) filtroUsuario.value = 'todos';
        if (filtroAccion) filtroAccion.value = 'todos';
        if (fechaDesde) fechaDesde.value = '';
        if (fechaHasta) fechaHasta.value = '';
        
        aplicarFiltros();
        
    } catch (e) {
        console.error('Error limpiando filtros:', e);
    }
}

function actualizarContador() {
    try {
        const contador = obtenerElementoSeguro('resultados-auditoria');
        if (!contador) return;
        
        const visibles = document.querySelectorAll('#tablaAuditoria tbody tr:not([style*="display: none"])').length;
        const total = document.querySelectorAll('#tablaAuditoria tbody tr').length;
        
        contador.innerText = `Mostrando ${visibles} de ${total} registros`;
        
    } catch (e) {
        console.error('Error actualizando contador:', e);
    }
}

// ========================================
// DETALLES EXPANDIBLES
// ========================================

function inicializarDetallesExpandibles() {
    try {
        document.querySelectorAll('.audit-details-toggle').forEach(toggle => {
            toggle.addEventListener('click', function() {
                try {
                    const content = this.nextElementSibling;
                    if (content) {
                        content.classList.toggle('show');
                        this.classList.toggle('active');
                        
                        const icon = this.querySelector('i');
                        if (icon) {
                            icon.classList.toggle('fa-chevron-down');
                            icon.classList.toggle('fa-chevron-up');
                        }
                    }
                } catch (error) {
                    console.error('Error expandiendo detalles:', error);
                }
            });
        });
    } catch (e) {
        console.error('Error inicializando detalles:', e);
    }
}

// ========================================
// EXPORTACIÓN
// ========================================

function exportarExcel() {
    try {
        if (typeof XLSX === 'undefined') {
            alert('Librería de exportación no disponible');
            return;
        }
        
        const tabla = document.getElementById('tablaAuditoria');
        if (!tabla) {
            alert('Tabla no encontrada');
            return;
        }
        
        const wb = XLSX.utils.table_to_book(tabla, {sheet: "Auditoría"});
        XLSX.writeFile(wb, `auditoria_${new Date().toISOString().split('T')[0]}.xlsx`);
        
    } catch (e) {
        console.error('Error exportando Excel:', e);
        alert('Error al exportar a Excel');
    }
}

// static/js/manual.js - CORREGIDO Y OPTIMIZADO

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
        console.log('📖 Inicializando manual de usuario...');
        
        inicializarFAQ();
        inicializarScrollSpy();
        inicializarBusqueda();
        
        console.log('✅ Manual inicializado correctamente');
        
    } catch (e) {
        console.error('❌ Error en inicialización del manual:', e);
    }
});

// ========================================
// PREGUNTAS FRECUENTES (FAQ)
// ========================================

function inicializarFAQ() {
    try {
        const faqQuestions = document.querySelectorAll('.faq-question');
        
        faqQuestions.forEach(question => {
            question.addEventListener('click', function(e) {
                try {
                    e.preventDefault();
                    this.classList.toggle('active');
                    
                    const answer = this.nextElementSibling;
                    if (answer && answer.classList.contains('faq-answer')) {
                        answer.classList.toggle('show');
                        
                        // Icono
                        const icon = this.querySelector('i');
                        if (icon) {
                            if (answer.classList.contains('show')) {
                                icon.classList.remove('fa-chevron-down');
                                icon.classList.add('fa-chevron-up');
                            } else {
                                icon.classList.remove('fa-chevron-up');
                                icon.classList.add('fa-chevron-down');
                            }
                        }
                    }
                } catch (error) {
                    console.error('Error en FAQ click:', error);
                }
            });
        });
        
        console.log('✅ FAQ inicializado');
        
    } catch (e) {
        console.error('Error inicializando FAQ:', e);
    }
}

// ========================================
// SCROLL SPY (RESALTAR SECCIÓN ACTIVA)
// ========================================

function inicializarScrollSpy() {
    try {
        const sections = document.querySelectorAll('.manual-section');
        const navLinks = document.querySelectorAll('.manual-indice a');
        
        if (!sections.length || !navLinks.length) return;
        
        window.addEventListener('scroll', function() {
            try {
                let current = '';
                const scrollPosition = window.scrollY + 100;
                
                sections.forEach(section => {
                    const sectionTop = section.offsetTop;
                    const sectionHeight = section.clientHeight;
                    
                    if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                        current = section.getAttribute('id');
                    }
                });
                
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    const href = link.getAttribute('href');
                    if (href === `#${current}`) {
                        link.classList.add('active');
                    }
                });
                
            } catch (error) {
                console.error('Error en scroll spy:', error);
            }
        });
        
        console.log('✅ Scroll spy inicializado');
        
    } catch (e) {
        console.error('Error inicializando scroll spy:', e);
    }
}

function exportarPDF() {
    try {
        if (typeof window.jspdf === 'undefined') {
            alert('Librería de PDF no disponible');
            return;
        }
        
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        
        doc.autoTable({ 
            html: '#tablaAuditoria',
            styles: { fontSize: 8 },
            headStyles: { fillColor: [30, 60, 114] }
        });
        
        doc.save(`auditoria_${new Date().toISOString().split('T')[0]}.pdf`);
        
    } catch (e) {
        console.error('Error exportando PDF:', e);
        alert('Error al exportar a PDF');
    }
}

// ========================================
// MANEJADOR DE TECLA ESCAPE
// ========================================

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        // Cerrar cualquier modal abierto
        const detallesAbiertos = document.querySelectorAll('.audit-details-content.show');
        detallesAbiertos.forEach(detalle => {
            detalle.classList.remove('show');
        });
    }
});

console.log('📊 Módulo de auditoría cargado correctamente');
