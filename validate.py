import sys
from pathlib import Path
import importlib

ROOT = Path(__file__).resolve().parent
REQUIRED_FILES = ["Dockerfile", "openenv.yaml", "inference.py"]


def fail(message):
    print(f"ERROR: {message}")
    sys.exit(1)


def check_files():
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail(f"Missing required root files: {', '.join(missing)}")
    print("✔ Required root files exist")


def parse_openenv_yaml():
    path = ROOT / "openenv.yaml"
    contents = path.read_text(encoding="utf-8")
    entrypoint = None
    for line in contents.splitlines():
        stripped = line.strip()
        if stripped.startswith("entrypoint:"):
            _, value = stripped.split(":", 1)
            entrypoint = value.strip()
            break
    if entrypoint != "app.main:app":
        fail("openenv.yaml entrypoint must be 'app.main:app'")
    print("✔ openenv.yaml entrypoint is correct")


def check_reset_routes():
    sys.path.insert(0, str(ROOT))
    try:
        module = importlib.import_module("app.main")
    except Exception as exc:
        fail(f"Failed to import app.main: {exc}")

    if not hasattr(module, "app"):
        fail("app.main does not expose FastAPI app object named 'app'")

    routes = module.app.routes
    has_get = any(
        route.path == "/reset" and "GET" in {method.upper() for method in (route.methods or set())}
        for route in routes
    )
    has_post = any(
        route.path == "/reset" and "POST" in {method.upper() for method in (route.methods or set())}
        for route in routes
    )

    if not has_post:
        fail("/reset route must accept POST requests")
    if not has_get:
        fail("/reset route must accept GET requests")

    print("✔ /reset route supports both GET and POST")


def main():
    print("Running validation checks...")
    check_files()
    parse_openenv_yaml()
    check_reset_routes()
    print("\nAll validation checks passed.")


if __name__ == "__main__":
    main()
