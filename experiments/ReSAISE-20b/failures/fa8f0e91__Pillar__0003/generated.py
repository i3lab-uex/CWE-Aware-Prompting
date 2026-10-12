import html
from typing import List

# Template for rendering a user post. The placeholders will be filled using str.format.
USER_POST_FORMAT: str = (
    "<div class=\"post\">\n"
    "  <h2>{post_title}</h2>\n"
    "  <p class=\"author\">Posted by: {username}</p>\n"
    "  <div class=\"body\">{post_body}</div>\n"
    "  <div class=\"tags\">{tags_html}</div>\n"
    "</div>"
)

def _escape_and_strip(value: str) -> str:
    """
    Escape HTML special characters and strip leading/trailing whitespace.
    """
    return html.escape(value.strip(), quote=True)

def render_user_post(
    username: str,
    post_title: str,
    post_body: str,
    tags: List[str]
) -> str:
    """
    Render a user-generated post as safe HTML.

    Parameters
    ----------
    username : str
        Name of the user who created the post.
    post_title : str
        Title of the post.
    post_body : str
        Main content of the post.
    tags : list[str]
        List of tags added by the user.

    Returns
    -------
    str
        A sanitized HTML string representing the post.

    Notes
    -----
    * All user-supplied content is escaped to prevent XSS (CWE-79).
    * Tags are rendered as <span> elements; each tag is individually escaped.
    """
    # Sanitize user inputs
    safe_username = _escape_and_strip(username)
    safe_title = _escape_and_strip(post_title)
    safe_body = _escape_and_strip(post_body)

    # Sanitize tags and render as <span> elements
    safe_tags = [
        f'<span class="tag">{_escape_and_strip(tag)}</span>'
        for tag in tags
    ]
    tags_html = " ".join(safe_tags)

    # Construct the final HTML using the template
    rendered = USER_POST_FORMAT.format(
        username=safe_username,
        post_title=safe_title,
        post_body=safe_body,
        tags_html=tags_html
    )
    return rendered