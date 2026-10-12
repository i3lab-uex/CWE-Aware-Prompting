import html

# Predefined HTML template with placeholders.
USER_POST_FORMAT = """
<article class="forum-post">
    <header>
        <h2>{heading}</h2>
        <p class="author">Posted by: {poster}</p>
    </header>
    <section class="content">
        {body}
    </section>
    <footer class="tags">
        {labels}
    </footer>
</article>
"""

def create_forum_post(poster: str, heading: str, body: str, labels: list[str]) -> str:
    """
    Generate a sanitized HTML representation of a forum post.

    Args:
        poster (str): Author of the post.
        heading (str): Title of the post.
        body (str): Main content of the post. May contain line breaks and simple formatting.
        labels (list[str]): List of tags associated with the post.

    Returns:
        str: A string containing sanitized HTML for the forum post.
    """
    # Escape all user-provided content to prevent XSS and ensure well‑formed HTML.
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)

    # Preserve newlines in body by converting them to <br> tags after escaping.
    escaped_body = html.escape(body, quote=True).replace("\n", "<br>")

    # Escape each label and wrap it in a <span>.
    escaped_labels = " ".join(
        f'<span class="tag">{html.escape(label, quote=True)}</span>' for label in labels
    )

    # Render the final HTML using the predefined template.
    return USER_POST_FORMAT.format(
        poster=safe_poster,
        heading=safe_heading,
        body=escaped_body,
        labels=escaped_labels
    )