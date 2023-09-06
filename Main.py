import xml.etree.ElementTree as ET
import graphviz
import os
import sys

# Definición de clases
class Dato:
    def __init__(self, t, A, value):
        self.t = t
        self.A = A
        self.value = value
        self.next = None

class Senal:
    def __init__(self, nombre):
        self.nombre = nombre
        self.head = None
        self.tabla = []

senales = []

# Funciones para cargar y procesar datos
def cargar_datos_desde_xml(xml_string):
    senales = []
    root = ET.fromstring(xml_string)
    
    for senal_elem in root.findall('senal'):
        nombre = senal_elem.get('nombre')
        senal = Senal(nombre)
        
        for dato_elem in senal_elem.findall('dato'):
            t = int(dato_elem.get('t'))
            A = int(dato_elem.get('A'))
            value = int(dato_elem.text)
            
            dato = Dato(t, A, value)
            
            if senal.head is None:
                senal.head = dato
            else:
                current = senal.head
                while current.next:
                    current = current.next
                current.next = dato
        
        # Crear una tabla para almacenar los datos de la señal
        tabla = []
        for _ in range(5):  # Aquí asumimos 5 filas en la tabla
            tabla.append([None] * 4)  # Inicializar con valores None
        
        # Llenar la tabla con los valores de los datos
        current = senal.head
        while current:
            tabla[current.t - 1][current.A - 1] = current.value
            current = current.next
        
        senal.tabla = tabla 
        senales.append(senal)
    
    return senales

# Función para mostrar los datos de las señales y tablas
def mostrar_datos_y_tablas(senales):
    for senal in senales:
        print(f"Señal: {senal.nombre}")
        current = senal.head
        while current:
            print(f"t: {current.t}, A: {current.A}, Valor: {current.value}")
            current = current.next
        
        print("\nTabla para la señal:")
        for fila in senal.tabla:
            print(fila)
        
        print("\nMatriz binaria:")
        matriz_binaria = []
        for fila in senal.tabla:
            fila_binaria = [1 if value > 0 else 0 for value in fila]
            matriz_binaria.append(fila_binaria)
            print(fila_binaria)
        
        print("\nMensaje: Matriz binaria\n")
        print()

# Función principal y menú
def main():

    global senales
    senales = []

    while True:
        print("Menú:")
        print("1. Cargar archivo")
        print("2. Procesar archivo")
        print("3. Escribir archivo de salida")
        print("4. Mostrar datos del estudiante")
        print("5. Generar gráfica")
        print("6. Inicializar sistema")
        print("7. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            cargar_archivo()
        elif opcion == '2':
            senales = procesar_archivo()
        elif opcion == '3':
            escribir_archivo_salida(senales)
        elif opcion == '4':
            mostrar_datos_estudiante()
        elif opcion == '5':
            generar_grafica(senales)
        elif opcion == '6':
            inicializar_sistema()
        elif opcion == '7':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")


def cargar_archivo():
    ruta_archivo = input("Ingrese la ruta del archivo a cargar: ")

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            print("Archivo cargado exitosamente.")
    except FileNotFoundError:
        print("Archivo no encontrado.")
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
    print("")

def procesar_archivo():
    ruta_archivo = input("Ingrese la ruta del archivo a cargar: ")
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()

            # Declarar senales como global
            global senales
            senales = cargar_datos_desde_xml(contenido)
            mostrar_datos_y_tablas(senales)
            print("Datos del archivo XML cargados y procesados.")
    except FileNotFoundError:
        print("Archivo no encontrado.")
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
    print("")

def escribir_archivo_salida(senales):
    root = ET.Element('senalesReducidas')

    for senal in senales:
        senal_elem = ET.SubElement(root, 'senal', nombre=senal.nombre, A=str(len(senal.tabla[0])))
        
        for grupo_num, grupo_tiempos, grupo_datos in zip(range(1, len(senal.tabla) + 1), senal.tabla, senal.tabla):
            grupo_elem = ET.SubElement(senal_elem, 'grupo', g=str(grupo_num))
            tiempos_elem = ET.SubElement(grupo_elem, 'tiempos')
            tiempos_elem.text = ','.join(str(i + 1) for i, value in enumerate(grupo_tiempos) if value is not None)
            
            datos_grupo_elem = ET.SubElement(grupo_elem, 'datosGrupo')
            for A, value in enumerate(grupo_datos, start=1):
                if value is not None:
                    dato_elem = ET.SubElement(datos_grupo_elem, 'dato', A=str(A))
                    dato_elem.text = str(value)
    
    tree = ET.ElementTree(root)
    tree.write('salida.xml', encoding='utf-8', xml_declaration=True)
    
    print("Archivo de salida XML creado exitosamente.")

def mostrar_datos_estudiante():
    print("******************************************************")
    print("Frander Oveldo Carreto Gómez")
    print("201901371")
    print("Introduccion a la programación y computacion 2 sección  D")
    print("Ingenieria en Ciencias y sistemas")
    print("4to Semestre")
    print("******************************************************")
    print("Cada línea de código es un peldaño hacia la cima de tus metas")
    print("")

def generar_grafica(senales):
    try:
        if not senales:
            print("No hay señales cargadas para generar gráfica.")
            return

        primera_senal = senales[0]

        if not primera_senal.tabla:
            print("La primera señal no tiene datos para generar gráfica.")
            return

        matriz = primera_senal.tabla
        filas = len(matriz)
        columnas = len(matriz[0])

        dot = graphviz.Digraph(format='png')

        # Agregar nodos para cada celda en la matriz
        for fila in range(filas):
            for columna in range(columnas):
                valor = matriz[fila][columna]
                dot.node(f"{fila}_{columna}", label=str(valor))

        # Agregar bordes entre celdas vecinas
        for fila in range(filas):
            for columna in range(columnas):
                nodo_actual = f"{fila}_{columna}"
                if fila + 1 < filas:
                    nodo_vecino = f"{fila + 1}_{columna}"
                    dot.edge(nodo_actual, nodo_vecino)
                if columna + 1 < columnas:
                    nodo_vecino = f"{fila}_{columna + 1}"
                    dot.edge(nodo_actual, nodo_vecino)

        dot.render('matriz_grafica', view=True)
        print("Gráfica creada correctamente.")
    except Exception as e:
        print("Error al generar la gráfica:", e)

def inicializar_sistema():
    print("Reiniciando el programa...")
    input("Presione Enter para continuar...")
    os.system('clear' if os.name == 'posix' else 'cls')  # Limpia la consola según el sistema operativo
    os.execl(sys.executable, sys.executable, *sys.argv)

def salir():
    print("Saliendo......")
    print("")

while True:
    print("Menú:")
    print("1. Cargar archivo")
    print("2. Procesar archivo")
    print("3. Escribir archivo de salida")
    print("4. Mostrar datos del estudiante")
    print("5. Generar gráfica")
    print("6. Inicializar sistema")
    print("7. Salir")
    
    opcion = input("Seleccione una opción: ")
    
    if opcion == '1':
        cargar_archivo()
    elif opcion == '2':
        procesar_archivo()
    elif opcion == '3':
        escribir_archivo_salida(senales)
    elif opcion == '4':
        mostrar_datos_estudiante()
    elif opcion == '5':
        generar_grafica(senales)
    elif opcion == '6':
        inicializar_sistema()
    elif opcion == '7':
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()
