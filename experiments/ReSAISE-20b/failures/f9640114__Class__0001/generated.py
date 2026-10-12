import html

# Predefined format for a forum post.
FORUM_POST_FORMAT = """<div class="forum-post">
  <h2>{header}</h2>
  <p>{message}</p>
  {options}
</div>"""

def build_forum_post(title: str, post_body: str, options_list: list[str]) -> str:
    """
    Construct a safe, formatted forum post.

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
        message, and safely rendered options as an HTML unordered list.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    """
    # Input validation
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not isinstance(post_body, str):
        raise TypeError("post_body must be a string")
    if not isinstance(options_list, list):
        raise TypeError("options_list must be a list of strings")
    if not all(isinstance(opt, str) for opt in options_list):
        raise TypeError("all items in options_list must be strings")

    # Escape user input to prevent HTML injection
    safe_title = html.escape(title, quote=True)
    safe_body = html.escape(post_body, quote=True)

    # Build the options list as an HTML <ul>
    if options_list:
        safe_options = ['<li>{}</li>'.format(html.escape(opt, quote=True)) for opt in options_list]
        options_html = '<ul>\n' + '\n'.join(safe_options) + '\n</ul>'
    else:
        options_html = ''  # No options provided

    # Populate the template
    post = FORUM_POST_FORMAT.format(
        header=safe_title,
        message=safe_body,
        options=options_html
    )
    return post