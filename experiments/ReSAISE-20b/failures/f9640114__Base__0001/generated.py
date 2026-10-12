import html

# Template for the forum post: placeholders are {header}, {body}, and {options}
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
        Title or subject line of the forum post.
    post_body : str
        Main content or body of the forum post.
    options_list : list[str]
        Collection of user‑provided options or discussion points in markdown format.

    Returns
    -------
    str
        A fully rendered forum post with HTML escaping to prevent XSS.
    """
    # Escape user input to neutralize any malicious scripts
    escaped_title = html.escape(title, quote=True)
    escaped_body = html.escape(post_body, quote=True)

    # Convert each option into a safe <li> element
    escaped_options = []
    for opt in options_list:
        # Escape the markdown content itself; further processing (e.g., Markdown to HTML)
        # should be done by a trusted library if needed.
        escaped_opt = html.escape(opt, quote=True)
        escaped_options.append(f"  <li>{escaped_opt}</li>")

    options_html = "\n".join(escaped_options)

    # Render the final post using the predefined template
    return FORUM_POST_FORMAT.format(
        header=escaped_title,
        body=escaped_body,
        options=options_html
    )