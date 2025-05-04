#!/usr/bin/env python3
"""
Script to set up the documentation structure for the Salesforce Documentation Generator.
This will create the necessary folders and placeholder files based on the preferred structure.
"""

import os
import shutil
from pathlib import Path

# Define the base docs directory
DOCS_DIR = "docs"

# Define the documentation structure
DOCS_STRUCTURE = {
    "index.md": "# Salesforce Org Documentation\n\nWelcome to the comprehensive documentation for your Salesforce organization.",
    "org_overview": {
        "index.md": "# Organization Overview\n\nOverview of your Salesforce organization structure and key metrics.",
        "introduction.md": "# Introduction\n\nIntroduction to your Salesforce organization.",
        "key_metrics.md": "# Key Metrics\n\nKey metrics for your Salesforce organization.",
        "org_structure.md": "# Organization Structure\n\nThe structure of your Salesforce organization.",
        "strategic_initiatives.md": "# Strategic Initiatives\n\nStrategic initiatives within your Salesforce organization.",
    },
    "data_model": {
        "index.md": "# Data Model\n\nOverview of your Salesforce data model.",
        "objects": {
            "index.md": "# Objects\n\nOverview of all objects in your Salesforce organization.",
            "standard_objects.md": "# Standard Objects\n\nDetails about standard objects in your Salesforce org.",
            "custom_objects.md": "# Custom Objects\n\nDetails about custom objects in your Salesforce org.",
        },
        "fields": {
            "index.md": "# Fields\n\nOverview of fields in your Salesforce organization.",
            "data_dictionary.md": "# Data Dictionary\n\nComprehensive data dictionary for your Salesforce fields.",
            "formula_fields.md": "# Formula Fields\n\nDetails about formula fields in your Salesforce org.",
            "field_dependencies.md": "# Field Dependencies\n\nField dependencies in your Salesforce org.",
        },
        "relationships": {
            "index.md": "# Relationships\n\nOverview of relationships in your data model.",
            "erd.md": "# Entity Relationship Diagrams\n\nERD diagrams for your Salesforce objects.",
        },
    },
    "automation": {
        "index.md": "# Automation\n\nAutomation tools and processes in your Salesforce org.",
        "flows": {
            "index.md": "# Flows\n\nOverview of flows in your Salesforce org.",
            "record_triggered.md": "# Record-Triggered Flows\n\nDetails about record-triggered flows.",
            "scheduled.md": "# Scheduled Flows\n\nDetails about scheduled flows.",
        },
        "triggers": {
            "index.md": "# Triggers\n\nOverview of triggers in your Salesforce org.",
            "apex_triggers.md": "# Apex Triggers\n\nDetails about Apex triggers.",
        },
        "validation_rules": {
            "index.md": "# Validation Rules\n\nOverview of validation rules.",
            "rules_matrix.md": "# Rules Matrix\n\nMatrix of validation rules in your org.",
        },
        "processes": {
            "index.md": "# Processes\n\nOverview of Process Builder processes.",
            "process_builder.md": "# Process Builder\n\nDetails about Process Builder processes.",
        },
        "workflows": {
            "index.md": "# Workflows\n\nOverview of workflow rules.",
            "email_alerts.md": "# Email Alerts\n\nWorkflow email alerts in your org.",
        },
    },
    "security": {
        "index.md": "# Security\n\nSecurity configuration for your Salesforce org.",
        "dashboard": {
            "index.md": "# Security Dashboard\n\nOverview of your security posture.",
            "overview.md": "# Security Overview\n\nGeneral security overview.",
            "permissions.md": "# Permission Analysis\n\nAnalysis of permissions in your org.",
            "fls.md": "# Field Level Security\n\nField level security configuration.",
            "sharing_rules.md": "# Sharing Rule Analysis\n\nAnalysis of sharing rules.",
            "vulnerability_scans.md": "# Vulnerability Scans\n\nResults of vulnerability scans.",
        },
        "profiles": {
            "index.md": "# Profiles\n\nOverview of profiles in your org.",
            "profile_matrix.md": "# Profile Matrix\n\nMatrix of profile permissions.",
        },
        "permissions": {
            "index.md": "# Permissions\n\nPermission configuration in your org.",
            "permission_sets.md": "# Permission Sets\n\nDetails about permission sets.",
        },
        "sharing": {
            "index.md": "# Sharing\n\nSharing configuration in your org.",
            "sharing_rules.md": "# Sharing Rules\n\nDetails about sharing rules.",
            "role_hierarchy.md": "# Role Hierarchy\n\nRole hierarchy configuration.",
        },
    },
    "integrations": {
        "index.md": "# Integrations\n\nIntegrations with external systems.",
        "apis": {
            "index.md": "# APIs\n\nAPI integrations overview.",
            "rest_services.md": "# REST Services\n\nREST API services.",
            "soap_services.md": "# SOAP Services\n\nSOAP API services.",
        },
        "middleware": {
            "index.md": "# Middleware\n\nMiddleware integrations.",
            "mulesoft.md": "# MuleSoft\n\nMuleSoft integration details.",
        },
        "external_services": {
            "index.md": "# External Services\n\nExternal service integrations.",
            "named_credentials.md": "# Named Credentials\n\nNamed credential configurations.",
            "connected_apps.md": "# Connected Apps\n\nConnected app configurations.",
        },
    },
    "customization": {
        "index.md": "# Customization\n\nCustomizations in your Salesforce org.",
        "layouts": {
            "index.md": "# Layouts\n\nPage layout configurations.",
            "page_layouts.md": "# Page Layouts\n\nDetails about page layouts.",
            "record_types.md": "# Record Types\n\nRecord type configurations.",
        },
        "apps": {
            "index.md": "# Apps\n\nCustom and standard apps.",
            "lightning_apps.md": "# Lightning Apps\n\nLightning app details.",
        },
        "components": {
            "index.md": "# Components\n\nCustom components.",
            "lightning_components.md": "# Lightning Components\n\nLightning component details.",
        },
    },
    "administration": {
        "index.md": "# Administration\n\nAdministration tools and processes.",
        "users": {
            "index.md": "# Users\n\nUser management.",
            "user_management.md": "# User Management\n\nUser management processes.",
            "login_history.md": "# Login History\n\nUser login history.",
        },
        "licenses": {
            "index.md": "# Licenses\n\nLicense management.",
            "license_usage.md": "# License Usage\n\nLicense usage metrics.",
        },
        "settings": {
            "index.md": "# Settings\n\nOrg settings configuration.",
            "custom_settings.md": "# Custom Settings\n\nCustom settings configuration.",
            "custom_metadata.md": "# Custom Metadata\n\nCustom metadata configuration.",
        },
    },
    "development": {
        "index.md": "# Development\n\nDevelopment practices and tools.",
        "apex": {
            "index.md": "# Apex\n\nApex code overview.",
            "code_coverage.md": "# Code Coverage\n\nApex code coverage metrics.",
            "apex_code.md": "# Apex Code Samples\n\nSample Apex code snippets.",
        },
        "testing": {
            "index.md": "# Testing\n\nTesting practices.",
            "test_classes.md": "# Test Classes\n\nApex test class details.",
        },
        "deployments": {
            "index.md": "# Deployments\n\nDeployment practices.",
            "deployment_strategy.md": "# Deployment Strategy\n\nStrategies for deploying changes.",
        },
    },
    "monitoring": {
        "index.md": "# Monitoring\n\nMonitoring tools and metrics.",
        "logs": {
            "index.md": "# Logs\n\nLog monitoring.",
            "debug_logs.md": "# Debug Logs\n\nDebug log analysis.",
        },
        "metrics": {
            "index.md": "# Metrics\n\nPerformance metrics.",
            "usage_metrics.md": "# Usage Metrics\n\nOrg usage metrics.",
            "api_usage.md": "# API Usage\n\nAPI usage metrics.",
        },
        "reports": {
            "index.md": "# Reports\n\nReporting tools.",
            "report_inventory.md": "# Report Inventory\n\nInventory of reports.",
        },
    },
    "compliance": {
        "index.md": "# Compliance\n\nCompliance requirements and reports.",
        "reports": {
            "index.md": "# Compliance Reports\n\nCompliance reporting.",
            "audit_trail.md": "# Audit Trail\n\nAudit trail reports.",
            "data_access_logs.md": "# Data Access Logs\n\nData access log analysis.",
            "standards.md": "# Compliance Standards\n\nRelevant compliance standards.",
            "regulations.md": "# Regulatory Requirements\n\nRegulatory requirements.",
        },
    },
    "best_practices": {
        "index.md": "# Best Practices\n\nBest practices for Salesforce.",
        "development.md": "# Development Guidelines\n\nBest practices for development.",
        "deployment.md": "# Deployment Strategies\n\nBest practices for deployments.",
        "performance.md": "# Performance Optimization\n\nBest practices for performance.",
        "security.md": "# Security Best Practices\n\nBest practices for security.",
    },
}


def create_structure(base_path, structure, current_path=""):
    """Create folder structure and files from a nested dictionary"""
    for name, content in structure.items():
        path = os.path.join(base_path, current_path, name)

        if isinstance(content, dict):
            # This is a directory
            os.makedirs(path, exist_ok=True)
            create_structure(base_path, content, os.path.join(current_path, name))
        else:
            # This is a file
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(content)
            print(f"Created {path}")


def main():
    # Create base docs directory
    docs_path = Path(DOCS_DIR)

    # Check if docs directory exists and is not empty
    if docs_path.exists() and any(docs_path.iterdir()):
        response = input(
            "Docs directory already exists and is not empty. Do you want to replace it? (y/n): "
        )
        if response.lower() != "y":
            print("Operation cancelled.")
            return

        # Remove existing docs directory
        shutil.rmtree(docs_path)
        print(f"Removed existing {DOCS_DIR} directory.")

    # Create docs directory
    os.makedirs(docs_path, exist_ok=True)

    # Create structure
    create_structure(DOCS_DIR, DOCS_STRUCTURE)

    print(f"\nDocumentation structure created in {DOCS_DIR} directory.")
    print("You can now update the mkdocs.yml file to match this structure.")


if __name__ == "__main__":
    main()
