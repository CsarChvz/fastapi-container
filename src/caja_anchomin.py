import matplotlib.pyplot as plt
import numpy as np
import math
import itertools
import io
import base64

def calcular_distancia(circulo1, circulo2):
    x1, y1 = circulo1['centro']['x'], circulo1['centro']['y']
    x2, y2 = circulo2['centro']['x'], circulo2['centro']['y']
    return math.hypot(x2 - x1, y2 - y1)

def verificar_superposicion(circulo1, circulo2):
    distancia = calcular_distancia(circulo1, circulo2)
    return distancia < (circulo1['radio'] + circulo2['radio'])

def ordenar_para_minimo_ancho(radios: list[float]):
    mejor_permutacion, min_ancho = None, float('inf')
    
    for perm in itertools.permutations(radios):
        caja, es_valida = [], True
        
        for i, radio in enumerate(perm):
            x_centro, y_centro = calcular_coordenadas(i, radio, caja)
            nuevo = {'centro': {'x': x_centro, 'y': y_centro}, 'radio': radio}
            
            if any(verificar_superposicion(nuevo, existente) for existente in caja):
                es_valida = False
                break
            
            caja.append(nuevo)
        
        if es_valida:
            ancho = caja[-1]['centro']['x'] + caja[-1]['radio']

            if ancho < min_ancho:
                min_ancho, mejor_permutacion = ancho, perm

    return list(mejor_permutacion) if mejor_permutacion else radios.copy()

def calcular_coordenadas(i, radio, caja):
    y_centro = radio
    if i == 0:
        return radio, y_centro
    previo = caja[i-1]
    d = previo['radio'] + radio
    dx = math.sqrt(max(d**2 - (y_centro - previo['centro']['y'])**2, 0))
    return previo['centro']['x'] + dx, y_centro

# def entrada_usuario():
#     while True:
#         try:
#             n_circulos = int(input("¿Cuántos círculos quieres? (2-5): "))
#             if 2 <= n_circulos <= 5:
#                 break
#             print("Ingresa un valor entre 2 y 5.")
#         except ValueError:
#             print("Ingresa un número válido.")
    
#     radios = []
#     for i in range(n_circulos):
#         while True:
#             try:
#                 r = float(input(f"Radio del círculo {i+1}: "))
#                 if r > 0:
#                     radios.append(r)
#                     break
#                 print("El radio debe ser positivo.")
#             except ValueError:
#                 print("Ingresa un número válido.")
    
#     return ordenar_para_minimo_ancho(radios)

def entrada_usuario(radios: list[float]):
    return ordenar_para_minimo_ancho(radios)

def construir_caja(orden_optimo):
    caja = []
    for i, radio in enumerate(orden_optimo):
        x_centro, y_centro = calcular_coordenadas(i, radio, caja)
        caja.append({'p1': {'x': x_centro - radio, 'y': y_centro},
                     'centro': {'x': x_centro, 'y': y_centro},
                     'p3': {'x': x_centro + radio, 'y': y_centro},
                     'radio': radio})
    return caja

def ajustar_desplazamiento(caja):
    min_x = min(circulo['p1']['x'] for circulo in caja)
    if min_x < 0:
        for circulo in caja:
            desplazamiento = abs(min_x)
            circulo['p1']['x'] += desplazamiento
            circulo['centro']['x'] += desplazamiento
            circulo['p3']['x'] += desplazamiento
    return caja

def graficar_caja(caja):
    # Calcular dimensiones
    min_x = min(circulo['p1']['x'] for circulo in caja)
    max_x = max(circulo['p3']['x'] for circulo in caja)
    altura = max(circulo['radio'] * 2 for circulo in caja)
    
    # Crear figura con estilo mejorado
    plt.style.use('default')  # Cambiado a estilo default
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')
    ax.set_facecolor('white')
    
    # Colores personalizados para una mejor visualización
    colores_circulos = plt.cm.viridis(np.linspace(0, 0.8, len(caja)))
    
    # Dibujar los círculos y puntos
    for i, circulo in enumerate(caja):
        x = circulo['centro']['x']
        y = circulo['centro']['y']
        radio = circulo['radio']
        
        # Dibujar círculo con alpha para mejor visibilidad
        circle = plt.Circle((x, y), radio, fill=False, 
                          color=colores_circulos[i], 
                          linewidth=2,
                          alpha=0.7)
        ax.add_patch(circle)
        
        # Dibujar puntos clave con mejor formato
        ax.scatter(circulo['p1']['x'], circulo['p1']['y'], 
                color='crimson', s=12.5, zorder=5,
                label="P1" if i == 0 else "", 
                edgecolor='white', linewidth=1)

        ax.scatter(circulo['centro']['x'], circulo['centro']['y'], 
                color='royalblue', s=12.5, zorder=5,
                label="Centro" if i == 0 else "", 
                edgecolor='white', linewidth=1)

        ax.scatter(circulo['p3']['x'], circulo['p3']['y'], 
                color='forestgreen', s=12.5, zorder=5,
                label="P3" if i == 0 else "", 
                edgecolor='white', linewidth=1)

        
        # Dibujar radio con estilo mejorado
        ax.plot([x, x + radio], [y, y], 
                color='gray', linestyle='--', 
                linewidth=1, alpha=0.5)
        
        # Etiquetas de coordenadas con mejor formato
        bbox_props = dict(boxstyle="round,pad=0.3", 
                         fc="white", ec="gray", alpha=0.7)
        
        ax.text(circulo['p1']['x'], circulo['p1']['y'] - 0.2, 
                f"P1 ({round(circulo['p1']['x'], 2)}, {round(circulo['p1']['y'], 2)})",
                fontsize=8, color='crimson', 
                bbox=bbox_props, ha='right', va='top')
        ax.text(circulo['centro']['x'], circulo['centro']['y'] + 0.2, 
                f"C ({round(circulo['centro']['x'], 2)}, {round(circulo['centro']['y'], 2)})",
                fontsize=8, color='royalblue', 
                bbox=bbox_props, ha='left', va='bottom')
        ax.text(circulo['p3']['x'], circulo['p3']['y'] - 0.2, 
                f"P3 ({round(circulo['p3']['x'], 2)}, {round(circulo['p3']['y'], 2)})",
                fontsize=8, color='forestgreen', 
                bbox=bbox_props, ha='left', va='top')
    
    # Dibujar la caja contenedora con mejor estilo
    rect = plt.Rectangle((min_x, 0), max_x - min_x, altura,
                        fill=False, 
                        edgecolor='purple',
                        linewidth=2,
                        linestyle='--',
                        label="Caja de límites",
                        alpha=0.8)
    ax.add_patch(rect)
    
    # Mejorar la configuración del gráfico
    margen = max(1, altura * 0.1)  # Margen dinámico
    ax.set_xlim(min_x - margen, max_x + margen)
    ax.set_ylim(-margen, altura + margen)
    ax.set_aspect('equal')
    
    # Título y leyenda mejorados
    ax.set_title("Configuración Óptima de Círculos\n" + 
                 f"Ancho: {round(max_x - min_x, 2)}, Altura: {round(altura, 2)}", 
                 pad=20, fontsize=12, fontweight='bold')
    
    # Leyenda mejorada
    ax.legend(bbox_to_anchor=(1.05, 1), 
             loc='upper left', 
             borderaxespad=0,
             frameon=True,
             fancybox=True,
             shadow=True)
    
    # Grid mejorado
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Ajustar espaciado
    plt.tight_layout()
    
    return fig, ax


def guardar_imagen(fig, formato="png"):

    with io.BytesIO() as buffer:
        fig.savefig(buffer, format=formato, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    # Cerrar la figura para liberar memoria
    plt.close(fig)

    return {"image": image_base64}

# Flujo principal
def grafc(list_radios: list[float]):
    #orden_optimo = entrada_usuario()
    orden_optimo = entrada_usuario(list_radios)
    caja = construir_caja(orden_optimo)
    caja = ajustar_desplazamiento(caja)
    fig, ax = graficar_caja(caja)
    image = guardar_imagen(fig)
    return image

# if __name__ == "__main__":
#     main()