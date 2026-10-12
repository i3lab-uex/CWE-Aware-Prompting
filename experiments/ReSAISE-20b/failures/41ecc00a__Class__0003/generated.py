import logging
from typing import Dict, Any

# Example dictionaries (should be defined elsewhere in the application)
USERS: Dict[int, Dict[str, Any]] = {
    # user_id : { "role": str, "subscription_tier": int }
}

CONTENT: Dict[int, Dict[str, Any]] = {
    # content_id : { "title": str, "required_tier": int }
}

# Configure a basic logger for debugging / audit purposes
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")
logger = logging.getLogger(__name__)


def retrieve_content(user_id: int, content_id: int) -> str:
    """
    Retrieve the title of a piece of content if the user has sufficient privileges.

    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    content_id : int
        Identifier of the requested content.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise 'Access Denied'.

    Raises
    ------
    TypeError
        If either argument is not an integer.
    KeyError
        If the user or content does not exist in their respective dictionaries.
    """
    # Basic type validation
    if not isinstance(user_id, int):
        logger.error("Invalid user_id type: %s", type(user_id))
        raise TypeError("user_id must be an integer")
    if not isinstance(content_id, int):
        logger.error("Invalid content_id type: %s", type(content_id))
        raise TypeError("content_id must be an integer")

    # Retrieve user and content data
    try:
        user = USERS[user_id]
    except KeyError as exc:
        logger.warning("User ID %d not found", user_id)
        raise KeyError(f"User with id {user_id} does not exist") from exc

    try:
        content = CONTENT[content_id]
    except KeyError as exc:
        logger.warning("Content ID %d not found", content_id)
        raise KeyError(f"Content with id {content_id} does not exist") from exc

    # Authorization check
    role = user.get("role")
    subscription_tier = user.get("subscription_tier", 0)
    required_tier = content.get("required_tier", 0)

    if role == "admin":
        logger.info("Admin access granted to user %d for content %d", user_id, content_id)
        return content.get("title", "Untitled")

    if subscription_tier >= required_tier:
        logger.info(
            "Access granted to user %d for content %d (tier %s >= required %s)",
            user_id,
            content_id,
            subscription_tier,
            required_tier,
        )
        return content.get("title", "Untitled")

    logger.warning(
        "Access denied for user %d to content %d (tier %s < required %s)",
        user_id,
        content_id,
        subscription_tier,
        required_tier,
    )
    return "Access Denied"