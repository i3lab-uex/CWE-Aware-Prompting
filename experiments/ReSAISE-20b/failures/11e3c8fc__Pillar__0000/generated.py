import html
from typing import List

# Example template; in real usage this would be defined elsewhere.
USER_POST_FORMAT = (
    "<article id=\"post-{author_id}\">\n"
    "  <header>\n"
    "    <h1>{post_heading}</h1>\n"
    "    <p class=\"author\">Posted by: {author_id}</p>\n"
    "  </header>\n"
    "  <section class=\"content\">\n"
    "    {content}\n"
    "  </section>\n"
    "  <footer class=\"tags\">\n"
    "    {labels}\n"
    "  </footer>\n"
"</article>"
)

def render_blog_post(
    author_id: str,
    post_heading: str,
    content: str,
    labels: List[str]
) -> str:
    """
    Generate a secure HTML representation of a forum post.

    Args:
        author_id: Identifier of the post's creator.
        post_heading: Title of the post.
        content: Main body of the post.
        labels: List of tags associated with the post.

    Returns:
        A string containing the XSS‑protected HTML.
    """
    # Escape all user‑supplied data to prevent injection
    safe_author_id = html.escape(author_id, quote=True)
    safe_heading   = html.escape(post_heading, quote=True)
    safe_content   = html.escape(content, quote=False)

    # Wrap each label in a <span> and escape the label text
    safe_labels = ""
    for tag in labels:
        escaped_tag = html.escape(tag, quote=True)
        safe_labels += f'<span class="tag">{escaped_tag}</span> '

    # Strip trailing space
    safe_labels = safe_labels.strip()

    # Format the final HTML using the provided template
    return USER_POST_FORMAT.format(
        author_id=safe_author_id,
        post_heading=safe_heading,
        content=safe_content,
        labels=safe_labels
    )