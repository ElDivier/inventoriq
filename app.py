import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="InventiQ - Gestión de Inventarios",
    page_icon="📦",
    layout="wide"
)

PRODUCTOS_FILE = Path("productos_inventiq.csv")
VENTAS_FILE = Path("ventas_inventiq.csv")

COLUMNAS_PRODUCTOS = [
    "codigo",
    "nombre",
    "categoria",
    "proveedor",
    "precio_compra",
    "precio_venta",
    "stock",
    "stock_minimo",
    "ubicacion",
    "fecha_ingreso"
]

COLUMNAS_VENTAS = [
    "fecha",
    "codigo",
    "producto",
    "categoria",
    "cantidad",
    "precio_unitario",
    "total"
]

# =========================================================
# ESTILO VISUAL EN TEMA BLANCO
# =========================================================

st.markdown(
    """
    <style>

    /* Fondo general */
    .stApp {
        background-color: #f4f7fb !important;
        color: #111827 !important;
    }

    .block-container {
        background-color: #f4f7fb !important;
        color: #111827 !important;
        padding-top: 2rem;
    }

    /* Textos principales */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #111827 !important;
    }

    /* Sidebar en blanco */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e5e7eb !important;
    }

    section[data-testid="stSidebar"] * {
        color: #111827 !important;
    }

    section[data-testid="stSidebar"] .stAlert {
        background-color: #eff6ff !important;
        color: #1e40af !important;
        border-radius: 12px !important;
    }

    /* Títulos */
    .titulo-principal {
        font-size: 42px;
        font-weight: 800;
        color: #111827 !important;
        margin-bottom: 0px;
    }

    .subtitulo {
        font-size: 18px;
        color: #374151 !important;
        margin-bottom: 25px;
    }

    /* Tarjetas */
    .card {
        background-color: #ffffff !important;
        color: #111827 !important;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        margin-bottom: 18px;
        font-size: 16px;
        line-height: 1.6;
    }

    .card * {
        color: #111827 !important;
    }

    .metric-card {
        background-color: #ffffff !important;
        padding: 18px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 3px 12px rgba(0,0,0,0.06);
        text-align: center;
    }

    .metric-title {
        font-size: 14px;
        color: #4b5563 !important;
        font-weight: 600;
    }

    .metric-value {
        font-size: 28px;
        color: #111827 !important;
        font-weight: 800;
    }

    /* Alertas personalizadas */
    .alerta {
        background-color: #fff7ed !important;
        color: #9a3412 !important;
        border-left: 6px solid #f97316;
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    .alerta * {
        color: #9a3412 !important;
    }

    .exito {
        background-color: #ecfdf5 !important;
        color: #065f46 !important;
        border-left: 6px solid #10b981;
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    .exito * {
        color: #065f46 !important;
    }

    .info-box {
        background-color: #eff6ff !important;
        color: #1e40af !important;
        border-left: 6px solid #3b82f6;
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    .info-box * {
        color: #1e40af !important;
    }

    .danger-box {
        background-color: #fef2f2 !important;
        color: #991b1b !important;
        border-left: 6px solid #ef4444;
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    .danger-box * {
        color: #991b1b !important;
    }

    /* Botones */
    .stButton button {
        background-color: #2563eb !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
    }

    .stButton button:hover {
        background-color: #1d4ed8 !important;
        color: white !important;
    }

    .stDownloadButton button {
        background-color: #16a34a !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
    }

    .stDownloadButton button:hover {
        background-color: #15803d !important;
        color: white !important;
    }

    /* Inputs */
    input, textarea, select {
        background-color: #ffffff !important;
        color: #111827 !important;
    }

    /* Métricas nativas */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 16px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }

    div[data-testid="stMetric"] * {
        color: #111827 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FUNCIONES DE DATOS
# =========================================================

def cargar_productos():
    if PRODUCTOS_FILE.exists():
        df = pd.read_csv(PRODUCTOS_FILE)
    else:
        df = pd.DataFrame(columns=COLUMNAS_PRODUCTOS)

    for col in COLUMNAS_PRODUCTOS:
        if col not in df.columns:
            df[col] = ""

    if not df.empty:
        df["precio_compra"] = pd.to_numeric(df["precio_compra"], errors="coerce").fillna(0)
        df["precio_venta"] = pd.to_numeric(df["precio_venta"], errors="coerce").fillna(0)
        df["stock"] = pd.to_numeric(df["stock"], errors="coerce").fillna(0).astype(int)
        df["stock_minimo"] = pd.to_numeric(df["stock_minimo"], errors="coerce").fillna(0).astype(int)

    return df[COLUMNAS_PRODUCTOS]


def guardar_productos(df):
    df.to_csv(PRODUCTOS_FILE, index=False)


def cargar_ventas():
    if VENTAS_FILE.exists():
        df = pd.read_csv(VENTAS_FILE)
    else:
        df = pd.DataFrame(columns=COLUMNAS_VENTAS)

    for col in COLUMNAS_VENTAS:
        if col not in df.columns:
            df[col] = ""

    if not df.empty:
        df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce").fillna(0).astype(int)
        df["precio_unitario"] = pd.to_numeric(df["precio_unitario"], errors="coerce").fillna(0)
        df["total"] = pd.to_numeric(df["total"], errors="coerce").fillna(0)

    return df[COLUMNAS_VENTAS]


def guardar_ventas(df):
    df.to_csv(VENTAS_FILE, index=False)


def formato_dinero(valor):
    return f"${valor:,.2f}"


def obtener_resumen_ventas(ventas):
    if ventas.empty:
        return pd.DataFrame(columns=["producto", "categoria", "cantidad", "total"])

    resumen = (
        ventas.groupby(["producto", "categoria"], as_index=False)
        .agg({"cantidad": "sum", "total": "sum"})
        .sort_values(by="cantidad", ascending=False)
    )

    return resumen


def generar_recomendacion_compra(row, promedio_ventas):
    stock = row["stock"]
    stock_minimo = row["stock_minimo"]
    ventas_producto = row.get("cantidad_vendida", 0)

    if stock <= stock_minimo and ventas_producto >= promedio_ventas:
        return "Comprar más urgente: alta demanda y stock bajo"
    elif stock <= stock_minimo:
        return "Reponer inventario: stock crítico"
    elif ventas_producto >= promedio_ventas and stock > stock_minimo:
        return "Mantener stock alto: producto con buena rotación"
    elif ventas_producto == 0:
        return "Comprar menos: no registra ventas"
    elif ventas_producto < promedio_ventas:
        return "Comprar con moderación: baja rotación"
    else:
        return "Mantener compra normal"


def generar_sugerencia_ubicacion(row, promedio_ventas):
    producto = str(row["nombre"]).lower()
    categoria = str(row["categoria"]).lower()
    ventas_producto = row.get("cantidad_vendida", 0)

    if ventas_producto == 0:
        return "Ubicar en zona visible o aplicar promoción para llamar la atención"
    elif ventas_producto < promedio_ventas:
        return "Mover a estante frontal para mejorar su exposición"
    elif "chocolate" in producto or "caramelo" in producto or "galleta" in producto or "snack" in categoria:
        return "Colocar cerca de caja como producto de impulso"
    elif "bebida" in categoria or "agua" in producto or "cola" in producto or "jugo" in producto:
        return "Ubicar cerca de snacks para incentivar compra combinada"
    elif "limpieza" in categoria or "detergente" in producto or "cloro" in producto:
        return "Agrupar con productos complementarios de limpieza"
    elif ventas_producto >= promedio_ventas:
        return "Mantener en zona de fácil acceso por su alta rotación"
    else:
        return "Mantener ubicación actual y revisar semanalmente"


# =========================================================
# CARGA DE DATOS
# =========================================================

productos = cargar_productos()
ventas = cargar_ventas()

# =========================================================
# MENÚ LATERAL
# =========================================================

st.sidebar.title("📦 InventiQ")
st.sidebar.caption("Sistema inteligente de inventarios")

menu = st.sidebar.radio(
    "Menú principal",
    [
        "🏠 Inicio",
        "➕ Registrar producto",
        "🛒 Registrar venta",
        "📋 Inventario",
        "📊 Análisis de ventas",
        "💡 Recomendaciones",
        "🧾 Reportes"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "InventiQ ayuda a controlar productos, analizar ventas y tomar mejores decisiones de compra y ubicación."
)

# =========================================================
# INICIO
# =========================================================

if menu == "🏠 Inicio":
    st.markdown('<p class="titulo-principal">InventiQ</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitulo">Aplicación inteligente de gestión de inventarios para pequeñas tiendas</p>',
        unsafe_allow_html=True
    )

    total_productos = len(productos)
    stock_total = int(productos["stock"].sum()) if not productos.empty else 0
    ventas_totales = float(ventas["total"].sum()) if not ventas.empty else 0

    productos_stock_bajo = 0
    if not productos.empty:
        productos_stock_bajo = len(productos[productos["stock"] <= productos["stock_minimo"]])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Productos registrados</div>
                <div class="metric-value">{total_productos}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Stock total</div>
                <div class="metric-value">{stock_total}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Stock bajo</div>
                <div class="metric-value">{productos_stock_bajo}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Ventas registradas</div>
                <div class="metric-value">{formato_dinero(ventas_totales)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### 🧠 ¿Qué hace InventiQ?")

    st.markdown(
        """
        <div class="card">
        <strong>InventiQ</strong> permite registrar productos, controlar existencias,
        registrar ventas, identificar productos más vendidos, detectar productos con baja rotación
        y generar recomendaciones para comprar más o menos mercadería. Además, sugiere estrategias
        de ubicación de productos dentro de la tienda para mejorar su venta.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🚨 Alertas rápidas")

    if productos.empty:
        st.markdown(
            '<div class="info-box">Todavía no hay productos registrados. Ingresa al módulo “Registrar producto”.</div>',
            unsafe_allow_html=True
        )
    else:
        stock_bajo_df = productos[productos["stock"] <= productos["stock_minimo"]]

        if stock_bajo_df.empty:
            st.markdown(
                '<div class="exito">No existen productos con stock crítico en este momento.</div>',
                unsafe_allow_html=True
            )
        else:
            for _, row in stock_bajo_df.iterrows():
                st.markdown(
                    f"""
                    <div class="alerta">
                    El producto <b>{row['nombre']}</b> tiene stock bajo.
                    Stock actual: <b>{row['stock']}</b> | Stock mínimo: <b>{row['stock_minimo']}</b>.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# =========================================================
# REGISTRAR PRODUCTO
# =========================================================

elif menu == "➕ Registrar producto":
    st.markdown('<p class="titulo-principal">Registrar producto</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitulo">Agrega productos al inventario de la tienda</p>',
        unsafe_allow_html=True
    )

    with st.form("form_producto"):
        col1, col2 = st.columns(2)

        with col1:
            codigo = st.text_input("Código del producto", placeholder="Ejemplo: P001")
            nombre = st.text_input("Nombre del producto", placeholder="Ejemplo: Coca-Cola 500 ml")
            categoria = st.selectbox(
                "Categoría",
                [
                    "Bebidas",
                    "Snacks",
                    "Lácteos",
                    "Limpieza",
                    "Aseo personal",
                    "Alimentos",
                    "Otros"
                ]
            )
            proveedor = st.text_input("Proveedor", placeholder="Ejemplo: Distribuidora XYZ")

        with col2:
            precio_compra = st.number_input("Precio de compra", min_value=0.0, step=0.05)
            precio_venta = st.number_input("Precio de venta", min_value=0.0, step=0.05)
            stock = st.number_input("Stock inicial", min_value=0, step=1)
            stock_minimo = st.number_input("Stock mínimo", min_value=0, step=1)
            ubicacion = st.text_input("Ubicación en tienda", placeholder="Ejemplo: Estante frontal")

        guardar = st.form_submit_button("Guardar producto")

    if guardar:
        if codigo.strip() == "" or nombre.strip() == "":
            st.error("Debes ingresar al menos el código y el nombre del producto.")
        elif codigo in productos["codigo"].astype(str).values:
            st.error("Ya existe un producto con ese código.")
        else:
            nuevo_producto = pd.DataFrame(
                [{
                    "codigo": codigo,
                    "nombre": nombre,
                    "categoria": categoria,
                    "proveedor": proveedor,
                    "precio_compra": precio_compra,
                    "precio_venta": precio_venta,
                    "stock": int(stock),
                    "stock_minimo": int(stock_minimo),
                    "ubicacion": ubicacion,
                    "fecha_ingreso": datetime.now().strftime("%Y-%m-%d")
                }]
            )

            productos = pd.concat([productos, nuevo_producto], ignore_index=True)
            guardar_productos(productos)
            st.success("Producto registrado correctamente.")

    st.markdown("### 📋 Productos registrados")
    st.dataframe(productos, width="stretch")

# =========================================================
# REGISTRAR VENTA
# =========================================================

elif menu == "🛒 Registrar venta":
    st.markdown('<p class="titulo-principal">Registrar venta</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitulo">Registra la venta de productos y actualiza automáticamente el stock</p>',
        unsafe_allow_html=True
    )

    if productos.empty:
        st.warning("Primero debes registrar productos en el inventario.")
    else:
        productos_disponibles = productos[productos["stock"] > 0]

        if productos_disponibles.empty:
            st.error("No existen productos con stock disponible para vender.")
        else:
            lista_productos = productos_disponibles["codigo"] + " - " + productos_disponibles["nombre"]

            with st.form("form_venta"):
                producto_seleccionado = st.selectbox("Producto vendido", lista_productos)
                codigo_producto = producto_seleccionado.split(" - ")[0]

                producto_info = productos[productos["codigo"] == codigo_producto].iloc[0]

                st.info(
                    f"Producto: {producto_info['nombre']} | Stock disponible: {producto_info['stock']} | "
                    f"Precio unitario: {formato_dinero(producto_info['precio_venta'])}"
                )

                cantidad = st.number_input(
                    "Cantidad vendida",
                    min_value=1,
                    max_value=int(producto_info["stock"]),
                    step=1
                )

                total = cantidad * float(producto_info["precio_venta"])
                st.metric("Total de la venta", formato_dinero(total))

                vender = st.form_submit_button("Registrar venta")

            if vender:
                indice_producto = productos[productos["codigo"] == codigo_producto].index[0]
                productos.loc[indice_producto, "stock"] = int(productos.loc[indice_producto, "stock"]) - int(cantidad)

                nueva_venta = pd.DataFrame(
                    [{
                        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "codigo": codigo_producto,
                        "producto": producto_info["nombre"],
                        "categoria": producto_info["categoria"],
                        "cantidad": int(cantidad),
                        "precio_unitario": float(producto_info["precio_venta"]),
                        "total": float(total)
                    }]
                )

                ventas = pd.concat([ventas, nueva_venta], ignore_index=True)

                guardar_productos(productos)
                guardar_ventas(ventas)

                st.success("Venta registrada correctamente. El stock fue actualizado.")

                nuevo_stock = int(productos.loc[indice_producto, "stock"])
                stock_minimo = int(productos.loc[indice_producto, "stock_minimo"])

                if nuevo_stock <= stock_minimo:
                    st.warning(
                        f"Atención: el producto {producto_info['nombre']} quedó con stock bajo. "
                        f"Stock actual: {nuevo_stock}."
                    )

    st.markdown("### 🧾 Historial de ventas")
    historial = ventas.sort_values(by="fecha", ascending=False) if not ventas.empty else ventas
    st.dataframe(historial, width="stretch")

# =========================================================
# INVENTARIO
# =========================================================

elif menu == "📋 Inventario":
    st.markdown('<p class="titulo-principal">Inventario</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitulo">Consulta el estado actual de los productos registrados</p>',
        unsafe_allow_html=True
    )

    if productos.empty:
        st.warning("No existen productos registrados.")
    else:
        filtro_categoria = st.selectbox(
            "Filtrar por categoría",
            ["Todas"] + sorted(productos["categoria"].dropna().unique().tolist())
        )

        df_filtrado = productos.copy()

        if filtro_categoria != "Todas":
            df_filtrado = df_filtrado[df_filtrado["categoria"] == filtro_categoria]

        df_filtrado["estado_stock"] = df_filtrado.apply(
            lambda row: "Stock bajo" if row["stock"] <= row["stock_minimo"] else "Stock normal",
            axis=1
        )

        st.dataframe(df_filtrado, width="stretch")

        st.markdown("### 🔄 Actualizar stock")

        producto_actualizar = st.selectbox(
            "Selecciona un producto para aumentar stock",
            productos["codigo"] + " - " + productos["nombre"]
        )

        codigo_actualizar = producto_actualizar.split(" - ")[0]
        cantidad_agregar = st.number_input("Cantidad a agregar", min_value=0, step=1)

        if st.button("Agregar stock"):
            indice = productos[productos["codigo"] == codigo_actualizar].index[0]
            productos.loc[indice, "stock"] = int(productos.loc[indice, "stock"]) + int(cantidad_agregar)
            guardar_productos(productos)
            st.success("Stock actualizado correctamente.")

# =========================================================
# ANÁLISIS DE VENTAS
# =========================================================

elif menu == "📊 Análisis de ventas":
    st.markdown('<p class="titulo-principal">Análisis de ventas</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitulo">Identifica qué productos se venden más y cuáles se venden menos</p>',
        unsafe_allow_html=True
    )

    if ventas.empty:
        st.warning("Todavía no existen ventas registradas.")
    else:
        resumen = obtener_resumen_ventas(ventas)

        st.markdown("### 🏆 Productos más vendidos")
        mas_vendidos = resumen.sort_values(by="cantidad", ascending=False).head(5)
        st.dataframe(mas_vendidos, width="stretch")
        st.bar_chart(mas_vendidos.set_index("producto")["cantidad"])

        st.markdown("### 📉 Productos menos vendidos")
        menos_vendidos = resumen.sort_values(by="cantidad", ascending=True).head(5)
        st.dataframe(menos_vendidos, width="stretch")
        st.bar_chart(menos_vendidos.set_index("producto")["cantidad"])

        st.markdown("### 💰 Ingresos por producto")
        ingresos = resumen.sort_values(by="total", ascending=False)
        st.dataframe(ingresos, width="stretch")
        st.bar_chart(ingresos.set_index("producto")["total"])

# =========================================================
# RECOMENDACIONES
# =========================================================

elif menu == "💡 Recomendaciones":
    st.markdown('<p class="titulo-principal">Recomendaciones inteligentes</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitulo">Sugerencias de compra, reposición y ubicación estratégica de productos</p>',
        unsafe_allow_html=True
    )

    if productos.empty:
        st.warning("Primero debes registrar productos.")
    else:
        resumen = obtener_resumen_ventas(ventas)
        productos_analisis = productos.copy()

        if resumen.empty:
            productos_analisis["cantidad_vendida"] = 0
            productos_analisis["ingreso_generado"] = 0
            promedio_ventas = 0
        else:
            resumen_simple = resumen[["producto", "cantidad", "total"]].rename(
                columns={
                    "producto": "nombre",
                    "cantidad": "cantidad_vendida",
                    "total": "ingreso_generado"
                }
            )

            productos_analisis = productos_analisis.merge(
                resumen_simple,
                on="nombre",
                how="left"
            )

            productos_analisis["cantidad_vendida"] = productos_analisis["cantidad_vendida"].fillna(0)
            productos_analisis["ingreso_generado"] = productos_analisis["ingreso_generado"].fillna(0)
            promedio_ventas = productos_analisis["cantidad_vendida"].mean()

        productos_analisis["recomendacion_compra"] = productos_analisis.apply(
            lambda row: generar_recomendacion_compra(row, promedio_ventas),
            axis=1
        )

        productos_analisis["sugerencia_ubicacion"] = productos_analisis.apply(
            lambda row: generar_sugerencia_ubicacion(row, promedio_ventas),
            axis=1
        )

        columnas_mostrar = [
            "codigo",
            "nombre",
            "categoria",
            "stock",
            "stock_minimo",
            "cantidad_vendida",
            "recomendacion_compra",
            "sugerencia_ubicacion"
        ]

        st.markdown("### 🛒 Recomendaciones de compra")
        st.dataframe(productos_analisis[columnas_mostrar], width="stretch")

        st.markdown("### 🚨 Productos que requieren atención")

        productos_criticos = productos_analisis[
            (productos_analisis["stock"] <= productos_analisis["stock_minimo"]) |
            (productos_analisis["cantidad_vendida"] == 0)
        ]

        if productos_criticos.empty:
            st.markdown(
                '<div class="exito">No existen productos críticos en este momento.</div>',
                unsafe_allow_html=True
            )
        else:
            for _, row in productos_criticos.iterrows():
                st.markdown(
                    f"""
                    <div class="alerta">
                    <b>{row['nombre']}</b><br>
                    Stock actual: {row['stock']} | Ventas registradas: {int(row['cantidad_vendida'])}<br>
                    Recomendación: {row['recomendacion_compra']}<br>
                    Marketing: {row['sugerencia_ubicacion']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("### 🧠 Interpretación general")

        st.markdown(
            """
            <div class="card">
            La aplicación analiza el comportamiento de cada producto según su stock actual,
            stock mínimo y cantidad vendida. Con esta información, <strong>InventiQ</strong>
            recomienda qué productos comprar más, cuáles comprar menos y qué artículos deben ser
            reubicados dentro de la tienda para mejorar su visibilidad y aumentar sus ventas.
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# REPORTES
# =========================================================

elif menu == "🧾 Reportes":
    st.markdown('<p class="titulo-principal">Reportes</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitulo">Resumen general para la toma de decisiones</p>',
        unsafe_allow_html=True
    )

    if productos.empty:
        st.warning("No hay datos suficientes para generar reportes.")
    else:
        total_inventario = float((productos["precio_compra"] * productos["stock"]).sum())
        ganancia_estimada = float(((productos["precio_venta"] - productos["precio_compra"]) * productos["stock"]).sum())
        ventas_acumuladas = float(ventas["total"].sum()) if not ventas.empty else 0

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Valor del inventario", formato_dinero(total_inventario))

        with col2:
            st.metric("Ganancia potencial", formato_dinero(ganancia_estimada))

        with col3:
            st.metric("Ventas acumuladas", formato_dinero(ventas_acumuladas))

        st.markdown("### 📦 Stock por categoría")

        stock_categoria = productos.groupby("categoria", as_index=False)["stock"].sum()

        st.dataframe(stock_categoria, width="stretch")
        st.bar_chart(stock_categoria.set_index("categoria")["stock"])

        st.markdown("### 🧾 Exportar información")

        col_a, col_b = st.columns(2)

        with col_a:
            st.download_button(
                label="Descargar inventario en CSV",
                data=productos.to_csv(index=False).encode("utf-8"),
                file_name="inventario_inventiq.csv",
                mime="text/csv"
            )

        with col_b:
            st.download_button(
                label="Descargar ventas en CSV",
                data=ventas.to_csv(index=False).encode("utf-8"),
                file_name="ventas_inventiq.csv",
                mime="text/csv"
            )
