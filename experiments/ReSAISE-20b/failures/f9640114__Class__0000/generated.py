import html

# Predefined template for forum posts.
FORUM_POST_FORMAT = """
<h1>{header}</h1>
<div class="post-body">{body}</div>
<ul class="options">
{options}
</ul>
"""

def build_forum_post(title: str, post_body: str, options_list: list[str]) -> str:
    """
    Construct a sanitized forum post.

    Parameters
    ----------
    title : str
        The title or subject line of the forum post.
    post_body : str
        The main content or body of the forum post.
    options_list : list[str]
        A collection of user‑provided options or discussion points in markdown format.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post, including the header,
        message, and safely rendered options.
    """
    # Escape HTML special characters to prevent injection (CWE‑74).
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Render each option as a list item. Each option is escaped individually.
    safe_options = "\n".join(
        f"  <li>{html.escape(option, quote=True)}</li>" for option in options_list
    )

    # Fill the template with sanitized content.
    return FORUM_POST_FORMAT.format(
        header=safe_title,
        body=safe_body,
        options=safe_options
    )