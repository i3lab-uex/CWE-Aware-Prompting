import html

# Predefined template with placeholders for the post components.
# Example: "<div class='post'><h2>{title}</h2><p>by {author_name}</p><div class='body'>{body}</div>{tags}</div>"
USER_POST_FORMAT: str = (
    "<article class='forum-post'>"
    "  <header><h2>{title}</h2>by {author_name}</header>"
    "  <section class='content'>{body}</section>"
    "  <footer>{tags}</footer>"
    "</article>"
)

def render_forum_post(
    author_name: str,
    title: str,
    body_content: str,
    tag_list: list[str],
) -> str:
    """
    Return an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Identifier of the post's creator.
    title : str
        Heading of the user's post.
    body_content : str
        Primary content of the user's post.
    tag_list : list[str]
        Sequence of tags associated with the post.

    Returns
    -------
    str
        A fully escaped HTML string suitable for safe rendering in a browser.
    """
    # Escape all user supplied content to neutralise special HTML characters.
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body_content, quote=False)  # Preserve newlines

    # Wrap each tag in a <span> element, escaping the tag text.
    escaped_tags = [
        f"<span class='tag'>{html.escape(tag, quote=True)}</span>"
        for tag in tag_list
    ]
    tags_html = "".join(escaped_tags)

    # Construct the final HTML using the template.
    return USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        body=safe_body,
        tags=tags_html
    )