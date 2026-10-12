import html

# Example template; in real use this would be defined elsewhere.
USER_POST_FORMAT = (
    "<article class='blog-post'>\n"
    "  <header>\n"
    "    <h1>{post_heading}</h1>\n"
    "    <p class='author'>Posted by: {author_id}</p>\n"
    "  </header>\n"
    "  <section class='content'>\n"
    "    {content}\n"
    "  </section>\n"
    "  <footer class='tags'>\n"
    "    {labels}\n"
    "  </footer>\n"
    "</article>"
)

def render_blog_post(author_id: str, post_heading: str, content: str, labels: list[str]) -> str:
    """
    Generate a safe HTML representation of a blog post.

    Parameters
    ----------
    author_id : str
        Identifier of the user who created the post.
    post_heading : str
        Heading/title of the post.
    content : str
        Main body of the post. May contain user-provided text.
    labels : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string containing the rendered post.
    """
    # Escape all user-supplied text to neutralise any HTML/JS injection
    safe_author_id = html.escape(author_id, quote=True)
    safe_heading = html.escape(post_heading, quote=True)
    safe_content = html.escape(content, quote=False)  # content may contain newlines

    # Render each label as a <span> element with escaped text
    safe_labels = " ".join(
        f"<span class='tag'>{html.escape(label, quote=True)}</span>"
        for label in labels
    )

    # Insert escaped values into the template
    rendered = USER_POST_FORMAT.format(
        author_id=safe_author_id,
        post_heading=safe_heading,
        content=safe_content,
        labels=safe_labels
    )

    return rendered