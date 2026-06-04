import traceback

from app import create_app


try:
    app = create_app()
    if app is None:
        raise RuntimeError("create_app() returned None. Check MONGODB_URI and backend environment variables.")
except Exception:
    print("[STARTUP ERROR] Banking API failed to start.")
    print("[STARTUP ERROR] Required Render env vars: MONGODB_URI, MONGODB_DB_NAME, ALLOWED_ORIGINS, FLASK_ENV.")
    print("[STARTUP ERROR] Do not paste secret values into logs; verify them in the Render dashboard.")
    traceback.print_exc()
    raise
