from app.config import Environment
from app.utils.env_vars import validate_variables


def env_factory() -> Environment:
    return validate_variables(Environment)

