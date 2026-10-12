import html

# Example template with a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Safe Response</title>
</head>
<body>
    <div id="content">
        {user_content}
    </div>
</body>
</html>
"""

def generate_html_response(user_content: str) -> str:
    """
    Generates an HTML response by safely embedding user-provided content into a template.

    Parameters
    ----------
    user_content : str
        The raw text supplied by the user. This string may contain characters that need to be escaped
        to prevent injection of malicious HTML or scripts.

    Returns
    -------
    str
        A fully-formed HTML document with the escaped user content inserted into the template.
    """
    # Escape all special characters to neutralize any potential HTML/JS injection.
    safe_content = html.escape(user_content, quote=True)

    # Insert the escaped content into the template.
    return html_template.format(user_content=safe_content)