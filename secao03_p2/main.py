from fastapi import FastAPI

from routes import curso_router, usuario_router

app = FastAPI()
app.include_router(curso_router.router, tags=['cursos'])
app.include_router(usuario_router.router, tags=['usuarios'])

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)