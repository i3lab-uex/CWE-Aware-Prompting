import html
from typing import List

# Pre‑existing template with placeholders. 
# Example: "<div class='post'><h1>{title}</h1><p>by {author_name}</p><div class='content'>{content}</div>{tags_section}</div>"
USER_POST_FORMAT: str = (
    "<div class='post'>"
    "  <h1>{title}</h1>"
    "  <p class='author'>by {author_name}</p>"
    "  <div class='content'>{content}</div>"
    "  {tags_section}"
    "</div>"
)

def create_post_html(
    author_name: str,
    post_title: str,
    content: str,
    post_tags: List[str]
) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_name : str
        Name of the author.
    post_title : str
        Title/headline of the post.
    content : str
        Main body text of the post.
    post_tags : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        Safe HTML string for rendering.
    """
    # Escape all user‑supplied text to prevent injection
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_content = html.escape(content, quote=True)

    # Build tags section: each tag wrapped in <span class='tag'>
    safe_tags = []
    for tag in post_tags:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f"<span class='tag'>{escaped_tag}</span>")
    tags_section = "".join(safe_tags)

    # Insert into template
    html_output = USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        content=safe_content,
        tags_section=tags_section
    )
    return html_output