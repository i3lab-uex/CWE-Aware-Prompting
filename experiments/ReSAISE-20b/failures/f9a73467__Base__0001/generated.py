import html
from typing import List

# Pre‑defined HTML template for the forum post.  The placeholders are
# {title}, {body} and {list_items}.  In a real system this would be read
# from configuration or a template file.
FORUM_POST_FORMAT = """
<div class="forum-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
  <ul>{list_items}</ul>
</div>
"""

def compile_post(subject: str, text: str, highlights: List[str]) -> str:
    """
    Assemble a forum post from user supplied content.

    Parameters
    ----------
    subject : str
        The title of the forum post.
    text : str
        The main body content of the post.
    highlights : list[str]
        Discussion points or options supplied by the user.  They are
        expected to be simple markdown‑like strings but will be rendered
        as plain text inside list items.

    Returns
    -------
    str
        A fully formatted, HTML‑escaped forum post string.

    Raises
    ------
    ValueError
        If any argument is not of the expected type.
    """
    # Input validation – ensure arguments are correct types
    if not isinstance(subject, str):
        raise ValueError("subject must be a string")
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    if not isinstance(highlights, list) or not all(isinstance(h, str) for h in highlights):
        raise ValueError("highlights must be a list of strings")

    # Escape all user input to neutralise any HTML or JavaScript.
    escaped_subject = html.escape(subject, quote=True)
    escaped_body = html.escape(text, quote=True)

    # Convert each highlight into a safe <li> element.
    list_items = "".join(
        f"<li>{html.escape(item, quote=True)}</li>" for item in highlights
    )

    # Render the final post using the template.
    return FORUM_POST_FORMAT.format(
        title=escaped_subject,
        body=escaped_body,
        list_items=list_items
    )