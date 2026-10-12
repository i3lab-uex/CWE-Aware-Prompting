import html

# Base HTML template with a placeholder for user-provided content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe User Page</title>
</head>
<body>
    <h1>User Content</h1>
    <div>{user_content}</div>
</body>
</html>
"""

def render_html_output(user_input: str) -> str:
    """
    Construct a safe HTML page that embeds the provided user input.

    Parameters
    ----------
    user_input : str
        Content supplied by a user. It may contain characters that need escaping.

    Returns
    -------
    str
        A complete HTML document with the user content safely inserted.
    """
    # Escape special characters to prevent XSS or HTML injection.
    safe_content = html.escape(user_input, quote=True)

    # Inject the escaped content into the template.
    return html_template.format(user_content=safe_content)