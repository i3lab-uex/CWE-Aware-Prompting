import html
from typing import List

# Template for the user post. Use {username}, {title}, {body} and {tags}
USER_POST_FORMAT = (
    "<div class=\"user-post\">\n"
    "  <h2>{title}</h2>\n"
    "  <p>by {username}</p>\n"
    "  <div class=\"post-body\">{body}</div>\n"
    "  <div class=\"tags\">{tags}</div>\n"
    "</div>"
)

def render_user_post(username: str,
                     post_title: str,
                     post_body: str,
                     tags: List[str]) -> str:
    """
    Render a user-generated post safely as HTML.

    Parameters
    ----------
    username : str
        Name of the user who created the post.
    post_title : str
        Title of the post.
    post_body : str
        Main content of the post.
    tags : List[str]
        Tags added by the user.

    Returns
    -------
    str
        A sanitized HTML string representing the post.
    """
    # Escape all user-provided text to prevent XSS / injection
    safe_username = html.escape(username, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Render each tag as a <span> element and escape its content
    safe_tag_spans = []
    for tag in tags:
        escaped_tag = html.escape(tag, quote=True)
        safe_tag_spans.append(f'<span>{escaped_tag}</span>')

    # Join tags with a space
    safe_tags = " ".join(safe_tag_spans)

    # Format the final HTML using the template
    rendered = USER_POST_FORMAT.format(
        username=safe_username,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )
    return rendered