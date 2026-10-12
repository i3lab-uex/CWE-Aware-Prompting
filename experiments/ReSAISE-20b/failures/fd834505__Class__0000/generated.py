import html

# Base HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Page</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def render_html_output(user_input: str) -> str:
    """
    Construct a safe HTML page embedding the user-provided content.

    Parameters
    ----------
    user_input : str
        The raw string supplied by the user that should be displayed in the page.

    Returns
    -------
    str
        A complete HTML document with the user content safely escaped.
    """
    # Escape special HTML characters to prevent injection (CWE-74).
    safe_content = html.escape(user_input, quote=True)

    # Format the template with the escaped content.
    return html_template.format(user_content=safe_content)