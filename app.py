import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import hashlib

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="InventiQ - Gestión de Inventarios",
    page_icon="📦",
    layout="wide"
)

USUARIOS_FILE = Path("usuarios_inventiq.csv")
PRODUCTOS_FILE = Path("productos_inventiq.csv")
VENTAS_FILE = Path("ventas_inventiq.csv")

COLUMNAS_USUARIOS = [
    "usuario",
    "password_hash",
    "tienda",
    "encargado",
    "fecha_registro"
]

COLUMNAS_PRODUCTOS = [
    "tienda",
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
    "tienda",
    "fecha",
    "codigo",
    "producto",
    "categoria",
    "cantidad",
    "precio_unitario",
    "total"
]

# =========================================================
# ESTILO VISUAL GENERAL
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f4f7fb !important;
        color: #111827 !important;
    }

    .block-container {
        background-color: #f4f7fb !important;
        color: #111827 !important;
        padding-top: 2rem;
    }

    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #111827 !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e5e7eb !important;
    }

    section[data-testid="stSidebar"] * {
        color: #111827 !important;
    }

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

    input, textarea, select {
        background-color: #ffffff !important;
        color: #111827 !important;
    }

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
# FUNCIONES GENERALES
# =========================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def formato_dinero(valor):
    return f"${valor:,.2f}"


def cargar_csv(ruta, columnas):
    if ruta.exists():
        df = pd.read_csv(ruta)
    else:
        df = pd.DataFrame(columns=columnas)

    for col in columnas:
        if col not in df.columns:
            df[col] = ""

    return df[columnas]


def guardar_csv(df, ruta):
    df.to_csv(ruta, index=False)


def cargar_usuarios():
    return cargar_csv(USUARIOS_FILE, COLUMNAS_USUARIOS)


def guardar_usuarios(df):
    guardar_csv(df, USUARIOS_FILE)


def cargar_productos():
    df = cargar_csv(PRODUCTOS_FILE, COLUMNAS_PRODUCTOS)

    if not df.empty:
        df["precio_compra"] = pd.to_numeric(df["precio_compra"], errors="coerce").fillna(0)
        df["precio_venta"] = pd.to_numeric(df["precio_venta"], errors="coerce").fillna(0)
        df["stock"] = pd.to_numeric(df["stock"], errors="coerce").fillna(0).astype(int)
        df["stock_minimo"] = pd.to_numeric(df["stock_minimo"], errors="coerce").fillna(0).astype(int)

    return df


def guardar_productos(df):
    guardar_csv(df, PRODUCTOS_FILE)


def cargar_ventas():
    df = cargar_csv(VENTAS_FILE, COLUMNAS_VENTAS)

    if not df.empty:
        df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce").fillna(0).astype(int)
        df["precio_unitario"] = pd.to_numeric(df["precio_unitario"], errors="coerce").fillna(0)
        df["total"] = pd.to_numeric(df["total"], errors="coerce").fillna(0)

    return df


def guardar_ventas(df):
    guardar_csv(df, VENTAS_FILE)


def obtener_resumen_ventas(ventas_tienda):
    if ventas_tienda.empty:
        return pd.DataFrame(columns=["producto", "categoria", "cantidad", "total"])

    resumen = (
        ventas_tienda.groupby(["producto", "categoria"], as_index=False)
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
# ESTADO DE SESIÓN
# =========================================================

if "logueado" not in st.session_state:
    st.session_state.logueado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

if "tienda" not in st.session_state:
    st.session_state.tienda = ""

if "encargado" not in st.session_state:
    st.session_state.encargado = ""

if "mostrar_registro" not in st.session_state:
    st.session_state.mostrar_registro = False

if "mensaje_registro" not in st.session_state:
    st.session_state.mensaje_registro = ""


# =========================================================
# LOGIN Y REGISTRO CORREGIDO Y CENTRADO
# =========================================================

def pantalla_login_registro():
    usuarios = cargar_usuarios()

    st.markdown(
        """
        <style>

        header[data-testid="stHeader"] {
            background: transparent !important;
        }

        .stApp {
            background: linear-gradient(135deg, #2dd4bf, #60a5fa, #f9a8d4) !important;
        }

        .block-container {
            max-width: 520px !important;
            padding-top: 8vh !important;
            padding-bottom: 4vh !important;
            background: transparent !important;
        }

        div[data-testid="stForm"] {
            background: #ffffff !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 24px !important;
            padding: 34px !important;
            box-shadow: 0 18px 45px rgba(0,0,0,0.22) !important;
        }

        div[data-testid="stForm"] * {
            color: #111827 !important;
        }

        .login-icon {
            width: 90px;
            height: 90px;
            background: #0f3a66;
            color: white !important;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0 auto -35px auto;
            font-size: 46px;
            border: 5px solid white;
            box-shadow: 0 8px 20px rgba(0,0,0,0.22);
            position: relative;
            z-index: 5;
        }

        .login-title {
            text-align: center;
            font-size: 34px;
            font-weight: 800;
            color: #0f172a !important;
            margin-top: 42px;
            margin-bottom: 4px;
        }

        .login-subtitle {
            text-align: center;
            font-size: 14px;
            color: #64748b !important;
            margin-bottom: 20px;
        }

        .login-link {
            text-align: center;
            font-size: 14px;
            color: #0f3a66 !important;
            font-weight: 600;
            margin-top: 16px;
            margin-bottom: 8px;
        }

        .stTextInput label {
            color: #111827 !important;
            font-weight: 600 !important;
        }

        .stTextInput input {
            border-radius: 10px !important;
            border: 1px solid #d1d5db !important;
            padding: 10px !important;
            background-color: #ffffff !important;
            color: #111827 !important;
        }

        .stFormSubmitButton button {
            width: 100%;
            background-color: #2563eb !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
            font-weight: 700 !important;
            padding: 0.70rem 1rem !important;
            margin-top: 8px;
        }

        .stButton button {
            width: 100%;
            background-color: #3b82f6 !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
            font-weight: 700 !important;
            padding: 0.65rem 1rem !important;
        }

        .stButton button:hover,
        .stFormSubmitButton button:hover {
            background-color: #2563eb !important;
            color: white !important;
        }

        div[data-testid="stAlert"] {
            border-radius: 12px !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.mostrar_registro:
        st.markdown('<div class="login-icon">👤</div>', unsafe_allow_html=True)

        with st.form("form_login"):
            st.markdown('<div class="login-title">InventiQ</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="login-subtitle">Inicia sesión para gestionar tu inventario</div>',
                unsafe_allow_html=True
            )

            if st.session_state.mensaje_registro:
                st.success(st.session_state.mensaje_registro)
                st.session_state.mensaje_registro = ""

            usuario_login = st.text_input("Usuario", placeholder="Ingresa tu usuario")
            password_login = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")
            ingresar = st.form_submit_button("LOGIN")

        if ingresar:
            if usuario_login.strip() == "" or password_login.strip() == "":
                st.warning("Ingresa usuario y contraseña.")
            else:
                password_hash = hash_password(password_login)

                usuario_encontrado = usuarios[
                    (usuarios["usuario"] == usuario_login) &
                    (usuarios["password_hash"] == password_hash)
                ]

                if usuario_encontrado.empty:
                    st.error("Usuario o contraseña incorrectos.")
                else:
                    datos = usuario_encontrado.iloc[0]

                    st.session_state.logueado = True
                    st.session_state.usuario = datos["usuario"]
                    st.session_state.tienda = datos["tienda"]
                    st.session_state.encargado = datos["encargado"]

                    st.success("Inicio de sesión correcto.")
                    st.rerun()

        st.markdown(
            '<div class="login-link">¿No tienes cuenta?</div>',
            unsafe_allow_html=True
        )

        if st.button("Registrarse"):
            st.session_state.mostrar_registro = True
            st.rerun()

    else:
        st.markdown('<div class="login-icon">📝</div>', unsafe_allow_html=True)

        with st.form("form_registro"):
            st.markdown('<div class="login-title">Crear cuenta</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="login-subtitle">Registra tu tienda para usar InventiQ</div>',
                unsafe_allow_html=True
            )

            tienda = st.text_input("Nombre de la tienda", placeholder="Ejemplo: Minimarket La Esquina")
            encargado = st.text_input("Nombre del encargado", placeholder="Ejemplo: Juan Pérez")
            nuevo_usuario = st.text_input("Crear usuario", placeholder="Ejemplo: tienda1")
            nueva_password = st.text_input("Crear contraseña", type="password")
            confirmar_password = st.text_input("Confirmar contraseña", type="password")
            registrar = st.form_submit_button("LISTO")

        if registrar:
            if tienda.strip() == "" or encargado.strip() == "" or nuevo_usuario.strip() == "" or nueva_password.strip() == "":
                st.warning("Completa todos los campos.")
            elif nueva_password != confirmar_password:
                st.error("Las contraseñas no coinciden.")
            elif nuevo_usuario in usuarios["usuario"].astype(str).values:
                st.error("Ese usuario ya existe. Elige otro.")
            else:
                nuevo_registro = pd.DataFrame(
                    [{
                        "usuario": nuevo_usuario,
                        "password_hash": hash_password(nueva_password),
                        "tienda": tienda,
                        "encargado": encargado,
                        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }]
                )

                usuarios = pd.concat([usuarios, nuevo_registro], ignore_index=True)
                guardar_usuarios(usuarios)

                st.session_state.mostrar_registro = False
                st.session_state.mensaje_registro = "Cuenta creada correctamente. Ahora inicia sesión."
                st.rerun()

        st.markdown(
            '<div class="login-link">¿Ya tienes cuenta?</div>',
            unsafe_allow_html=True
        )

        if st.button("Volver al login"):
            st.session_state.mostrar_registro = False
            st.rerun()


if not st.session_state.logueado:
    pantalla_login_registro()
    st.stop()


# =========================================================
# CARGA DE DATOS
# =========================================================

usuarios = cargar_usuarios()
productos = cargar_productos()
ventas = cargar_ventas()

tienda_actual = st.session_state.tienda
usuario_actual = st.session_state.usuario
encargado_actual = st.session_state.encargado

productos_tienda = productos[productos["tienda"] == tienda_actual].copy()
ventas_tienda = ventas[ventas["tienda"] == tienda_actual].copy()


# =========================================================
# MENÚ LATERAL
# =========================================================

st.sidebar.title("📦 InventiQ")
st.sidebar.caption("Panel de tienda")

st.sidebar.markdown(
    f"""
    <div class="card">
    <strong>Tienda:</strong><br>{tienda_actual}<br><br>
    <strong>Encargado:</strong><br>{encargado_actual}
    </div>
    """,
    unsafe_allow_html=True
)

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

if st.sidebar.button("Cerrar sesión"):
    st.session_state.logueado = False
    st.session_state.usuario = ""
    st.session_state.tienda = ""
    st.session_state.encargado = ""
    st.session_state.mostrar_registro = False
    st.rerun()


# =========================================================
# INICIO
# =========================================================

if menu == "🏠 Inicio":
    st.markdown('<p class="titulo-principal">InventiQ</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="subtitulo">Panel de gestión de inventarios - {tienda_actual}</p>',
        unsafe_allow_html=True
    )

    total_productos = len(productos_tienda)
    stock_total = int(productos_tienda["stock"].sum()) if not productos_tienda.empty else 0
    ventas_totales = float(ventas_tienda["total"].sum()) if not ventas_tienda.empty else 0

    productos_stock_bajo = 0
    if not productos_tienda.empty:
        productos_stock_bajo = len(productos_tienda[productos_tienda["stock"] <= productos_tienda["stock_minimo"]])

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
        <strong>InventiQ</strong> permite que cada tienda tenga su propio panel de inventario.
        Desde aquí puedes registrar productos, registrar ventas, controlar stock, revisar productos
        más vendidos, identificar productos con baja rotación y recibir recomendaciones de compra
        y ubicación estratégica dentro del local.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🚨 Alertas rápidas")

    if productos_tienda.empty:
        st.markdown(
            '<div class="info-box">Todavía no hay productos registrados para esta tienda.</div>',
            unsafe_allow_html=True
        )
    else:
        stock_bajo_df = productos_tienda[productos_tienda["stock"] <= productos_tienda["stock_minimo"]]

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
        f'<p class="subtitulo">Agrega productos al inventario de {tienda_actual}</p>',
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
                    "Papelería",
                    "Tecnología",
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
        else:
            producto_existente = productos[
                (productos["tienda"] == tienda_actual) &
                (productos["codigo"] == codigo)
            ]

            if not producto_existente.empty:
                st.error("Ya existe un producto con ese código en esta tienda.")
            else:
                nuevo_producto = pd.DataFrame(
                    [{
                        "tienda": tienda_actual,
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
                st.rerun()

    st.markdown("### 📋 Productos registrados")
    st.dataframe(productos_tienda, width="stretch")


# =========================================================
# REGISTRAR VENTA
# =========================================================

elif menu == "🛒 Registrar venta":
    st.markdown('<p class="titulo-principal">Registrar venta</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="subtitulo">Registra ventas de productos de {tienda_actual}</p>',
        unsafe_allow_html=True
    )

    if productos_tienda.empty:
        st.warning("Primero debes registrar productos en el inventario.")
    else:
        productos_disponibles = productos_tienda[productos_tienda["stock"] > 0]

        if productos_disponibles.empty:
            st.error("No existen productos con stock disponible para vender.")
        else:
            lista_productos = productos_disponibles["codigo"] + " - " + productos_disponibles["nombre"]

            with st.form("form_venta"):
                producto_seleccionado = st.selectbox("Producto vendido", lista_productos)
                codigo_producto = producto_seleccionado.split(" - ")[0]

                producto_info = productos_tienda[productos_tienda["codigo"] == codigo_producto].iloc[0]

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
                condicion_producto = (
                    (productos["tienda"] == tienda_actual) &
                    (productos["codigo"] == codigo_producto)
                )

                indice_producto = productos[condicion_producto].index[0]
                productos.loc[indice_producto, "stock"] = int(productos.loc[indice_producto, "stock"]) - int(cantidad)

                nueva_venta = pd.DataFrame(
                    [{
                        "tienda": tienda_actual,
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
                st.rerun()

    st.markdown("### 🧾 Historial de ventas")
    historial = ventas_tienda.sort_values(by="fecha", ascending=False) if not ventas_tienda.empty else ventas_tienda
    st.dataframe(historial, width="stretch")


# =========================================================
# INVENTARIO
# =========================================================

elif menu == "📋 Inventario":
    st.markdown('<p class="titulo-principal">Inventario</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="subtitulo">Consulta, actualiza o elimina productos de {tienda_actual}</p>',
        unsafe_allow_html=True
    )

    if productos_tienda.empty:
        st.warning("No existen productos registrados para esta tienda.")
    else:
        filtro_categoria = st.selectbox(
            "Filtrar por categoría",
            ["Todas"] + sorted(productos_tienda["categoria"].dropna().unique().tolist())
        )

        df_filtrado = productos_tienda.copy()

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
            productos_tienda["codigo"] + " - " + productos_tienda["nombre"],
            key="producto_actualizar"
        )

        codigo_actualizar = producto_actualizar.split(" - ")[0]
        cantidad_agregar = st.number_input("Cantidad a agregar", min_value=0, step=1)

        if st.button("Agregar stock"):
            condicion_producto = (
                (productos["tienda"] == tienda_actual) &
                (productos["codigo"] == codigo_actualizar)
            )

            indice = productos[condicion_producto].index[0]
            productos.loc[indice, "stock"] = int(productos.loc[indice, "stock"]) + int(cantidad_agregar)

            guardar_productos(productos)
            st.success("Stock actualizado correctamente.")
            st.rerun()

        st.markdown("### 🗑️ Eliminar producto")

        producto_eliminar = st.selectbox(
            "Selecciona un producto para eliminar",
            productos_tienda["codigo"] + " - " + productos_tienda["nombre"],
            key="producto_eliminar"
        )

        codigo_eliminar = producto_eliminar.split(" - ")[0]

        confirmar_eliminacion = st.checkbox(
            "Confirmo que deseo eliminar este producto del inventario"
        )

        if st.button("Eliminar producto"):
            if confirmar_eliminacion:
                productos = productos[
                    ~(
                        (productos["tienda"] == tienda_actual) &
                        (productos["codigo"] == codigo_eliminar)
                    )
                ]

                guardar_productos(productos)
                st.success("Producto eliminado correctamente.")
                st.rerun()
            else:
                st.warning("Debes confirmar la eliminación antes de continuar.")


# =========================================================
# ANÁLISIS DE VENTAS
# =========================================================

elif menu == "📊 Análisis de ventas":
    st.markdown('<p class="titulo-principal">Análisis de ventas</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="subtitulo">Productos más vendidos y menos vendidos de {tienda_actual}</p>',
        unsafe_allow_html=True
    )

    if ventas_tienda.empty:
        st.warning("Todavía no existen ventas registradas para esta tienda.")
    else:
        resumen = obtener_resumen_ventas(ventas_tienda)

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
        f'<p class="subtitulo">Sugerencias de compra y ubicación para {tienda_actual}</p>',
        unsafe_allow_html=True
    )

    if productos_tienda.empty:
        st.warning("Primero debes registrar productos.")
    else:
        resumen = obtener_resumen_ventas(ventas_tienda)
        productos_analisis = productos_tienda.copy()

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


# =========================================================
# REPORTES
# =========================================================

elif menu == "🧾 Reportes":
    st.markdown('<p class="titulo-principal">Reportes</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="subtitulo">Resumen general de {tienda_actual}</p>',
        unsafe_allow_html=True
    )

    if productos_tienda.empty:
        st.warning("No hay datos suficientes para generar reportes.")
    else:
        total_inventario = float((productos_tienda["precio_compra"] * productos_tienda["stock"]).sum())
        ganancia_estimada = float(((productos_tienda["precio_venta"] - productos_tienda["precio_compra"]) * productos_tienda["stock"]).sum())
        ventas_acumuladas = float(ventas_tienda["total"].sum()) if not ventas_tienda.empty else 0

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Valor del inventario", formato_dinero(total_inventario))

        with col2:
            st.metric("Ganancia potencial", formato_dinero(ganancia_estimada))

        with col3:
            st.metric("Ventas acumuladas", formato_dinero(ventas_acumuladas))

        st.markdown("### 📦 Stock por categoría")

        stock_categoria = productos_tienda.groupby("categoria", as_index=False)["stock"].sum()

        st.dataframe(stock_categoria, width="stretch")
        st.bar_chart(stock_categoria.set_index("categoria")["stock"])

        st.markdown("### 🧾 Exportar información")

        col_a, col_b = st.columns(2)

        with col_a:
            st.download_button(
                label="Descargar inventario en CSV",
                data=productos_tienda.to_csv(index=False).encode("utf-8"),
                file_name=f"inventario_{tienda_actual}.csv",
                mime="text/csv"
            )

        with col_b:
            st.download_button(
                label="Descargar ventas en CSV",
                data=ventas_tienda.to_csv(index=False).encode("utf-8"),
                file_name=f"ventas_{tienda_actual}.csv",
                mime="text/csv"
            )
