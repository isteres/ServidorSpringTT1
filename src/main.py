import uvicorn
from src.infrastructure.web.app import app

if __name__ == "__main__":
    # Run the application programmatically
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)