import html
from typing import List

# Example template; in real use this would be defined elsewhere.
USER_POST_FORMAT = (
    "<article class=\"post\" data-author-id=\"{author_id}\">"
    "  <h2>{post_heading}</h2>"
    "  <div class=\"content\">{content}</div>"
    "  <footer>{labels}</footer>"
    "</article>"
)

def render_blog_post(
    author_id: str,
    post_heading: str,
    content: str,
    labels: List[str]
) -> str:
    """
    Generate a safe HTML representation of a forum post.

    Parameters
    ----------
    author_id : str
        Identifier of the user who created the post.
    post_heading : str
        The title or heading of the post.
    content : str
        Main body text of the post.
    labels : list[str]
        A sequence of tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string representing the post.
    """
    # Escape all user-provided content to prevent XSS
    safe_author_id = html.escape(author_id, quote=True)
    safe_heading   = html.escape(post_heading, quote=False)
    safe_content   = html.escape(content, quote=False)

    # Build label spans; each label is escaped and wrapped in a <span>
    safe_labels = [
        f"<span class=\"tag\">{html.escape(label, quote=False)}</span>"
        for label in labels
    ]
    labels_html = " ".join(safe_labels)

    # Format the final HTML using the template
    html_output = USER_POST_FORMAT.format(
        author_id=safe_author_id,
        post_heading=safe_heading,
        content=safe_content,
        labels=labels_html
    )
    return html_output