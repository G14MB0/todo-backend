

'''
uvicorn app.main:app --reload #start the server without the main.py file
'''

from fastapi import FastAPI, staticfiles, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import todo, user, auth

from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app import models
from app.database import engine

from contextlib import asynccontextmanager



# This bind the database with the models (creating the tables if not present and all the stuff). no need for this if using Alembic (but can still be leaved for auto db creation)
models.Base.metadata.create_all(bind=engine) 


origins = [
    "http://localhost:5173", #dev mode
    "http://127.0.0.1:5173", #dev mode
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """this lifespan metohod, used with the @asynccontextmanager decorator
    is the new way to deal with event in fastapi since the classical app.on("event") is deprecated
    """    

    # Code here runs after the app startup
    print("---------------------------------------------------------------")
    print("--------------------- The app has started ---------------------")
    print("---------------------------------------------------------------")

    yield  # This yield separates startup from shutdown code

    # Code here runs after the app stops

   
    print("-------------------------------------------------------------")
    print("-------------------- The app has stopped --------------------")
    print("-------------------------------------------------------------")




app = FastAPI(
    title="todo-backend",
    version="0.1",
    root_path="",
    lifespan=lifespan,  # this handle the lifespan method define before
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],    # Restrict this based on needs to increase security
    allow_headers=["*"],    # Restrict this based on needs to increase security
)


app.include_router(user.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(todo.router, prefix="/api/v1")


# This will mount the docs as a static file. get them at "/mkdocs" endpoint
app.mount("/mkdocs", staticfiles.StaticFiles(directory="./site", html=True), name="mkdocs")

# This mount a static file that will be served at ./filename (so for example in order to open it, call .../index.html)
# Since I mounted a Vue-Vite app with base = ".", I MUST mount at "/" thus Vite app's relative import still works correctly
# Mounting at root path will also hide the index.html from the url path when called
app.mount("/", staticfiles.StaticFiles(directory="./dist", html=True), name="dist")


## Creat this custom midderlware class to handle 404 responses. I this case I force the app
# To redirect at root path (static website) at all the not found path. This is used specifically
# in this particula care and just as a demontration.
class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if response.status_code == 404:
            # Redirect to root if a 404 response is generated
            return RedirectResponse(url="/")
        return response

# Add custom middleware to the application
app.add_middleware(CustomMiddleware)



## Hide this since overwritten by the app.mount
# @app.get("/")
# def root():
#     return {"message": "This are the APIs. Go to ./docs to see documentations"}



@app.get("/health")
def healt():
    """this is just an enpoint to reach for alive
    """    
    return {"message": "the server is online!"}
