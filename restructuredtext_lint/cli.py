def _main(filepath, stream=print):
    pass

def main():
    # Set up options and parse arguments
    parser = argparse.ArgumentParser(description='Lint a reStructuredText file')
    parser.add_argument('filepath', type=str, help='File to lint')
    args = parser.parse_args()

    # Lint the file
    with open(args.filepath) as f:
        # Read and lin the file
        content = f.read()
        errors = lint(content, args.filepath)

        # If there were no errors, exit gracefully
        if not errors:
            print 'File was clean.'
            sys.exit(0)

        # Otherwise, output the errors as JSON
        error_dicts = [{
            'line': error.line,
            'source': error.source,
            'level': error.level,
            'type': error.type,
            'message': error.message,
            'full_message': error.full_message,
        } for error in errors]
        print json.dumps(error_dicts)

        sys.exit(1)
