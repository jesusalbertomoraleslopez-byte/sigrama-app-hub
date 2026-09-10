"""
SIGRAMA App Hub - Streamlit Cloud Wrapper
Renders the 100% exact Odoo-Style Enterprise UI inside Streamlit Cloud.
"""
import os
import json
import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="SIGRAMA - Portal de Aplicaciones",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ocultar marcos y paddings de Streamlit
st.markdown("""
<style>
    #MainMenu, header, footer, [data-testid="stHeader"] { display: none !important; }
    .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
    [data-testid="stAppViewContainer"] { padding: 0 !important; background-color: #F1F5F9; }
    iframe { border: none !important; width: 100% !important; }
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent

def load_file(p):
    return p.read_text(encoding="utf-8-sig") if p.exists() else ""

css_content = load_file(BASE_DIR / "static" / "css" / "odoo-theme.css")
catalog_data = json.loads(load_file(BASE_DIR / "data" / "catalog.json") or "[]")
users_data = json.loads(load_file(BASE_DIR / "data" / "users.json") or "[]")

logo_path = BASE_DIR / "static" / "img" / "logo_sigrama.png"
b64_logo = base64.b64encode(logo_path.read_bytes()).decode() if logo_path.exists() else ""

# HTML completo autónomo
standalone_html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <style>
    {css_content}
    body {{
      background-color: #F1F5F9;
      min-height: 100vh;
      overflow-y: auto;
    }}
  </style>
</head>
<body>

  <!-- LOGIN OVERLAY -->
  <div class="login-overlay" id="loginOverlay" style="display: none;">
    <div class="login-card">
      <img src="data:image/png;base64,{b64_logo}" alt="SIGRAMA" class="login-brand-logo">
      <h2 class="login-title">Acceso Concentradora</h2>
      <p class="login-subtitle">Ingresa tus credenciales corporativas autorizadas</p>

      <form class="login-form" id="loginForm" method="POST" action="#">
        <div class="login-field">
          <label for="loginUserInput">Usuario Corporativo o Código de Acceso</label>
          <input type="text" id="loginUserInput" name="username" class="login-input" placeholder="Ej. jmorales o SIG-ADM-01" required autocomplete="username">
        </div>

        <div class="login-field">
          <label for="loginPasswordInput">Clave de Acceso</label>
          <input type="password" id="loginPasswordInput" name="password" class="login-input" placeholder="Ingresa tu clave de acceso" required autocomplete="current-password">
        </div>

        <button type="submit" class="btn-login-submit" id="btnLoginSubmit">
          <span>Ingresar al Portal</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="5" y1="12" x2="19" y2="12"></line>
            <polyline points="12 5 19 12 12 19"></polyline>
          </svg>
        </button>
      </form>
    </div>
  </div>

  <!-- ODOO TOP NAVBAR -->
  <header class="odoo-navbar">
    <div class="navbar-left">
      <button class="app-switcher-btn" id="btnHomeLauncher" title="Inicio / Menú de Aplicaciones">
        <div class="app-switcher-grid-icon">
          <span></span><span></span><span></span>
          <span></span><span></span><span></span>
          <span></span><span></span><span></span>
        </div>
      </button>

      <div class="brand-container" id="brandHomeLink" onclick="closeWorkspace()">
        <img src="data:image/png;base64,{b64_logo}" alt="SIGRAMA" class="brand-logo">
        <div class="brand-title">
          SIGRAMA <span class="brand-badge">HUB</span>
        </div>
      </div>
    </div>

    <div class="navbar-center">
      <div class="search-container">
        <span class="search-icon">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </span>
        <input type="text" id="searchInput" class="search-input" placeholder="Buscar aplicaciones... (Presiona /)" autocomplete="off">
        <span class="search-shortcut-badge">/</span>
      </div>
    </div>

    <div class="navbar-right">
      <div class="sys-stat-pill" id="sysStatsDisplay">
        <span class="stat-dot-live"></span>
        <span id="statTextLive">En línea &middot; Streamlit Cloud</span>
      </div>

      <!-- USER PROFILE WIDGET -->
      <div class="user-profile-widget" id="userProfileWidget" style="display: none;">
        <div class="user-avatar-circle" id="userAvatarCircle">JM</div>
        <div class="user-info-text">
          <span class="user-full-name" id="userFullName">Usuario</span>
          <span class="user-role-badge" id="userRoleBadge">Rol</span>
        </div>
        <button class="btn-logout" id="btnLogout" title="Cerrar Sesión">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
        </button>
      </div>

      <div class="clock-display" id="clockDisplay">00:00:00</div>
    </div>
  </header>

  <!-- CATEGORY SUBNAV -->
  <nav class="category-navbar" id="categoriesNav">
    <button class="category-pill active">Todas las Apps</button>
  </nav>

  <!-- MAIN WRAPPER -->
  <main class="main-wrapper">
    <!-- APPS GRID -->
    <div class="hub-container" id="hubContainer">
      <div class="hub-header">
        <div class="hub-title-block">
          <h1>Centro de Aplicaciones y Servicios</h1>
          <p id="hubWelcomeText">Plataforma centralizada de operaciones, ingeniería y gestión SIGRAMA</p>
        </div>
        <div class="hub-stats-badge" id="totalAppsBadge">
          Cargando...
        </div>
      </div>

      <div class="apps-grid" id="appsGrid"></div>
    </div>

    <!-- EMBEDDED WORKSPACE -->
    <div class="workspace-container" id="workspaceContainer">
      <div class="workspace-toolbar">
        <div class="workspace-left">
          <button class="btn-back-to-hub" id="btnBackToHub" title="Volver al menú de aplicaciones">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="19" y1="12" x2="5" y2="12"></line>
              <polyline points="12 19 5 12 12 5"></polyline>
            </svg>
            <span>Volver al Menú</span>
          </button>
          <span class="workspace-app-title" id="workspaceAppTitle">Aplicación</span>
        </div>

        <div class="workspace-right">
          <button class="btn-icon-action" id="btnWorkspaceReload" title="Recargar Aplicación" style="color: #cbd5e1;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"></path>
              <path d="M21 3v5h-5"></path>
            </svg>
          </button>
          <button class="btn-icon-action" id="btnWorkspaceNewTab" title="Abrir en Pestaña Externa" style="color: #cbd5e1;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M15 3h6v6"></path>
              <path d="M10 14 21 3"></path>
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
            </svg>
          </button>
        </div>
      </div>

      <div id="workspaceNotice" style="display: none; flex: 1; align-items: center; justify-content: center; background: #f8fafc; min-height: 500px;">
        <div id="workspaceNoticeText"></div>
      </div>
      <iframe id="workspaceIframe" class="workspace-iframe-frame" src="about:blank" allow="clipboard-read; clipboard-write"></iframe>
    </div>
  </main>

  <div class="toast-container" id="toastContainer"></div>

  <!-- CLIENT SCRIPT -->
  <script>
    const CATALOG = {json.dumps(catalog_data)};
    const USERS = {json.dumps(users_data)};

    const ICONS = {{
      "shopping-cart": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>`,
      "truck": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18.5" r="2.5"/><circle cx="7" cy="18.5" r="2.5"/></svg>`,
      "scissors": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><path d="M8.12 8.12 12 12"/><circle cx="6" cy="18" r="3"/><path d="M8.12 15.88 16 8l4 4-8 8"/></svg>`,
      "ruler": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 4.27-2-2a2 2 0 0 0-2.83 0l-14.14 14.14a2 2 0 0 0 0 2.83l2 2a2 2 0 0 0 2.83 0l14.14-14.14a2 2 0 0 0 0-2.83Z"/><path d="m14.5 5.5 3 3"/><path d="m11.5 8.5 2 2"/><path d="m8.5 11.5 3 3"/><path d="m5.5 14.5 2 2"/></svg>`,
      "shield-check": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>`,
      "calculator": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="20" x="4" y="2" rx="2"/><line x1="8" x2="16" y1="6" y2="6"/><line x1="16" x2="16" y1="14" y2="18"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/></svg>`,
      "layers": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 12.5-8.58 3.91a2 2 0 0 1-1.66 0L2.6 12.5"/><path d="m22 17.5-8.58 3.91a2 2 0 0 1-1.66 0L2.6 17.5"/></svg>`,
      "users": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
      "cpu": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>`,
      "globe": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>`
    }};

    let currentUser = null;
    let activeCategory = "all";
    let searchQuery = "";
    let currentOpenedApp = null;

    const loginOverlay = document.getElementById("loginOverlay");
    const loginUserInput = document.getElementById("loginUserInput");
    const loginPasswordInput = document.getElementById("loginPasswordInput");
    const userProfileWidget = document.getElementById("userProfileWidget");
    const userAvatarCircle = document.getElementById("userAvatarCircle");
    const userFullName = document.getElementById("userFullName");
    const userRoleBadge = document.getElementById("userRoleBadge");
    const btnLogout = document.getElementById("btnLogout");
    const appsGrid = document.getElementById("appsGrid");
    const categoriesNav = document.getElementById("categoriesNav");
    const searchInput = document.getElementById("searchInput");
    const clockEl = document.getElementById("clockDisplay");
    const hubContainer = document.getElementById("hubContainer");
    const workspaceContainer = document.getElementById("workspaceContainer");
    const workspaceIframe = document.getElementById("workspaceIframe");
    const workspaceAppTitle = document.getElementById("workspaceAppTitle");
    const workspaceNotice = document.getElementById("workspaceNotice");
    const workspaceNoticeText = document.getElementById("workspaceNoticeText");
    const totalAppsBadge = document.getElementById("totalAppsBadge");
    const hubWelcomeText = document.getElementById("hubWelcomeText");
    const toastContainer = document.getElementById("toastContainer");

    document.addEventListener("DOMContentLoaded", () => {{
      initClock();
      setupEvents();
      checkStoredSession();
    }});

    function initClock() {{
      const update = () => {{
        clockEl.innerText = new Date().toLocaleTimeString([], {{ hour: '2-digit', minute: '2-digit', second: '2-digit' }});
      }};
      update();
      setInterval(update, 1000);
    }}

    function checkStoredSession() {{
      const savedUser = localStorage.getItem("sigrama_hub_user");
      if (savedUser) {{
        try {{
          const u = JSON.parse(savedUser);
          const found = USERS.find(x => x.id === u.id);
          if (found) {{
            setAuth(found);
            return;
          }}
        }} catch(e) {{}}
      }}
      showLogin();
    }}

    function showLogin() {{
      currentUser = null;
      loginOverlay.style.display = "flex";
      userProfileWidget.style.display = "none";
      appsGrid.innerHTML = "";
      if (loginUserInput) loginUserInput.value = "";
      if (loginPasswordInput) loginPasswordInput.value = "";
    }}

    function setAuth(user) {{
      currentUser = user;
      localStorage.setItem("sigrama_hub_user", JSON.stringify(user));
      loginOverlay.style.display = "none";
      userProfileWidget.style.display = "flex";

      const parts = user.name.split(" ");
      userAvatarCircle.innerText = (parts.length > 1 ? (parts[0][0] + parts[1][0]) : user.name.substring(0, 2)).toUpperCase();
      userFullName.innerText = user.name;
      userRoleBadge.innerText = user.is_global_admin ? "Administrador General" : "Usuario Autorizado";
      hubWelcomeText.innerText = `Sesión activa: ${{user.name}} | Aplicaciones autorizadas según tu perfil`;

      renderCategories();
      renderApps();
    }}

    function setupEvents() {{
      document.getElementById("loginForm").addEventListener("submit", (e) => {{
        e.preventDefault();
        const inputVal = (loginUserInput ? loginUserInput.value : "").trim().toLowerCase();
        const pass = (loginPasswordInput ? loginPasswordInput.value : "").trim();
        const matched = USERS.find(u => 
          (u.username && u.username.toLowerCase() === inputVal) ||
          (u.user_code && u.user_code.toLowerCase() === inputVal) ||
          (u.id && u.id.toLowerCase() === inputVal)
        );
        if (matched && matched.password === pass) {{
          showToast(`Bienvenido, ${{matched.name}}`, "success");
          if (window.PasswordCredential && navigator.credentials) {{
            try {{
              const cred = new PasswordCredential({{
                id: inputVal,
                password: pass,
                name: matched.name
              }});
              navigator.credentials.store(cred);
            }} catch(err) {{}}
          }}
          if (loginPasswordInput) loginPasswordInput.value = "";
          setAuth(matched);
        }} else {{
          showToast("Usuario o clave incorrectos", "error");
        }}
      }});

      btnLogout.addEventListener("click", () => {{
        localStorage.removeItem("sigrama_hub_user");
        showToast("Sesión cerrada", "info");
        showLogin();
      }});

      const btnBack = document.getElementById("btnBackToHub");
      if (btnBack) {{
        btnBack.addEventListener("click", closeWorkspace);
      }}

      searchInput.addEventListener("input", (e) => {{
        searchQuery = e.target.value.toLowerCase().trim();
        renderApps();
      }});

      document.addEventListener("keydown", (e) => {{
        if (e.key === "/" && document.activeElement !== searchInput && !loginOverlay.offsetParent) {{
          e.preventDefault();
          searchInput.focus();
        }}
      }});

      document.getElementById("btnHomeLauncher").addEventListener("click", closeWorkspace);
      document.getElementById("btnBackToHub").addEventListener("click", closeWorkspace);
      document.getElementById("btnWorkspaceReload").addEventListener("click", () => {{
        if (workspaceIframe.src) workspaceIframe.src = workspaceIframe.src;
      }});
      document.getElementById("btnWorkspaceNewTab").addEventListener("click", () => {{
        if (currentOpenedApp) window.open(currentOpenedApp.target_url, "_blank");
      }});
    }}

    function getAuthorizedApps() {{
      if (!currentUser) return [];
      const isGlobalAdmin = currentUser.is_global_admin;
      const perms = currentUser.permissions || {{}};
      const list = [];

      CATALOG.forEach(app => {{
        let role = "Usuario";
        if (isGlobalAdmin) {{
          role = "Admin";
          const copy = Object.assign({{}}, app, {{ user_role: role }});
          list.push(copy);
        }} else {{
          const p = perms[app.id] || "N/A";
          if (p !== "N/A") {{
            const copy = Object.assign({{}}, app, {{ user_role: p }});
            list.push(copy);
          }}
        }}
      }});
      return list;
    }}

    function renderCategories() {{
      const apps = getAuthorizedApps();
      const categories = ["all"];
      apps.forEach(a => {{
        if (a.category && !categories.includes(a.category)) categories.push(a.category);
      }});

      categoriesNav.innerHTML = categories.map(cat => {{
        const label = cat === "all" ? "Todas las Apps" : cat;
        const isActive = activeCategory === cat ? "active" : "";
        return `<button class="category-pill ${{isActive}}" onclick="selectCategory('${{cat}}')">${{label}}</button>`;
      }}).join("");
    }}

    window.selectCategory = function(cat) {{
      activeCategory = cat;
      renderCategories();
      renderApps();
    }};

    function renderApps() {{
      const apps = getAuthorizedApps();
      totalAppsBadge.innerText = `${{apps.length}} Apps Disponibles`;

      const filtered = apps.filter(app => {{
        const matchesCategory = activeCategory === "all" || app.category === activeCategory;
        const matchesSearch = !searchQuery || 
          app.name.toLowerCase().includes(searchQuery) ||
          (app.description && app.description.toLowerCase().includes(searchQuery)) ||
          (app.category && app.category.toLowerCase().includes(searchQuery));
        return matchesCategory && matchesSearch;
      }});

      if (filtered.length === 0) {{
        appsGrid.innerHTML = `
          <div class="empty-state">
            <h3>No se encontraron aplicaciones</h3>
            <p>No tienes aplicaciones asignadas en esta categoría o no coinciden con la búsqueda.</p>
          </div>`;
        return;
      }}

      appsGrid.innerHTML = filtered.map(app => {{
        const iconSvg = ICONS[app.icon] || ICONS["globe"];
        const bgGradient = app.bg_gradient || "linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)";
        const roleClass = app.user_role === "Admin" ? "admin" : "usuario";
        
        // Determinar URL de lanzamiento
        const baseTarget = app.cloud_url || app.url || `http://localhost:${{app.port}}`;
        const sep = baseTarget.includes("?") ? "&" : "?";
        const finalUrl = `${{baseTarget}}${{sep}}sso_user=${{encodeURIComponent(currentUser.name)}}&sso_role=${{encodeURIComponent(app.user_role)}}&sso_token=SIGRAMA_AUTH_TOKEN`;
        app.target_url = finalUrl;

        return `
          <div class="app-card" onclick="openApp('${{app.id}}')">
            <div class="app-card-top">
              <div class="app-icon-squircle" style="background: ${{bgGradient}};">
                ${{iconSvg}}
              </div>
              <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 4px;">
                <div class="app-status-badge online">
                  <span class="status-indicator-dot"></span>
                  <span>En línea</span>
                </div>
                <span class="app-role-pill ${{roleClass}}">Rol: ${{app.user_role}}</span>
              </div>
            </div>
            <div class="app-card-body">
              <div class="app-category-label">${{app.category || 'General'}}</div>
              <div class="app-name">${{app.name}}</div>
              <div class="app-desc">${{app.description || ''}}</div>
            </div>
            <div class="app-card-footer" onclick="event.stopPropagation()">
              <span class="app-meta-port">${{app.cloud_url ? 'Nube / Cloud' : 'Puerto ' + app.port}}</span>
              <div class="app-actions">
                ${{app.cloud_url ? `
                  <button class="btn-icon-action" title="Abrir Streamlit Cloud" onclick="window.open('${{app.cloud_url}}', '_blank')">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>
                  </button>
                ` : ''}}
                <button class="btn-icon-action" title="Abrir en Nueva Pestaña" onclick="window.open('${{finalUrl}}', '_blank')">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>
                </button>
              </div>
            </div>
          </div>
        `;
      }}).join("");
    }}

    window.openApp = function(appId) {{
      const apps = getAuthorizedApps();
      const app = apps.find(a => a.id === appId);
      if (!app) return;

      currentOpenedApp = app;
      workspaceAppTitle.innerText = `${{app.name}} - Rol: ${{app.user_role}}`;

      if (app.cloud_url) {{
        const sep = app.cloud_url.includes("?") ? "&" : "?";
        const embedUrl = `${{app.cloud_url}}${{sep}}embed=true&sso_user=${{encodeURIComponent(currentUser.name)}}&sso_role=${{encodeURIComponent(app.user_role)}}&sso_token=SIGRAMA_AUTH_TOKEN`;
        workspaceIframe.src = embedUrl;
        workspaceNotice.style.display = "none";
        workspaceIframe.style.display = "block";
      }} else {{
        const localUrl = `http://localhost:${{app.port}}?sso_user=${{encodeURIComponent(currentUser.name)}}&sso_role=${{encodeURIComponent(app.user_role)}}&sso_token=SIGRAMA_AUTH_TOKEN`;
        workspaceIframe.style.display = "none";
        workspaceNotice.style.display = "flex";
        workspaceNoticeText.innerHTML = `
          <div style="text-align: center; max-width: 520px; padding: 40px 30px; background: white; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; margin: 40px auto;">
            <div style="font-size: 48px; margin-bottom: 12px;">💻</div>
            <h3 style="margin-bottom: 8px; color: #002B49; font-size: 1.25rem;">${{app.name}}</h3>
            <p style="color: #64748b; font-size: 0.95rem; line-height: 1.5; margin-bottom: 24px;">
              Esta aplicación está alojada en tu entorno local (<b>Puerto ${{app.port}}</b>) y aún no ha sido desplegada en Streamlit Cloud.<br><br>
              Por seguridad, Google Chrome bloquea incrustar puertos locales <code>http://localhost</code> dentro de sitios web en la nube <code>https://</code>.
            </p>
            <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
              <button onclick="window.open('${{localUrl}}', '_blank')" style="padding: 10px 20px; font-size: 0.9rem; font-weight: 600; background: #002B49; color: white; border: none; border-radius: 8px; cursor: pointer; display: flex; align-items: center; gap: 8px;">
                <span>Abrir enlace local en tu PC</span>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>
              </button>
              <button onclick="closeWorkspace()" style="padding: 10px 20px; font-size: 0.9rem; font-weight: 600; background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; border-radius: 8px; cursor: pointer;">
                Volver al Menú
              </button>
            </div>
          </div>
        `;
      }}

      hubContainer.style.display = "none";
      categoriesNav.style.display = "none";
      workspaceContainer.classList.add("active");
      window.scrollTo(0, 0);
    }};

    window.closeWorkspace = function() {{
      if (workspaceIframe) workspaceIframe.src = "about:blank";
      if (workspaceContainer) workspaceContainer.classList.remove("active");
      if (categoriesNav) categoriesNav.style.display = "flex";
      if (hubContainer) hubContainer.style.display = "block";
      currentOpenedApp = null;
      window.scrollTo(0, 0);
    }};

    function showToast(msg, type = "info") {{
      const t = document.createElement("div");
      t.className = `toast ${{type}}`;
      t.innerText = msg;
      toastContainer.appendChild(t);
      setTimeout(() => {{
        t.style.opacity = "0";
        setTimeout(() => t.remove(), 300);
      }}, 3500);
    }}
  </script>
</body>
</html>
"""

components.html(standalone_html, height=1000, scrolling=True)
