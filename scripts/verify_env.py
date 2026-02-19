import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

try:
    from app.core.config import settings
    print("✅ Configuration loaded successfully.")
    print(f"Env: {settings.APP_ENV}")
    print(f"Symbols: {settings.SYMBOLS}")
    print(f"Bar Frequency: {settings.BAR_FREQUENCY}")
except Exception as e:
    print(f"❌ Configuration loading failed: {e}")
    sys.exit(1)

try:
    from app.main import app
    print("✅ FastAPI app initialized successfully.")
except Exception as e:
    print(f"❌ App initialization failed: {e}")
    sys.exit(1)

print("🚀 Verification complete!")
