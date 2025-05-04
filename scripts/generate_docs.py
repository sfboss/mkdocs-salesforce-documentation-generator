#!/usr/bin/env python3
"""
Salesforce Documentation CLI

This script provides a command-line interface for generating Salesforce documentation.
It calls the SalesforceDocGenerator class to do the actual work.

Usage:
    python generate_docs.py --username your_username --password your_password --token your_token
"""

import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Add the scripts directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

# Import our documentation generator
from scripts.salesforce_docs_generator import SalesforceDocGenerator


def main():
    """Main entry point for the documentation CLI"""
    # Load environment variables from .env file if it exists
    load_dotenv()

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Generate Salesforce org documentation"
    )

    # Authentication options
    parser.add_argument("--username", help="Salesforce username")
    parser.add_argument("--password", help="Salesforce password")
    parser.add_argument("--token", help="Salesforce security token")
    parser.add_argument(
        "--domain", default="login", help="Salesforce domain (default: login)"
    )

    # Documentation options
    parser.add_argument(
        "--template-dir",
        default="templates",
        help="Directory containing templates (default: templates)",
    )
    parser.add_argument(
        "--output-dir",
        default="docs/data-model/objects",
        help="Directory to save documentation (default: docs/data-model/objects)",
    )

    # Object filter options
    parser.add_argument("--object", help="Document a specific object")
    parser.add_argument(
        "--standard", action="store_true", help="Document standard objects only"
    )
    parser.add_argument(
        "--custom", action="store_true", help="Document custom objects only"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Get credentials from environment variables if not provided as arguments
    username = args.username or os.environ.get("SALESFORCE_USERNAME")
    password = args.password or os.environ.get("SALESFORCE_PASSWORD")
    token = args.token or os.environ.get("SALESFORCE_TOKEN")

    # Check if credentials are available
    if not (username and password):
        print("Error: Salesforce credentials are required.")
        print("Provide them as command-line arguments or in a .env file.")
        print("Example .env file:")
        print("SALESFORCE_USERNAME=your.username@example.com")
        print("SALESFORCE_PASSWORD=your_password")
        print("SALESFORCE_TOKEN=your_security_token")
        sys.exit(1)

    print(
        f"Starting documentation generation at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print(f"Connecting to Salesforce as: {username}")

    try:
        # Initialize the doc generator
        doc_generator = SalesforceDocGenerator(
            username=username,
            password=password,
            security_token=token,
            domain=args.domain,
            template_dir=args.template_dir,
        )

        # Generate documentation based on arguments
        if args.object:
            print(f"Generating documentation for {args.object}...")
            output_path = os.path.join(args.output_dir, f"{args.object.lower()}.md")
            doc_generator.generate_object_documentation(args.object, output_path)
            print(f"Documentation for {args.object} saved to {output_path}")
        elif args.standard:
            print("Generating documentation for standard objects...")
            objects = doc_generator.generate_standard_objects_documentation(
                args.output_dir
            )
            print(f"Documented {len(objects)} standard objects")
        elif args.custom:
            print("Generating documentation for custom objects...")
            objects = doc_generator.generate_custom_objects_documentation(
                args.output_dir
            )
            print(f"Documented {len(objects)} custom objects")
        else:
            print("Generating documentation for all objects...")
            std_objects = doc_generator.generate_standard_objects_documentation(
                args.output_dir
            )
            custom_objects = doc_generator.generate_custom_objects_documentation(
                args.output_dir
            )
            print(
                f"Documented {len(std_objects)} standard objects and {len(custom_objects)} custom objects"
            )

        print(
            f"Documentation generation completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print(f"Documentation saved to: {args.output_dir}")
        print("Run 'mkdocs serve' to view the documentation.")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
