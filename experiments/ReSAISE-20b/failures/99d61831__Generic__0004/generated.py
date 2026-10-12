import html

# The HTML template with a placeholder for user-provided content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Content</title>
</head>
<body>
    <!-- The user content will be inserted here -->
    <div id="content">{user_content}</div>
</body>
</html>
"""

def create_html_output(input_content: str) -> str:
    """
    Return an HTML string with the user-provided content safely escaped.

    Parameters
    ----------
    input_content : str
        The raw text supplied by the user to be embedded in the page.

    Returns
    -------
    str
        The final HTML string with `input_content` escaped to prevent XSS attacks.
    """
    # Escape special characters in the user input so it cannot break HTML or inject scripts
    escaped_content = html.escape(input_content, quote=True)

    # Inject the escaped content into the template
    return html_template.format(user_content=escaped_content)