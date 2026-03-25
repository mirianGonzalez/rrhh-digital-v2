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

// ========================================
// BÚSQUEDA EN EL MANUAL
// ========================================

let timeoutBusqueda = null;

function inicializarBusqueda() {
    try {
        const buscador = obtenerElementoSeguro('buscar-manual');
        
        if (buscador) {
            buscador.addEventListener('keyup', function() {
                try {
                    // Debounce para no buscar en cada tecla
                    clearTimeout(timeoutBusqueda);
                    timeoutBusqueda = setTimeout(() => {
                        const termino = this.value.toLowerCase().trim();
                        buscarEnManual(termino);
                    }, 300);
                } catch (error) {
                    console.error('Error en búsqueda:', error);
                }
            });
            
            // Limpiar búsqueda con botón Esc
            buscador.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    this.value = '';
                    buscarEnManual('');
                }
            });
        }
        
        console.log('✅ Búsqueda inicializada');
        
    } catch (e) {
        console.error('Error inicializando búsqueda:', e);
    }
}

function buscarEnManual(termino) {
    try {
        const contenidos = document.querySelectorAll('.manual-card, .manual-section p, .manual-section li, .manual-section h3, .manual-section h4');
        
        if (termino === '') {
            // Limpiar resaltados
            contenidos.forEach(el => {
                el.style.backgroundColor = '';
                el.style.borderRadius = '';
                el.style.transition = '';
            });
            
            const resultados = obtenerElementoSeguro('resultados-busqueda');
            if (resultados) resultados.style.display = 'none';
            
            return;
        }
        
        let encontrados = 0;
        
        contenidos.forEach(elemento => {
            const texto = elemento.innerText.toLowerCase();
            if (texto.includes(termino)) {
                elemento.style.backgroundColor = '#fff3e0';
                elemento.style.borderRadius = '4px';
                elemento.style.transition = 'background-color 0.3s';
                encontrados++;
                
                // Scroll al primer resultado
                if (encontrados === 1) {
                    setTimeout(() => {
                        elemento.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }, 100);
                }
            } else {
                elemento.style.backgroundColor = '';
            }
        });
        
        // Mostrar contador de resultados
        const resultadosSpan = obtenerElementoSeguro('resultados-busqueda');
        if (resultadosSpan) {
            resultadosSpan.style.display = 'inline';
            if (encontrados === 0) {
                resultadosSpan.innerText = '❌ No se encontraron resultados';
            } else {
                resultadosSpan.innerText = `✅ ${encontrados} resultado${encontrados !== 1 ? 's' : ''}`;
            }
        }
        
    } catch (e) {
        console.error('Error en búsqueda:', e);
    }
}

// ========================================
// IMPRESIÓN DEL MANUAL
// ========================================

function imprimirManual() {
    try {
        window.print();
    } catch (e) {
        console.error('Error imprimiendo manual:', e);
        alert('Error al imprimir el manual');
    }
}

function descargarManualPDF() {
    try {
        alert('Función de descarga de manual en PDF - Implementar según necesidad');
        // Aquí iría la implementación real de descarga de PDF
    } catch (e) {
        console.error('Error descargando PDF:', e);
        alert('Error al descargar el PDF');
    }
}

// ========================================
// NAVEGACIÓN POR SECCIONES
// ========================================

function irASeccion(seccionId) {
    try {
        const elemento = document.getElementById(seccionId);
        if (elemento) {
            elemento.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    } catch (e) {
        console.error('Error navegando a sección:', e);
    }
}

// ========================================
// ATAJOS DE TECLADO
// ========================================

document.addEventListener('keydown', function(e) {
    try {
        // Ctrl + F para buscar (solo si no hay un input activo)
        if (e.ctrlKey && e.key === 'f' && document.activeElement?.tagName !== 'INPUT') {
            e.preventDefault();
            const buscador = obtenerElementoSeguro('buscar-manual');
            if (buscador) {
                buscador.focus();
                buscador.select();
            }
        }
        
        // Ctrl + P para imprimir
        if (e.ctrlKey && e.key === 'p') {
            e.preventDefault();
            imprimirManual();
        }
        
        // Tecla H para ir al inicio
        if (e.key === 'h' && !e.ctrlKey && !e.altKey && document.activeElement?.tagName !== 'INPUT') {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        
    } catch (error) {
        console.error('Error en atajos de teclado:', error);
    }
});

// ========================================
// BOTÓN DE VOLVER ARRIBA
// ========================================

function crearBotonVolverArriba() {
    try {
        // Verificar si ya existe
        if (document.getElementById('btn-volver-arriba')) return;
        
        const btn = document.createElement('button');
        btn.id = 'btn-volver-arriba';
        btn.innerHTML = '<i class="fas fa-arrow-up"></i>';
        btn.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: #1e3c72;
            color: white;
            border: none;
            cursor: pointer;
            display: none;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            transition: all 0.3s;
            z-index: 1000;
        `;
        
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.background = '#2a5298';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.background = '#1e3c72';
        });
        
        btn.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        
        document.body.appendChild(btn);
        
        // Mostrar/ocultar según scroll
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                btn.style.display = 'flex';
            } else {
                btn.style.display = 'none';
            }
        });
        
    } catch (e) {
        console.error('Error creando botón volver arriba:', e);
    }
}

// Inicializar botón después de carga completa
window.addEventListener('load', function() {
    try {
        crearBotonVolverArriba();
    } catch (e) {
        console.error('Error creando botón:', e);
    }
});

console.log('📖 Módulo de manual cargado correctamente');