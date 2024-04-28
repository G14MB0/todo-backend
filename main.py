

import uvicorn
from app.main import app


### Parameters for uvicorn server
# HOST = "127.0.0.1"
HOST = "0.0.0.0"
PORT = 5174
WORKERS = 1

RELOAD = True # Reload the app after any save. to be FALSE in production
APPPATH = "app.main:app"



def serve(host: str, port: int, workers: int, reload: bool = False, appPath: str = ""):
    """This method start the FastAPI application using uvicorn

    Args:
        host (str): the app ip address
        port (int): the app port
        workers (int): if need multiprocess. 
        reload (bool, optional): is passed as the reload parameter of uvicorn. auto restart the app at any changes in the code.
        appPath (str, optional): if reload is True, the app argument must be passed as a string (like the one used directly in terminal)
    """    

    # Start the Uvicorn server
    if reload:
        if appPath == "":
            raise RuntimeError("The parameter appPath must be defined when reload is True! (something like app.main:app)")
        uvicorn.run(appPath, port=port, host=host, workers=workers, reload=reload)
    else:
        uvicorn.run(app, port=port, host=host, workers=workers, reload=reload)




if __name__ == "__main__":
    process = serve(HOST, PORT, WORKERS, reload=RELOAD, appPath=APPPATH)

    