import html

# Predefined format for a forum post.
# Placeholders: {header}, {body}, {options}
FORUM_POST_FORMAT = (
    "<div class='forum-post'>\n"
    "  <h2>{header}</h2>\n"
    "  <div class='post-body'>\n{body}\n  </div>\n"
    "  <div class='post-options'>\n{options}\n  </div>\n"
    "</div>"
)

def build_forum_post(title: str, post_body: str, options_list: list[str]) -> str:
    """
    Construct a sanitized and formatted forum post.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    post_body : str
        The main content or body of the forum post. May contain Markdown.
    options_list : list[str]
        A collection of user‑provided options or discussion points in Markdown.

    Returns
    -------
    str
        The fully rendered forum post as an HTML string.
    """
    # Escape user content to avoid XSS or unintended markup
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Build an unordered list for options
    list_items = []
    for opt in options_list:
        # Escape each option and wrap in <li>
        escaped_opt = html.escape(opt, quote=True)
        list_items.append(f"    <li>{escaped_opt}</li>")
    safe_options = "<ul>\n" + "\n".join(list_items) + "\n  </ul>" if list_items else ""

    # Format the final post using the predefined template
    return FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body,
        options=safe_options
    )