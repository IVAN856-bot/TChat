__all__ = ("router", )

from aiogram import Router

from .keyboard.callback import router as call_router

router = Router()
router.include_router(
    call_router
)
