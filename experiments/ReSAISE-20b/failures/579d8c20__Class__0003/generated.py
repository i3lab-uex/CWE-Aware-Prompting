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
    Construct an HTML page that safely embeds user-provided content.

    Parameters
    ----------
    visitor_content : str
        The string supplied by the user to be displayed in the page.

    Returns
    -------
    str
        The complete HTML document with the user content safely escaped.
    """
    # Escape special characters to prevent injection (CWE-74).
    safe_content = html.escape(visitor_content, quote=True)

    # Insert the escaped content into the template.
    return html_template.format(user_content=safe_content)