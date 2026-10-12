import html
from typing import List

# Predefined template with placeholders for the post components.
USER_POST_FORMAT = (
    "<div class='post'>"
    "  <h1>{title}</h1>"
    "  <p class='author'>by {author_name}</p>"
    "  <div class='content'>{body}</div>"
    "  <div class='tags'>{{tags}}</div>"
    "</div>"
)

def render_forum_post(
    author_name: str,
    title: str,
    body_content: str,
    tag_list: List[str]
) -> str:
    """
    Generate a secure, XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Identifier of the post's creator.
    title : str
        The heading of the user's post.
    body_content : str
        Primary content of the user's post.
    tag_list : list[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        Sanitized HTML string for rendering.
    """
    # Escape all user‑supplied content to prevent injection attacks (CWE‑74).
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body_content, quote=False)  # body may contain line breaks

    # Wrap each tag in a <span> and escape the tag text.
    safe_tags = "".join(
        f"<span class='tag'>{html.escape(tag, quote=True)}</span>"
        for tag in tag_list
    )

    # Render the final HTML using the template.
    return USER_POST_FORMAT.format(
        title=safe_title,
        author_name=safe_author,
        body=safe_body,
        tags=safe_tags
    )