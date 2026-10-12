import html

# Pre‑existing HTML template.
# The placeholders {writer_name}, {title}, {body} and {tags}
# will be replaced by the escaped values below.
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p class="author">Posted by: {writer_name}</p>
  <div class="content">{body}</div>
  <div class="tags">
    {tags}
  </div>
</div>
"""

def generate_post_html(writer_name: str, title: str, body: str,
                       tag_list: list[str]) -> str:
    """
    Build a safe HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        Name of the author.
    title : str
        Post headline.
    body : str
        Main text of the post.
    tag_list : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        XSS‑protected HTML string.
    """
    # Basic type checks – raise informative errors if types are wrong
    if not isinstance(writer_name, str):
        raise TypeError("writer_name must be a string")
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(body, str):
        raise TypeError("body must be a string")
    if not (isinstance(tag_list, list) and all(isinstance(t, str) for t in tag_list)):
        raise TypeError("tag_list must be a list of strings")

    # Escape user supplied text to avoid XSS
    esc_writer = html.escape(writer_name, quote=True)
    esc_title = html.escape(title, quote=True)
    esc_body  = html.escape(body)

    # Wrap each tag in a <span> element, escaping the tag text itself
    escaped_tags = " ".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    )

    # Populate the template with escaped values
    html_output = USER_POST_FORMAT.format(
        writer_name=esc_writer,
        title=esc_title,
        body=esc_body,
        tags=escaped_tags
    )

    return html_output.strip()