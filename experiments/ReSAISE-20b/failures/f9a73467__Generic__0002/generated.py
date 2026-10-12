import html

# Assume this template is defined elsewhere in the environment.
# It should contain three placeholders: {title}, {body} and {points}
FORUM_POST_FORMAT = (
    "<article>"
    "  <h1>{title}</h1>"
    "  <div class=\"post-body\">{body}</div>"
    "  {points}"
    "</article>"
)

def compile_post(subject: str, text: str, highlights: list[str]) -> str:
    """
    Assemble a forum post using the given subject, body text and
    discussion points.

    Parameters
    ----------
    subject : str
        The title or main topic of the forum post.
    text : str
        The primary content or body text of the post.
    highlights : list[str]
        A series of user‑supplied discussion points or options in markdown
        format.

    Returns
    -------
    str
        A fully formatted and sanitized forum post, including a header,
        message body and an unordered list of discussion points.

    Notes
    -----
    All user‑supplied data is escaped using :func:`html.escape` to prevent
    cross‑site scripting (XSS) attacks.  The highlights are rendered as an
    HTML unordered list (<ul>...</ul>) where each point is wrapped in a <li>.
    """

    # Escape all user input to avoid HTML injection
    safe_title = html.escape(subject, quote=True)
    safe_body = html.escape(text, quote=True)

    # Build the list of discussion points
    if highlights:
        list_items = []
        for point in highlights:
            # Escape the markdown text; if you need to support a subset of
            # Markdown, consider adding a lightweight parser here.
            escaped_point = html.escape(point, quote=True)
            list_items.append(f"<li>{escaped_point}</li>")
        points_html = f"\n<ul>\n{''.join(list_items)}\n</ul>"
    else:
        points_html = ""

    # Format the final post using the template
    return FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        points=points_html
    )