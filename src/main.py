from pathlib import Path
import uvicorn
from src.app import app
from src.scripts.settings import load_settings, SettingsDep

settings = load_settings()

def main():

    if settings.api.use_uds:
        socketPath: Path = Path(settings.api.linux.socket)
        if socketPath.exists(): socketPath.rmdir() # We need a new socket
        
        uvicorn.run("app:app", uds=settings.api.linux.socket)
    
    else:
        uvicorn.run("app:app", host=settings.api.windows.host, port=settings.api.windows.port)



if __name__ == "__main__":
    main()