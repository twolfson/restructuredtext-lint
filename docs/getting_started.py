import restructuredtext_lint
errors = restructuredtext_lint.lint("""
Hello World
=======
""")
print errors
print errors[0].message
