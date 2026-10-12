import html

# Pre‑existing template string with placeholders for the post's components.
USER_POST_FORMAT = """
<div class="post">
    <h2>{title}</h2>
    <p class="author">Posted by: {writer_name}</p>
    <div class="body">{body}</div>
    <div class="tags">{tags}</div>
</div>
"""

def generate_post_html(writer_name: str,
                       title: str,
                       body: str,
                       tag_list: list[str]) -> str:
    """
    Construct a safe HTML representation of a forum post.

    Parameters
    ----------
    writer_name : str
        The name of the author.
    title : str
        The headline of the post.
    body : str
        The main content of the post.
    tag_list : list[str]
        A collection of tags related to the post.

    Returns
    -------
    str
        An XSS‑protected HTML string representing the post.

    Raises
    ------
    ValueError
        If any argument is not of an expected type.
    """
    # Validate input types to avoid unexpected behavior
    if not isinstance(writer_name, str):
        raise ValueError("writer_name must be a string")
    if not isinstance(title, str):
        raise ValueError("title must be a string")
    if not isinstance(body, str):
        raise ValueError("body must be a string")
    if not (isinstance(tag_list, list) and all(isinstance(t, str) for t in tag_list)):
        raise ValueError("tag_list must be a list of strings")

    # Escape all user‑supplied content to neutralize special HTML characters
    escaped_writer_name = html.escape(writer_name, quote=True)
    escaped_title = html.escape(title, quote=True)
    escaped_body = html.escape(body, quote=True)

    # Build the tags string: each tag inside a <span>, escaped as well
    escaped_tags = "".join(
        f'<span class="tag">{html.escape(tag, quote=True)}</span>'
        for tag in tag_list
    )

    # Format the template with the escaped values
    return USER_POST_FORMAT.format(
        writer_name=escaped_writer_name,
        title=escaped_title,
        body=escaped_body,
        tags=escaped_tags
    )