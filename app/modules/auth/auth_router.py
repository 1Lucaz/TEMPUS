from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import get_auth_service
from app.modules.auth.auth_service import AuthService
from app.modules.utils.app_exception import *

router = APIRouter(tags=["Autenticação"])


@router.post("/login",
             status_code=status.HTTP_200_OK)
def login(is_colaborador: bool,
                  form: OAuth2PasswordRequestForm = Depends(),
                  service: AuthService = Depends(get_auth_service)):
    return service.login (is_colaborador = is_colaborador,
                                 email=form.username,
                                 senha=form.password)
