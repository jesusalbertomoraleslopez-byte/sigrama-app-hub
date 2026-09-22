"""
SIGRAMA App Hub - Streamlit Cloud Wrapper v2.7.0
Renders the 100% exact Odoo-Style Enterprise UI inside Streamlit Cloud.
Integración con Requisiciones de Compra (sigrama-requisiciones-app)
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
    #MainMenu, header, footer, [data-testid="stHeader"], [data-testid="stFooter"], [data-testid="stDecoration"], [data-testid="stViewerBadge"], div[class*="viewerBadge"], div[class*="ProfileButton"], a[href*="streamlit.io"], div[class*="manageApp"], div[class*="ManageApp"], button[title*="Manage app"], [data-testid="stStatusWidget"] { display: none !important; }
    html, body, [data-testid="stAppViewContainer"], .main, .block-container {
        height: 100vh !important;
        max-height: 100vh !important;
        overflow: hidden !important;
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    [data-testid="stCustomComponentV1"], iframe {
        border: none !important;
        width: 100% !important;
        height: 100vh !important;
        min-height: 100vh !important;
    }
</style>
""", unsafe_allow_html=True)

components.html("""
<script>
(function() {
  function hideFooter() {
    document.querySelectorAll('footer').forEach(function(el) { el.style.display='none'; });
    ['stFooter','stDecoration','stViewerBadge'].forEach(function(id) {
      document.querySelectorAll('[data-testid="'+id+'"]').forEach(function(el) { el.style.display='none'; });
    });
    document.querySelectorAll('div[class*="viewerBadge"],div[class*="ProfileButton"],a[href*="streamlit.io"]').forEach(function(el) { el.style.display='none'; });
  }
  var observer = new MutationObserver(hideFooter);
  observer.observe(document.documentElement, {childList:true, subtree:true});
  hideFooter();
})();
</script>
""", height=0)

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

        <div style="display: flex; justify-content: flex-end; margin-top: -6px; margin-bottom: 14px;">
          <button type="button" id="btnOpenChangePassLogin" style="background: none; border: none; color: #0284c7; font-size: 0.8rem; font-weight: 600; cursor: pointer; text-decoration: underline; padding: 2px 0;">
            🔑 ¿Deseas cambiar tu contraseña?
          </button>
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
      <div class="user-profile-widget" id="userProfileWidget" title="Clic para administrar tu perfil y contraseña" style="display: none;">
        <div class="user-avatar-circle" id="userAvatarCircle">JM</div>
        <div class="user-info-text">
          <span class="user-full-name" id="userFullName">Usuario</span>
          <span class="user-role-badge" id="userRoleBadge">Rol</span>
        </div>
        <button class="btn-profile-manage" id="btnOpenUserProfileHeader" title="Administrar Perfil y Datos">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
        </button>
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
          <button class="btn-icon-action" id="btnWorkspaceFullscreen" title="Maximizar / Pantalla Completa" style="color: #cbd5e1;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" id="iconFullscreen">
              <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path>
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
      <div class="workspace-iframe-wrapper">
        <iframe id="workspaceIframe" class="workspace-iframe-frame" src="about:blank" allow="clipboard-read; clipboard-write"></iframe>
      </div>
    </div>
  </main>

  <!-- MODAL ADMINISTRACIÓN PERFIL DE USUARIO -->
  <div class="modal-backdrop" id="userProfileModal">
    <div class="modal-card" style="max-width: 640px; max-height: 92vh; display: flex; flex-direction: column;">
      <div class="modal-header">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="width: 36px; height: 36px; border-radius: 8px; background: #e0f2fe; color: #0284c7; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </div>
          <div>
            <h3 style="margin: 0; font-size: 1.1rem; font-weight: 700; color: #0f172a;">Administración de Perfil</h3>
            <span style="font-size: 0.75rem; color: #64748b;">Configura tus datos, contraseña y consulta accesos autorizados</span>
          </div>
        </div>
        <button class="modal-close-btn" id="btnCloseUserProfileModal" title="Cerrar">&times;</button>
      </div>

      <!-- TABS NAVEGACIÓN -->
      <div class="profile-nav-tabs">
        <button type="button" class="profile-nav-tab active" id="tabBtnPersonal" data-tab="tabProfilePersonal">
          <span>👤 Mis Datos</span>
        </button>
        <button type="button" class="profile-nav-tab" id="tabBtnSecurity" data-tab="tabProfileSecurity">
          <span>🔐 Contraseña & Seguridad</span>
        </button>
        <button type="button" class="profile-nav-tab" id="tabBtnAdminUsers" data-tab="tabProfileAdminUsers" style="display: none;">
          <span>👥 Gestión de Usuarios (Admin)</span>
        </button>
      </div>

      <div class="modal-body" style="padding: 18px 20px; overflow-y: auto; flex: 1;">
        <!-- TAB 1: MIS DATOS -->
        <div class="profile-tab-pane active" id="tabProfilePersonal">
          <div class="profile-avatar-banner">
            <div class="profile-avatar-banner-circle" id="profBannerAvatarCircle">JM</div>
            <div class="profile-avatar-meta">
              <div class="profile-avatar-title" id="profBannerName">Jesús Alberto Morales López</div>
              <div class="profile-avatar-subtitle">
                <span id="profBannerRole" style="font-weight: 700; color: #0284c7;">Administrador General</span>
                <span>&bull;</span>
                <span id="profBannerId" style="color: #64748b;">ID: jmorales</span>
              </div>
            </div>
          </div>

          <form id="formProfilePersonal" style="margin: 0;">
            <div class="form-group">
              <label for="profEditName">Nombre Completo del Colaborador</label>
              <input type="text" id="profEditName" class="form-input" placeholder="Nombre completo" required>
            </div>

            <div class="form-grid-2">
              <div class="form-group">
                <label for="profEditUsername">Nombre de Usuario (Login)</label>
                <input type="text" id="profEditUsername" class="form-input" placeholder="usuario" required>
              </div>
              <div class="form-group">
                <label for="profEditCode">Código de Empleado / Clave</label>
                <input type="text" id="profEditCode" class="form-input" placeholder="Ej. SIG-ADM-01" required>
              </div>
            </div>

            <div class="form-grid-2">
              <div class="form-group">
                <label for="profEditEmail">Correo Electrónico Corporativo</label>
                <input type="email" id="profEditEmail" class="form-input" placeholder="correo@sigrama.com.mx">
              </div>
              <div class="form-group">
                <label for="profEditDepartment">Departamento / Área</label>
                <input type="text" id="profEditDepartment" class="form-input" placeholder="Ej. Dirección General, Almacén, Corte y Doblez">
              </div>
            </div>

            <div style="display: flex; justify-content: flex-end; margin-top: 14px;">
              <button type="submit" class="btn-primary" style="background: #002B49; color: white; padding: 9px 20px; border-radius: 8px; font-weight: 600; border: none; cursor: pointer; display: flex; align-items: center; gap: 8px;">
                <span>💾 Guardar Datos del Perfil</span>
              </button>
            </div>
          </form>
        </div>

        <!-- TAB 2: CONTRASEÑA & SEGURIDAD -->
        <div class="profile-tab-pane" id="tabProfileSecurity">
          <div class="profile-info-callout">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink: 0; margin-top: 2px;">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            <div>
              <strong>Seguridad de la Cuenta:</strong> Para actualizar tu contraseña, es obligatorio ingresar tu contraseña anterior para autorizar la actualización.
            </div>
          </div>

          <form id="formProfileSecurity" style="margin: 0;">
            <div class="form-group">
              <label for="profSecOldPassword">Contraseña Anterior (Actual)</label>
              <input type="password" id="profSecOldPassword" class="form-input" placeholder="Ingresa tu contraseña actual" required autocomplete="current-password">
            </div>

            <div class="form-grid-2">
              <div class="form-group">
                <label for="profSecNewPassword">Nueva Contraseña</label>
                <input type="password" id="profSecNewPassword" class="form-input" placeholder="Mínimo 4 caracteres" required autocomplete="new-password">
              </div>
              <div class="form-group">
                <label for="profSecConfirmPassword">Confirmar Nueva Contraseña</label>
                <input type="password" id="profSecConfirmPassword" class="form-input" placeholder="Repite la nueva contraseña" required autocomplete="new-password">
              </div>
            </div>

            <div style="display: flex; justify-content: flex-end; margin-top: 14px;">
              <button type="submit" class="btn-primary" style="background: #002B49; color: white; padding: 9px 20px; border-radius: 8px; font-weight: 600; border: none; cursor: pointer; display: flex; align-items: center; gap: 8px;">
                <span>🔒 Actualizar mi Contraseña</span>
              </button>
            </div>
          </form>
        </div>

        <!-- TAB 3: GESTIÓN DE USUARIOS (ADMIN) -->
        <div class="profile-tab-pane" id="tabProfileAdminUsers">
          <div class="profile-info-callout warning">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink: 0; margin-top: 2px;">
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            <div>
              <strong>Panel de Administrador General:</strong> Puedes seleccionar a cualquier colaborador para modificar sus datos, restablecer su contraseña directamente o definir sus permisos por aplicación.
            </div>
          </div>

          <div class="form-group" style="margin-bottom: 14px;">
            <label for="adminSelectUser" style="font-weight: 700; color: #002B49;">Seleccionar Colaborador / Usuario:</label>
            <select id="adminSelectUser" class="form-input" style="font-weight: 600; font-size: 0.9rem; background-color: #f8fafc; border-color: #0284c7;"></select>
          </div>

          <form id="formProfileAdminUser" style="margin: 0;">
            <div class="form-group">
              <label for="adminEditName">Nombre Completo</label>
              <input type="text" id="adminEditName" class="form-input" required>
            </div>

            <div class="form-grid-2">
              <div class="form-group">
                <label for="adminEditUsername">Usuario</label>
                <input type="text" id="adminEditUsername" class="form-input" required>
              </div>
              <div class="form-group">
                <label for="adminEditCode">Código de Empleado</label>
                <input type="text" id="adminEditCode" class="form-input" required>
              </div>
            </div>

            <div class="form-grid-2">
              <div class="form-group">
                <label for="adminEditEmail">Correo</label>
                <input type="email" id="adminEditEmail" class="form-input">
              </div>
              <div class="form-group">
                <label for="adminEditDepartment">Departamento</label>
                <input type="text" id="adminEditDepartment" class="form-input">
              </div>
            </div>

            <div class="form-group">
              <label for="adminEditNewPass" style="color: #b91c1c; font-weight: 700;">🔑 Asignar Nueva Contraseña (Reseteo sin requerir clave anterior)</label>
              <input type="text" id="adminEditNewPass" class="form-input" placeholder="Escribe para cambiar la clave de este usuario, o déjalo vacío para mantenerla">
            </div>

            <div class="form-group" style="margin-top: 10px;">
              <label style="display: flex; align-items: center; gap: 8px; font-weight: 600; cursor: pointer;">
                <input type="checkbox" id="adminEditIsAdmin" style="width: 16px; height: 16px;">
                <span>Otorgar privilegios de Administrador General (Acceso Total al sistema)</span>
              </label>
            </div>

            <div style="margin-top: 14px;">
              <label style="font-weight: 700; color: #0f172a; margin-bottom: 6px; display: block;">Permisos por Aplicación del Catálogo:</label>
              <div class="permissions-table-wrapper">
                <table class="permissions-table">
                  <thead>
                    <tr>
                      <th>Aplicación</th>
                      <th style="width: 150px;">Nivel de Permiso</th>
                    </tr>
                  </thead>
                  <tbody id="adminPermissionsTableBody"></tbody>
                </table>
              </div>
            </div>

            <div style="display: flex; justify-content: flex-end; margin-top: 16px;">
              <button type="submit" class="btn-primary" style="background: #002B49; color: white; padding: 9px 20px; border-radius: 8px; font-weight: 600; border: none; cursor: pointer; display: flex; align-items: center; gap: 8px;">
                <span>💾 Guardar Cambios de este Usuario</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- MODAL CAMBIAR CONTRASEÑA -->
  <div class="modal-backdrop" id="changePasswordModal">
    <div class="modal-card" style="max-width: 440px;">
      <div class="modal-header">
        <div style="display: flex; align-items: center; gap: 10px;">
          <div style="width: 34px; height: 34px; border-radius: 8px; background: #e0f2fe; color: #0284c7; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </div>
          <div>
            <h3 style="margin: 0; font-size: 1.05rem; font-weight: 700; color: #0f172a;">Cambiar Contraseña</h3>
            <span style="font-size: 0.75rem; color: #64748b;">Ingresa tu clave anterior para autorizar el cambio</span>
          </div>
        </div>
        <button class="modal-close-btn" id="btnCloseChangePassModal" title="Cerrar">&times;</button>
      </div>

      <form id="changePasswordForm" style="margin: 0;">
        <div class="modal-body" style="padding: 20px;">
          <div class="form-group">
            <label for="cpUsernameInput">Usuario o Código Corporativo</label>
            <input type="text" id="cpUsernameInput" class="form-input" placeholder="Ej. bflores o SIG-COR-03" required autocomplete="username">
          </div>

          <div class="form-group">
            <label for="cpOldPasswordInput">Contraseña Anterior (Actual)</label>
            <input type="password" id="cpOldPasswordInput" class="form-input" placeholder="Ingresa tu contraseña actual" required autocomplete="current-password">
          </div>

          <div class="form-group">
            <label for="cpNewPasswordInput">Nueva Contraseña</label>
            <input type="password" id="cpNewPasswordInput" class="form-input" placeholder="Mínimo 4 caracteres" required autocomplete="new-password">
          </div>

          <div class="form-group" style="margin-bottom: 8px;">
            <label for="cpConfirmPasswordInput">Confirmar Nueva Contraseña</label>
            <input type="password" id="cpConfirmPasswordInput" class="form-input" placeholder="Repite la nueva contraseña" required autocomplete="new-password">
          </div>
        </div>

        <div class="modal-footer" style="padding: 14px 20px; background: #f8fafc; border-top: 1px solid #e2e8f0; display: flex; justify-content: flex-end; gap: 10px;">
          <button type="button" class="btn-secondary" id="btnCancelChangePass">Cancelar</button>
          <button type="submit" class="btn-primary" style="background: #002B49; color: white; padding: 8px 18px; border-radius: 8px; font-weight: 600; border: none; cursor: pointer; display: flex; align-items: center; gap: 6px;">
            <span>Actualizar Contraseña</span>
          </button>
        </div>
      </form>
    </div>
  </div>

  <div class="toast-container" id="toastContainer"></div>

  <!-- CLIENT SCRIPT -->
  <script>
    const CATALOG = {json.dumps(catalog_data)};
    const DEFAULT_USERS = {json.dumps(users_data)};

    function getStoredPasswords() {{
      try {{
        return JSON.parse(localStorage.getItem("sigrama_custom_passwords") || "{{}}");
      }} catch(e) {{
        return {{}};
      }}
    }}

    function saveStoredPassword(userId, newPassword) {{
      const stored = getStoredPasswords();
      stored[userId] = newPassword;
      localStorage.setItem("sigrama_custom_passwords", JSON.stringify(stored));
    }}

    function getStoredUsers() {{
      try {{
        return JSON.parse(localStorage.getItem("sigrama_custom_users") || "{{}}");
      }} catch(e) {{
        return {{}};
      }}
    }}

    function saveStoredUser(userObj) {{
      const stored = getStoredUsers();
      stored[userObj.id] = userObj;
      localStorage.setItem("sigrama_custom_users", JSON.stringify(stored));
    }}

    const USERS = DEFAULT_USERS.map(u => {{
      const customUsers = getStoredUsers();
      const customPass = getStoredPasswords()[u.id];
      let userCopy = Object.assign({{}}, u);
      if (customUsers[u.id]) {{
        userCopy = Object.assign(userCopy, customUsers[u.id]);
      }}
      if (customPass) {{
        userCopy.password = customPass;
      }}
      return userCopy;
    }});

    function handleUpdatePassword(userId, newPassword) {{
      saveStoredPassword(userId, newPassword);
      const inMemory = USERS.find(x => x.id === userId);
      if (inMemory) {{
        inMemory.password = newPassword;
      }}
      if (currentUser && currentUser.id === userId) {{
        currentUser.password = newPassword;
        localStorage.setItem("sigrama_hub_user", JSON.stringify(currentUser));
      }}
      try {{
        fetch("/api/auth/change-password", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{
            user_id: userId,
            username: inMemory ? inMemory.username : userId,
            new_password: newPassword
          }})
        }}).catch(() => {{}});
      }} catch(e) {{}}
    }}

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
      "globe": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>`,
      "file-text": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>`
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

      btnLogout.addEventListener("click", (e) => {{
        e.stopPropagation();
        localStorage.removeItem("sigrama_hub_user");
        showToast("Sesión cerrada", "info");
        showLogin();
      }});

      // ============================================
      // MODAL ADMINISTRACIÓN PERFIL DE USUARIO
      // ============================================
      const userProfileModal = document.getElementById("userProfileModal");
      const btnCloseUserProfileModal = document.getElementById("btnCloseUserProfileModal");
      const btnOpenUserProfileHeader = document.getElementById("btnOpenUserProfileHeader");
      const tabBtnPersonal = document.getElementById("tabBtnPersonal");
      const tabBtnSecurity = document.getElementById("tabBtnSecurity");
      const tabBtnAdminUsers = document.getElementById("tabBtnAdminUsers");
      const tabProfilePersonal = document.getElementById("tabProfilePersonal");
      const tabProfileSecurity = document.getElementById("tabProfileSecurity");
      const tabProfileAdminUsers = document.getElementById("tabProfileAdminUsers");

      function switchProfileTab(targetTabId) {{
        [tabBtnPersonal, tabBtnSecurity, tabBtnAdminUsers].forEach(btn => {{
          if (btn) {{
            if (btn.getAttribute("data-tab") === targetTabId) {{
              btn.classList.add("active");
            }} else {{
              btn.classList.remove("active");
            }}
          }}
        }});
        [tabProfilePersonal, tabProfileSecurity, tabProfileAdminUsers].forEach(pane => {{
          if (pane) {{
            if (pane.id === targetTabId) {{
              pane.classList.add("active");
            }} else {{
              pane.classList.remove("active");
            }}
          }}
        }});
      }}

      if (tabBtnPersonal) tabBtnPersonal.addEventListener("click", () => switchProfileTab("tabProfilePersonal"));
      if (tabBtnSecurity) tabBtnSecurity.addEventListener("click", () => switchProfileTab("tabProfileSecurity"));
      if (tabBtnAdminUsers) tabBtnAdminUsers.addEventListener("click", () => switchProfileTab("tabProfileAdminUsers"));

      function openUserProfileModal(initialTab = "tabProfilePersonal") {{
        if (!currentUser) return;

        // Actualizar banner
        const parts = (currentUser.name || "").split(" ");
        const initials = (parts.length > 1 ? (parts[0][0] + parts[1][0]) : (currentUser.name || "US").substring(0, 2)).toUpperCase();
        const bannerCircle = document.getElementById("profBannerAvatarCircle");
        const bannerName = document.getElementById("profBannerName");
        const bannerRole = document.getElementById("profBannerRole");
        const bannerId = document.getElementById("profBannerId");
        if (bannerCircle) bannerCircle.innerText = initials;
        if (bannerName) bannerName.innerText = currentUser.name || "Usuario";
        if (bannerRole) bannerRole.innerText = currentUser.is_global_admin ? "Administrador General" : "Usuario Autorizado";
        if (bannerId) bannerId.innerText = `Usuario: ${{currentUser.username || currentUser.id}} | Cód: ${{currentUser.user_code || 'S/C'}}`;

        // Tab 1: Mis Datos
        const editName = document.getElementById("profEditName");
        const editUsername = document.getElementById("profEditUsername");
        const editCode = document.getElementById("profEditCode");
        const editEmail = document.getElementById("profEditEmail");
        const editDept = document.getElementById("profEditDepartment");
        if (editName) editName.value = currentUser.name || "";
        if (editUsername) editUsername.value = currentUser.username || currentUser.id || "";
        if (editCode) editCode.value = currentUser.user_code || "";
        if (editEmail) editEmail.value = currentUser.email || "";
        if (editDept) editDept.value = currentUser.department || "";

        // Tab 2: Seguridad
        const secOld = document.getElementById("profSecOldPassword");
        const secNew = document.getElementById("profSecNewPassword");
        const secConf = document.getElementById("profSecConfirmPassword");
        if (secOld) secOld.value = "";
        if (secNew) secNew.value = "";
        if (secConf) secConf.value = "";

        // Tab 3: Admin
        if (tabBtnAdminUsers) {{
          if (currentUser.is_global_admin) {{
            tabBtnAdminUsers.style.display = "flex";
            populateAdminUserSelector();
          }} else {{
            tabBtnAdminUsers.style.display = "none";
          }}
        }}

        switchProfileTab(initialTab);
        if (userProfileModal) userProfileModal.classList.add("active");
      }}

      function closeUserProfileModal() {{
        if (userProfileModal) userProfileModal.classList.remove("active");
      }}

      if (btnCloseUserProfileModal) {{
        btnCloseUserProfileModal.addEventListener("click", closeUserProfileModal);
      }}

      if (userProfileWidget) {{
        userProfileWidget.addEventListener("click", () => {{
          openUserProfileModal("tabProfilePersonal");
        }});
      }}

      if (btnOpenUserProfileHeader) {{
        btnOpenUserProfileHeader.addEventListener("click", (e) => {{
          e.stopPropagation();
          openUserProfileModal("tabProfilePersonal");
        }});
      }}

      // Tab 1: Guardar Mis Datos
      const formProfilePersonal = document.getElementById("formProfilePersonal");
      if (formProfilePersonal) {{
        formProfilePersonal.addEventListener("submit", (e) => {{
          e.preventDefault();
          if (!currentUser) return;

          const nName = (document.getElementById("profEditName").value || "").trim();
          const nUser = (document.getElementById("profEditUsername").value || "").trim();
          const nCode = (document.getElementById("profEditCode").value || "").trim();
          const nEmail = (document.getElementById("profEditEmail").value || "").trim();
          const nDept = (document.getElementById("profEditDepartment").value || "").trim();

          if (!nName) {{
            showToast("El nombre completo es obligatorio", "error");
            return;
          }}

          currentUser.name = nName;
          currentUser.username = nUser;
          currentUser.user_code = nCode;
          currentUser.email = nEmail;
          currentUser.department = nDept;

          const inMemory = USERS.find(x => x.id === currentUser.id);
          if (inMemory) {{
            inMemory.name = nName;
            inMemory.username = nUser;
            inMemory.user_code = nCode;
            inMemory.email = nEmail;
            inMemory.department = nDept;
          }}

          saveStoredUser(currentUser);
          localStorage.setItem("sigrama_hub_user", JSON.stringify(currentUser));

          const parts = currentUser.name.split(" ");
          userAvatarCircle.innerText = (parts.length > 1 ? (parts[0][0] + parts[1][0]) : currentUser.name.substring(0, 2)).toUpperCase();
          userFullName.innerText = currentUser.name;
          hubWelcomeText.innerText = `Sesión activa: ${{currentUser.name}} | Aplicaciones autorizadas según tu perfil`;

          try {{
            fetch("/api/users/update", {{
              method: "POST",
              headers: {{ "Content-Type": "application/json" }},
              body: JSON.stringify(currentUser)
            }}).catch(() => {{}});
          }} catch(err) {{}}

          closeUserProfileModal();
          showToast("¡Datos de perfil guardados correctamente!", "success");
        }});
      }}

      // Tab 2: Guardar Mi Contraseña
      const formProfileSecurity = document.getElementById("formProfileSecurity");
      if (formProfileSecurity) {{
        formProfileSecurity.addEventListener("submit", (e) => {{
          e.preventDefault();
          if (!currentUser) return;

          const oldPass = (document.getElementById("profSecOldPassword").value || "").trim();
          const newPass = (document.getElementById("profSecNewPassword").value || "").trim();
          const confPass = (document.getElementById("profSecConfirmPassword").value || "").trim();

          if (!oldPass) {{
            showToast("Ingresa tu contraseña actual", "error");
            return;
          }}
          if (oldPass !== currentUser.password) {{
            showToast("La contraseña anterior no coincide con la registrada", "error");
            return;
          }}
          if (newPass.length < 4) {{
            showToast("La nueva contraseña debe tener al menos 4 caracteres", "error");
            return;
          }}
          if (newPass !== confPass) {{
            showToast("La confirmación no coincide con la nueva contraseña", "error");
            return;
          }}
          if (newPass === oldPass) {{
            showToast("La nueva contraseña debe ser diferente a la actual", "error");
            return;
          }}

          handleUpdatePassword(currentUser.id, newPass);
          closeUserProfileModal();
          showToast("¡Tu contraseña ha sido actualizada con éxito!", "success");
        }});
      }}

      // Tab 3: Panel Admin de Usuarios
      const adminSelectUser = document.getElementById("adminSelectUser");
      const formProfileAdminUser = document.getElementById("formProfileAdminUser");

      function populateAdminUserSelector() {{
        if (!adminSelectUser) return;
        const currentSel = adminSelectUser.value || (currentUser ? currentUser.id : USERS[0].id);
        adminSelectUser.innerHTML = "";
        USERS.forEach(u => {{
          const opt = document.createElement("option");
          opt.value = u.id;
          opt.textContent = `${{u.name}} (@${{u.username || u.id}} - ${{u.user_code || 'S/C'}})`;
          adminSelectUser.appendChild(opt);
        }});
        adminSelectUser.value = currentSel;
        loadAdminSelectedUser(adminSelectUser.value);
      }}

      function loadAdminSelectedUser(userId) {{
        const u = USERS.find(x => x.id === userId);
        if (!u) return;

        const aName = document.getElementById("adminEditName");
        const aUser = document.getElementById("adminEditUsername");
        const aCode = document.getElementById("adminEditCode");
        const aEmail = document.getElementById("adminEditEmail");
        const aDept = document.getElementById("adminEditDepartment");
        const aPass = document.getElementById("adminEditNewPass");
        const aIsAdmin = document.getElementById("adminEditIsAdmin");

        if (aName) aName.value = u.name || "";
        if (aUser) aUser.value = u.username || u.id || "";
        if (aCode) aCode.value = u.user_code || "";
        if (aEmail) aEmail.value = u.email || "";
        if (aDept) aDept.value = u.department || "";
        if (aPass) aPass.value = "";
        if (aIsAdmin) aIsAdmin.checked = !!u.is_global_admin;

        const tbody = document.getElementById("adminPermissionsTableBody");
        if (tbody) {{
          tbody.innerHTML = "";
          CATALOG.forEach(app => {{
            const currentPerm = (u.permissions && u.permissions[app.id]) || (u.is_global_admin ? "Admin" : "N/A");
            const tr = document.createElement("tr");
            tr.innerHTML = `
              <td>
                <strong style="color: #0f172a;">${{app.title}}</strong>
                <div style="font-size: 0.72rem; color: #64748b;">${{app.category}}</div>
              </td>
              <td>
                <select class="perm-select" data-app="${{app.id}}">
                  <option value="Admin" ${{currentPerm === 'Admin' ? 'selected' : ''}}>Admin</option>
                  <option value="Usuario" ${{currentPerm === 'Usuario' ? 'selected' : ''}}>Usuario</option>
                  <option value="N/A" ${{currentPerm === 'N/A' ? 'selected' : ''}}>Sin Acceso (N/A)</option>
                </select>
              </td>
            `;
            tbody.appendChild(tr);
          }});
        }}
      }}

      if (adminSelectUser) {{
        adminSelectUser.addEventListener("change", (e) => {{
          loadAdminSelectedUser(e.target.value);
        }});
      }}

      if (formProfileAdminUser) {{
        formProfileAdminUser.addEventListener("submit", (e) => {{
          e.preventDefault();
          const targetId = adminSelectUser ? adminSelectUser.value : "";
          const targetUser = USERS.find(x => x.id === targetId);
          if (!targetUser) return;

          const nName = (document.getElementById("adminEditName").value || "").trim();
          const nUser = (document.getElementById("adminEditUsername").value || "").trim();
          const nCode = (document.getElementById("adminEditCode").value || "").trim();
          const nEmail = (document.getElementById("adminEditEmail").value || "").trim();
          const nDept = (document.getElementById("adminEditDepartment").value || "").trim();
          const nPass = (document.getElementById("adminEditNewPass").value || "").trim();
          const nIsAdmin = document.getElementById("adminEditIsAdmin").checked;

          if (!nName) {{
            showToast("El nombre del colaborador no puede estar vacío", "error");
            return;
          }}

          const newPerms = Object.assign({{}}, targetUser.permissions || {{}});
          document.querySelectorAll("#adminPermissionsTableBody .perm-select").forEach(sel => {{
            const appId = sel.getAttribute("data-app");
            newPerms[appId] = sel.value;
          }});

          targetUser.name = nName;
          targetUser.username = nUser;
          targetUser.user_code = nCode;
          targetUser.email = nEmail;
          targetUser.department = nDept;
          targetUser.is_global_admin = nIsAdmin;
          targetUser.permissions = newPerms;

          if (nPass) {{
            if (nPass.length < 4) {{
              showToast("La nueva contraseña debe tener al menos 4 caracteres", "error");
              return;
            }}
            targetUser.password = nPass;
            saveStoredPassword(targetUser.id, nPass);
          }}

          saveStoredUser(targetUser);

          if (currentUser && currentUser.id === targetUser.id) {{
            currentUser = Object.assign({{}}, targetUser);
            localStorage.setItem("sigrama_hub_user", JSON.stringify(currentUser));
            const parts = currentUser.name.split(" ");
            userAvatarCircle.innerText = (parts.length > 1 ? (parts[0][0] + parts[1][0]) : currentUser.name.substring(0, 2)).toUpperCase();
            userFullName.innerText = currentUser.name;
            userRoleBadge.innerText = currentUser.is_global_admin ? "Administrador General" : "Usuario Autorizado";
            renderCategories();
            renderApps();
          }}

          try {{
            fetch("/api/users/update", {{
              method: "POST",
              headers: {{ "Content-Type": "application/json" }},
              body: JSON.stringify(Object.assign({{}}, targetUser, {{ new_password: nPass || undefined }}))
            }}).catch(() => {{}});
          }} catch(err) {{}}

          closeUserProfileModal();
          showToast(`¡Usuario ${{targetUser.name}} actualizado correctamente!`, "success");
        }});
      }}

      // ============================================
      // MODAL CAMBIAR CONTRASEÑA (PANTALLA DE LOGIN)
      // ============================================

      // Modal Cambiar Contraseña
      const changePasswordModal = document.getElementById("changePasswordModal");
      const btnOpenChangePassLogin = document.getElementById("btnOpenChangePassLogin");
      const btnOpenChangePassHeader = document.getElementById("btnOpenChangePassHeader");
      const btnCloseChangePassModal = document.getElementById("btnCloseChangePassModal");
      const btnCancelChangePass = document.getElementById("btnCancelChangePass");
      const changePasswordForm = document.getElementById("changePasswordForm");
      const cpUsernameInput = document.getElementById("cpUsernameInput");
      const cpOldPasswordInput = document.getElementById("cpOldPasswordInput");
      const cpNewPasswordInput = document.getElementById("cpNewPasswordInput");
      const cpConfirmPasswordInput = document.getElementById("cpConfirmPasswordInput");

      function openChangePassModal(prefillUser = "") {{
        if (cpUsernameInput) {{
          cpUsernameInput.value = prefillUser;
          cpUsernameInput.readOnly = !!prefillUser;
        }}
        if (cpOldPasswordInput) cpOldPasswordInput.value = "";
        if (cpNewPasswordInput) cpNewPasswordInput.value = "";
        if (cpConfirmPasswordInput) cpConfirmPasswordInput.value = "";
        if (changePasswordModal) {{
          changePasswordModal.classList.add("active");
          setTimeout(() => {{
            if (prefillUser && cpOldPasswordInput) {{
              cpOldPasswordInput.focus();
            }} else if (cpUsernameInput) {{
              cpUsernameInput.focus();
            }}
          }}, 100);
        }}
      }}

      function closeChangePassModal() {{
        if (changePasswordModal) changePasswordModal.classList.remove("active");
      }}

      if (btnOpenChangePassLogin) {{
        btnOpenChangePassLogin.addEventListener("click", () => {{
          const currLoginVal = (loginUserInput ? loginUserInput.value : "").trim();
          openChangePassModal(currLoginVal);
        }});
      }}

      if (btnOpenChangePassHeader) {{
        btnOpenChangePassHeader.addEventListener("click", () => {{
          const currUserVal = currentUser ? (currentUser.username || currentUser.id) : "";
          openChangePassModal(currUserVal);
        }});
      }}

      if (btnCloseChangePassModal) btnCloseChangePassModal.addEventListener("click", closeChangePassModal);
      if (btnCancelChangePass) btnCancelChangePass.addEventListener("click", closeChangePassModal);

      if (changePasswordForm) {{
        changePasswordForm.addEventListener("submit", (e) => {{
          e.preventDefault();
          const uInput = (cpUsernameInput ? cpUsernameInput.value : "").trim().toLowerCase();
          const oldPass = (cpOldPasswordInput ? cpOldPasswordInput.value : "").trim();
          const newPass = (cpNewPasswordInput ? cpNewPasswordInput.value : "").trim();
          const confPass = (cpConfirmPasswordInput ? cpConfirmPasswordInput.value : "").trim();

          if (!uInput) {{
            showToast("Por favor ingresa tu usuario o código", "error");
            return;
          }}
          if (!oldPass) {{
            showToast("Ingresa tu contraseña actual", "error");
            return;
          }}
          if (!newPass) {{
            showToast("Ingresa la nueva contraseña", "error");
            return;
          }}

          const matched = USERS.find(u => 
            (u.username && u.username.toLowerCase() === uInput) ||
            (u.user_code && u.user_code.toLowerCase() === uInput) ||
            (u.id && u.id.toLowerCase() === uInput)
          );

          if (!matched) {{
            showToast("Usuario no encontrado en el sistema", "error");
            return;
          }}

          if (matched.password !== oldPass) {{
            showToast("La contraseña anterior no coincide con la registrada", "error");
            return;
          }}

          if (newPass.length < 4) {{
            showToast("La nueva contraseña debe tener al menos 4 caracteres", "error");
            return;
          }}

          if (newPass !== confPass) {{
            showToast("La confirmación no coincide con la nueva contraseña", "error");
            return;
          }}

          if (newPass === oldPass) {{
            showToast("La nueva contraseña debe ser diferente a la actual", "error");
            return;
          }}

          handleUpdatePassword(matched.id, newPass);
          closeChangePassModal();
          showToast(`¡Contraseña de ${{matched.name}} actualizada con éxito!`, "success");

          if (window.PasswordCredential && navigator.credentials) {{
            try {{
              const cred = new PasswordCredential({{
                id: matched.username || matched.id,
                password: newPass,
                name: matched.name
              }});
              navigator.credentials.store(cred);
            }} catch(err) {{}}
          }}
        }});
      }}

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
      const btnFs = document.getElementById("btnWorkspaceFullscreen");
      if (btnFs) {{
        btnFs.addEventListener("click", () => {{
          workspaceContainer.classList.toggle("fullscreen");
          const isFull = workspaceContainer.classList.contains("fullscreen");
          const icon = document.getElementById("iconFullscreen");
          if (icon) {{
            if (isFull) {{
              icon.innerHTML = `<path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"></path>`;
              btnFs.title = "Restaurar tamaño";
            }} else {{
              icon.innerHTML = `<path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path>`;
              btnFs.title = "Maximizar / Pantalla Completa";
            }}
          }}
        }});
      }}
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
      document.body.style.overflow = "hidden";
      window.scrollTo(0, 0);
    }};

    window.closeWorkspace = function() {{
      if (workspaceIframe) workspaceIframe.src = "about:blank";
      if (workspaceContainer) {{
        workspaceContainer.classList.remove("active");
        workspaceContainer.classList.remove("fullscreen");
      }}
      if (categoriesNav) categoriesNav.style.display = "flex";
      if (hubContainer) hubContainer.style.display = "block";
      document.body.style.overflow = "auto";
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
