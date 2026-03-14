from dataclasses import dataclass

from fastapi import Header, HTTPException


@dataclass
class AuthContext:
    user_id: str
    role: str


_ALLOWED_ROLES = {"viewer", "editor", "admin"}


def get_auth_context(
    x_user_id: str | None = Header(default=None),
    x_user_role: str | None = Header(default=None),
) -> AuthContext:
    user_id = x_user_id or "local-dev"
    role = x_user_role or "admin"

    if role not in _ALLOWED_ROLES:
        raise HTTPException(status_code=403, detail="Invalid role")

    return AuthContext(user_id=user_id, role=role)


def require_editor_or_admin(
    x_user_id: str | None = Header(default=None),
    x_user_role: str | None = Header(default=None),
) -> AuthContext:
    ctx = get_auth_context(x_user_id=x_user_id, x_user_role=x_user_role)
    if ctx.role not in {"editor", "admin"}:
        raise HTTPException(status_code=403, detail="Editor or admin role required")
    return ctx


def require_admin(
    x_user_id: str | None = Header(default=None),
    x_user_role: str | None = Header(default=None),
) -> AuthContext:
    ctx = get_auth_context(x_user_id=x_user_id, x_user_role=x_user_role)
    if ctx.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    return ctx
