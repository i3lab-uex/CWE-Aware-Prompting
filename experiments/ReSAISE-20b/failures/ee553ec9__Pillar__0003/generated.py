import html

# The HTML template containing a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Message</title>
</head>
<body>
    <div class="user-message">
        {user_content}
    </div>
</body>
</html>
"""

def build_html_output(client_message: str) -> str:
    """
    Create an HTML response by safely inserting user content into a predefined template.

    Parameters
    ----------
    client_message : str
        The raw text contributed by the user. It may contain characters that need to be escaped.

    Returns
    -------
    str
        The final HTML string with the user's content safely embedded.
    """
    # Escape user-provided content to prevent XSS or malformed HTML
    safe_content = html.escape(client_message, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)