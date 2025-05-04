#!/usr/bin/env python3
import os
import argparse
import json
import logging
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from simple_salesforce import Salesforce

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SalesforceDocumentationGenerator:
    def __init__(self, username=None, password=None, security_token=None, 
                 domain='login', template_path='templates/object_documentation.j2'):
        """
        Initialize the documentation generator with Salesforce credentials
        and template configuration.
        """
        self.sf = None
        if username and password:
            try:
                self.sf = Salesforce(
                    username=username,
                    password=password,
                    security_token=security_token,
                    domain=domain
                )
                logger.info(f"Successfully connected to Salesforce as {username}")
            except Exception as e:
                logger.error(f"Failed to connect to Salesforce: {str(e)}")
                raise
        
        # Set up Jinja2 environment
        template_dir = os.path.dirname(template_path)
        template_file = os.path.basename(template_path)
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template(template_file)
        logger.info(f"Using template: {template_path}")
    
    def _get_object_metadata(self, object_name):
        """
        Fetch metadata for a specific Salesforce object.
        
        Args:
            object_name (str): API name of the Salesforce object
            
        Returns:
            dict: Object metadata
        """
        try:
            # Get the object description
            obj_desc = getattr(self.sf, object_name).describe()
            
            # Basic object info
            obj_data = {
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
                "relationships": {
                    "child_relationships": [],
                    "reference_fields": []
                },
                "record_types": [],
                "validation_rules": []
            }
            
            # Add fields information
            for field in obj_desc["fields"]:
                field_data = {
                    "label": field["label"],
                    "api_name": field["name"],
                    "type": field["type"],
                    "required": not field["nillable"],
                    "description": field.get("description", "")
                }
                obj_data["fields"].append(field_data)
                
                # If it's a reference field, add to relationship section
                if field["type"] == "reference" and field.get("referenceTo"):
                    ref_data = {
                        "label": field["label"],
                        "api_name": field["name"],
                        "reference_to": ", ".join(field["referenceTo"]),
                        "description": field.get("description", "")
                    }
                    obj_data["relationships"]["reference_fields"].append(ref_data)
            
            # Add child relationships
            for rel in obj_desc.get("childRelationships", []):
                if rel.get("childSObject") and rel.get("field"):
                    rel_data = {
                        "label": rel.get("childSObject"),
                        "api_name": rel.get("field"),
                        "description": f"Child relationship from {rel.get('childSObject')}"
                    }
                    obj_data["relationships"]["child_relationships"].append(rel_data)
            
            # Get record types
            try:
                query = f"SELECT Id, Name, DeveloperName, Description, IsActive FROM RecordType WHERE SObjectType = '{object_name}'"
                record_types = self.sf.query(query)
                
                for rt in record_types.get("records", []):
                    rt_data = {
                        "label": rt.get("Name"),
                        "api_name": rt.get("DeveloperName"),
                        "active": rt.get("IsActive", False),
                        "description": rt.get("Description", "")
                    }
                    obj_data["record_types"].append(rt_data)
            except Exception as e:
                logger.warning(f"Failed to get record types for {object_name}: {str(e)}")
            
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
                        "error_message": vr.get("ErrorMessage", "")
                    }
                    obj_data["validation_rules"].append(vr_data)
            except Exception as e:
                logger.warning(f"Failed to get validation rules for {object_name}: {str(e)}")
            
            return obj_data
            
        except Exception as e:
            logger.error(f"Error getting metadata for {object_name}: {str(e)}")
            return None
    
    def generate_object_documentation(self, object_name, output_path=None):
        """
        Generate documentation for a specific Salesforce object.
        
        Args:
            object_name (str): API name of the Salesforce object
            output_path (str, optional): Path to save the documentation
            
        Returns:
            str: Generated documentation
        """
        if not self.sf:
            logger.error("Salesforce connection not established")
            return None
        
        object_data = self._get_object_metadata(object_name)
        if not object_data:
            logger.error(f"Could not generate documentation for {object_name}")
            return None
        
        # Render documentation with template
        documentation = self.template.render(object_data=object_data)
        
        # Save to file if output path provided
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w") as file:
                file.write(documentation)
            logger.info(f"Documentation saved to {output_path}")
        
        return documentation
    
    def generate_standard_objects_documentation(self, output_dir="docs/data-model/objects"):
        """
        Generate documentation for all standard objects in Salesforce.
        
        Args:
            output_dir (str): Directory to save the documentation files
            
        Returns:
            list: List of objects documented
        """
        if not self.sf:
            logger.error("Salesforce connection not established")
            return []
        
        # Get the global describe to list all objects
        describe = self.sf.describe()
        standard_objects = [obj["name"] for obj in describe["sobjects"] if not obj["custom"]]
        
        documented_objects = []
        for obj_name in standard_objects:
            try:
                output_path = os.path.join(output_dir, f"{obj_name.lower()}.md")
                result = self.generate_object_documentation(obj_name, output_path)
                if result:
                    documented_objects.append(obj_name)
            except Exception as e:
                logger.error(f"Error documenting {obj_name}: {str(e)}")
        
        logger.info(f"Generated documentation for {len(documented_objects)} standard objects")
        return documented_objects
    
    def generate_custom_objects_documentation(self, output_dir="docs/data-model/objects"):
        """
        Generate documentation for all custom objects in Salesforce.
        
        Args:
            output_dir (str): Directory to save the documentation files
            
        Returns:
            list: List of objects documented
        """
        if not self.sf:
            logger.error("Salesforce connection not established")
            return []
        
        # Get the global describe to list all objects
        describe = self.sf.describe()
        custom_objects = [obj["name"] for obj in describe["sobjects"] if obj["custom"]]
        
        documented_objects = []
        for obj_name in custom_objects:
            try:
                output_path = os.path.join(output_dir, f"{obj_name.lower()}.md")
                result = self.generate_object_documentation(obj_name, output_path)
                if result:
                    documented_objects.append(obj_name)
            except Exception as e:
                logger.error(f"Error documenting {obj_name}: {str(e)}")
        
        logger.info(f"Generated documentation for {len(documented_objects)} custom objects")
        return documented_objects


def setup_documentation_generator(username, password, security_token, 
                                template_path='templates/object_documentation.j2', 
                                domain='login'):
    """
    Set up the documentation generator with the provided credentials.
    
    Args:
        username (str): Salesforce username
        password (str): Salesforce password
        security_token (str): Salesforce security token
        template_path (str): Path to the Jinja2 template
        domain (str): Salesforce login domain
        
    Returns:
        SalesforceDocumentationGenerator: Configured generator instance
    """
    try:
        generator = SalesforceDocumentationGenerator(
            username=username,
            password=password,
            security_token=security_token,
            template_path=template_path,
            domain=domain
        )
        return generator
    except Exception as e:
        logger.error(f"Failed to set up documentation generator: {str(e)}")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Salesforce documentation")
    parser.add_argument("--username", help="Salesforce username")
    parser.add_argument("--password", help="Salesforce password")
    parser.add_argument("--token", help="Salesforce security token")
    parser.add_argument("--domain", default="login", help="Salesforce domain (default: login)")
    parser.add_argument("--template", default="templates/object_documentation.j2", help="Template path")
    parser.add_argument("--output", default="docs/data-model/objects", help="Output directory")
    parser.add_argument("--object", help="Specific object to document")
    parser.add_argument("--standard", action="store_true", help="Document standard objects")
    parser.add_argument("--custom", action="store_true", help="Document custom objects")
    
    args = parser.parse_args()
    
    # Check for required credentials
    if not (args.username and args.password):
        # Try environment variables if not provided as arguments
        import os
        args.username = args.username or os.environ.get("SALESFORCE_USERNAME")
        args.password = args.password or os.environ.get("SALESFORCE_PASSWORD")
        args.token = args.token or os.environ.get("SALESFORCE_TOKEN")
        
        if not (args.username and args.password):
            parser.error("Salesforce credentials are required (--username and --password)")
    
    try:
        # Set up the documentation generator
        generator = setup_documentation_generator(
            username=args.username,
            password=args.password,
            security_token=args.token,
            template_path=args.template,
            domain=args.domain
        )
        
        # Generate documentation based on arguments
        if args.object:
            output_path = os.path.join(args.output, f"{args.object.lower()}.md")
            generator.generate_object_documentation(args.object, output_path)
        elif args.standard:
            generator.generate_standard_objects_documentation(args.output)
        elif args.custom:
            generator.generate_custom_objects_documentation(args.output)
        else:
            # Default: document both standard and custom objects
            generator.generate_standard_objects_documentation(args.output)
            generator.generate_custom_objects_documentation(args.output)
        
        print(f"Documentation generation completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Documentation saved to: {args.output}")
        print("Run 'mkdocs serve' to view the documentation.")
        
    except Exception as e:
        logger.error(f"Documentation generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)