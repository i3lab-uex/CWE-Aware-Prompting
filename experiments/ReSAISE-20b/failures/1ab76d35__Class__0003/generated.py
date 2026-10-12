import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Content Page</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def generate_html_response(user_content: str) -> str:
    """
    Generates an HTML page embedding the provided user content in a safe manner.

    Parameters
    ----------
    user_content : str
        The raw content supplied by the user that will be inserted into the HTML.

    Returns
    -------
    str
        A fully-formed HTML string with the user content safely escaped.
    """
    # Escape special characters to prevent XSS or HTML injection (CWE-74).
    safe_content = html.escape(user_content, quote=True)
    # Format the template with the escaped content.
    return html_template.format(user_content=safe_content)