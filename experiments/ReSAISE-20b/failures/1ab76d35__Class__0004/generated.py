import html

# Define a simple HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Response</title>
</head>
<body>
    <h1>User Response</h1>
    <div>{user_content}</div>
</body>
</html>
"""

def generate_html_response(user_content: str) -> str:
    """
    Generates an HTML page by safely embedding the provided user content.

    Parameters
    ----------
    user_content : str
        The raw content supplied by the user that should appear in the page.

    Returns
    -------
    str
        A complete HTML document with the user content safely escaped.
    """
    # Escape special HTML characters to prevent injection attacks (CWE-74).
    safe_content = html.escape(user_content, quote=True)
    return html_template.format(user_content=safe_content)