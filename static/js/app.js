/**
 * SIGRAMA App Hub - Odoo-Style Client with SSO & RBAC
 */

// SVG Icons Registry
const ICONS = {
  "shopping-cart": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>`,
  "truck": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18.5" r="2.5"/><circle cx="7" cy="18.5" r="2.5"/></svg>`,
  "scissors": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><path d="M8.12 8.12 12 12"/><circle cx="6" cy="18" r="3"/><path d="M8.12 15.88 16 8l4 4-8 8"/></svg>`,
  "ruler": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 4.27-2-2a2 2 0 0 0-2.83 0l-14.14 14.14a2 2 0 0 0 0 2.83l2 2a2 2 0 0 0 2.83 0l14.14-14.14a2 2 0 0 0 0-2.83Z"/><path d="m14.5 5.5 3 3"/><path d="m11.5 8.5 2 2"/><path d="m8.5 11.5 3 3"/><path d="m5.5 14.5 2 2"/></svg>`,
  "shield-check": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>`,
  "calculator": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="20" x="4" y="2" rx="2"/><line x1="8" x2="16" y1="6" y2="6"/><line x1="16" x2="16" y1="14" y2="18"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/></svg>`,
  "layers": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 12.5-8.58 3.91a2 2 0 0 1-1.66 0L2.6 12.5"/><path d="m22 17.5-8.58 3.91a2 2 0 0 1-1.66 0L2.6 17.5"/></svg>`,
  "users": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
  "cpu": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>`,
  "lightbulb": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>`,
  "external-link": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>`,
  "globe": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>`,
  "file-text": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>`
};

// State
let currentUser = null;
let appsData = [];
let activeCategory = "all";
let searchQuery = "";
let currentOpenedApp = null;
let pollTimer = null;

// DOM Elements
const loginOverlay = document.getElementById("loginOverlay");
const loginForm = document.getElementById("loginForm");
const loginUserInput = document.getElementById("loginUserInput");
const loginPasswordInput = document.getElementById("loginPasswordInput");

const userProfileWidget = document.getElementById("userProfileWidget");
const userAvatarCircle = document.getElementById("userAvatarCircle");
const userFullName = document.getElementById("userFullName");
const userRoleBadge = document.getElementById("userRoleBadge");
const btnLogout = document.getElementById("btnLogout");
const btnOpenNewAppModal = document.getElementById("btnOpenNewAppModal");

const appsGrid = document.getElementById("appsGrid");
const categoriesNav = document.getElementById("categoriesNav");
const searchInput = document.getElementById("searchInput");
const clockEl = document.getElementById("clockDisplay");
const hubContainer = document.getElementById("hubContainer");
const workspaceContainer = document.getElementById("workspaceContainer");
const workspaceIframe = document.getElementById("workspaceIframe");
const workspaceAppTitle = document.getElementById("workspaceAppTitle");
const appModal = document.getElementById("appModal");
const appForm = document.getElementById("appForm");
const toastContainer = document.getElementById("toastContainer");
const sysStatsEl = document.getElementById("sysStatsDisplay");
const totalAppsBadge = document.getElementById("totalAppsBadge");
const hubWelcomeText = document.getElementById("hubWelcomeText");

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  initClock();
  setupEventListeners();
  checkAuthAndInitialize();

  pollTimer = setInterval(() => {
    if (currentUser) {
      loadApps(true);
      loadSystemStats();
    }
  }, 4000);
});

// Check Session on Start
async function checkAuthAndInitialize() {
  try {
    const res = await fetch("/api/auth/me");
    const data = await res.json();

    if (data.authenticated && data.user) {
      setAuthenticatedUser(data.user);
    } else {
      showLoginScreen();
    }
  } catch (err) {
    showLoginScreen();
  }
}

// Show Login Screen
function showLoginScreen() {
  currentUser = null;
  loginOverlay.style.display = "flex";
  userProfileWidget.style.display = "none";
  if (btnOpenNewAppModal) btnOpenNewAppModal.style.display = "none";
  appsGrid.innerHTML = "";
  if (loginUserInput) loginUserInput.value = "";
  if (loginPasswordInput) loginPasswordInput.value = "";
}

// Set Authenticated User UI
function setAuthenticatedUser(user) {
  currentUser = user;
  loginOverlay.style.display = "none";
  userProfileWidget.style.display = "flex";

  // Initials for avatar
  const names = user.name.split(" ");
  const initials = names.length > 1 ? (names[0][0] + names[1][0]).toUpperCase() : user.name.substring(0, 2).toUpperCase();
  userAvatarCircle.innerText = initials;
  userFullName.innerText = user.name;
  userRoleBadge.innerText = user.is_global_admin ? "Administrador General" : "Usuario Autorizado";

  if (hubWelcomeText) {
    hubWelcomeText.innerText = `Sesión activa: ${user.name} | Aplicaciones autorizadas según tu perfil`;
  }

  // Show "Nueva App" button only for Global Admin
  if (btnOpenNewAppModal) {
    btnOpenNewAppModal.style.display = user.is_global_admin ? "flex" : "none";
  }

  loadApps();
  loadSystemStats();
}

// Clock
function initClock() {
  const updateClock = () => {
    const now = new Date();
    clockEl.innerText = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };
  updateClock();
  setInterval(updateClock, 1000);
}

// Event Listeners
function setupEventListeners() {
  // Login Form
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = loginUserInput ? loginUserInput.value.trim() : "";
    const password = loginPasswordInput ? loginPasswordInput.value : "";

    if (!username) {
      showToast("Por favor ingresa tu usuario o código de acceso", "error");
      return;
    }

    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, password: password })
      });
      const data = await res.json();
      if (data.success) {
        showToast(data.message, "success");
        if (window.PasswordCredential && navigator.credentials) {
          try {
            const cred = new PasswordCredential({
              id: username,
              password: password,
              name: data.user.name
            });
            navigator.credentials.store(cred);
          } catch (err) {}
        }
        if (loginPasswordInput) loginPasswordInput.value = "";
        setAuthenticatedUser(data.user);
      } else {
        showToast(data.message || "Usuario o clave incorrectos", "error");
      }
    } catch (err) {
      showToast(`Error de conexión: ${err.message}`, "error");
    }
  });

  // Logout
  btnLogout.addEventListener("click", async () => {
    try {
      await fetch("/api/auth/logout", { method: "POST" });
      showToast("Sesión cerrada", "info");
      showLoginScreen();
    } catch (err) {
      showLoginScreen();
    }
  });

  // Search input
  searchInput.addEventListener("input", (e) => {
    searchQuery = e.target.value.toLowerCase().trim();
    renderApps();
  });

  // Global shortcut '/'
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && document.activeElement !== searchInput && !loginOverlay.offsetParent) {
      e.preventDefault();
      searchInput.focus();
    }
  });

  // Workspace controls
  document.getElementById("btnHomeLauncher").addEventListener("click", closeWorkspace);
  document.getElementById("btnBackToHub").addEventListener("click", closeWorkspace);

  document.getElementById("btnWorkspaceReload").addEventListener("click", () => {
    if (workspaceIframe.src) {
      workspaceIframe.src = workspaceIframe.src;
      showToast("Recargando aplicación...", "info");
    }
  });

  document.getElementById("btnWorkspaceNewTab").addEventListener("click", () => {
    if (currentOpenedApp && (currentOpenedApp.launch_url || currentOpenedApp.url)) {
      window.open(currentOpenedApp.launch_url || currentOpenedApp.url, "_blank");
    }
  });

  document.getElementById("btnWorkspaceFullscreen").addEventListener("click", () => {
    if (!document.fullscreenElement) {
      workspaceContainer.requestFullscreen().catch(err => {
        showToast(`Error al activar pantalla completa: ${err.message}`, "error");
      });
    } else {
      document.exitFullscreen();
    }
  });

  // App Modal
  if (btnOpenNewAppModal) {
    btnOpenNewAppModal.addEventListener("click", () => openAppModal());
  }
  document.getElementById("btnModalClose").addEventListener("click", closeAppModal);
  document.getElementById("btnModalCancel").addEventListener("click", closeAppModal);
  document.getElementById("btnDeleteApp").addEventListener("click", handleDeleteApp);
  appForm.addEventListener("submit", handleSaveApp);
}

// Fetch apps
async function loadApps(isPolling = false) {
  if (!currentUser) return;

  try {
    const res = await fetch("/api/apps");
    const data = await res.json();
    if (data.success) {
      appsData = data.apps;
      renderCategories();
      renderApps();
      if (totalAppsBadge) {
        totalAppsBadge.innerText = `${appsData.length} Apps Disponibles`;
      }
    }
  } catch (err) {
    if (!isPolling) console.error("Error al cargar aplicaciones:", err);
  }
}

// Fetch stats
async function loadSystemStats() {
  try {
    const res = await fetch("/api/system/stats");
    const data = await res.json();
    if (data.success && sysStatsEl) {
      sysStatsEl.innerHTML = `
        <span class="stat-dot-live"></span>
        <span><b>${data.active_apps}</b> en línea | CPU: <b>${data.cpu_percent}%</b> | RAM: <b>${data.ram_percent}%</b></span>
      `;
    }
  } catch (err) {}
}

// Render Categories
function renderCategories() {
  const categories = ["all"];
  appsData.forEach(a => {
    if (a.category && !categories.includes(a.category)) {
      categories.push(a.category);
    }
  });

  categoriesNav.innerHTML = categories.map(cat => {
    const label = cat === "all" ? "Todas las Apps" : cat;
    const isActive = activeCategory === cat ? "active" : "";
    return `<button class="category-pill ${isActive}" onclick="selectCategory('${cat}')">${label}</button>`;
  }).join("");
}

function selectCategory(cat) {
  activeCategory = cat;
  renderCategories();
  renderApps();
}

// Render Apps Grid
function renderApps() {
  const filtered = appsData.filter(app => {
    const matchesCategory = activeCategory === "all" || app.category === activeCategory;
    const matchesSearch = !searchQuery || 
      app.name.toLowerCase().includes(searchQuery) ||
      (app.description && app.description.toLowerCase().includes(searchQuery)) ||
      (app.category && app.category.toLowerCase().includes(searchQuery));
    return matchesCategory && matchesSearch;
  });

  if (filtered.length === 0) {
    appsGrid.innerHTML = `
      <div class="empty-state">
        <h3>No se encontraron aplicaciones</h3>
        <p>No tienes aplicaciones asignadas en esta categoría o no coinciden con la búsqueda.</p>
      </div>
    `;
    return;
  }

  appsGrid.innerHTML = filtered.map(app => {
    const isOnline = app.status ? app.status.online : false;
    const isStarting = app.status ? app.status.starting : false;
    const iconSvg = ICONS[app.icon] || ICONS["globe"];
    const statusClass = isOnline ? "online" : (isStarting ? "starting" : "");
    const statusText = app.status ? app.status.status_text : "Detenido";
    const bgGradient = app.bg_gradient || "linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)";
    const userRole = app.user_role || "Usuario";
    const roleClass = userRole === "Admin" ? "admin" : "usuario";

    return `
      <div class="app-card" onclick="handleAppPrimaryClick('${app.id}')">
        <div class="app-card-top">
          <div class="app-icon-squircle" style="background: ${bgGradient};">
            ${iconSvg}
          </div>
          <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 4px;">
            <div class="app-status-badge ${statusClass}">
              <span class="status-indicator-dot"></span>
              <span>${statusText}</span>
            </div>
            <span class="app-role-pill ${roleClass}">${userRole}</span>
          </div>
        </div>
        <div class="app-card-body">
          <div class="app-category-label">${app.category || 'General'}</div>
          <div class="app-name">${app.name}</div>
          <div class="app-desc">${app.description || ''}</div>
        </div>
        <div class="app-card-footer" onclick="event.stopPropagation()">
          <span class="app-meta-port">${app.port ? 'Puerto ' + app.port : 'Externo'}</span>
          <div class="app-actions">
            ${renderControlButtons(app, isOnline, isStarting)}
            ${currentUser && currentUser.is_global_admin ? `
              <button class="btn-icon-action" title="Editar Configuración" onclick="openAppModal('${app.id}')">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
              </button>
            ` : ''}
            ${app.cloud_url ? `
              <button class="btn-icon-action" title="Abrir en Streamlit Cloud" onclick="launchCloudApp('${app.id}')">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>
              </button>
            ` : ''}
            <button class="btn-icon-action" title="Abrir en Nueva Pestaña" onclick="launchInNewTab('${app.id}')">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>
            </button>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

function renderControlButtons(app, isOnline, isStarting) {
  if (app.type === "external_url") return "";

  if (isOnline) {
    return `
      <button class="btn-icon-action" style="color: #ef4444;" title="Detener Aplicación" onclick="stopApp('${app.id}')">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><rect width="18" height="18" x="3" y="3" rx="2"/></svg>
      </button>
    `;
  } else if (isStarting) {
    return `
      <span style="font-size: 0.72rem; color: #d97706; padding: 4px 6px;">Cargando...</span>
    `;
  } else {
    return `
      <button class="btn-icon-action" style="color: #059669;" title="Iniciar Proceso" onclick="startApp('${app.id}')">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg>
      </button>
    `;
  }
}

// Click on App Card -> Smart Launch
async function handleAppPrimaryClick(appId) {
  const app = appsData.find(a => a.id === appId);
  if (!app) return;

  if (app.type === "external_url") {
    window.open(app.url, "_blank");
    return;
  }

  const isOnline = app.status && app.status.online;

  if (!isOnline) {
    showToast(`Iniciando ${app.name}... espera unos segundos`, "info");
    await startApp(appId, false);
    await waitForPortAndOpen(app);
  } else {
    openInIntegratedWorkspace(app);
  }
}

async function waitForPortAndOpen(app) {
  let attempts = 0;
  const maxAttempts = 15;
  const checkInterval = setInterval(async () => {
    attempts++;
    const res = await fetch("/api/apps");
    const data = await res.json();
    if (data.success) {
      const updated = data.apps.find(a => a.id === app.id);
      if (updated && updated.status && updated.status.online) {
        clearInterval(checkInterval);
        showToast(`${app.name} está en línea 🟢`, "success");
        loadApps();
        openInIntegratedWorkspace(updated);
      }
    }
    if (attempts >= maxAttempts) {
      clearInterval(checkInterval);
      showToast(`Tiempo de espera agotado al iniciar ${app.name}.`, "error");
    }
  }, 1000);
}

// Start App Process
async function startApp(appId, notify = true) {
  try {
    const res = await fetch(`/api/apps/start/${appId}`, { method: "POST" });
    const data = await res.json();
    if (notify) {
      showToast(data.message, data.success ? "info" : "error");
    }
    loadApps();
  } catch (err) {
    showToast(`Error de conexión: ${err.message}`, "error");
  }
}

// Stop App Process
async function stopApp(appId) {
  try {
    const res = await fetch(`/api/apps/stop/${appId}`, { method: "POST" });
    const data = await res.json();
    showToast(data.message, data.success ? "success" : "error");
    loadApps();
  } catch (err) {
    showToast(`Error al detener: ${err.message}`, "error");
  }
}

// Launch in New Tab with SSO URL
async function launchInNewTab(appId) {
  const app = appsData.find(a => a.id === appId);
  if (!app) return;

  const targetUrl = app.launch_url || app.url || `http://localhost:${app.port}`;

  if (app.type === "external_url") {
    window.open(targetUrl, "_blank");
    return;
  }

  const isOnline = app.status && app.status.online;

  if (!isOnline) {
    showToast(`Iniciando servicio para ${app.name}...`, "info");
    await startApp(appId, false);
    setTimeout(() => {
      window.open(targetUrl, "_blank");
    }, 2500);
  } else {
    window.open(targetUrl, "_blank");
  }
}

// Launch in Streamlit Cloud with SSO Parameters
function launchCloudApp(appId) {
  const app = appsData.find(a => a.id === appId);
  if (!app || !app.cloud_url) return;

  const sep = app.cloud_url.includes("?") ? "&" : "?";
  const userName = currentUser ? currentUser.name : "Administrador General";
  const userRole = app.user_role || (currentUser && currentUser.is_global_admin ? "Admin" : "Usuario");
  const ssoUrl = `${app.cloud_url}${sep}sso_user=${encodeURIComponent(userName)}&sso_role=${encodeURIComponent(userRole)}&sso_token=SIGRAMA_AUTH_TOKEN`;
  window.open(ssoUrl, "_blank");
}

// Open In Integrated Workspace
function openInIntegratedWorkspace(app) {
  currentOpenedApp = app;
  const targetUrl = app.launch_url || app.url || `http://localhost:${app.port}`;

  workspaceAppTitle.innerText = `${app.name} (${app.port ? 'Puerto ' + app.port : 'Externo'}) - Rol: ${app.user_role || 'Usuario'}`;
  workspaceIframe.src = targetUrl;

  hubContainer.style.display = "none";
  workspaceContainer.classList.add("active");
  window.scrollTo(0, 0);
}

// Close Workspace
function closeWorkspace() {
  workspaceIframe.src = "about:blank";
  workspaceContainer.classList.remove("active");
  hubContainer.style.display = "block";
  currentOpenedApp = null;
  loadApps();
}

// Modal Form
function openAppModal(appId = null) {
  const deleteBtn = document.getElementById("btnDeleteApp");
  const modalTitle = document.getElementById("modalTitle");

  if (appId) {
    const app = appsData.find(a => a.id === appId);
    if (!app) return;
    modalTitle.innerText = "Editar Aplicación";
    document.getElementById("formAppId").value = app.id;
    document.getElementById("formAppId").readOnly = true;
    document.getElementById("formAppName").value = app.name || "";
    document.getElementById("formAppCategory").value = app.category || "";
    document.getElementById("formAppType").value = app.type || "streamlit";
    document.getElementById("formAppPath").value = app.path || "";
    document.getElementById("formAppEntry").value = app.entry_file || "app.py";
    document.getElementById("formAppPort").value = app.port || "";
    document.getElementById("formAppUrl").value = app.url || "";
    document.getElementById("formAppIcon").value = app.icon || "layers";
    document.getElementById("formAppDesc").value = app.description || "";
    deleteBtn.style.display = "block";
  } else {
    modalTitle.innerText = "Registrar Nueva Aplicación";
    appForm.reset();
    document.getElementById("formAppId").readOnly = false;
    document.getElementById("formAppType").value = "streamlit";
    document.getElementById("formAppEntry").value = "app.py";
    deleteBtn.style.display = "none";
  }

  appModal.classList.add("active");
}

function closeAppModal() {
  appModal.classList.remove("active");
  appForm.reset();
}

async function handleSaveApp(e) {
  e.preventDefault();
  const payload = {
    id: document.getElementById("formAppId").value.trim(),
    name: document.getElementById("formAppName").value.trim(),
    category: document.getElementById("formAppCategory").value.trim() || "General",
    type: document.getElementById("formAppType").value,
    path: document.getElementById("formAppPath").value.trim(),
    entry_file: document.getElementById("formAppEntry").value.trim() || "app.py",
    port: parseInt(document.getElementById("formAppPort").value) || 0,
    url: document.getElementById("formAppUrl").value.trim() || `http://localhost:${document.getElementById("formAppPort").value}`,
    icon: document.getElementById("formAppIcon").value || "layers",
    description: document.getElementById("formAppDesc").value.trim()
  };

  try {
    const res = await fetch("/api/apps/save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, "success");
      closeAppModal();
      loadApps();
    } else {
      showToast(data.message, "error");
    }
  } catch (err) {
    showToast(`Error al guardar: ${err.message}`, "error");
  }
}

async function handleDeleteApp() {
  const appId = document.getElementById("formAppId").value;
  if (!appId) return;

  if (!confirm(`¿Estás seguro de eliminar esta aplicación del catálogo?`)) return;

  try {
    const res = await fetch(`/api/apps/${appId}`, { method: "DELETE" });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, "success");
      closeAppModal();
      loadApps();
    } else {
      showToast(data.message, "error");
    }
  } catch (err) {
    showToast(`Error al eliminar: ${err.message}`, "error");
  }
}

// Toast
function showToast(message, type = "info") {
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerText = message;
  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(10px)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}
