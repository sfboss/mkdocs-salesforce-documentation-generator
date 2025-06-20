# MkDocs Blog and Navigation Structure

## Purpose

This project leverages [MkDocs](https://www.mkdocs.org/) to generate comprehensive, easy-to-navigate documentation for Salesforce projects. The goal is to provide a clear, organized, and searchable resource for developers, admins, and stakeholders.

## Blog Structure

The blog feature in MkDocs (enabled via plugins like `mkdocs-blog-plugin`) allows y. ou to publish updates, release notes, tutorials, and best practices. Blog posts are typically stored in a `blog/` directory and are automatically listed in a chronological feed.

**Example Blog Directory:**
```
docs/
    blog/
        2024-06-01-release-notes.md
        2024-05-15-getting-started.md
```

## Navigation (`nav`) Structure

The `nav` section in `mkdocs.yml` defines the sidebar and top navigation for your documentation. It organizes content into logical sections, making it easy for users to find information.

**Example `mkdocs.yml` Navigation:**
```yaml
nav:
    - Home: index.md
    - Getting Started:
            - Introduction: getting-started/introduction.md
            - Installation: getting-started/installation.md
    - Guides:
            - Configuration: guides/configuration.md
            - Usage: guides/usage.md
    - Blog:
            - "Release Notes": blog/2024-06-01-release-notes.md
            - "Getting Started": blog/2024-05-15-getting-started.md
    - API Reference: api-reference.md
    - FAQ: faq.md
```

## Summary

- **Blog:** Share updates, tutorials, and news.
- **Nav:** Organize documentation for easy access.
- **Purpose:** Deliver clear, structured Salesforce documentation using MkDocs..


# Menu System

```
docs
├── admin
│   ├── automation
│   │   ├── einstein_automations.md
│   │   ├── email_alerts.md
│   │   ├── flow_builder.md
│   │   ├── index.md
│   │   ├── process_builder.md
│   │   ├── validation_rules.md
│   │   └── workflow_rules.md
│   ├── data
│   │   ├── data_changes.md
│   │   ├── data_dictionary.md
│   │   ├── duplicates.md
│   │   ├── erd.md
│   │   └── index.md
│   ├── index.md
│   ├── integrations
│   │   ├── api_integrations.md
│   │   ├── connected_apps.md
│   │   ├── external_systems.md
│   │   ├── index.md
│   │   └── mulesoft.md
│   ├── monitoring
│   │   ├── index.md
│   │   ├── license_usage.md
│   │   ├── limits.md
│   │   ├── login_history.md
│   │   └── usage_metrics.md
│   ├── permission_sets.md
│   ├── profiles
│   │   ├── index.md
│   │   └── profile_matrix.md
│   ├── security
│   │   ├── audit_trail.md
│   │   ├── fls.md
│   │   ├── index.md
│   │   ├── role_hierarchy.md
│   │   └── sharing_rules.md
│   └── user_management.md
├── administration
│   ├── index.md
│   ├── licenses
│   │   ├── index.md
│   │   └── license_usage.md
│   ├── settings
│   │   ├── custom_metadata.md
│   │   ├── custom_settings.md
│   │   └── index.md
│   └── users
│       ├── index.md
│       ├── login_history.md
│       └── user_management.md
├── analytics
│   ├── active_users.md
│   ├── data_access_logs.md
│   ├── feature_adoption.md
│   ├── index.md
│   └── records_touched.md
├── assets
│   ├── images
│   │   ├── favicon.png
│   │   ├── logo.svg
│   │   └── placeholder-logo.svg
│   ├── javascripts
│   │   └── extra.js
│   └── stylesheets
│       └── extra.css
├── automation
│   ├── flows
│   │   ├── index.md
│   │   ├── record_triggered.md
│   │   └── scheduled.md
│   ├── index.md
│   ├── processes
│   │   ├── index.md
│   │   └── process_builder.md
│   ├── triggers
│   │   ├── apex_triggers.md
│   │   └── index.md
│   ├── validation_rules
│   │   ├── index.md
│   │   └── rules_matrix.md
│   └── workflows
│       ├── email_alerts.md
│       └── index.md
├── best_practices
│   ├── deployment.md
│   ├── development.md
│   ├── index.md
│   ├── performance.md
│   └── security.md
├── compliance
│   ├── index.md
│   └── reports
│       ├── audit_trail.md
│       ├── data_access_logs.md
│       ├── index.md
│       ├── regulations.md
│       └── standards.md
├── customization
│   ├── apps
│   │   ├── index.md
│   │   └── lightning_apps.md
│   ├── components
│   │   ├── index.md
│   │   └── lightning_components.md
│   ├── index.md
│   └── layouts
│       ├── index.md
│       ├── page_layouts.md
│       └── record_types.md
├── data_model
│   ├── fields
│   │   ├── data_dictionary.md
│   │   ├── field_dependencies.md
│   │   ├── formula_fields.md
│   │   └── index.md
│   ├── index.md
│   ├── objects
│   │   ├── custom_objects.md
│   │   ├── index.md
│   │   └── standard_objects.md
│   └── relationships
│       ├── erd.md
│       └── index.md
├── developer
│   ├── apex
│   │   ├── apex_code.md
│   │   ├── apex_triggers.md
│   │   ├── code_coverage.md
│   │   ├── index.md
│   │   └── test_classes.md
│   ├── api
│   │   ├── api_usage.md
│   │   ├── index.md
│   │   ├── named_credentials.md
│   │   ├── rest_services.md
│   │   └── soap_services.md
│   ├── database
│   │   ├── field_dependencies.md
│   │   ├── formula_fields.md
│   │   ├── index.md
│   │   └── soql_queries.md
│   ├── debugging
│   │   ├── debug_logs.md
│   │   └── index.md
│   ├── deployment
│   │   ├── deployment_strategy.md
│   │   └── index.md
│   ├── index.md
│   ├── lightning
│   │   ├── index.md
│   │   └── lightning_components.md
│   ├── metadata
│   │   ├── custom_metadata.md
│   │   ├── custom_settings.md
│   │   ├── index.md
│   │   └── page_layouts.md
│   └── standards.md
├── development
│   ├── apex
│   │   ├── apex_code.md
│   │   ├── code_coverage.md
│   │   └── index.md
│   ├── deployments
│   │   ├── deployment_strategy.md
│   │   └── index.md
│   ├── index.md
│   └── testing
│       ├── index.md
│       └── test_classes.md
├── governance
│   ├── index.md
│   ├── regulations.md
│   ├── security_events.md
│   ├── strategic_initiatives.md
│   └── vulnerability_scans.md
├── index.md
├── integrations
│   ├── apis
│   │   ├── index.md
│   │   ├── rest_services.md
│   │   └── soap_services.md
│   ├── external_services
│   │   ├── connected_apps.md
│   │   ├── index.md
│   │   └── named_credentials.md
│   ├── index.md
│   └── middleware
│       ├── index.md
│       └── mulesoft.md
├── introduction.md
├── monitoring
│   ├── index.md
│   ├── logs
│   │   ├── debug_logs.md
│   │   └── index.md
│   ├── metrics
│   │   ├── api_usage.md
│   │   ├── index.md
│   │   └── usage_metrics.md
│   └── reports
│       ├── index.md
│       └── report_inventory.md
├── org_overview
│   ├── index.md
│   ├── introduction.md
│   ├── key_metrics.md
│   ├── org_structure.md
│   └── strategic_initiatives.md
├── overview.md
├── reference
│   ├── flow_executions.md
│   ├── index.md
│   ├── objects_fields.md
│   ├── rules_matrix.md
│   └── scheduled_jobs.md
├── security
│   ├── dashboard
│   │   ├── fls.md
│   │   ├── index.md
│   │   ├── overview.md
│   │   ├── permissions.md
│   │   ├── sharing_rules.md
│   │   └── vulnerability_scans.md
│   ├── index.md
│   ├── permissions
│   │   ├── index.md
│   │   └── permission_sets.md
│   ├── profiles
│   │   ├── index.md
│   │   └── profile_matrix.md
│   └── sharing
│       ├── index.md
│       ├── role_hierarchy.md
│       └── sharing_rules.md
├── snippets
│   ├── abbreviations.md
│   └── apex_governor_limits.md
└── user
    ├── custom_objects.md
    ├── getting_started.md
    ├── index.md
    ├── key_metrics.md
    ├── lightning_apps.md
    ├── record_types.md
    ├── reports
    │   ├── index.md
    │   └── report_inventory.md
    └── standard_objects.md

64 directories, 186 files
```