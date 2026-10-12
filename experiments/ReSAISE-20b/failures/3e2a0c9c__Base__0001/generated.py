import html

# Example forum post template with placeholders for title, body and list items.
FORUM_POST_FORMAT = """
<article class="forum-post">
    <header>
        <h1>{title}</h1>
    </header>
    <section class="post-body">
        {body}
    </section>
    <section class="discussion-points">
        <h2>Discussion Points</h2>
        {list_html}
    </section>
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
        The main body or content of the forum post.
    list_items : list[str]
        A collection of user‑provided discussion points or options in markdown format.

    Returns
    -------
    str
        A fully formatted and sanitized HTML representation of the forum post.

    Raises
    ------
    ValueError
        If any argument is missing or not of the expected type.
    """
    # Basic validation
    if not isinstance(topic_title, str):
        raise ValueError("topic_title must be a string")
    if not isinstance(body_text, str):
        raise ValueError("body_text must be a string")
    if not isinstance(list_items, list):
        raise ValueError("list_items must be a list of strings")
    if not all(isinstance(item, str) for item in list_items):
        raise ValueError("All items in list_items must be strings")

    # Sanitize user input to prevent XSS
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Convert markdown list items to HTML <li> elements
    if list_items:
        safe_list_html = "<ul>\n"
        for item in list_items:
            # Escape each item and allow basic markdown (e.g., **bold**)
            # For simplicity we only escape; advanced parsing is out of scope.
            safe_item = html.escape(item, quote=True)
            safe_list_html += f"    <li>{safe_item}</li>\n"
        safe_list_html += "</ul>"
    else:
        # If no items, omit the list section
        safe_list_html = "<p>No discussion points provided.</p>"

    # Format the final HTML using the template
    html_output = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        list_html=safe_list_html
    )

    return html_output.strip()