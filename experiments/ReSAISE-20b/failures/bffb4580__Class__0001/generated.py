import html

# Example HTML template with a placeholder for user content.
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
    Construct an HTML page embedding the user-provided input safely.

    Parameters
    ----------
    client_input : str
        Content supplied by the user that will be inserted into the page.

    Returns
    -------
    str
        The full HTML page with the escaped user content.
    """
    # Escape special characters to neutralize potential injection
    safe_input = html.escape(client_input, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_input)