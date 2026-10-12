import html

# Example template; in real use this should be defined elsewhere.
USER_POST_FORMAT = """
<div class="post">
  <h2>{title}</h2>
  <p class="author">Posted by {writer_name}</p>
  <div class="content">{body}</div>
  <div class="tags">{tags}</div>
</div>
"""

def generate_post_html(writer_name: str, title: str, body: str, tag_list: list[str]) -> str:
    """
    Construct a safe HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        The name of the post's author.
    title : str
        The headline of the user's post.
    body : str
        The primary text content of the user's post.
    tag_list : list[str]
        A collection of tags related to the post.

    Returns
    -------
    str
        An XSS‑protected HTML string representing the forum post.

    Raises
    ------
    ValueError
        If any of the required arguments are not strings or if tag_list contains non‑string elements.
    """
    # Validate input types
    if not isinstance(writer_name, str):
        raise ValueError("writer_name must be a string")
    if not isinstance(title, str):
        raise ValueError("title must be a string")
    if not isinstance(body, str):
        raise ValueError("body must be a string")
    if not isinstance(tag_list, list) or any(not isinstance(t, str) for t in tag_list):
        raise ValueError("tag_list must be a list of strings")

    # Escape user input to prevent XSS
    safe_writer_name = html.escape(writer_name, quote=True)
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=False)  # body may contain newlines; escape tags only

    # Build the tags HTML, each tag wrapped in a <span>
    safe_tags = ""
    for tag in tag_list:
        escaped_tag = html.escape(tag, quote=True)
        safe_tags += f'<span class="tag">{escaped_tag}</span> '

    # Trim trailing space
    safe_tags = safe_tags.rstrip()

    # Populate the template
    return USER_POST_FORMAT.format(
        writer_name=safe_writer_name,
        title=safe_title,
        body=safe_body,
        tags=safe_tags
    )