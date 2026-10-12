import html

# Default forum post template.  Placeholders:
# {title}   – the title of the post
# {body}    – the main body/content
# {list}    – the discussion points as an unordered list (<ul>)
FORUM_POST_FORMAT = """
<article class="forum-post">
  <h1>{title}</h1>
  <div class="post-body">{body}</div>
  {list}
</article>
"""

def build_post_html(topic_title: str, body_text: str, list_items: list[str]) -> str:
    """
    Build a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main body/content of the forum post.
    list_items : list[str]
        A collection of user‑provided discussion points or options in markdown
        format.  The function treats them as plain text and escapes any HTML
        characters to prevent XSS.

    Returns
    -------
    str
        A fully formatted and sanitized HTML string containing the title,
        body, and discussion points as an unordered list.

    Raises
    ------
    ValueError
        If any argument is not of the expected type.
    """
    # Basic type checks to avoid accidental injection
    if not isinstance(topic_title, str):
        raise ValueError("topic_title must be a string")
    if not isinstance(body_text, str):
        raise ValueError("body_text must be a string")
    if not isinstance(list_items, list):
        raise ValueError("list_items must be a list of strings")
    if not all(isinstance(item, str) for item in list_items):
        raise ValueError("All elements of list_items must be strings")

    # Escape user input to neutralize potential XSS vectors
    escaped_title = html.escape(topic_title, quote=True)
    escaped_body = html.escape(body_text, quote=True)

    # Build the list of discussion points
    if list_items:
        escaped_list_items = [
            f"<li>{html.escape(item, quote=True)}</li>" for item in list_items
        ]
        ul_content = "<ul>\n" + "\n".join(escaped_list_items) + "\n</ul>"
    else:
        ul_content = ""

    # Format the final HTML
    post_html = FORUM_POST_FORMAT.format(
        title=escaped_title,
        body=escaped_body,
        list=ul_content
    )

    return post_html.strip()