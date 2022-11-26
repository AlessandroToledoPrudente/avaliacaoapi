from fastapi import FastAPI, status, Response
from pydantic import BaseModel, Field
from typing import Optional, Union

app = FastAPI()

class Cliente(BaseModel):
    id: int 
    nome:str = Field(max_length=20)
    data: str
    tipo: str = Field(max_length=1)
    atendido: bool

db_clientes = [
    Cliente(id=0, nome="Carlos da Silva", data="19/11/2022", tipo="N", atendido=False),
    Cliente(id=1, nome="Maria Aparecida", data="21/11/2022", tipo="N", atendido=False),
    Cliente(id=2, nome="Fernando Correa", data="22/11/2022", tipo="N", atendido=False),
    Cliente(id=3, nome="Euclides Castro", data="24/11/2022", tipo="N", atendido=False),
    Cliente(id=4, nome="Mariana Torres", data="25/11/2022", tipo="N", atendido=False)
]

@app.get("/fila", status_code=status.HTTP_200_OK)
async def exibir_fila():
    return {"fila": db_clientes}

@app.get("/fila/{id}")
async def cliente_posicao(id: int):
    for cliente in db_clientes:
        if cliente.id == id:
            return {"fila": [cliente for cliente in db_clientes if cliente.id == id ]}
    Response.status_code=status.HTTP_404_NOT_FOUND
    return {"mensagem": "Cliente não localizado"}
            
@app.post("/fila", status_code=status.HTTP_200_OK)
async def add_cliente(cliente: Cliente):
    if len(db_clientes) == 0:
        return {"Fila vazia"}
    cliente.id = db_clientes[-1].id + 1
    db_clientes.append(cliente)
    return {"mensagem": "Cliente adicionado à fila"}

@app.put("/fila")
async def atender_cliente():
    if len(db_clientes) == 0:
        return {"Fila vazia"}
    db_clientes[0].atendido = True
    aux = db_clientes[0]
    db_clientes.remove(aux)
    return {"Próximo ": aux}

@app.delete("/fila/{id}")
async def deletar_cliente(id: int):
    for cliente in db_clientes:
        if cliente.id == id:
            cliente = [cliente for cliente in db_clientes if cliente.id == id]
            db_clientes.remove(cliente[0])
            return {"mensagem": "Cliente removido"}
    Response.status_code=status.HTTP_404_NOT_FOUND
    return {"mensagem": "Cliente não localizado"}