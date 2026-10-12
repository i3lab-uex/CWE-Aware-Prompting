import html
from typing import List

# Template for user posts. Placeholders are named for readability.
USER_POST_FORMAT = (
    "<div class=\"user-post\">\n"
    "  <h2>{post_title}</h2>\n"
    "  <p class=\"author\">Posted by: {username}</p>\n"
    "  <div class=\"content\">{post_body}</div>\n"
    "  <div class=\"tags\">{tags}</div>\n"
    "</div>"
)

def render_user_post(username: str, post_title: str, post_body: str, tags: List[str]) -> str:
    """
    Render a user-generated post as sanitized HTML.

    Parameters
    ----------
    username : str
        The name of the user who created the post.
    post_title : str
        The title of the post.
    post_body : str
        The main content of the post.
    tags : list[str]
        A list of tags added by the user.

    Returns
    -------
    str
        Sanitized HTML representation of the post.
    """
    # Escape all user-provided strings to prevent XSS and other injection attacks
    safe_username = html.escape(username, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=False)  # Preserve newlines

    # Render tags as <span> elements. Each tag is escaped individually.
    safe_tags = " ".join(
        f"<span>{html.escape(tag, quote=True)}</span>" for tag in tags
    )

    # Format the final HTML using the template
    rendered = USER_POST_FORMAT.format(
        username=safe_username,
        post_title=safe_title,
        post_body=safe_body,
        tags=safe_tags
    )
    return rendered