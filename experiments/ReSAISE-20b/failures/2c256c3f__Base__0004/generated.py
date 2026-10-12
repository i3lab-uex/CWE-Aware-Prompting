import html

# The template should contain placeholders named exactly as the function arguments.
# Example:
# USER_POST_FORMAT = """
# <article>
#   <h1>{title}</h1>
#   <p class="author">By {writer_name}</p>
#   <div class="body">{body}</div>
#   <ul class="tags">{tags}</ul>
# </article>
# """
USER_POST_FORMAT = """<article>
  <h1>{title}</h1>
  <p class="author">By {writer_name}</p>
  <div class="body">{body}</div>
  <ul class="tags">{tags}</ul>
</article>"""


def generate_post_html(writer_name: str, title: str, body: str, tag_list: list[str]) -> str:
    """
    Construct an XSS‑protected HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        Name of the author.
    title : str
        Title/headline of the post.
    body : str
        Main text content of the post.
    tag_list : list[str]
        Tags associated with the post.

    Returns
    -------
    str
        Safe HTML string ready to be served in a web page.

    Raises
    ------
    ValueError
        If any argument is not of the expected type.
    """
    # Basic type checking (helps catch programming errors early)
    if not isinstance(writer_name, str):
        raise ValueError("writer_name must be a string")
    if not isinstance(title, str):
        raise ValueError("title must be a string")
    if not isinstance(body, str):
        raise ValueError("body must be a string")
    if not isinstance(tag_list, list) or not all(isinstance(t, str) for t in tag_list):
        raise ValueError("tag_list must be a list of strings")

    # Escape user‑controlled content to neutralize XSS vectors
    safe_writer_name = html.escape(writer_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False).replace("\n", "<br>")

    # Render tags as individual <span> elements inside a <ul>
    rendered_tags = ""
    for tag in tag_list:
        safe_tag = html.escape(tag, quote=True)
        rendered_tags += f'<li><span>{safe_tag}</span></li>'

    # Insert escaped content into the template
    html_output = USER_POST_FORMAT.format(
        writer_name=safe_writer_name,
        title=safe_title,
        body=safe_body,
        tags=rendered_tags
    )
    return html_output