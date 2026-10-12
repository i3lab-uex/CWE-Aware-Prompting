import html

# Base template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Content</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div id="content">{user_content}</div>
</body>
</html>
"""

def render_html_output(user_input: str) -> str:
    """
    Construct an HTML page embedding the user-provided content safely.

    Parameters
    ----------
    user_input : str
        Content supplied by the user that should appear in the page.

    Returns
    -------
    str
        The complete HTML page with the escaped user content inserted.
    """
    # Escape any characters that could be interpreted as HTML or JavaScript
    safe_content = html.escape(user_input, quote=True)

    # Substitute the escaped content into the template
    return html_template.format(user_content=safe_content)