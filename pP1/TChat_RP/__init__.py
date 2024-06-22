__all__ = ("router", )

from aiogram import Router

from .start_registr.startings import router as start_router

from .profile.profile import router as profile_router
from .profile.edit import router as edit_profile_router

from .rp_commands.admin_rp import router as admin_router
from .rp_commands.rp import router as rp_router

from .game_play.rabota import router as game_router
from .game_play.reiting import router as rank_router
from .game_play.rabstvo import router as rab_router

router = Router()
router.include_routers(
    start_router,
    profile_router, edit_profile_router,
    admin_router, rp_router,
    game_router, rank_router, rab_router
)
