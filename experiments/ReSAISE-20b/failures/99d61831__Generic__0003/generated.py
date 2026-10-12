import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Output</title>
</head>
<body>
    <div class="content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_output(input_content: str) -> str:
    """
    Inject user-supplied content into an HTML template after escaping it.

    Parameters
    ----------
    input_content : str
        The dynamic content provided by the user. It will be escaped to prevent XSS.

    Returns
    -------
    str
        The final HTML string with the escaped user content inserted.
    """
    # Escape special HTML characters to prevent injection attacks.
    safe_content = html.escape(input_content, quote=True)

    # Format the template with the escaped content.
    return html_template.format(user_content=safe_content)