from typing import Optional

from pydantic import BaseModel, validator

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    @validator('titulo')
    def validar_titulo(cls, value: str):
        palavras = value.split(' ')

        if len(palavras) < 3:
            raise ValueError('O título deve ter pelo menos 3 palavras.')

        if value.islower():
            raise ValueError('O título deve ser capitalizado.')

        return value

    @validator('aulas')
    def validar_aulas(cls, value: int):

        if value <= 12:
            raise ValueError('O curso deve possuir mais de 12 aulas')

        return value

    @validator('horas')
    def validar_horas(cls, value: int):

        if value <= 10:
            raise ValueError('O curso deve ter mais de 10 horas de duração')

        return value

cursos = [
    Curso(id=1, titulo='Programação para Leigos', aulas=42, horas=56),
    Curso(id=2, titulo='Algoritmos e Lógica de Programação', aulas=52, horas=66)
]