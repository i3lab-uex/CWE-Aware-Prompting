import html
from typing import List

# Template for rendering a user post. Placeholders are:
#   {username} - the author of the post
#   {title}    - the title of the post
#   {body}     - the body content of the post
#   {tags}     - a string containing <span> elements for each tag
USER_POST_FORMAT = (
    "<article class=\"user-post\">\n"
    "  <header>\n"
    "    <h2>{title}</h2>\n"
    "    <p class=\"author\">Posted by {username}</p>\n"
    "  </header>\n"
    "  <section class=\"content\">\n"
    "    {body}\n"
    "  </section>\n"
    "  <footer class=\"tags\">\n"
    "    {tags}\n"
    "  </footer>\n"
    "</article>"
)

def render_user_post(
    username: str,
    post_title: str,
    post_body: str,
    tags: List[str]
) -> str:
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
    tags : List[str]
        A list of tags added by the user.

    Returns
    -------
    str
        Sanitized HTML string representing the post.
    """
    # Escape user-provided data to prevent XSS
    safe_username = html.escape(username, quote=True)
    safe_title = html.escape(post_title, quote=True)
    # For the body we escape but preserve line breaks as <br>
    safe_body = html.escape(post_body, quote=True).replace("\n", "<br>")

    # Render tags as <span> elements
    safe_tags = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tags
    )

    return USER_POST_FORMAT.format(
        username=safe_username,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )