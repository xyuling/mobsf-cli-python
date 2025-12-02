"""Command-line argument parser."""

import argparse
import sys


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser.
    
    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        prog="mobsf-cli",
        description="mobsf-cli app - CLI wrapper for Mobile Security Framework (MobSF) REST API",
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    
    # Global options
    parser.add_argument(
        "-a",
        dest="api_key",
        metavar="API_KEY",
        help="Api key/token (overrides MOBSF_API_KEY env)",
    )
    
    parser.add_argument(
        "-s",
        dest="server",
        metavar="SERVER",
        help="Server, example: http://localhost:8000 (overrides MOBSF_SERVER env)",
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.required = True
    
    # Upload command
    upload_parser = subparsers.add_parser(
        "upload",
        help="Upload a file.",
    )
    upload_parser.add_argument(
        "file_path",
        help="Path to file to upload",
    )
    
    # Scan command
    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan a file.",
    )
    scan_parser.add_argument(
        "scan_type",
        choices=["xapk", "apk", "zip", "ipa", "appx"],
        help="Scan type",
    )
    scan_parser.add_argument(
        "file_name",
        help="File name",
    )
    scan_parser.add_argument(
        "file_hash",
        help="File hash",
    )
    scan_parser.add_argument(
        "-r",
        dest="re_scan",
        action="store_true",
        help="Rescan a file",
    )
    
    # Scans command
    subparsers.add_parser(
        "scans",
        help="Display recent scans.",
    )
    
    # Report command
    report_parser = subparsers.add_parser(
        "report",
        help="Get report.",
    )
    report_subparsers = report_parser.add_subparsers(
        dest="report_type",
        help="Report format",
    )
    report_subparsers.required = True
    
    # PDF report
    pdf_parser = report_subparsers.add_parser(
        "pdf",
        help="PDF report format",
    )
    pdf_parser.add_argument(
        "file_hash",
        help="File hash",
    )
    pdf_parser.add_argument(
        "-o",
        dest="output_file_path",
        default="report.pdf",
        help="File path to save a report (default: report.pdf)",
    )
    
    # JSON report
    json_parser = report_subparsers.add_parser(
        "json",
        help="JSON report format",
    )
    json_parser.add_argument(
        "file_hash",
        help="File hash",
    )
    json_parser.add_argument(
        "-o",
        dest="output_file_path",
        default="report.json",
        help="File path to save a report (default: report.json)",
    )
    json_parser.add_argument(
        "-p",
        dest="stdout_output",
        action="store_true",
        help="Print to stdout instead of saving a file",
    )
    
    # Delete command
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete scan.",
    )
    delete_parser.add_argument(
        "file_hash",
        help="File hash",
    )
    
    # Play command
    play_parser = subparsers.add_parser(
        "play",
        help="Upload a file and auto start scan.",
    )
    play_parser.add_argument(
        "file_path",
        help="Path to file to upload",
    )
    play_parser.add_argument(
        "-r",
        dest="re_scan",
        action="store_true",
        help="Rescan a file",
    )
    
    # CI command
    ci_parser = subparsers.add_parser(
        "ci",
        help="For CI/CD stages. Upload a file, auto start scan, save reports, check scores.",
    )
    ci_parser.add_argument(
        "file_path",
        help="Path to file to upload",
    )
    ci_parser.add_argument(
        "-p",
        dest="path_to_save",
        required=True,
        help="Path to directory to save reports (pdf and json).",
    )
    ci_parser.add_argument(
        "-r",
        dest="re_scan",
        action="store_true",
        help="Rescan a file",
    )
    ci_parser.add_argument(
        "-c",
        dest="cvss",
        type=float,
        default=3.9,
        help="Above this score rise a cvss error. 0.0-10.0 (default: 3.9)",
    )
    ci_parser.add_argument(
        "-t",
        dest="trackers",
        type=int,
        default=0,
        help="Above this score rise a trackers error. 0-407 (default: 0)",
    )
    ci_parser.add_argument(
        "-u",
        dest="security",
        type=int,
        default=71,
        help="Below this score rise a security error. 0-100 (default: 71)",
    )
    
    # Source command
    source_parser = subparsers.add_parser(
        "source",
        help="View source files.",
    )
    source_parser.add_argument(
        "scan_type",
        choices=["apk", "ipa", "studio", "eclipse", "ios"],
        help="Scan type",
    )
    source_parser.add_argument(
        "file_path",
        help="Relative file path",
    )
    source_parser.add_argument(
        "file_hash",
        help="File hash",
    )
    
    return parser


def parse_args(args=None):
    """Parse command-line arguments.
    
    Args:
        args: Arguments to parse (default: sys.argv)
        
    Returns:
        Parsed arguments
    """
    parser = create_parser()
    
    # If no arguments provided, print help
    if args is None and len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    return parser.parse_args(args)
