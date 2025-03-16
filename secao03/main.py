from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, status, Response, Path, Query, Header, Depends
from models import Curso, cursos
from time import sleep

def fake_db():
    try:
        print('Abrindo conexão com banco de dados...')
        sleep(0.1)
    finally:
        print('Fechando conexão com banco de dados...')
        sleep(0.1)

app = FastAPI(
    title='API de Cursos da Geek University',
    version='0.0.1',
    description='Uma API para estudo do FastAPI'
)

@app.get('/cursos',
    description='Retorna todos os cursos ou uma lista vazia.',
    summary='Retorna todos os cursos',
    response_model=List[Curso],
    response_description='Cursos encontrados com sucesso.'
)
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos

@app.get('/cursos/{curso_id}',
    description='Obtém um curso por ID, se o curso não for encontrado, uma HTTPException com status 404 Not Found é lançada',
    summary='Obtém um curso por ID'
)
async def get_curso(curso_id: int = Path(title='ID do curso', description='Deve ser entre 1 e 2', gt=0, lt=3),  db: Any = Depends(fake_db)):
    try:
        curso = next((c for c in cursos if c.id == curso_id), None)
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')
    
@app.post('/cursos',
    status_code=status.HTTP_201_CREATED,
    description='Adiciona um novo curso à lista de cursos',
    summary='Adiciona um novo curso',
    response_model=Curso
)
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    next_id: int = len(cursos) + 1
    curso.id = next_id
    cursos.append(curso)
    return curso

@app.put('/cursos/{curso_id}',
    description='Atualiza um curso existente',
    summary='Atualiza um curso'
)
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    curso_encontrado = next((c for c in cursos if c.id == curso_id), None)

    if curso_encontrado:
        curso_encontrado.titulo = curso.titulo
        curso_encontrado.horas = curso.horas
        curso_encontrado.aulas = curso.aulas
        return curso_encontrado
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe um curso com id {curso_id}')
    
@app.delete('/cursos/{curso_id}',
    description='Exclui um curso existente',
    summary='Exclui um curso'
)
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    curso_encontrado = next((c for c in cursos if c.id == curso_id), None)

    if curso_encontrado:
        cursos.remove(curso_encontrado)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe um curso com id {curso_id}')

# http://localhost:8000/calculadora?a=1&b=2&c=3
@app.get('/calculadora')
# async def calcular(a: Optional[int] = 0, b: Optional[int] = 0, c: Optional[int] = 0):
async def calcular(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), c: Optional[int] = 0, x_geek: str = Header(default=None)):
    soma = a + b + c

    print(f'X-GEEK: {x_geek}')

    return {"resultado": soma}    

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)