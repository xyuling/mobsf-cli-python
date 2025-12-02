"""Main entry point for mobsf-cli."""

import os
import sys
from .arguments import parse_args
from .app import App
from .error import AppError


# Constants
VERSION = "0.1.0"
NAME = "mobsf-cli"
SERVER_DEFAULT = "http://localhost:8000"
API_KEY_DEFAULT = ""


def main():
    """Main entry point."""
    try:
        # Parse arguments
        args = parse_args()
        
        # Get API key and server from environment or arguments
        api_key = os.environ.get("MOBSF_API_KEY", API_KEY_DEFAULT)
        server = os.environ.get("MOBSF_SERVER", SERVER_DEFAULT)
        
        # Override with command-line arguments if provided
        if args.api_key:
            api_key = args.api_key
        if args.server:
            server = args.server
        
        # Initialize app
        app = App(api_key, server)
        
        # Execute command
        execute(app, args)
        
    except AppError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def execute(app: App, args):
    """Execute the command based on parsed arguments.
    
    Args:
        app: Application instance
        args: Parsed arguments
    """
    command = args.command
    
    if command == "upload":
        app.upload_file(args.file_path)
    
    elif command == "scan":
        app.scan(
            args.scan_type,
            args.file_name,
            args.file_hash,
            args.re_scan,
        )
    
    elif command == "scans":
        app.scans()
    
    elif command == "report":
        report_type = args.report_type
        
        if report_type == "pdf":
            app.report_pdf(args.file_hash, args.output_file_path)
        
        elif report_type == "json":
            if args.stdout_output:
                app.print_report_json(args.file_hash)
            else:
                app.write_report_json(args.file_hash, args.output_file_path)
    
    elif command == "delete":
        app.delete_scan(args.file_hash)
    
    elif command == "play":
        app.play(args.file_path, args.re_scan)
    
    elif command == "ci":
        app.ci(
            args.file_path,
            args.re_scan,
            args.path_to_save,
            args.cvss,
            args.trackers,
            args.security,
        )
    
    elif command == "source":
        app.view_source(args.scan_type, args.file_path, args.file_hash)


if __name__ == "__main__":
    main()
