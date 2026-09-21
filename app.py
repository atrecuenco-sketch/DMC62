import streamlit as st
import pandas as pd
import numpy as np

# Importando los archivos proporcionados para el proyecto
import libreria_funciones_proyecto1 as fn
import libreria_clases_proyecto1 as cl

# Configuración básica de la página
st.set_page_config(page_title="Proyecto Python Fundamentals", layout="wide")

# Inicialización de variables de sesión (st.session_state)
if 'caja' not in st.session_state:
    st.session_state.caja = []
if 'inventario' not in st.session_state:
    st.session_state.inventario = []
if 'historial_ej3' not in st.session_state:
    st.session_state.historial_ej3 = []
if 'crud_db' not in st.session_state:
    st.session_state.crud_db = {}

# --- MENÚ LATERAL ---
st.sidebar.title("Navegación")
opcion = st.sidebar.selectbox("Seleccione una sección:", 
                              ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"])

# --- SECCIÓN: HOME ---
if opcion == "Home":
    st.title("Proyecto 1: Aplicación en Streamlit")
    st.subheader("Módulo 1 - Python Fundamentals")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Información General**
        * **Estudiante:** Angie Tatiana Recuenco Tapia
        * **Perfil:** Bachiller en Ingeniería Mecatrónica
        * **Año:** 2026
        
        **Descripción del Proyecto**
        
        Esta aplicación interactiva corresponde al proyecto final del módulo 1 del curso, en donde se demuestra 
        la integración de conceptos fundamentales de Python, incluyendo estructuras de datos, control de flujo, 
        funciones y programación orientada a objetos (POO), mediante una interfaz construida íntegramente con 
        Streamlit, una platafoma que permite correr aplicaciones web enlazadas aun repositorio en GitHub.
        
        **Tecnologías Utilizadas**
        * Python 3
        * Streamlit
        * Pandas
        * NumPy
        """)
  
    with col2:
        st.image("logo_python_DMC.jfif", use_container_width=True)
        st.write("") 
        st.image("logo_DMC.jfif", use_container_width=True)

# --- SECCIÓN: EJERCICIO 1 ---
elif opcion == "Ejercicio 1":
    st.title("Ejercicio 1: Flujo de Caja con Listas")
    st.markdown("Módulo para registrar movimientos financieros operativos diarios.")
    
    with st.form("form_caja"):
        concepto = st.text_input("Concepto del movimiento (Ej: Compra repuestos, Servicio taller)")
        tipo = st.selectbox("Tipo de movimiento", ["Ingreso", "Gasto"])
        valor = st.number_input("Valor", min_value=0.0, step=10.0)
        btn_caja = st.form_submit_button("Agregar Movimiento")
        
        if btn_caja and concepto != "":
            st.session_state.caja.append({"Concepto": concepto, "Tipo": tipo, "Valor": valor})
            st.success(f"Movimiento '{concepto}' agregado correctamente.")

    if st.session_state.caja:
        df_caja = pd.DataFrame(st.session_state.caja)
        st.dataframe(df_caja, use_container_width=True)
        
        ingresos = df_caja[df_caja['Tipo'] == 'Ingreso']['Valor'].sum()
        gastos = df_caja[df_caja['Tipo'] == 'Gasto']['Valor'].sum()
        saldo = ingresos - gastos
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ingresos", f"${ingresos:.2f}")
        col2.metric("Total Gastos", f"${gastos:.2f}")
        col3.metric("Saldo Final", f"${saldo:.2f}")
        
        if saldo > 0:
            st.success("El flujo de caja está **a favor**.")
        elif saldo < 0:
            st.error("El flujo de caja está **en contra**.")
        else:
            st.info("El flujo de caja está **equilibrado**.")

# --- SECCIÓN: EJERCICIO 2 ---
elif opcion == "Ejercicio 2":
    st.title("Ejercicio 2: Registro con NumPy y DataFrame")
    st.markdown("Gestión de suministros de alta rotación para el taller mediante arrays.")
    
    col1, col2 = st.columns(2)
    with col1:
        producto = st.text_input("Nombre del Suministro")
        codigo = st.text_input("Código SAP / Interno")
    with col2:
        precio = st.number_input("Precio Unitario", min_value=0.0, step=0.5)
        cantidad = st.number_input("Cantidad Solicitada", min_value=1, step=1)
    
    if st.button("Agregar a la Lista de Pedido"):
        if producto and codigo:
            total = precio * cantidad
            # Uso de NumPy array según rúbrica
            nuevo_registro = np.array([codigo, producto, precio, cantidad, total])
            st.session_state.inventario.append(nuevo_registro)
            st.success("Suministro registrado exitosamente.")
        else:
            st.warning("Por favor ingrese el nombre del producto y su código.")
            
    if st.session_state.inventario:
        df_inv = pd.DataFrame(st.session_state.inventario, 
                              columns=["Código", "Suministro", "Precio Unitario", "Cantidad", "Total"])
        st.write("### Consolidado de Suministros")
        st.dataframe(df_inv, use_container_width=True)

# --- SECCIÓN: EJERCICIO 3 ---
elif opcion == "Ejercicio 3":
    st.title("Ejercicio 3: Uso de Funciones (Librería Externa)")
    st.markdown("Cálculo de indicadores de mantenimiento (MTBF, MTTR, Disponibilidad).")
    
    # Selector de función según rúbrica
    funcion_sel = st.selectbox("Seleccione la función a ejecutar:", ["Calcular Indicadores de Mantenimiento"])
    
    if funcion_sel == "Calcular Indicadores de Mantenimiento":
        col1, col2, col3 = st.columns(3)
        with col1:
            tiempo_op = st.number_input("Tiempo de Operación (h)", min_value=1.0, value=100.0)
        with col2:
            num_fallas = st.number_input("Número de Fallas", min_value=1, value=2)
        with col3:
            tiempo_rep = st.number_input("Tiempo Reparación Total (h)", min_value=0.0, value=10.0)
            
        if st.button("Ejecutar Función"):
            try:
                # Llama a la función de la librería externa
                resultado = fn.calcular_indicadores_mantenimiento(tiempo_op, num_fallas, tiempo_rep)
                
                st.success("Cálculo realizado con éxito")
                c1, c2, c3 = st.columns(3)
                c1.metric("MTBF (Horas)", resultado["mtbf_h"])
                c2.metric("MTTR (Horas)", resultado["mttr_h"])
                c3.metric("Disponibilidad", f"{resultado['disponibilidad_pct']}%")
                
                # Guardar histórico
                st.session_state.historial_ej3.append({
                    "T. Operación (h)": tiempo_op,
                    "Fallas": num_fallas,
                    "T. Reparación (h)": tiempo_rep,
                    "MTBF (h)": resultado["mtbf_h"],
                    "MTTR (h)": resultado["mttr_h"],
                    "Disponibilidad (%)": resultado["disponibilidad_pct"]
                })
            except ValueError as e:
                st.error(f"Error en los datos ingresados: {e}")
            
    if st.session_state.historial_ej3:
        st.write("#### Histórico de Evaluaciones")
        st.dataframe(pd.DataFrame(st.session_state.historial_ej3), use_container_width=True)

# --- SECCIÓN: EJERCICIO 4 ---
elif opcion == "Ejercicio 4":
    st.title("Ejercicio 4: Uso de Clases (CRUD)")
    st.markdown("Gestión de Equipos de Mantenimiento utilizando Programación Orientada a Objetos.")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Create (C)", "Read (R)", "Update (U)", "Delete (D)"])
    
    with tab1:
        st.subheader("Registrar Nuevo Equipo")
        nombre_equipo = st.text_input("Identificador del Equipo (Ej: Cargador Frontal 994K)")
        col1, col2, col3 = st.columns(3)
        with col1:
            h_op = st.number_input("Horas de Operación", min_value=1.0, value=500.0, key="c_op")
        with col2:
            n_fallas = st.number_input("Número de Fallas", min_value=1, value=1, key="c_falla")
        with col3:
            h_rep = st.number_input("Horas de Reparación", min_value=0.0, value=24.0, key="c_rep")
        
        if st.button("Crear Registro"):
            if nombre_equipo in st.session_state.crud_db:
                st.error("El equipo ya existe. Intente con otro nombre o actualícelo.")
            elif nombre_equipo != "":
                try:
                    # Instancia de la clase externa
                    nuevo_obj = cl.EquipoMantenimiento(nombre_equipo, h_op, n_fallas, h_rep)
                    st.session_state.crud_db[nombre_equipo] = nuevo_obj
                    st.success(f"Equipo '{nombre_equipo}' creado exitosamente.")
                except ValueError as e:
                    st.error(f"Error de validación: {e}")
                
    with tab2:
        st.subheader("Base de Datos de Equipos")
        if st.session_state.crud_db:
            # Convierte los objetos extrayendo el resumen mediante el método de la clase
            datos = [obj.resumen() for obj in st.session_state.crud_db.values()]
            st.dataframe(pd.DataFrame(datos), use_container_width=True)
        else:
            st.info("No hay registros almacenados.")
            
    with tab3:
        st.subheader("Actualizar Registro de Equipo")
        if st.session_state.crud_db:
            id_update = st.selectbox("Seleccione el Equipo a actualizar", list(st.session_state.crud_db.keys()))
            equipo_actual = st.session_state.crud_db[id_update]
            
            c1, c2, c3 = st.columns(3)
            with c1:
                nuevas_h_op = st.number_input("Nuevas Horas Op.", min_value=1.0, value=float(equipo_actual.horas_operacion))
            with c2:
                nuevas_fallas = st.number_input("Nuevas Fallas", min_value=1, value=int(equipo_actual.numero_fallas))
            with c3:
                nuevas_h_rep = st.number_input("Nuevas Horas Rep.", min_value=0.0, value=float(equipo_actual.horas_reparacion))
                
            if st.button("Actualizar"):
                # Reinstanciamos para aprovechar las validaciones de inicialización de la clase
                st.session_state.crud_db[id_update] = cl.EquipoMantenimiento(id_update, nuevas_h_op, nuevas_fallas, nuevas_h_rep)
                st.success("Registro actualizado.")
        else:
            st.info("Agregue registros primero.")
            
    with tab4:
        st.subheader("Eliminar Equipo")
        if st.session_state.crud_db:
            id_delete = st.selectbox("Seleccione Equipo a eliminar", list(st.session_state.crud_db.keys()))
            if st.button("Eliminar Registro"):
                del st.session_state.crud_db[id_delete]
                st.success("Registro eliminado de la base de datos.")
        else:
            st.info("Agregue registros primero.")
