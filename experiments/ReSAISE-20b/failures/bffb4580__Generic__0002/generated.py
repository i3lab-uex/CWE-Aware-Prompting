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

def build_html_page(client_input: str) -> str:
    """
    Construct an HTML page embedding the provided user content safely.

    Parameters
    ----------
    client_input : str
        The raw string supplied by the user to be inserted into the page.

    Returns
    -------
    str
        A complete HTML document with the user content safely escaped.
    """
    # Escape any special characters to prevent XSS attacks
    safe_content = html.escape(client_input, quote=True)

    # Render the final page using the template
    return html_template.format(user_content=safe_content)