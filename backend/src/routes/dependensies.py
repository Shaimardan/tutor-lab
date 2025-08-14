from typing import Annotated

from fastapi import Depends

from src.db.session import db_connections
from src.service_layer.unit_of_work import IUnitOfWork, UnitOfWork


def get_uow() -> IUnitOfWork:
    return UnitOfWork(db_connections.async_session)


UOWDep = Annotated[IUnitOfWork, Depends(get_uow)]
