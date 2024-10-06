import logging
import os
from typing import TypeVar

from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)

logger = logging.getLogger(__name__)


def _pretty_print_validation_error(e: ValidationError, logger: logging.Logger) -> None:
    for error in e.errors():
        logger.error(f"Error in {error['loc']}: {error['msg']}")


def validate_variables(model: type[T], logger: logging.Logger = logger) -> T:
    try:
        return model.model_validate(os.environ)
    except ValidationError as e:
        logger.error(f"Invalid environment variables for {model.__name__}")
        _pretty_print_validation_error(e, logger)
        exit(1)
