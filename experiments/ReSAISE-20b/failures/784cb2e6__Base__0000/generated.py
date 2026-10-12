import html

# Predefined template for the forum post.
FORUM_POST_FORMAT = """<h1>{header}</h1>
<div>{message}</div>
<ul>
{options}
</ul>"""

def create_forum_post(title: str, body: str, topics: list[str]) -> str:
    """
    Construct a sanitized forum post from user-provided content.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    body : str
        The main content or body of the forum post.
    topics : list[str]
        A collection of user-provided options or discussion points in markdown format.

    Returns
    -------
    str
        A sanitized and formatted forum post string suitable for HTML rendering.

    Notes
    -----
    * All user input is escaped using html.escape to prevent XSS (CWE‑79).
    * Markdown formatting inside topics is preserved only as plain text; no
      rendering of markdown to HTML is performed.
    """
    # Sanitize title and body
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(body, quote=True)

    # Build the list of options
    escaped_topics = [html.escape(t.strip(), quote=True) for t in topics]
    options_html = "\n".join(f"<li>{t}</li>" for t in escaped_topics)

    # Assemble the final post
    return FORUM_POST_FORMAT.format(
        header=safe_title,
        message=safe_body,
        options=options_html
    )