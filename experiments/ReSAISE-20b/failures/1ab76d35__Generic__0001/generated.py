import html

def generate_html_response(user_content: str) -> str:
    """
    Generate an HTML page by embedding the provided user content into a template.

    Parameters
    ----------
    user_content : str
        The raw content supplied by the user that will be inserted into the page.

    Returns
    -------
    str
        A complete HTML document with the user content safely escaped.
    """
    # Basic HTML template with a placeholder for user content
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Content Page</title>
    <style>
        body {font-family: Arial, sans-serif; margin: 2rem;}
    </style>
</head>
<body>
    <h1>Your Content</h1>
    <div>{user_content}</div>
</body>
</html>"""

    # Escape the user content to prevent XSS attacks
    safe_content = html.escape(user_content)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)