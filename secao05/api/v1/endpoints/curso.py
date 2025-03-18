from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.curso_model import CursoModel
from core.deps import get_session

# Bypass warning SQLModel select
# https://github.com/fastapi/sqlmodel/issues/189
from sqlmodel.sql.expression import Select, SelectOfScalar
SelectOfScalar.inherit_cache = True # type: ignore
Select.inherit_cache = True # type: ignore
# Fim Bypass

router = APIRouter()

# POST curso
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def post_curso(curso: CursoModel, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)

    db.add(novo_curso)
    await db.commit()

    return novo_curso

# GET cursos
@router.get('/', response_model=List[CursoModel])
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()

        return cursos