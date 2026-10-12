import html

# Base HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Visitor Page</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_response(visitor_content: str) -> str:
    """
    Construct an HTML response embedding the user-provided content in a safe manner.

    Parameters
    ----------
    visitor_content : str
        The raw string supplied by the user that should appear inside the page.

    Returns
    -------
    str
        The full HTML document with the user content safely escaped.
    """
    # Escape special characters to prevent HTML injection (CWE-74).
    safe_content = html.escape(visitor_content, quote=True)

    # Render the template with the escaped content.
    return html_template.format(user_content=safe_content)