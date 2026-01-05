from pathlib import Path
import uvicorn
from src.app import app
from scripts import configToObject

settings = configToObject.settings

def main():
    socketPath: Path = Path("tmp/Moris/MALDC.sock")
    
    if socketPath.exists(): socketPath.rmdir() # We need a new socket
    
    if settings.api.use_uds:
        uvicorn.run("app:app", uds=settings.api.linux.socket)
    else:
        uvicorn.run("app:app", host=settings.api.windows.host, port=settings.api.windows.port)



if __name__ == "__main__":
    main()