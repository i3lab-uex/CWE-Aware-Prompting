import html

# Predefined template for a forum post.  
# It contains placeholders for poster, heading, body and labels.
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

    Parameters
    ----------
    poster : str
        Author of the post.
    heading : str
        Title of the post.
    body : str
        Main content of the post.
    labels : list[str]
        List of tags to associate with the post.

    Returns
    -------
    str
        A string containing safe HTML for rendering on a web page.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    """
    # Basic type checking to catch programming errors early
    if not isinstance(poster, str):
        raise TypeError("poster must be a string")
    if not isinstance(heading, str):
        raise TypeError("heading must be a string")
    if not isinstance(body, str):
        raise TypeError("body must be a string")
    if not isinstance(labels, list) or not all(isinstance(l, str) for l in labels):
        raise TypeError("labels must be a list of strings")

    # Escape user-supplied content to prevent XSS
    safe_poster = html.escape(poster, quote=True)
    safe_heading = html.escape(heading, quote=True)
    safe_body = html.escape(body, quote=False).replace('\n', '<br>')

    # Build the tags section
    safe_labels = []
    for label in labels:
        escaped_label = html.escape(label, quote=True)
        safe_labels.append(f'<span class="tag">{escaped_label}</span>')
    labels_html = ' '.join(safe_labels)

    # Format the final HTML
    return USER_POST_FORMAT.format(
        poster=safe_poster,
        heading=safe_heading,
        body=safe_body,
        labels=labels_html
    )