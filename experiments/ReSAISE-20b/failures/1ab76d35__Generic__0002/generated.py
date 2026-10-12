import html

# Example template – in practice this could be loaded from a file or defined elsewhere.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Generated Page</title>
</head>
<body>
    <h1>User Content</h1>
    <div>{user_content}</div>
</body>
</html>
"""

def generate_html_response(user_content: str) -> str:
    """
    Generate an HTML page by safely embedding user-provided content.

    Parameters
    ----------
    user_content : str
        Raw text supplied by the user that should be displayed on the page.

    Returns
    -------
    str
        The full HTML document with `user_content` safely escaped.

    Notes
    -----
    - Uses ``html.escape`` to prevent XSS attacks by converting special characters
      (e.g., <, >, &, ", ') into their corresponding HTML entities.
    - No exceptions are raised by this function; any errors would arise from
      the underlying ``html.escape`` implementation.
    """
    safe_content = html.escape(user_content, quote=True)
    return html_template.format(user_content=safe_content)