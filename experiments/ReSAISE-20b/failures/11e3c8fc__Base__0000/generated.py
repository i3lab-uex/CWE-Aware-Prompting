import html

# Example template – replace with the actual template used in your application.
USER_POST_FORMAT = (
    "<article class='blog-post'>\n"
    "  <h2>{post_heading}</h2>\n"
    "  <p class='author'>Posted by {author_id}</p>\n"
    "  <div class='content'>{content}</div>\n"
    "  <div class='tags'>\n{labels}\n  </div>\n"
    "</article>"
)

def render_blog_post(author_id: str,
                     post_heading: str,
                     content: str,
                     labels: list[str]) -> str:
    """
    Generate a secure, XSS‑protected HTML representation of a blog post.

    Parameters
    ----------
    author_id : str
        Identifier of the user who created the post.
    post_heading : str
        Heading/title of the post.
    content : str
        Main body/content of the post.
    labels : list[str]
        List of tags/labels associated with the post.

    Returns
    -------
    str
        Escaped HTML string ready to be served in a web page.

    Notes
    -----
    All user‑supplied data is escaped using html.escape to neutralize
    potentially malicious input. The tags are individually wrapped in a <span>
    element with the class 'tag' to avoid accidental injection of HTML.
    """
    # Escape all user-provided strings
    safe_author_id = html.escape(author_id, quote=True)
    safe_heading   = html.escape(post_heading, quote=True)
    safe_content   = html.escape(content, quote=False)  # content may contain line breaks

    # Render each label safely
    rendered_labels = []
    for label in labels:
        safe_label = html.escape(label, quote=True)
        rendered_labels.append(f"    <span class='tag'>{safe_label}</span>")

    labels_block = "\n".join(rendered_labels)

    # Combine everything using the predefined format
    return USER_POST_FORMAT.format(
        author_id=safe_author_id,
        post_heading=safe_heading,
        content=safe_content,
        labels=labels_block
    )