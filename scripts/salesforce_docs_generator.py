#!/usr/bin/env python3
"""
Salesforce Documentation Generator

This script connects to Salesforce, extracts metadata about objects, fields, and other components,
and generates markdown documentation using Jinja2 templates.

Usage:
    python salesforce_docs_generator.py --username your_username --password your_password --token your_token

    # To document specific objects
    python salesforce_docs_generator.py --username your_username --password your_password --token your_token --object Account

    # To document standard objects only
    python salesforce_docs_generator.py --username your_username --password your_password --token your_token --standard

    # To document custom objects only
    python salesforce_docs_generator.py --username your_username --password your_password --token your_token --custom
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from simple_salesforce import Salesforce

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SalesforceDocGenerator:
    """Main class for generating Salesforce documentation"""

    def __init__(
        self,
        username=None,
        password=None,
        security_token=None,
        domain="login",
        template_dir="templates",
    ):
        """
        Initialize the documentation generator

        Args:
            username (str): Salesforce username
            password (str): Salesforce password
            security_token (str): Salesforce security token
            domain (str): Salesforce login domain (default: login)
            template_dir (str): Directory containing Jinja2 templates
        """
        self.sf = None
        self.template_dir = template_dir

        # Connect to Salesforce if credentials are provided
        if username and password:
            try:
                self.sf = Salesforce(
                    username=username,
                    password=password,
                    security_token=security_token,
                    domain=domain,
                )
                logger.info(f"Successfully connected to Salesforce as {username}")
            except Exception as e:
                logger.error(f"Failed to connect to Salesforce: {str(e)}")
                raise

        # Set up Jinja2 environment
        try:
            self.env = Environment(loader=FileSystemLoader(template_dir))
            logger.info(f"Jinja2 environment set up with templates from {template_dir}")
        except Exception as e:
            logger.error(f"Failed to set up Jinja2 environment: {str(e)}")
            raise

    def get_template(self, template_name):
        """
        Get a Jinja2 template by name

        Args:
            template_name (str): Name of the template file

        Returns:
            jinja2.Template: Loaded template
        """
        try:
            template = self.env.get_template(template_name)
            return template
        except Exception as e:
            logger.error(f"Failed to load template {template_name}: {str(e)}")
            raise

    def get_object_metadata(self, object_name):
        """
        Get metadata for a specific Salesforce object

        Args:
            object_name (str): API name of the Salesforce object

        Returns:
            dict: Object metadata
        """
        if not self.sf:
            logger.error("Not connected to Salesforce")
            return None

        try:
            # Get object description
            obj_desc = getattr(self.sf, object_name).describe()

            # Basic object info
            metadata = {
                "label": obj_desc["label"],
                "api_name": obj_desc["name"],
                "plural_label": obj_desc["labelPlural"],
                "custom": obj_desc["custom"],
                "description": obj_desc.get("description", "No description available"),
                "sharing_model": obj_desc.get("sharingModel", "Unknown"),
                "searchable": obj_desc.get("searchable", False),
                "deletable": obj_desc.get("deletable", False),
                "feed_enabled": obj_desc.get("feedEnabled", False),
                "fields": [],
                "relationships": {"child_relationships": [], "reference_fields": []},
                "record_types": [],
                "validation_rules": [],
                "permissions": [],
            }

            # Add fields
            for field in obj_desc["fields"]:
                field_data = {
                    "label": field["label"],
                    "api_name": field["name"],
                    "type": field["type"],
                    "required": not field["nillable"],
                    "description": field.get("description", ""),
                }
                metadata["fields"].append(field_data)

                # If it's a reference field, add to relationships
                if field["type"] == "reference" and field.get("referenceTo"):
                    ref_data = {
                        "label": field["label"],
                        "api_name": field["name"],
                        "reference_to": ", ".join(field["referenceTo"]),
                        "description": field.get("description", ""),
                    }
                    metadata["relationships"]["reference_fields"].append(ref_data)

            # Add child relationships
            for rel in obj_desc.get("childRelationships", []):
                if rel.get("childSObject") and rel.get("field"):
                    rel_data = {
                        "label": rel.get("childSObject"),
                        "api_name": rel.get("field"),
                        "description": f"Child relationship from {rel.get('childSObject')}",
                    }
                    metadata["relationships"]["child_relationships"].append(rel_data)

            # Get record types
            try:
                query = f"SELECT Id, Name, DeveloperName, Description, IsActive FROM RecordType WHERE SObjectType = '{object_name}'"
                record_types = self.sf.query(query)

                for rt in record_types.get("records", []):
                    rt_data = {
                        "label": rt.get("Name"),
                        "api_name": rt.get("DeveloperName"),
                        "active": rt.get("IsActive", False),
                        "description": rt.get("Description", ""),
                    }
                    metadata["record_types"].append(rt_data)
            except Exception as e:
                logger.warning(
                    f"Failed to get record types for {object_name}: {str(e)}"
                )

            # Get validation rules
            try:
                # Using tooling API to get validation rules
                query = f"SELECT Id, ValidationName, Active, Description, ErrorMessage FROM ValidationRule WHERE EntityDefinition.QualifiedApiName = '{object_name}'"
                validation_rules = self.sf.tooling.query(query)

                for vr in validation_rules.get("records", []):
                    vr_data = {
                        "label": vr.get("ValidationName"),
                        "api_name": vr.get("ValidationName"),
                        "active": vr.get("Active", False),
                        "description": vr.get("Description", ""),
                        "error_message": vr.get("ErrorMessage", ""),
                    }
                    metadata["validation_rules"].append(vr_data)
            except Exception as e:
                logger.warning(
                    f"Failed to get validation rules for {object_name}: {str(e)}"
                )

            return metadata

        except Exception as e:
            logger.error(f"Error getting metadata for {object_name}: {str(e)}")
            return None

    def generate_object_documentation(
        self, object_name, output_path=None, template_name="object_documentation.j2"
    ):
        """
        Generate documentation for a specific Salesforce object

        Args:
            object_name (str): API name of the Salesforce object
            output_path (str, optional): Path to save the documentation
            template_name (str): Name of the template to use

        Returns:
            str: Generated documentation
        """
        if not self.sf:
            logger.error("Not connected to Salesforce")
            return None

        try:
            # Get object metadata
            metadata = self.get_object_metadata(object_name)
            if not metadata:
                logger.error(f"Failed to get metadata for {object_name}")
                return None

            # Get template
            template = self.get_template(template_name)
            if not template:
                logger.error(f"Failed to get template {template_name}")
                return None

            # Render template
            documentation = template.render(object_data=metadata)

            # Save to file if output path is provided
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "w") as f:
                    f.write(documentation)
                logger.info(f"Documentation for {object_name} saved to {output_path}")

            return documentation

        except Exception as e:
            logger.error(f"Error generating documentation for {object_name}: {str(e)}")
            return None

    def generate_standard_objects_documentation(
        self, output_dir="docs/data-model/objects"
    ):
        """
        Generate documentation for standard Salesforce objects

        Args:
            output_dir (str): Directory to save the documentation

        Returns:
            list: List of objects documented
        """
        if not self.sf:
            logger.error("Not connected to Salesforce")
            return []

        documented_objects = []

        try:
            # Get global describe to list all objects
            describe = self.sf.describe()
            standard_objects = [
                obj["name"] for obj in describe["sobjects"] if not obj["custom"]
            ]

            logger.info(f"Found {len(standard_objects)} standard objects")

            # Generate documentation for each standard object
            for obj_name in standard_objects:
                try:
                    output_path = os.path.join(output_dir, f"{obj_name.lower()}.md")
                    documentation = self.generate_object_documentation(
                        obj_name, output_path
                    )
                    if documentation:
                        documented_objects.append(obj_name)
                except Exception as e:
                    logger.error(f"Error documenting {obj_name}: {str(e)}")

            logger.info(
                f"Generated documentation for {len(documented_objects)} standard objects"
            )

            # Create an index file listing all standard objects
            self._create_object_index(
                documented_objects,
                os.path.join(output_dir, "standard-objects.md"),
                "Standard Objects",
            )

            return documented_objects

        except Exception as e:
            logger.error(f"Error generating standard objects documentation: {str(e)}")
            return []

    def generate_custom_objects_documentation(
        self, output_dir="docs/data-model/objects"
    ):
        """
        Generate documentation for custom Salesforce objects

        Args:
            output_dir (str): Directory to save the documentation

        Returns:
            list: List of objects documented
        """
        if not self.sf:
            logger.error("Not connected to Salesforce")
            return []

        documented_objects = []

        try:
            # Get global describe to list all objects
            describe = self.sf.describe()
            custom_objects = [
                obj["name"] for obj in describe["sobjects"] if obj["custom"]
            ]

            logger.info(f"Found {len(custom_objects)} custom objects")

            # Generate documentation for each custom object
            for obj_name in custom_objects:
                try:
                    output_path = os.path.join(output_dir, f"{obj_name.lower()}.md")
                    documentation = self.generate_object_documentation(
                        obj_name, output_path
                    )
                    if documentation:
                        documented_objects.append(obj_name)
                except Exception as e:
                    logger.error(f"Error documenting {obj_name}: {str(e)}")

            logger.info(
                f"Generated documentation for {len(documented_objects)} custom objects"
            )

            # Create an index file listing all custom objects
            self._create_object_index(
                documented_objects,
                os.path.join(output_dir, "custom-objects.md"),
                "Custom Objects",
            )

            return documented_objects

        except Exception as e:
            logger.error(f"Error generating custom objects documentation: {str(e)}")
            return []

    def _create_object_index(self, object_list, output_path, title):
        """
        Create an index file listing all objects

        Args:
            object_list (list): List of object names
            output_path (str): Path to save the index file
            title (str): Title for the index page
        """
        try:
            # Sort the object list
            object_list.sort()

            # Create content
            content = f"""---
title: {title}
description: List of {title.lower()} in the Salesforce organization
---

# {title}

This page lists all {title.lower()} in the Salesforce organization.

## Object List

| Object Name | Documentation |
|-------------|---------------|
"""

            # Add each object
            for obj_name in object_list:
                content += f"| {obj_name} | [{obj_name}](./{obj_name.lower()}.md) |\n"

            # Save to file
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w") as f:
                f.write(content)

            logger.info(f"Created {title} index at {output_path}")

        except Exception as e:
            logger.error(f"Error creating object index: {str(e)}")


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Generate Salesforce documentation")

    # Authentication
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
        "--standard", action="store_true", help="Document standard objects"
    )
    parser.add_argument("--custom", action="store_true", help="Document custom objects")

    return parser.parse_args()


def main():
    """Main entry point"""
    # Parse command line arguments
    args = parse_args()

    # Try to get credentials from environment if not provided
    username = args.username or os.environ.get("SALESFORCE_USERNAME")
    password = args.password or os.environ.get("SALESFORCE_PASSWORD")
    token = args.token or os.environ.get("SALESFORCE_TOKEN")

    # Check if we have credentials
    if not username or not password:
        logger.error("Salesforce username and password are required")
        sys.exit(1)

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
            logger.info(f"Generating documentation for {args.object}")
            output_path = os.path.join(args.output_dir, f"{args.object.lower()}.md")
            doc_generator.generate_object_documentation(args.object, output_path)
        elif args.standard:
            logger.info("Generating documentation for standard objects")
            doc_generator.generate_standard_objects_documentation(args.output_dir)
        elif args.custom:
            logger.info("Generating documentation for custom objects")
            doc_generator.generate_custom_objects_documentation(args.output_dir)
        else:
            # Default: document both standard and custom objects
            logger.info("Generating documentation for all objects")
            doc_generator.generate_standard_objects_documentation(args.output_dir)
            doc_generator.generate_custom_objects_documentation(args.output_dir)

        logger.info(
            f"Documentation generation completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        logger.info(f"Documentation saved to {args.output_dir}")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
