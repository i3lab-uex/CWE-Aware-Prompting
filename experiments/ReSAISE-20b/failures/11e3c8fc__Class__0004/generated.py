import html

# Predefined HTML template with placeholders.
# Placeholders are surrounded by double curly braces for clarity.
USER_POST_FORMAT = """
<article class="blog-post" data-author-id="{{author_id}}">
  <header>
    <h1>{{post_heading}}</h1>
    <p class="author">Posted by: {{author_id}}</p>
  </header>
  <section class="content">
    {{content}}
  </section>
  <footer class="tags">
    {{labels}}
  </footer>
</article>
"""

def render_blog_post(author_id: str,
                     post_heading: str,
                     content: str,
                     labels: list[str]) -> str:
    """
    Render a secure, XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    author_id : str
        Identifier of the post's creator.
    post_heading : str
        Heading/title of the post.
    content : str
        Main body of the post. May contain user‑supplied markup that must be escaped.
    labels : list[str]
        Sequence of tags/labels to display. Each will be wrapped in a <span>.

    Returns
    -------
    str
        A fully escaped HTML string ready for rendering in a browser.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    """
    # Basic type checks (prevent accidental injection from non‑string types)
    if not isinstance(author_id, str):
        raise TypeError("author_id must be a string")
    if not isinstance(post_heading, str):
        raise TypeError("post_heading must be a string")
    if not isinstance(content, str):
        raise TypeError("content must be a string")
    if not (isinstance(labels, list) and all(isinstance(l, str) for l in labels)):
        raise TypeError("labels must be a list of strings")

    # Escape all user‑supplied content to neutralize HTML/JS injection.
    esc_author_id = html.escape(author_id, quote=True)
    esc_post_heading = html.escape(post_heading, quote=True)
    esc_content = html.escape(content, quote=False)  # preserve newlines

    # Render each label as a safe <span>
    escaped_labels = []
    for tag in labels:
        esc_tag = html.escape(tag, quote=True)
        escaped_labels.append(f'<span class="tag">{esc_tag}</span>')

    # Join labels with a space for readability
    labels_html = " ".join(escaped_labels)

    # Replace placeholders in the template
    rendered = USER_POST_FORMAT.format(
        author_id=esc_author_id,
        post_heading=esc_post_heading,
        content=esc_content,
        labels=labels_html
    )

    return rendered.strip()