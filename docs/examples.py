import restructuredtext_lint
rst = """
Some content.

Hello World
=======
Some more content!
"""
errors = restructuredtext_lint.lint(rst, 'myfile.py')
print 'errors[0].line  #', errors[0].line
print 'errors[0].source  #', errors[0].source
print 'errors[0].level  #', errors[0].level
print 'errors[0].type  #', errors[0].type
print 'errors[0].message  #', errors[0].message
print 'errors[0].full_message  #', errors[0].full_message
