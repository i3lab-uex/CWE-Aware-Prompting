import html

# Predefined format for a forum post.
FORUM_POST_FORMAT = """<div class="forum-post">
  <h2>{header}</h2>
  <div class="post-body">{body}</div>
  {options}
</div>"""

def build_forum_post(title: str, post_body: str, options_list: list[str]) -> str:
    """
    Construct a sanitized forum post containing a title, body, and an unordered list of options.

    Args:
        title (str): The forum post title.
        post_body (str): The main content of the post.
        options_list (list[str]): A list of user-provided discussion points in markdown format.

    Returns:
        str: The fully formatted and HTML‑escaped forum post string.
    """
    # Escape user input to prevent XSS
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Build the <ul> list from options
    if options_list:
        ul_items = []
        for option in options_list:
            # Escape each option; no markdown rendering to keep it safe
            escaped_option = html.escape(option, quote=True)
            ul_items.append(f"<li>{escaped_option}</li>")
        options_html = "<ul>\n" + "\n".join(ul_items) + "\n</ul>"
    else:
        options_html = ""

    # Format the final post
    return FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body,
        options=options_html
    )