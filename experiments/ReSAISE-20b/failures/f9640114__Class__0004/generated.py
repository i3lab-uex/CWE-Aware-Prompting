import html

# Example template; replace with the actual format used by your forum system.
FORUM_POST_FORMAT = """
<h1>{header}</h1>
<div class="post-body">
{message}
</div>
<ul class="options-list">
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
        A collection of user-provided options or discussion points in markdown format.

    Returns
    -------
    str
        A string containing the sanitized and formatted forum post, including the header,
        message, and safely rendered options.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    """
    # Basic type checks
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(post_body, str):
        raise TypeError("post_body must be a string")
    if not isinstance(options_list, list) or not all(isinstance(opt, str) for opt in options_list):
        raise TypeError("options_list must be a list of strings")

    # Escape all user input to neutralize special HTML characters
    escaped_title = html.escape(title, quote=True)
    escaped_body = html.escape(post_body, quote=True)

    # Build the unordered list of options
    escaped_options = []
    for opt in options_list:
        # Convert markdown to plain text by escaping HTML; no actual markdown rendering
        escaped_opt = html.escape(opt, quote=True)
        escaped_options.append(f"  <li>{escaped_opt}</li>")
    options_html = "\n".join(escaped_options)

    # Populate the template
    formatted_post = FORUM_POST_FORMAT.format(
        header=escaped_title,
        message=escaped_body.replace("\n", "<br>"),
        options=options_html
    )

    return formatted_post.strip()