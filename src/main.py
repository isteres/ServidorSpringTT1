import uvicorn
import os
import sys

# Añadimos el directorio src al path para que los imports funcionen
sys.path.append(os.path.join(os.path.dirname(__file__)))

if __name__ == "__main__":
    uvicorn.run("infrastructure.web.app:app", host="0.0.0.0", port=8000, reload=True)
