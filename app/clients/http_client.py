import logging
from typing import Any, List

from fastapi import HTTPException
from httpx import AsyncClient, HTTPStatusError, TimeoutException
from pydantic import BaseModel


class UnprocessableEntity(BaseModel):
    type: str
    loc: List[str]
    msg: str
    input: Any


class HTTPClientException(HTTPException):
    def __init__(
        self, status_code: int, details: Any, code: str = "", message: str = ""
    ):
        super().__init__(status_code=status_code)
        self.code = code
        self.details = details
        self.message = message


class HttpClient:
    async def make_request(self, url: str, method: str, **kwargs):
        try:
            response = await AsyncClient().request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except HTTPStatusError as http_err:

            if response.status_code == 422:
                unprocessable_entities: List[UnprocessableEntity] = []

                detail = http_err.response.json().get("detail")

                if len(detail) == 0:
                    raise HTTPClientException(
                        status_code=422,
                        code="INVALID_INPUT",
                        message="invalid input",
                        details="",
                    )

                for error in detail:
                    unprocessable_entity = UnprocessableEntity(
                        type=error.get("type"),
                        loc=error.get("loc"),
                        msg=error.get("msg"),
                        input=error.get("input"),
                    )
                    unprocessable_entities.append(unprocessable_entity)

                raise HTTPClientException(
                    status_code=response.status_code,
                    code="INVALID_INPUT",
                    message="invalid input",
                    details=unprocessable_entities,
                )
            if 400 <= response.status_code < 500:
                raise HTTPClientException(
                    status_code=response.status_code,
                    code=http_err.response.json().get("code"),
                    details=http_err.response.json().get("details"),
                    message=http_err.response.json().get("message"),
                )
            elif 500 <= response.status_code < 600:
                raise HTTPClientException(
                    status_code=response.status_code,
                    code="SERVER_ERROR",
                    details="",
                    message="Server error",
                )
        except TimeoutException as e:
            logging.error(e)
            raise HTTPClientException(
                status_code=408, code="TIMEOUT", details="", message="Request timeout"
            )
        except Exception as e:
            logging.error(e)
            raise HTTPClientException(
                status_code=500, code="SERVER_ERROR", details="", message="Server error"
            )
