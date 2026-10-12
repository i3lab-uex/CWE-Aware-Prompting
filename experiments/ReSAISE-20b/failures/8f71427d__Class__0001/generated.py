import html
from typing import List

# Predefined template with placeholders:
USER_POST_FORMAT = """
<div class="post">
  <h2>{title_key}</h2>
  <p>by <span class="author">{username_key}</span></p>
  <div class="content">{body_key}</div>
  <div class="tags">{tag_elements}</div>
</div>
"""

def render_user_content(
    username_key: str,
    title_key: str,
    body_key: str,
    tag_elements: List[str]
) -> str:
    """
    Generate a safe HTML representation of a forum post.

    Parameters
    ----------
    username_key : str
        The identifier of the post's creator.
    title_key : str
        The heading of the user's post.
    body_key : str
        The primary content of the user's post.
    tag_elements : list[str]
        A sequence of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string of the user’s post.

    Notes
    -----
    * All user-supplied data is escaped using ``html.escape`` to neutralize
      special characters and prevent injection attacks (CWE‑74).
    * Tags are wrapped individually in `<span>` elements and also escaped.
    """
    # Escape all user-supplied strings
    safe_username = html.escape(username_key, quote=True)
    safe_title = html.escape(title_key, quote=True)
    safe_body = html.escape(body_key, quote=True)

    # Wrap each tag in a <span> and escape the tag content
    safe_tags = "".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_elements
    )

    # Format the final HTML string with escaped values
    return USER_POST_FORMAT.format(
        username_key=safe_username,
        title_key=safe_title,
        body_key=safe_body,
        tag_elements=safe_tags
    )