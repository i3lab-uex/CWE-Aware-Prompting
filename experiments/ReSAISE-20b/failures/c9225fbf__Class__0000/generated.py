import html
from typing import List

# Example template; in real usage this should be defined elsewhere.
USER_POST_FORMAT = (
    "<div class='post'>"
    "<h2>{title}</h2>"
    "<p><strong>Author:</strong> {author_name}</p>"
    "<div class='content'>{content}</div>"
    "<div class='tags'>Tags: {tags}</div>"
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
        Name of the post's author.
    post_title : str
        Headline of the user's post.
    content : str
        Primary text content of the user's post.
    post_tags : list[str]
        Collection of tags related to the post.

    Returns
    -------
    str
        A string containing the sanitized HTML representation of the post.
    """
    # Escape all user‑supplied content to prevent injection
    safe_author = html.escape(author_name, quote=True)
    safe_title = html.escape(post_title, quote=True)
    safe_content = html.escape(content, quote=False)

    # Build tag spans; each tag is escaped and wrapped in <span>
    safe_tags = []
    for tag in post_tags:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags.append(f"<span class='tag'>{escaped_tag}</span>")
    tags_html = " ".join(safe_tags)

    # Insert into the template
    html_output = USER_POST_FORMAT.format(
        author_name=safe_author,
        title=safe_title,
        content=safe_content,
        tags=tags_html
    )
    return html_output