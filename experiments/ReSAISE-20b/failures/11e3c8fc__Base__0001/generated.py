import html

# Example template; in real use this would be defined elsewhere.
USER_POST_FORMAT = (
    "<article class='blog-post'>"
    "  <h1>{post_heading}</h1>"
    "  <p class='author'>Posted by: {author_id}</p>"
    "  <div class='content'>{content}</div>"
    "  <footer class='tags'>"
    "    {labels}"
    "  </footer>"
    "</article>"
)

def render_blog_post(author_id: str,
                     post_heading: str,
                     content: str,
                     labels: list[str]) -> str:
    """
    Generate a safe, XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_id : str
        Identifier of the post's creator.
    post_heading : str
        Heading/title of the user's post.
    content : str
        Main body/content of the post.
    labels : list[str]
        Labels/tags associated with the post.

    Returns
    -------
    str
        An HTML string safe for inclusion in a web page.
    """
    # Escape all user‑controlled input to prevent XSS
    safe_author_id = html.escape(author_id, quote=True)
    safe_heading = html.escape(post_heading, quote=True)
    safe_content = html.escape(content)

    # Build the tags markup
    tag_spans = []
    for tag in labels:
        safe_tag = html.escape(tag, quote=True)
        tag_spans.append(f"<span class='tag'>{safe_tag}</span>")
    labels_html = " ".join(tag_spans)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        author_id=safe_author_id,
        post_heading=safe_heading,
        content=safe_content,
        labels=labels_html
    )