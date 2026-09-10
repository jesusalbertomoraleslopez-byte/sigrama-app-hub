"""
Process Manager for SIGRAMA App Hub
Manages starting, stopping, and monitoring status of local applications.
"""
import os
import sys
import time
import socket
import subprocess
import threading
import psutil

class ProcessManager:
    def __init__(self, logs_dir="logs"):
        self.logs_dir = logs_dir
        os.makedirs(self.logs_dir, exist_ok=True)
        self.active_processes = {}  # app_id -> subprocess.Popen

    def is_port_in_use(self, port: int, host="127.0.0.1") -> bool:
        """Check if a TCP port is currently listening."""
        if not port or port <= 0:
            return False
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.4)
            return s.connect_ex((host, port)) == 0

    def find_pid_by_port(self, port: int):
        """Find the PID listening on a given port."""
        if not port or port <= 0:
            return None
        
        # Try psutil first
        try:
            for conn in psutil.net_connections(kind="inet"):
                if conn.laddr and conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                    return conn.pid
        except Exception:
            pass

        # Fallback to netstat on Windows
        try:
            cmd = f'netstat -ano -p tcp | findstr /R /C:":{port} .*LISTENING"'
            output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
            for line in output.strip().splitlines():
                parts = line.strip().split()
                if len(parts) >= 5 and parts[-1].isdigit():
                    return int(parts[-1])
        except Exception:
            pass

        return None

    def get_app_status(self, app: dict) -> dict:
        """Returns status info for a single application."""
        app_id = app.get("id")
        app_type = app.get("type", "streamlit")
        port = app.get("port", 0)

        if app_type == "external_url" or (app.get("url") and app.get("url").startswith("https://")):
            return {
                "id": app_id,
                "online": True,
                "pid": None,
                "status_text": "En Línea (Cloud)",
                "can_start": False,
                "can_stop": False,
                "port": 0,
                "url": app.get("url")
            }

        # Check if port is open
        port_open = self.is_port_in_use(port)
        pid = self.find_pid_by_port(port) if port_open else None

        # Check in active_processes if still alive
        if not port_open and app_id in self.active_processes:
            proc = self.active_processes[app_id]
            if proc.poll() is None:
                # Process launched but port not yet responding
                return {
                    "id": app_id,
                    "online": False,
                    "starting": True,
                    "pid": proc.pid,
                    "status_text": "Iniciando...",
                    "can_start": False,
                    "can_stop": True,
                    "port": port,
                    "url": app.get("url") or f"http://localhost:{port}"
                }
            else:
                # Process died
                del self.active_processes[app_id]

        return {
            "id": app_id,
            "online": port_open,
            "starting": False,
            "pid": pid,
            "status_text": "En línea" if port_open else "Detenido",
            "can_start": not port_open,
            "can_stop": port_open,
            "port": port,
            "url": app.get("url") or f"http://localhost:{port}"
        }

    def start_app(self, app: dict) -> tuple[bool, str]:
        """Start an application if it is not already running."""
        app_id = app.get("id")
        app_type = app.get("type", "streamlit")
        port = app.get("port", 0)
        app_path = app.get("path", "")
        entry_file = app.get("entry_file", "app.py")

        if app_type == "external_url":
            return True, "Aplicación externa (no requiere inicio local)."

        if self.is_port_in_use(port):
            return True, f"La aplicación ya se encuentra en línea en el puerto {port}."

        if not os.path.exists(app_path):
            return False, f"La ruta configurada no existe: {app_path}"

        full_entry = os.path.join(app_path, entry_file)
        if not os.path.exists(full_entry):
            return False, f"No se encontró el archivo principal: {full_entry}"

        log_file_path = os.path.join(self.logs_dir, f"{app_id}.log")
        log_out = open(log_file_path, "a", encoding="utf-8")

        # Construct command
        if app_type == "streamlit":
            cmd = [
                sys.executable,
                "-m", "streamlit", "run", entry_file,
                "--server.port", str(port),
                "--server.headless", "true",
                "--browser.gatherUsageStats", "false",
                "--server.enableCORS", "false",
                "--server.enableXsrfProtection", "false"
            ]
        else:
            cmd = [sys.executable, entry_file]

        try:
            # CREATE_NEW_PROCESS_GROUP on Windows
            creationflags = 0
            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

            proc = subprocess.Popen(
                cmd,
                cwd=app_path,
                stdout=log_out,
                stderr=log_out,
                creationflags=creationflags
            )
            self.active_processes[app_id] = proc
            return True, f"Iniciando {app.get('name')} en el puerto {port}..."
        except Exception as e:
            return False, f"Error al lanzar el proceso: {str(e)}"

    def stop_app(self, app: dict) -> tuple[bool, str]:
        """Stop an application process."""
        app_id = app.get("id")
        port = app.get("port", 0)

        pid = self.find_pid_by_port(port)
        killed = False

        if pid:
            try:
                p = psutil.Process(pid)
                # Terminate children first
                for child in p.children(recursive=True):
                    try:
                        child.kill()
                    except Exception:
                        pass
                p.kill()
                killed = True
            except Exception as e:
                return False, f"No se pudo detener el proceso PID {pid}: {str(e)}"

        if app_id in self.active_processes:
            try:
                proc = self.active_processes[app_id]
                proc.kill()
                del self.active_processes[app_id]
                killed = True
            except Exception:
                pass

        if killed or not self.is_port_in_use(port):
            return True, f"Aplicación {app.get('name')} detenida correctamente."
        else:
            return False, "No se encontró ningún proceso activo asociado."
