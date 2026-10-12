import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Content</title>
</head>
<body>
    <div id="content">{user_content}</div>
</body>
</html>
"""

def create_html_output(input_content: str) -> str:
    """
    Inject user-provided content into an HTML template after proper escaping.

    Parameters
    ----------
    input_content : str
        Dynamic content supplied by the user. It will be escaped to prevent
        HTML injection attacks.

    Returns
    -------
    str
        The complete HTML string with the escaped user content inserted.
    """
    # Escape special characters to neutralize any potential HTML injection
    safe_content = html.escape(input_content, quote=True)

    # Use a safe formatting method; avoid f-strings with unescaped content
    final_html = html_template.format(user_content=safe_content)

    return final_html