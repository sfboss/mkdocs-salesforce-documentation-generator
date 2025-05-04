from simple_salesforce import Salesforce
from jinja2 import Environment, Template
import json
from datetime import datetime
import os
from pathlib import Path
import pickle
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from functools import lru_cache

metadata_type_to_docs_path = {
    "standard_objects": "docs/data-model/objects/standard-objects.md",
    "custom_objects": "docs/data-model/objects/custom-objects.md",
    "standard_fields": "docs/data-model/fields/data-dictionary.md",
    "custom_fields": "docs/data-model/fields/data-dictionary.md",
    "validation_rules": "docs/automation/validation-rules/rules-matrix.md",
    "field_usage": "docs/data-model/fields/data-dictionary.md",
    "object_relationships": "docs/data-model/relationships/erd.md",
    "object_metadata": "docs/data-model/objects/standard-objects.md",
    "license_usage": "docs/administration/licenses/license-usage.md",
    "profile_permissions": "docs/security/profiles/profile-matrix.md",
    "permission_sets": "docs/security/permissions/permission-sets.md",
    "user_permissions": "docs/security/permissions/permission-sets.md",
    "record_types": "docs/customization/layouts/record-types.md",
    "page_layouts": "docs/customization/layouts/page-layouts.md",
    "workflow_rules": "docs/automation/workflows/email-alerts.md",
    "process_builder": "docs/automation/processes/process-builder.md",
    "flow_usage": "docs/automation/flows/record-triggered.md",  # Changed from scheduled.md
    "apex_classes": "docs/development/apex/code-coverage.md",
    "apex_triggers": "docs/automation/triggers/apex-triggers.md",  # Moved from development to automation
    "apex_tests": "docs/development/testing/test-classes.md",
    "visualforce_pages": "docs/customization/components/lightning-components.md",
    "lightning_components": "docs/customization/components/lightning-components.md",
    "aura_components": "docs/customization/components/lightning-components.md",
    "lwc_components": "docs/customization/components/lightning-components.md",
    "static_resources": "docs/customization/components/lightning-components.md",
    "connected_apps": "docs/integrations/apis/rest-services.md",
    "named_credentials": "docs/integrations/external-services/named-credentials.md",
    "auth_providers": "docs/integrations/external-services/named-credentials.md",
    "custom_metadata": "docs/administration/settings/custom-metadata.md",
    "custom_settings": "docs/administration/settings/custom-settings.md",
    "email_templates": "docs/automation/workflows/email-alerts.md",
    "report_types": "docs/monitoring/reports/report-inventory.md",
    "dashboards": "docs/monitoring/reports/report-inventory.md",
    "list_views": "docs/data-model/fields/data-dictionary.md",
    "sharing_rules": "docs/security/sharing/sharing-rules.md",
    "roles": "docs/security/sharing/role-hierarchy.md",
    "groups": "docs/security/sharing/role-hierarchy.md",
    "queues": "docs/security/sharing/role-hierarchy.md",
    "territories": "docs/security/sharing/role-hierarchy.md",
    "public_groups": "docs/security/sharing/role-hierarchy.md",
    "email_alerts": "docs/automation/workflows/email-alerts.md",
}

metadata_type_to_template_path = {
    # Object & Field Templates
    "standard_objects": "backend/templates/standard_objects.j2",
    "custom_objects": "backend/templates/custom_objects.j2",
    "standard_fields": "backend/templates/standard_fields.j2",
    "custom_fields": "backend/templates/custom_fields.j2",
    "field_usage": "backend/templates/field_usage.j2",
    "object_relationships": "backend/templates/object_relationships.j2",
    "object_metadata": "backend/templates/object_metadata.j2",
    "record_types": "backend/templates/record_types.j2",
    "list_views": "backend/templates/list_views.j2",
    # Security Templates
    "license_usage": "backend/templates/license_usage.j2",
    "profile_permissions": "backend/templates/profile_permissions.j2",
    "permission_sets": "backend/templates/permission_sets.j2",
    "user_permissions": "backend/templates/user_permissions.j2",
    "sharing_rules": "backend/templates/sharing_rules.j2",
    "roles": "backend/templates/roles.j2",
    "groups": "backend/templates/groups.j2",
    "queues": "backend/templates/queues.j2",
    "territories": "backend/templates/territories.j2",
    "public_groups": "backend/templates/public_groups.j2",
    # Automation Templates
    "validation_rules": "backend/templates/validation_rules.j2",
    "workflow_rules": "backend/templates/workflow_rules.j2",
    "process_builder": "backend/templates/process_builder.j2",
    "flow_usage": "backend/templates/flow_usage.j2",
    "email_alerts": "backend/templates/email_alerts.j2",
    "email_templates": "backend/templates/email_templates.j2",
    # Development Templates
    "apex_classes": "backend/templates/apex_classes.j2",
    "apex_triggers": "backend/templates/apex_triggers.j2",
    "apex_tests": "backend/templates/apex_tests.j2",
    # UI/UX Templates
    "page_layouts": "backend/templates/page_layouts.j2",
    "visualforce_pages": "backend/templates/visualforce_pages.j2",
    "lightning_components": "backend/templates/lightning_components.j2",
    "aura_components": "backend/templates/aura_components.j2",
    "lwc_components": "backend/templates/lwc_components.j2",
    "static_resources": "backend/templates/static_resources.j2",
    # Integration Templates
    "connected_apps": "backend/templates/connected_apps.j2",
    "named_credentials": "backend/templates/named_credentials.j2",
    "auth_providers": "backend/templates/auth_providers.j2",
    # Configuration Templates
    "custom_metadata": "backend/templates/custom_metadata.j2",
    "custom_settings": "backend/templates/custom_settings.j2",
    # Analytics Templates
    "report_types": "backend/templates/report_types.j2",
    "dashboards": "backend/templates/dashboards.j2",
}

import os
from jinja2 import Environment, FileSystemLoader
from typing import Dict
from pathlib import Path
import pickle
from datetime import datetime
from simple_salesforce import Salesforce
from typing import Optional, List, Dict, Any


def ensure_map_paths_exist(docs_paths: Dict[str, str], template_paths: Dict[str, str]):
    print("creating paths")
    for path in set(docs_paths.values()):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        os.system(f"touch {path}")
    for path in set(template_paths.values()):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        os.system(f"touch {path}")


class JinjaRenderer:
    def __init__(self, config):
        self.config = config
        # Initialize the Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(self.config["template_dir"]))

    def render(self, template_name, context):
        # Load the template from the environment
        template = self.env.get_template(template_name)
        # Render the template with the provided context
        return template.render(context)

    def add_template_filter(self, name, func):
        """Add a custom filter to the Jinja2 environment."""
        self.env.filters[name] = func

    def add_template_test(self, name, func):
        """Add a custom test to the Jinja2 environment."""
        self.env.tests[name] = func

    def add_template_global(self, name, func):
        """Add a global function or variable to the Jinja2 environment."""
        self.env.globals[name] = func

    def add_template_function(self, name, func):
        """Add a custom function to the Jinja2 environment."""
        self.env.globals[name] = func

    def add_template_variable(self, name, value):
        """Add a global variable to the Jinja2 environment."""
        self.env.globals[name] = value


@dataclass
class CacheConfig:
    cache_dir: str = ".sf_cache"
    describes_file: str = "describes.pkl"
    metadata_file: str = "metadata.pkl"
    cache_ttl: int = 86400  # 24 hours in seconds


class SalesforceCache:
    def __init__(self, config: CacheConfig):
        self.config = config
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        Path(self.config.cache_dir).mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, filename: str) -> str:
        return os.path.join(self.config.cache_dir, filename)

    def save(self, data: Any, filename: str):
        cache_path = self._get_cache_path(filename)
        with open(cache_path, "wb") as f:
            pickle.dump({"timestamp": datetime.now().timestamp(), "data": data}, f)

    def load(self, filename: str) -> Optional[Any]:
        cache_path = self._get_cache_path(filename)
        if not os.path.exists(cache_path):
            return None

        with open(cache_path, "rb") as f:
            try:
                cache_data = pickle.load(f)
                if (
                    datetime.now().timestamp() - cache_data["timestamp"]
                ) > self.config.cache_ttl:
                    return None
                return cache_data["data"]
            except:
                return None


class SalesforceMetadata:
    # Set of known non-queryable fields by object
    NON_QUERYABLE_FIELDS: Dict[str, Set[str]] = {
        "Account": {
            "ChannelProgramName",
            "ChannelProgramLevelName",
            "HasOpenActivity",
            "HasOverdueTask",
        },
        "Opportunity": {
            "HasOpenActivity",
            "HasOverdueTask",
            "SyncedQuoteId",
            "LastAmountChangedHistoryId",
        },
        # Add more as needed
    }

    def __init__(self, sf_connection: Salesforce, cache: SalesforceCache):
        self.sf = sf_connection
        self.cache = cache

    def get_last_modified_date(self, object_name: str) -> Optional[str]:
        """Get the last modified date for any record in the object"""
        try:
            result = self.sf.query(
                f"SELECT LastModifiedDate FROM {object_name} "
                "ORDER BY LastModifiedDate DESC LIMIT 1"
            )
            records = result.get("records", [])
            if records:
                return records[0].get("LastModifiedDate")
        except Exception as e:
            print(f"Error getting last modified date for {object_name}: {str(e)}")
        return None

    def get_record_count(self, object_name: str) -> int:
        """Get total number of records for an object"""
        try:
            result = self.sf.query(f"SELECT COUNT() FROM {object_name}")
            return result.get("totalSize", 0)
        except Exception as e:
            print(f"Error getting record count for {object_name}: {str(e)}")
            return 0

    def _is_queryable_field(
        self, object_name: str, field_name: str, field_type: str
    ) -> bool:
        """Determine if a field can be queried"""
        # Check if field is in non-queryable set for this object
        if field_name in self.NON_QUERYABLE_FIELDS.get(object_name, set()):
            return False

        non_queryable_types = {
            "address",
            "location",
            "encrypted",
            "textarea",
            "calculated",
            "complexvalue",
            "datacategorygroupreference",
        }

        return field_type.lower() not in non_queryable_types

    def _get_field_usage_batch(
        self, object_name: str, fields: List[Dict]
    ) -> Dict[str, float]:
        """Get field usage statistics in optimized batches"""
        usage_stats = {}
        queryable_fields = [
            f["name"]
            for f in fields
            if self._is_queryable_field(object_name, f["name"], f.get("type", ""))
        ]

        # Process fields in smaller batches to avoid query limits
        batch_size = 3  # Reduced batch size
        for i in range(0, len(queryable_fields), batch_size):
            batch = queryable_fields[i : i + batch_size]
            if not batch:
                continue

            query_conditions = " OR ".join([f"{field} != null" for field in batch])

            try:
                query = f"SELECT COUNT() FROM {object_name} WHERE {query_conditions}"
                result = self.sf.query(query)
                total_records = result.get("totalSize", 0)
                record_count = self.get_record_count(object_name)

                for field in batch:
                    usage_stats[field] = (
                        (total_records / record_count * 100) if record_count > 0 else 0
                    )
            except Exception as e:
                print(f"Error in batch query for {object_name}: {str(e)}")
                for field in batch:
                    usage_stats[field] = 0

        return usage_stats

    def _get_relationships(self, describe_result: Dict) -> List[Dict]:
        """Extract relationship information"""
        relationships = []
        for child in describe_result.get("childRelationships", []) or []:
            relationship_name = child.get("relationshipName")
            child_sobject = child.get("childSObject")
            if relationship_name and child_sobject:
                relationships.append(
                    {
                        "type_symbol": "-->",
                        "related_object": child_sobject,
                        "relationship_name": relationship_name,
                    }
                )
        return relationships

    def _get_validation_rules(self, object_name: str) -> List[Dict]:
        """Fetch validation rules for the object"""
        try:
            tooling_query = f"""
                SELECT Id, Active, Description, ErrorDisplayField, ErrorMessage
                FROM ValidationRule 
                WHERE EntityDefinition.QualifiedApiName = '{object_name}'
            """
            result = self.sf.restful(f"tooling/query/?q={tooling_query}")
            return [
                {
                    "name": rule.get("ErrorDisplayField", ""),
                    "message": rule.get("ErrorMessage", ""),
                    "active": rule.get("Active", False),
                }
                for rule in result.get("records", [])
            ]
        except Exception as e:
            print(f"Error getting validation rules for {object_name}: {str(e)}")
            return []

    def get_object_metadata(self, object_name: str) -> Optional[Dict]:
        """Get metadata for specific object with caching"""
        cache_key = f"object_metadata_{object_name}.pkl"
        cached_data = self.cache.load(cache_key)

        if cached_data:
            return cached_data

        try:
            describe_result = self.sf.__getattr__(object_name).describe()

            metadata = {
                "label": describe_result.get("label", object_name),
                "api_name": describe_result.get("name", object_name),
                "description": describe_result.get("description", ""),
                "record_count": self.get_record_count(object_name),
                "last_modified_date": self.get_last_modified_date(object_name),
                "fields": describe_result.get("fields", []),
                "relationships": self._get_relationships(describe_result),
                "validation_rules": self._get_validation_rules(object_name),
            }

            self.cache.save(metadata, cache_key)
            return metadata
        except Exception as e:
            print(f"Error getting metadata for {object_name}: {str(e)}")
            return None


class SalesforceDocGenerator:
    def __init__(
        self,
        username: str,
        password: str,
        security_token: str,
        cache_config: Optional[CacheConfig] = None,
        template_path: Optional[str] = None,
    ):
        self.sf = Salesforce(
            username=username, password=password, security_token=security_token
        )
        self.cache = SalesforceCache(cache_config or CacheConfig())
        self.metadata = SalesforceMetadata(self.sf, self.cache)
        self.template_path = template_path or "templates/standard_objects.md"
        self.env = Environment()

    def generate_documentation(self, objects: Optional[List[str]] = None) -> str:
        try:
            if not objects:
                objects = self._get_core_sales_objects()

            metadata_list = []
            for obj in objects:
                try:
                    if metadata := self.metadata.get_object_metadata(obj):
                        metadata_list.append(metadata)
                except Exception as e:
                    print(f"Error processing {obj}: {str(e)}")
                    continue

            data = {
                "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "objects": metadata_list,
            }

            with open(self.template_path) as f:
                template = Template(f.read())
            return template.render(**data)
        except Exception as e:
            print(f"Error generating documentation: {str(e)}")
            return f"Error generating documentation: {str(e)}"

    def _get_core_sales_objects(self) -> List[str]:
        return [
            "Account",
            "Contact",
            "Lead",
            "Opportunity",
            "Campaign",
            "Case",
            "Product2",
            "User",
        ]

    def save_documentation(self, output_path: str):
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            documentation = self.generate_documentation()
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(documentation)
            print(f"Documentation saved to {output_path}")
            return documentation
        except Exception as e:
            print(f"Error saving documentation: {str(e)}")
            return None


def setup_documentation_generator(
    username: str,
    password: str,
    security_token: str,
    cache_dir: Optional[str] = None,
    template_path: Optional[str] = None,
) -> SalesforceDocGenerator:
    config = CacheConfig(cache_dir=cache_dir) if cache_dir else CacheConfig()
    return SalesforceDocGenerator(
        username=username,
        password=password,
        security_token=security_token,
        cache_config=config,
        template_path=template_path,
    )


if __name__ == "__main__":
    # Example usage
    generator = setup_documentation_generator(
        username="claytonboss+bosstools@gmail.com",
        password="c4Nbrl*ugyzcu",
        security_token="1jnkaUih1Mst2W3IbfLqBRCS",
        template_path="backend/templates/standard_objects.j2",
    )
    ensure_map_paths_exist(metadata_type_to_docs_path, metadata_type_to_template_path)

    generator.save_documentation("output/salesforce_documentation.md")
