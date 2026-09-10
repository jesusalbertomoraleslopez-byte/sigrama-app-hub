"""
SIGRAMA App Hub - Streamlit Cloud & Local Portal
Concentradora Oficial de Aplicaciones de Industria SIGRAMA estilo Odoo.
"""
import os
import json
import base64
from pathlib import Path
from urllib.parse import urlencode
import streamlit as st

# Configuración de página Streamlit
st.set_page_config(
    page_title="SIGRAMA | Portal de Aplicaciones",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
IMG_DIR = BASE_DIR / "static" / "img"

def load_json(filepath):
    if not filepath.exists():
        return []
    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error cargando {filepath.name}: {e}")
        return []

def get_base64_image(path):
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode()
    return ""

# Estilos CSS personalizados inspirados en Odoo y Branding SIGRAMA
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=Questrial&display=swap');

    html, body, [class*="css"] {
        font-family: 'Questrial', -apple-system, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700;
    }

    /* Odoo Header Bar */
    .odoo-top-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #FFFFFF;
        padding: 18px 24px;
        border-radius: 12px;
        margin-bottom: 22px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    }

    .brand-title-large {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .hub-pill-badge {
        background: #DC2626;
        color: white;
        font-size: 0.72rem;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 6px;
        letter-spacing: 0.5px;
    }

    /* Cards */
    .app-card-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .app-card-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.08);
        border-color: #CBD5E1;
    }

    .role-badge-admin {
        background: #FEE2E2;
        color: #B91C1C;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 8px;
        text-transform: uppercase;
    }

    .role-badge-user {
        background: #E0E7FF;
        color: #3730A3;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 8px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# Carga de catálogo y usuarios
catalog = load_json(DATA_DIR / "catalog.json")
users = load_json(DATA_DIR / "users.json")

# Estado de autenticación
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ==============================================================================
# PANTALLA DE ACCESO (LOGIN)
# ==============================================================================
if not st.session_state.authenticated:
    col_l1, col_l2, col_l3 = st.columns([1, 1.4, 1])
    with col_l2:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        logo_path = IMG_DIR / "logo_sigrama.png"
        if logo_path.exists():
            b64_logo = get_base64_image(logo_path)
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="background: #FFFFFF; display: inline-block; padding: 12px 24px; border-radius: 12px; box-shadow: 0 4px 14px rgba(0,0,0,0.06); margin-bottom: 12px;">
                    <img src="data:image/png;base64,{b64_logo}" style="width: 180px; height: auto; display: block;" alt="SIGRAMA">
                </div>
                <h2 style="margin: 4px 0 2px 0; color: #0F172A; font-weight: 800;">Concentradora de Aplicaciones</h2>
                <p style="color: #64748B; font-size: 14px; margin: 0;">Portal Unificado de Operaciones &middot; SIGRAMA HUB</p>
            </div>
            """, unsafe_allow_html=True)

        with st.form("form_sso_login", clear_on_submit=False):
            st.markdown("##### 🔐 Iniciar Sesión")
            user_names = [u["name"] for u in users]
            selected_name = st.selectbox("Colaborador / Usuario:", user_names, index=0)
            password_input = st.text_input("Clave de Acceso:", type="password", placeholder="••••••••")
            
            submit_login = st.form_submit_button("Ingresar al Portal", type="primary", use_container_width=True)
            
            if submit_login:
                matched_user = next((u for u in users if u["name"] == selected_name), None)
                if matched_user and matched_user["password"] == password_input.strip():
                    st.session_state.authenticated = True
                    st.session_state.current_user = matched_user
                    st.success(f"Bienvenido, {matched_user['name']}")
                    st.rerun()
                else:
                    st.error("❌ Clave o contraseña incorrecta para este colaborador.")

        st.info("🔑 **Claves de acceso:**\n- Administrador: `SigramaAdmin2026`\n- Operadores: `MAQUINADOS`")
    st.stop()

# ==============================================================================
# PORTAL PRINCIPAL AUTENTICADO
# ==============================================================================
curr_user = st.session_state.current_user
user_name = curr_user["name"]
is_admin = curr_user.get("is_global_admin", False)

# Barra superior corporativa
logo_path = IMG_DIR / "logo_sigrama.png"
b64_logo = get_base64_image(logo_path)

c_head1, c_head2, c_head3 = st.columns([2.5, 3.5, 2])
with c_head1:
    if b64_logo:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px;">
            <img src="data:image/png;base64,{b64_logo}" style="height: 38px; background: white; padding: 2px 6px; border-radius: 6px;" alt="Logo">
            <span style="font-size: 1.3rem; font-weight: 900; color: #0F172A;">SIGRAMA <span class="hub-pill-badge">HUB</span></span>
        </div>
        """, unsafe_allow_html=True)
with c_head2:
    search_q = st.text_input("🔍 Buscar aplicación:", placeholder="Presiona para buscar por nombre o área...", label_visibility="collapsed")
with c_head3:
    col_u1, col_u2 = st.columns([2.2, 1.2])
    with col_u1:
        role_label = "Administrador" if is_admin else "Usuario Autorizado"
        st.markdown(f"<div style='text-align: right; line-height: 1.2;'><b style='font-size: 0.85rem;'>{user_name}</b><br><span style='font-size: 0.72rem; color: #64748B;'>{role_label}</span></div>", unsafe_allow_html=True)
    with col_u2:
        if st.button("Salir 🚪", key="btn_logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.rerun()

st.markdown("<hr style='margin: 10px 0 20px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

# Filtrado por RBAC
user_perms = curr_user.get("permissions", {})
authorized_apps = []

for app in catalog:
    app_id = app.get("id")
    if is_admin:
        app_copy = dict(app)
        app_copy["user_role"] = "Admin"
        authorized_apps.append(app_copy)
    else:
        perm = user_perms.get(app_id, "N/A")
        if perm != "N/A":
            app_copy = dict(app)
            app_copy["user_role"] = perm
            authorized_apps.append(app_copy)

# Categorías
categories = ["Todas"]
for a in authorized_apps:
    cat = a.get("category", "General")
    if cat not in categories:
        categories.append(cat)

cat_selected = st.radio("Filtrar por Departamento:", categories, horizontal=True, label_visibility="collapsed")

# Filtrado por búsqueda y categoría
display_apps = []
for a in authorized_apps:
    matches_cat = (cat_selected == "Todas") or (a.get("category") == cat_selected)
    matches_search = (not search_q) or (search_q.lower() in a["name"].lower()) or (search_q.lower() in a.get("description", "").lower())
    if matches_cat and matches_search:
        display_apps.append(a)

st.markdown(f"#### 📦 Aplicaciones Disponibles ({len(display_apps)})")

# Cuadrícula Odoo (Columnas de 3)
cols_per_row = 3
for row_idx in range(0, len(display_apps), cols_per_row):
    cols = st.columns(cols_per_row)
    row_slice = display_apps[row_idx:row_idx+cols_per_row]
    for col_idx, app in enumerate(row_slice):
        with cols[col_idx]:
            with st.container(border=True):
                c_top1, c_top2 = st.columns([3, 1.2])
                with c_top1:
                    st.caption(f"**{app.get('category', 'GENERAL').upper()}**")
                    st.markdown(f"### {app['name']}")
                with c_top2:
                    role_cls = "role-badge-admin" if app.get("user_role") == "Admin" else "role-badge-user"
                    st.markdown(f"<span class='{role_cls}'>Rol: {app.get('user_role', 'Usuario')}</span>", unsafe_allow_html=True)
                
                st.write(app.get("description", ""))
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                
                # Enlaces y SSO
                sso_params = {
                    "sso_user": user_name,
                    "sso_role": app.get("user_role", "Usuario"),
                    "sso_token": "SIGRAMA_AUTH_TOKEN"
                }
                
                # Determinar URL objetivo (prioridad: Cloud URL o Local)
                target_url = app.get("cloud_url") or app.get("url") or f"http://localhost:{app.get('port', 8501)}"
                sep = "&" if "?" in target_url else "?"
                target_sso_url = f"{target_url}{sep}{urlencode(sso_params)}"
                
                c_btn1, c_btn2 = st.columns([1, 1])
                with c_btn1:
                    st.link_button("🚀 Abrir App", target_sso_url, type="primary", use_container_width=True)
                with c_btn2:
                    if app.get("cloud_url"):
                        st.link_button("☁️ Nube", app["cloud_url"], use_container_width=True)
                    else:
                        st.link_button("🌐 Puerto", target_url, use_container_width=True)

st.markdown("""
<div style="text-align: center; margin-top: 40px; padding: 20px; color: #94A3B8; font-size: 12px; border-top: 1px solid #E2E8F0;">
    Industria Sigrama S.A. de C.V. &bull; Portal de Aplicaciones Integrado &bull; <i>Ingeniería que da resultados!!</i>
</div>
""", unsafe_allow_html=True)
