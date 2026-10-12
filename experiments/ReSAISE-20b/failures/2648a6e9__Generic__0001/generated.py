import html

# Example HTML template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Submission</title>
</head>
<body>
    <h1>Welcome!</h1>
    <div class="user-content">
        {user_content}
    </div>
</body>
</html>
"""

def create_html_output(input_text: str) -> str:
    """
    Safely embed user-provided text into the predefined HTML template.

    Parameters
    ----------
    input_text : str
        The raw content supplied by the user.

    Returns
    -------
    str
        A complete HTML document with the user's content inserted in place of
        `{user_content}`.
    """
    # Escape any special HTML characters to prevent XSS or malformed markup
    safe_text = html.escape(input_text)

    # Format the template with the escaped user content
    return html_template.format(user_content=safe_text)