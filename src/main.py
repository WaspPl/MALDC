from pathlib import Path
import uvicorn
from app import app


def main():
    socketPath: Path = Path("tmp/Moris/MALDC.sock")
    
    if socketPath.exists(): socketPath.rmdir() # We need a new socket
    
    uvicorn.run("app:app", uds=socketPath)


if __name__ == "__main__":
    main()