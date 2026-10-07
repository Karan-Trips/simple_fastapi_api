from __future__ import annotations

# Backward compatibility repository module wrapping UserService
from app.services.user_service import UserService

get_all_users = UserService.get_all_users
get_user_by_name = UserService.get_user_by_name
get_user_by_email = UserService.get_user_by_email
get_user_by_id = UserService.get_user_by_id
register_user = UserService.register_user
update_user = UserService.update_user
delete_user = UserService.delete_user

__all__ = [
    "get_all_users",
    "get_user_by_name",
    "get_user_by_email",
    "get_user_by_id",
    "register_user",
    "update_user",
    "delete_user",
]
