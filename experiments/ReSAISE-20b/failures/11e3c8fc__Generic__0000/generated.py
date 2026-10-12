import html

# Example template; in real usage this would be defined elsewhere.
USER_POST_FORMAT = """
<article class="blog-post" data-author="{author_id}">
    <h1>{post_heading}</h1>
    <div class="content">{content}</div>
    <footer class="tags">
        {labels}
    </footer>
</article>
"""

def render_blog_post(author_id: str,
                     post_heading: str,
                     content: str,
                     labels: list[str]) -> str:
    """
    Generate a secure, XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_id : str
        Identifier of the post's creator.
    post_heading : str
        Heading/title of the user's post.
    content : str
        Primary content/body of the user's post.
    labels : list[str]
        Sequence of tags/labels associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string representing the forum post.
    """
    # Escape all user supplied strings to avoid XSS
    safe_author_id = html.escape(author_id, quote=True)
    safe_heading = html.escape(post_heading, quote=False)
    safe_content = html.escape(content, quote=False)

    # Wrap each escaped label in a <span> element
    safe_labels = []
    for lbl in labels:
        escaped_lbl = html.escape(lbl, quote=False)
        safe_labels.append(f'<span class="tag">{escaped_lbl}</span>')
    labels_html = " ".join(safe_labels)

    # Format the template with the escaped values
    html_output = USER_POST_FORMAT.format(
        author_id=safe_author_id,
        post_heading=safe_heading,
        content=safe_content,
        labels=labels_html
    )

    return html_output.strip()