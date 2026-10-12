import html

# A minimal but realistic template for a forum post.
FORUM_POST_FORMAT = """
<div class="forum-post">
    <h2>{title}</h2>
    <div class="post-body">{body}</div>
    <ul class="discussion-points">
        {list_items}
    </ul>
</div>
"""

def build_post_html(topic_title: str, body_text: str, list_items: list[str]) -> str:
    """
    Construct a sanitized HTML representation of a forum post.

    Parameters
    ----------
    topic_title : str
        The title or main topic of the forum post.
    body_text : str
        The main body or content of the forum post.
    list_items : list[str]
        A collection of user‑provided discussion points or options.

    Returns
    -------
    str
        The fully formatted and sanitized HTML string for the forum post.

    Notes
    -----
    * All user‑supplied strings are escaped with :func:`html.escape` to
      prevent injection of arbitrary HTML or JavaScript.
    * Each list item is wrapped in a `<li>` element. Empty items are omitted
      to keep the markup clean.
    """
    # Escape title and body text.
    safe_title = html.escape(topic_title, quote=True)
    safe_body = html.escape(body_text, quote=True)

    # Build the list of <li> elements.
    safe_list_items = []
    for item in list_items:
        # Skip empty or whitespace‑only items.
        if not isinstance(item, str) or not item.strip():
            continue
        safe_item = html.escape(item, quote=True)
        safe_list_items.append(f"<li>{safe_item}</li>")

    # Join the list items into a single string.
    list_html = "\n".join(safe_list_items)

    # Render the final HTML using the template.
    rendered = FORUM_POST_FORMAT.format(
        title=safe_title,
        body=safe_body,
        list_items=list_html
    )

    return rendered.strip()