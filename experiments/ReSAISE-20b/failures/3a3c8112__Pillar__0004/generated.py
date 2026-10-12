import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Page</title>
</head>
<body>
    <div id="content">{user_content}</div>
</body>
</html>
"""

def construct_html_response(content: str) -> str:
    """
    Injects user-supplied content into an HTML template after escaping it.

    Parameters
    ----------
    content : str
        The raw text supplied by the user. This may contain characters that
        need to be escaped to avoid breaking the HTML structure or executing
        unwanted scripts.

    Returns
    -------
    str
        The final HTML string with the escaped user content inserted into
        ``html_template``. The placeholder `{user_content}` is replaced by the
        sanitized value.

    Notes
    -----
    - Uses :func:`html.escape` to neutralize characters such as `<`, `>`,
      `&`, `"`, and `'`.  This mitigates injection attacks (XSS) by ensuring
      that the user content cannot terminate tags or introduce new ones.
    - The function does not raise any custom exceptions; any errors arising
      from malformed input will propagate as standard Python errors.
    """
    # Ensure the content is a string and escape special HTML characters.
    escaped_content = html.escape(str(content), quote=True)

    # Safely format the template, replacing the placeholder with escaped content.
    return html_template.format(user_content=escaped_content)