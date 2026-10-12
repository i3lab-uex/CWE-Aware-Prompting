import html

# Template for rendering a user post.
# Placeholders: {username}, {post_title}, {post_body}, {tags}
USER_POST_FORMAT = (
    "<article class=\"user-post\">\n"
    "  <header>\n"
    "    <h2>{post_title}</h2>\n"
    "    <p class=\"author\">Posted by {username}</p>\n"
    "  </header>\n"
    "  <section class=\"content\">{post_body}</section>\n"
    "  <footer class=\"tags\">{tags}</footer>\n"
    "</article>"
)

def render_user_post(username: str, post_title: str,
                     post_body: str, tags: list[str]) -> str:
    """
    Render a user-generated forum post as safe HTML.

    Args:
        username: The name of the user who created the post.
        post_title: The title of the post.
        post_body: The main content of the post.
        tags: A list of tags added by the user.

    Returns:
        A sanitized HTML string containing the post information.
    """
    # Escape all user-supplied data to prevent injection attacks
    safe_username = html.escape(username, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_body = html.escape(post_body, quote=False)  # Preserve newlines

    # Render tags as <span> elements separated by spaces
    safe_tags = " ".join(
        f"<span class=\"tag\">{html.escape(tag, quote=True)}</span>"
        for tag in tags
    )

    # Format the final HTML using the predefined template
    return USER_POST_FORMAT.format(
        username=safe_username,
        post_title=safe_title,
        post_body=safe_body,
        tags=safe_tags
    )