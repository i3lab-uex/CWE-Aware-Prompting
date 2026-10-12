import html

def generate_html_response(user_content: str) -> str:
    """
    Generate an HTML page by embedding user-provided content into a template.

    Parameters
    ----------
    user_content : str
        The raw content supplied by the user that will be inserted into the page.

    Returns
    -------
    str
        A complete HTML document with the user content safely escaped to prevent XSS.
    """
    # Basic HTML template with a placeholder for the user content
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>User Content</title>
</head>
<body>
<h1>Welcome!</h1>
<div id="user-content">{user_content}</div>
</body>
</html>"""

    # Escape the user content to neutralize any HTML or script injection
    safe_content = html.escape(user_content, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)