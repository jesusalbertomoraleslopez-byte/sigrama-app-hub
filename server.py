"""
SIGRAMA App Hub - Server Backend with SSO & RBAC
"""
import os
import json
import logging
import psutil
from urllib.parse import urlencode
from flask import Flask, render_template, jsonify, request, session
from process_manager import ProcessManager

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "sigrama_hub_super_secret_sso_key_2026"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "catalog.json")
USERS_FILE = os.path.join(BASE_DIR, "data", "users.json")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

process_manager = ProcessManager(logs_dir=LOGS_DIR)

def load_catalog():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        app.logger.error(f"Error loading catalog: {e}")
        return []

def save_catalog(catalog):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception as e:
        app.logger.error(f"Error loading users: {e}")
        return []

def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    users = load_users()
    return next((u for u in users if u["id"] == user_id), None)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/auth/login", methods=["POST"])
def auth_login():
    data = request.json or {}
    user_identifier = (data.get("username") or data.get("user_id", "")).strip().lower()
    password = data.get("password", "").strip()

    if not user_identifier or not password:
        return jsonify({"success": False, "message": "Ingrese usuario y contraseña"}), 400

    users = load_users()
    matched = None
    for u in users:
        u_id = u.get("id", "").lower()
        u_name = u.get("username", "").lower()
        u_code = u.get("user_code", "").lower()
        if user_identifier in [u_id, u_name, u_code]:
            matched = u
            break

    if not matched or matched["password"] != password:
        return jsonify({"success": False, "message": "Credenciales inválidas. Verifique su usuario y contraseña."}), 401

    session["user_id"] = matched["id"]
    return jsonify({
        "success": True,
        "message": f"Bienvenido, {matched['name']}",
        "user": {
            "id": matched["id"],
            "name": matched["name"],
            "username": matched.get("username", matched["id"]),
            "user_code": matched.get("user_code", ""),
            "is_global_admin": matched.get("is_global_admin", False),
            "permissions": matched.get("permissions", {})
        }
    })

@app.route("/api/auth/logout", methods=["POST"])
def auth_logout():
    session.pop("user_id", None)
    return jsonify({"success": True, "message": "Sesión cerrada correctamente"})

@app.route("/api/auth/me", methods=["GET"])
def auth_me():
    user = get_current_user()
    if not user:
        return jsonify({"success": True, "authenticated": False, "user": None})
    return jsonify({
        "success": True,
        "authenticated": True,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "is_global_admin": user.get("is_global_admin", False),
            "permissions": user.get("permissions", {})
        }
    })

@app.route("/api/apps", methods=["GET"])
def get_apps():
    user = get_current_user()
    catalog = load_catalog()
    results = []

    for item in catalog:
        app_id = item.get("id")
        user_role = "Usuario"

        if user:
            # Check permissions
            if user.get("is_global_admin"):
                user_role = "Admin"
            else:
                perms = user.get("permissions", {})
                perm = perms.get(app_id, "N/A")
                if perm == "N/A":
                    # User has no access to this app
                    continue
                user_role = perm
        else:
            # Unauthenticated: don't expose apps or mark them
            pass

        status = process_manager.get_app_status(item)
        combined = dict(item)

        # Inject SSO query parameters into URL
        base_url = item.get("url") or f"http://localhost:{item.get('port')}"
        if user and (item.get("type") in ["streamlit", "external_url"] or "streamlit.app" in base_url):
            params = {
                "sso_user": user["name"],
                "sso_role": user_role,
                "sso_token": "SIGRAMA_AUTH_TOKEN"
            }
            sep = "&" if "?" in base_url else "?"
            launch_url = f"{base_url}{sep}{urlencode(params)}"
        else:
            launch_url = base_url

        combined.update({
            "status": status,
            "user_role": user_role,
            "launch_url": launch_url
        })
        results.append(combined)

    return jsonify({
        "success": True,
        "authenticated": user is not None,
        "apps": results
    })

@app.route("/api/apps/start/<app_id>", methods=["POST"])
def start_app_endpoint(app_id):
    catalog = load_catalog()
    app_item = next((a for a in catalog if a.get("id") == app_id), None)
    if not app_item:
        return jsonify({"success": False, "message": "Aplicación no encontrada"}), 404

    success, message = process_manager.start_app(app_item)
    return jsonify({"success": success, "message": message})

@app.route("/api/apps/stop/<app_id>", methods=["POST"])
def stop_app_endpoint(app_id):
    catalog = load_catalog()
    app_item = next((a for a in catalog if a.get("id") == app_id), None)
    if not app_item:
        return jsonify({"success": False, "message": "Aplicación no encontrada"}), 404

    success, message = process_manager.stop_app(app_item)
    return jsonify({"success": success, "message": message})

@app.route("/api/apps/save", methods=["POST"])
def save_app_endpoint():
    user = get_current_user()
    if not user or not user.get("is_global_admin"):
        return jsonify({"success": False, "message": "Solo el Administrador General puede modificar el catálogo"}), 403

    data = request.json or {}
    app_id = data.get("id")
    if not app_id:
        return jsonify({"success": False, "message": "El ID de la aplicación es obligatorio"}), 400

    catalog = load_catalog()
    existing_idx = next((i for i, a in enumerate(catalog) if a.get("id") == app_id), None)

    if existing_idx is not None:
        catalog[existing_idx].update(data)
    else:
        catalog.append(data)

    save_catalog(catalog)
    return jsonify({"success": True, "message": "Aplicación guardada correctamente"})

@app.route("/api/apps/<app_id>", methods=["DELETE"])
def delete_app_endpoint(app_id):
    user = get_current_user()
    if not user or not user.get("is_global_admin"):
        return jsonify({"success": False, "message": "Solo el Administrador General puede eliminar aplicaciones"}), 403

    catalog = load_catalog()
    app_item = next((a for a in catalog if a.get("id") == app_id), None)
    if not app_item:
        return jsonify({"success": False, "message": "Aplicación no encontrada"}), 404

    process_manager.stop_app(app_item)
    catalog = [a for a in catalog if a.get("id") != app_id]
    save_catalog(catalog)
    return jsonify({"success": True, "message": "Aplicación eliminada"})

@app.route("/api/system/stats", methods=["GET"])
def system_stats():
    catalog = load_catalog()
    active_count = 0
    for a in catalog:
        if a.get("type") == "streamlit":
            if process_manager.is_port_in_use(a.get("port")):
                active_count += 1

    cpu_usage = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()

    return jsonify({
        "success": True,
        "active_apps": active_count,
        "total_apps": len(catalog),
        "cpu_percent": cpu_usage,
        "ram_percent": ram.percent,
        "ram_used_gb": round((ram.total - ram.available) / (1024 ** 3), 1),
        "ram_total_gb": round(ram.total / (1024 ** 3), 1)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"==================================================")
    print(f"      HUB DE APLICACIONES SIGRAMA (SSO & RBAC)    ")
    print(f"      Servidor iniciado en: http://localhost:{port} ")
    print(f"==================================================")
    app.run(host="0.0.0.0", port=port, debug=False)
