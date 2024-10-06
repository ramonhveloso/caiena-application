from fastapi import APIRouter

from app.api.v1.auth.auth_controller import router as auth_router
from app.api.v1.current_weather.current_weather_controller import (
    router as current_weather_router,
)
from app.api.v1.forecasts_weather.forecast_weather_controller import (
    router as forecast_weather_router,
)
from app.api.v1.gist_comments.gist_comment_controller import (
    router as gist_comments_router,
)
from app.api.v1.users.user_controller import router as users_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(
    current_weather_router, prefix="/current-weather", tags=["current-weather"]
)
router.include_router(
    forecast_weather_router, prefix="/forecast-weather", tags=["forecast-weather"]
)
router.include_router(
    gist_comments_router, prefix="/gist-comments", tags=["gist-comments"]
)
