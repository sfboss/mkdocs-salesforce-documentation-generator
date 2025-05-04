#!/bin/bash

# MkDocs Advanced Documentation Setup Script
# This script creates the entire structure for your Salesforce documentation
# with advanced MkDocs features and templates

# Exit on error
set -e

echo "Starting MkDocs documentation setup..."

# Create root directories
mkdir -p docs/assets/{images,stylesheets,javascripts}
mkdir -p docs/snippets
mkdir -p overrides/partials

# Create README file

# Create base directory structure
mkdir -p docs/{user,admin,developer,analytics,governance,reference}

# Create subdirectories for user section
mkdir -p docs/user/reports

# Create subdirectories for admin section
mkdir -p docs/admin/{profiles,security,data,automation,integrations,monitoring}

# Create subdirectories for developer section
mkdir -p docs/developer/{apex,metadata,lightning,api,debugging,database,deployment}

# Function to create a basic file with front matter
create_file() {
    local file_path=$1
    local title=$2
    local description=$3
    local doc_type=$4
    local audience=$5
    local icon=$6
    
    mkdir -p "$(dirname "$file_path")"
    
    cat > "$file_path" << EOF
---
title: $title
description: $description
doc_type: $doc_type
audience: [$audience]
status: published
last_reviewed: $(date +%Y-%m-%d)
icon: $icon
tags:
  - ${audience}
  - ${doc_type}
---

# $title

Add content here.
EOF

    echo "Created $file_path"
}

# Function to create a README file
create_readme() {
    cat > README.md << EOF
# Salesforce Documentation Project

This is a comprehensive Salesforce documentation project built with MkDocs and the Material for MkDocs theme, enhanced with PyMdown Extensions.

## Project Structure

The documentation is organized into the following main sections:

- **User Documentation**: Guides for end users of the Salesforce platform
- **Admin Documentation**: Information for Salesforce administrators
- **Developer Documentation**: Resources for developers
- **Analytics**: Analytics and reporting information
- **Governance**: Governance and compliance documentation
- **Reference**: Reference materials and guides

## Getting Started

### Installation

1. Install MkDocs and required dependencies:

\`\`\`bash
pip install mkdocs mkdocs-material pymdown-extensions
pip install mkdocs-minify-plugin mkdocs-git-revision-date-localized-plugin mkdocs-glightbox mkdocs-mermaid2-plugin
\`\`\`

2. Install other dependencies as needed (adjust based on your configuration):

\`\`\`bash
pip install mkdocstrings mkdocs-section-index
\`\`\`

### Development

To start the development server:

\`\`\`bash
mkdocs serve
\`\`\`

### Building the Site

To build the static site:

\`\`\`bash
mkdocs build
\`\`\`

### Project Configuration

The main configuration is in \`mkdocs.yml\`. This file contains:

- Site information
- Navigation structure
- Theme configuration
- Plugin settings
- Markdown extension settings

## Features

This documentation uses many advanced MkDocs features:

- **Material for MkDocs theme** with customization
- **Metadata-driven templating** using front matter
- **PyMdown Extensions** for enhanced content blocks
- **Custom styling** based on document types
- **Custom theme overrides** for specialized components
- **Advanced code blocks** with syntax highlighting and annotations
- **Interactive components** like tabs and expandable sections
- **Diagrams** using Mermaid

## Directory Structure

\`\`\`
docs/
├── index.md                  # Main landing page
├── introduction.md           # General introduction
├── overview.md               # System overview
├── user/                     # User documentation
├── admin/                    # Admin documentation
├── developer/                # Developer documentation
├── analytics/                # Analytics documentation
├── governance/               # Governance documentation
├── reference/                # Reference documentation
└── assets/                   # CSS, JS, and images
\`\`\`

## Content Guidelines

When creating content:

1. Use appropriate metadata front matter for each document
2. Follow the document structure for your document type
3. Use the available PyMdown Extensions for rich content
4. Keep related content together in logical sections
5. Use snippets for reusable content

EOF

    echo "Created README.md"
}

# Function to create index files
create_index_file() {
    local file_path=$1
    local title=$2
    local description=$3
    local doc_type=$4
    local audience=$5
    local icon=$6
    
    mkdir -p "$(dirname "$file_path")"
    
    cat > "$file_path" << EOF
---
title: $title
description: $description
doc_type: $doc_type
audience: [$audience]
status: published
last_reviewed: $(date +%Y-%m-%d)
icon: $icon
tags:
  - ${audience}
  - index
---

# $title

This section contains documentation about $description

## Contents

- [Example Page 1](#)
- [Example Page 2](#)
- [Example Page 3](#)

## Overview

Add overview content here.
EOF

    echo "Created index $file_path"
}

# Create root index file
cat > docs/index.md << EOF
---
title: Salesforce Documentation
description: Comprehensive Salesforce documentation for Users, Admins, and Developers
doc_type: index
audience: [user, admin, developer]
status: published
last_reviewed: $(date +%Y-%m-%d)
icon: material/home
tags:
  - home
  - index
---

# Salesforce Documentation

Welcome to the comprehensive Salesforce documentation. This site provides detailed information for users, administrators, and developers.

## Key Sections

- [User Documentation](user/index.md): Guides for end users of the Salesforce platform
- [Admin Documentation](admin/index.md): Information for Salesforce administrators
- [Developer Documentation](developer/index.md): Resources for developers
- [Analytics](analytics/index.md): Analytics and reporting information
- [Governance](governance/index.md): Governance and compliance documentation
- [Reference](reference/index.md): Reference materials and guides

## Recent Updates

- Added Apex Trigger best practices
- Updated User Management section
- New Flow Builder tutorials
EOF

# Create introduction and overview files
create_file "docs/introduction.md" "Introduction" "Introduction to the Salesforce platform" "overview" "user, admin, developer" "material/information-outline"
create_file "docs/overview.md" "System Overview" "Overview of the Salesforce system" "overview" "user, admin, developer" "material/view-dashboard-outline"

# Create section index files
create_index_file "docs/user/index.md" "User Documentation" "using the Salesforce platform" "user_guide" "user" "material/account-circle"
create_index_file "docs/admin/index.md" "Admin Documentation" "administering the Salesforce platform" "admin_guide" "admin" "material/shield-account"
create_index_file "docs/developer/index.md" "Developer Documentation" "developing on the Salesforce platform" "developer_guide" "developer" "material/code-braces"
create_index_file "docs/analytics/index.md" "Analytics" "analytics and reporting" "analytics" "admin, developer" "material/chart-bar"
create_index_file "docs/governance/index.md" "Governance" "governance and compliance" "governance" "admin" "material/gavel"
create_index_file "docs/reference/index.md" "Reference" "reference materials and guides" "reference" "user, admin, developer" "material/book-open-variant"

# Create subsection index files
# User section
create_index_file "docs/user/reports/index.md" "Reports" "Salesforce reporting" "user_guide" "user" "material/file-chart"

# Admin section
create_index_file "docs/admin/profiles/index.md" "Profiles" "Salesforce user profiles" "admin_guide" "admin" "material/account-cog"
create_index_file "docs/admin/security/index.md" "Security" "Salesforce security" "admin_guide" "admin" "material/security"
create_index_file "docs/admin/data/index.md" "Data Management" "managing data in Salesforce" "admin_guide" "admin" "material/database"
create_index_file "docs/admin/automation/index.md" "Automation" "Salesforce automation tools" "admin_guide" "admin" "material/robot"
create_index_file "docs/admin/integrations/index.md" "Integrations" "Salesforce integrations" "admin_guide" "admin" "material/connection"
create_index_file "docs/admin/monitoring/index.md" "Monitoring" "monitoring Salesforce usage" "admin_guide" "admin" "material/monitor-dashboard"

# Developer section
create_index_file "docs/developer/apex/index.md" "Apex" "Apex programming" "developer_guide" "developer" "material/language-java"
create_index_file "docs/developer/metadata/index.md" "Metadata" "Salesforce metadata" "developer_guide" "developer" "material/folder-cog"
create_index_file "docs/developer/lightning/index.md" "Lightning" "Lightning components" "developer_guide" "developer" "material/lightning-bolt"
create_index_file "docs/developer/api/index.md" "API" "Salesforce APIs" "developer_guide" "developer" "material/api"
create_index_file "docs/developer/debugging/index.md" "Debugging" "debugging Salesforce code" "developer_guide" "developer" "material/bug"
create_index_file "docs/developer/database/index.md" "Database" "working with the Salesforce database" "developer_guide" "developer" "material/database-cog"
create_index_file "docs/developer/deployment/index.md" "Deployment" "deploying to Salesforce" "developer_guide" "developer" "material/rocket-launch"

# Create user documentation files
create_file "docs/user/getting_started.md" "Getting Started" "Getting started with Salesforce" "user_guide" "user" "material/play-circle"
create_file "docs/user/standard_objects.md" "Standard Objects" "Overview of Salesforce standard objects" "user_guide" "user" "material/cube-outline"
create_file "docs/user/custom_objects.md" "Custom Objects" "Working with custom objects" "user_guide" "user" "material/cube"
create_file "docs/user/record_types.md" "Record Types" "Understanding record types" "user_guide" "user" "material/file-multiple"
create_file "docs/user/lightning_apps.md" "Lightning Apps" "Working with Lightning apps" "user_guide" "user" "material/application"
create_file "docs/user/reports/report_inventory.md" "Report Inventory" "Inventory of available reports" "user_guide" "user" "material/file-chart"
create_file "docs/user/key_metrics.md" "Key Metrics" "Important metrics for users" "user_guide" "user" "material/chart-line"

# Create admin documentation files
create_file "docs/admin/user_management.md" "User Management" "Managing Salesforce users" "admin_guide" "admin" "material/account-multiple"
create_file "docs/admin/permission_sets.md" "Permission Sets" "Working with permission sets" "admin_guide" "admin" "material/shield-key"
create_file "docs/admin/profiles/profile_matrix.md" "Profile Matrix" "Matrix of profile permissions" "admin_guide" "admin" "material/grid"
create_file "docs/admin/security/fls.md" "Field-Level Security" "Field-level security in Salesforce" "admin_guide" "admin" "material/lock"
create_file "docs/admin/security/sharing_rules.md" "Sharing Rules" "Setting up sharing rules" "admin_guide" "admin" "material/share-variant"
create_file "docs/admin/security/role_hierarchy.md" "Role Hierarchy" "Understanding role hierarchy" "admin_guide" "admin" "material/sitemap"
create_file "docs/admin/security/audit_trail.md" "Audit Trail" "Using the audit trail" "admin_guide" "admin" "material/history"
create_file "docs/admin/data/data_dictionary.md" "Data Dictionary" "Salesforce data dictionary" "admin_guide" "admin" "material/dictionary"
create_file "docs/admin/data/erd.md" "Entity Relationship Diagrams" "ERDs for Salesforce objects" "admin_guide" "admin" "material/graph"
create_file "docs/admin/data/duplicates.md" "Duplicates Management" "Managing duplicate records" "admin_guide" "admin" "material/content-duplicate"
create_file "docs/admin/data/data_changes.md" "Data Changes" "Tracking data changes" "admin_guide" "admin" "material/database-edit"
create_file "docs/admin/automation/flow_builder.md" "Flow Builder" "Building flows in Salesforce" "admin_guide" "admin" "material/direction-fork"
create_file "docs/admin/automation/process_builder.md" "Process Builder" "Using Process Builder" "admin_guide" "admin" "material/cog-transfer"
create_file "docs/admin/automation/workflow_rules.md" "Workflow Rules" "Setting up workflow rules" "admin_guide" "admin" "material/flask-outline"
create_file "docs/admin/automation/validation_rules.md" "Validation Rules" "Creating validation rules" "admin_guide" "admin" "material/check-decagram"
create_file "docs/admin/automation/email_alerts.md" "Email Alerts" "Configuring email alerts" "admin_guide" "admin" "material/email-alert"
create_file "docs/admin/automation/einstein_automations.md" "Einstein Automations" "Using Einstein automations" "admin_guide" "admin" "material/robot"
create_file "docs/admin/integrations/connected_apps.md" "Connected Apps" "Working with connected apps" "admin_guide" "admin" "material/puzzle"
create_file "docs/admin/integrations/api_integrations.md" "API Integrations" "Setting up API integrations" "admin_guide" "admin" "material/api"
create_file "docs/admin/integrations/mulesoft.md" "MuleSoft" "Integrating with MuleSoft" "admin_guide" "admin" "material/connection"
create_file "docs/admin/integrations/external_systems.md" "External Systems" "Connecting to external systems" "admin_guide" "admin" "material/server-network"
create_file "docs/admin/monitoring/license_usage.md" "License Usage" "Monitoring license usage" "admin_guide" "admin" "material/license"
create_file "docs/admin/monitoring/limits.md" "Limits" "Understanding Salesforce limits" "admin_guide" "admin" "material/gauge"
create_file "docs/admin/monitoring/login_history.md" "Login History" "Reviewing login history" "admin_guide" "admin" "material/login"
create_file "docs/admin/monitoring/usage_metrics.md" "Usage Metrics" "Tracking usage metrics" "admin_guide" "admin" "material/chart-areaspline"

# Create developer documentation files
create_file "docs/developer/standards.md" "Development Standards" "Salesforce development standards" "developer_guide" "developer" "material/ruler-square"
create_file "docs/developer/apex/apex_code.md" "Apex Code" "Working with Apex code" "developer_guide" "developer" "material/language-java"

# Create an advanced example file for Apex Triggers with rich formatting
cat > docs/developer/apex/apex_triggers.md << 'EOF'
---
title: Apex Triggers
description: Comprehensive guide to Apex triggers in Salesforce development
doc_type: developer_guide
audience: [developer]
status: published
last_reviewed: 2025-04-15
icon: material/lightning-bolt
code_example_lang: apex
code_example_options:
  linenums: 1
  hl_lines: "5-7 15"
tags:
  - developer
  - apex
  - triggers
---

# Apex Triggers

Apex triggers are powerful tools for executing custom logic in response to data manipulation language (DML) operations in Salesforce.

## Overview

/// info | Key Concept
Apex triggers execute before or after specific DML operations like insert, update, delete, or undelete events on Salesforce objects.
///

Triggers are essential for maintaining data integrity and implementing complex business logic.

## Trigger Context Variables

The following context variables are available in triggers:

/// tab | Trigger.new
```apex
// Access the list of new records
for(Account acc : Trigger.new) {
    System.debug('New Account: ' + acc.Name);
}
```
///

/// tab | Trigger.old
```apex
// Access the list of old records
for(Account acc : Trigger.old) {
    System.debug('Old Account: ' + acc.Name);
}
```
///

/// tab | Trigger.newMap
```apex
// Access the map of new records by Id
Map<Id, Account> newAccounts = Trigger.newMap;
System.debug('New Account Name: ' + newAccounts.get(someId).Name);
```
///

## Best Practices

/// danger | Anti-Pattern Warning
Never place SOQL queries inside loops in your triggers! This can quickly exceed Salesforce governor limits.
///

Here's an example of a well-structured trigger:

```apex {linenums="1" hl_lines="5-7 12"}
trigger AccountTrigger on Account (before insert, before update) {
    // Call handler class to execute logic
    AccountTriggerHandler.handleBeforeInsert(Trigger.new);
    
    // Example of a bad practice (don't do this):
    for(Account acc : Trigger.new) {
        List<Contact> contacts = [SELECT Id FROM Contact WHERE AccountId = :acc.Id]; // WRONG!
    }
    
    // Correct approach:
    Set<Id> accountIds = new Set<Id>();
    for(Account acc : Trigger.new) {
        accountIds.add(acc.Id);
    }
    List<Contact> contacts = [SELECT Id, AccountId FROM Contact WHERE AccountId IN :accountIds];
}
```

## Trigger Framework Diagram

```mermaid
flowchart TD
    A[DML Operation] --> B{Trigger}
    B --> C[Before Trigger]
    B --> D[After Trigger]
    C --> E[Handler Class]
    D --> E
    E --> F[Service Layer]
    F --> G[Domain Layer]
    G --> H[(Database)]
```

## Bulkification

Designing triggers to handle bulk operations is essential in Salesforce. Here's a comparison of approaches:

| Approach | Pros | Cons |
|----------|------|------|
| Individual Record Processing | Simple to understand | Not scalable |
| Bulk Processing | Efficient, handles governor limits | More complex code |
| Handler Pattern | Organized, testable | Requires more files |

## Related Topics

- [Test Classes](../test_classes.md)
- [Code Coverage](../code_coverage.md)
- [Apex Code Standards](../apex_code.md)
EOF

# Continue with more developer documentation files
create_file "docs/developer/apex/test_classes.md" "Test Classes" "Writing test classes in Apex" "developer_guide" "developer" "material/test-tube"
create_file "docs/developer/apex/code_coverage.md" "Code Coverage" "Measuring code coverage" "developer_guide" "developer" "material/percent"
create_file "docs/developer/metadata/custom_metadata.md" "Custom Metadata" "Working with custom metadata" "developer_guide" "developer" "material/table-cog"
create_file "docs/developer/metadata/custom_settings.md" "Custom Settings" "Using custom settings" "developer_guide" "developer" "material/cog-box"
create_file "docs/developer/metadata/page_layouts.md" "Page Layouts" "Configuring page layouts" "developer_guide" "developer" "material/page-layout-header"
create_file "docs/developer/lightning/lightning_components.md" "Lightning Components" "Building Lightning components" "developer_guide" "developer" "material/flash"
create_file "docs/developer/api/rest_services.md" "REST Services" "Using REST services" "developer_guide" "developer" "material/api"
create_file "docs/developer/api/soap_services.md" "SOAP Services" "Using SOAP services" "developer_guide" "developer" "material/xml"
create_file "docs/developer/api/named_credentials.md" "Named Credentials" "Setting up named credentials" "developer_guide" "developer" "material/key-chain"
create_file "docs/developer/api/api_usage.md" "API Usage" "Tracking API usage" "developer_guide" "developer" "material/graph"
create_file "docs/developer/debugging/debug_logs.md" "Debug Logs" "Working with debug logs" "developer_guide" "developer" "material/bug"
create_file "docs/developer/database/soql_queries.md" "SOQL Queries" "Writing SOQL queries" "developer_guide" "developer" "material/database-search"
create_file "docs/developer/database/field_dependencies.md" "Field Dependencies" "Managing field dependencies" "developer_guide" "developer" "material/connection-arrow"
create_file "docs/developer/database/formula_fields.md" "Formula Fields" "Creating formula fields" "developer_guide" "developer" "material/function"
create_file "docs/developer/deployment/deployment_strategy.md" "Deployment Strategy" "Planning your deployment strategy" "developer_guide" "developer" "material/rocket-launch"

# Create analytics documentation files
create_file "docs/analytics/active_users.md" "Active Users" "Tracking active users" "analytics" "admin" "material/account-group"
create_file "docs/analytics/feature_adoption.md" "Feature Adoption" "Measuring feature adoption" "analytics" "admin" "material/feature-search"
create_file "docs/analytics/data_access_logs.md" "Data Access Logs" "Analyzing data access logs" "analytics" "admin" "material/database-eye"
create_file "docs/analytics/records_touched.md" "Records Touched" "Tracking records touched" "analytics" "admin" "material/hand-touch"

# Create governance documentation files
create_file "docs/governance/regulations.md" "Regulations" "Compliance with regulations" "governance" "admin" "material/gavel"
create_file "docs/governance/security_events.md" "Security Events" "Tracking security events" "governance" "admin" "material/shield-alert"
create_file "docs/governance/vulnerability_scans.md" "Vulnerability Scans" "Running vulnerability scans" "governance" "admin" "material/scanner"
create_file "docs/governance/strategic_initiatives.md" "Strategic Initiatives" "Planning strategic initiatives" "governance" "admin" "material/lightbulb-on"

# Create reference documentation files
create_file "docs/reference/objects_fields.md" "Objects and Fields" "Reference for objects and fields" "reference" "admin, developer" "material/table-edit"
create_file "docs/reference/rules_matrix.md" "Rules Matrix" "Matrix of rules" "reference" "admin, developer" "material/matrix"
create_file "docs/reference/scheduled_jobs.md" "Scheduled Jobs" "Reference for scheduled jobs" "reference" "admin, developer" "material/clock-time-four"
create_file "docs/reference/flow_executions.md" "Flow Executions" "Tracking flow executions" "reference" "admin, developer" "material/flow"

# Create a sample snippet
mkdir -p docs/snippets
cat > docs/snippets/apex_governor_limits.md << EOF
## Governor Limits

Salesforce enforces strict governor limits to ensure the platform's multitenant architecture performs well:

- 100 SOQL queries per transaction
- 150 DML statements per transaction 
- 50,000 records retrieved by SOQL
- 10,000 records processed per transaction
EOF

# Create custom CSS file
mkdir -p docs/assets/stylesheets
cat > docs/assets/stylesheets/extra.css << 'EOF'
/* Doc type specific styling */
[data-doc-type="user_guide"] h1 {
  color: #4051b5;
  border-bottom: 2px solid #4051b5;
}

[data-doc-type="admin_guide"] h1 {
  color: #f50057;
  border-bottom: 2px solid #f50057;
}

[data-doc-type="developer_guide"] h1 {
  color: #00bfa5;
  border-bottom: 2px solid #00bfa5;
}

[data-doc-type="reference"] h1 {
  color: #ff9100;
  border-bottom: 2px solid #ff9100;
}

/* Status badges */
.doc-status {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-weight: 500;
}

.doc-status-published {
  background-color: #00c853;
  color: white;
}

.doc-status-draft {
  background-color: #ffc400;
  color: black;
}

.doc-status-deprecated {
  background-color: #ff3d00;
  color: white;
}

/* Audience banner */
.audience-banner {
  display: flex;
  gap: 8px;
  margin-bottom: 1rem;
}

.audience-tag {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 500;
}

.audience-tag-user {
  background-color: #4051b5;
  color: white;
}

.audience-tag-admin {
  background-color: #f50057;
  color: white;
}

.audience-tag-developer {
  background-color: #00bfa5;
  color: white;
}

/* Last reviewed date */
.doc-last-reviewed {
  margin-top: 3rem;
  padding-top: 0.5rem;
  border-top: 1px solid #e0e0e0;
  font-size: 0.8rem;
  color: #757575;
}

/* Enhanced admonitions */
.md-typeset .admonition,
.md-typeset details {
  border-width: 0;
  border-left-width: 4px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Enhanced code blocks */
.md-typeset pre > code {
  border-radius: 6px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* Enhanced tables */
.md-typeset table:not([class]) {
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  border-radius: 4px;
  overflow: hidden;
}

.md-typeset table:not([class]) th {
  background-color: #f5f5f5;
  color: #424242;
}
EOF

# Create custom JavaScript file
mkdir -p docs/assets/javascripts
cat > docs/assets/javascripts/extra.js << 'EOF'
document.addEventListener('DOMContentLoaded', function() {
  // Add class to body based on doc type
  const docType = document.querySelector('article[data-doc-type]')?.getAttribute('data-doc-type');
  if (docType) {
    document.body.classList.add(`doc-type-${docType}`);
  }
  
  // Add quick copy buttons to code blocks
  document.querySelectorAll('pre code').forEach((codeBlock) => {
    const copyButton = document.createElement('button');
    copyButton.className = 'copy-button';
    copyButton.textContent = 'Copy';
    
    copyButton.addEventListener('click', () => {
      navigator.clipboard.writeText(codeBlock.textContent);
      copyButton.textContent = 'Copied!';
      setTimeout(() => {
        copyButton.textContent = 'Copy';
      }, 2000);
    });
    
    const pre = codeBlock.parentNode;
    pre.style.position = 'relative';
    pre.appendChild(copyButton);
  });
});
EOF

# Create placeholder images
mkdir -p docs/assets/images
cat > docs/assets/images/placeholder-logo.svg << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
  <rect width="100" height="100" fill="#3F51B5"/>
  <text x="50" y="50" font-family="Arial" font-size="24" fill="white" text-anchor="middle" dominant-baseline="middle">LOGO</text>
</svg>
EOF

echo "Created placeholder logo"

# Copy placeholder logo to required locations
cp docs/assets/images/placeholder-logo.svg docs/assets/images/logo.svg
touch docs/assets/images/favicon.png

# Create theme overrides
mkdir -p overrides
cat > overrides/main.html << 'EOF'
{% extends "base.html" %}

{% block content %}
  <div class="md-content" data-md-component="content">
    <article class="md-content__inner md-typeset" role="main" data-doc-type="{{ page.meta.doc_type }}">
      
      {# Include audience banner if specified #}
      {% if page.meta.audience %}
        <div class="audience-banner">
          {% for audience_item in page.meta.audience %}
            <span class="audience-tag audience-tag-{{ audience_item }}">{{ audience_item }}</span>
          {% endfor %}
        </div>
      {% endif %}
      
      {# Add status badge if specified #}
      {% if page.meta.status %}
        <div class="doc-status doc-status-{{ page.meta.status }}">
          {{ config.extra.status[page.meta.status] }}
        </div>
      {% endif %}
      
      {# Include the actual content #}
      {{ page.content }}
      
      {# Add last reviewed information if available #}
      {% if page.meta.last_reviewed %}
        <div class="doc-last-reviewed">
          Last reviewed: {{ page.meta.last_reviewed }}
        </div>
      {% endif %}
      
      {# Add related content if available #}
      {% if page.meta.related_links %}
        <div class="related-content">
          <h2>Related Content</h2>
          <ul>
            {% for link in page.meta.related_links %}
              <li><a href="{{ link.url }}">{{ link.title }}</a></li>
            {% endfor %}
          </ul>
        </div>
      {% endif %}
    </article>
  </div>
{% endblock %}
EOF

# Create audience banner partial
mkdir -p overrides/partials
cat > overrides/partials/_audience_banner.html << 'EOF'
<div class="audience-banner">
  {% for audience_item in page.meta.audience %}
    <span class="audience-tag audience-tag-{{ audience_item }}">{{ audience_item }}</span>
  {% endfor %}
</div>
EOF

# Create document header partial
cat > overrides/partials/_doc_header.html << 'EOF'
<div class="doc-header">
  <h1>{{ page.meta.title }}</h1>
  {% if page.meta.description %}
    <p class="doc-description">{{ page.meta.description }}</p>
  {% endif %}
</div>
EOF

# Create mkdocs.yml
cat > mkdocs.yml << 'EOF'
# Site Information
site_name: Salesforce Documentation
site_url: https://your-domain.com/docs
site_description: Comprehensive Salesforce documentation for Users, Admins, and Developers
site_author: Your Organization

# Repository
repo_url: https://github.com/your-org/salesforce-docs
repo_name: your-org/salesforce-docs
edit_uri: edit/main/docs/

# Copyright
copyright: Copyright &copy; 2025 Your Organization

# Configuration
docs_dir: docs
site_dir: site

# Theme Configuration
theme:
  name: material
  custom_dir: overrides
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.tabs
    - navigation.tabs.sticky
    - navigation.sections
    - navigation.indexes
    - navigation.top
    - toc.follow
    - search.suggest
    - search.highlight
    - content.tabs.link
    - content.code.copy
    - content.code.annotate
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  font:
    text: Roboto
    code: Roboto Mono
  favicon: assets/images/favicon.png
  logo: assets/images/logo.svg
  icon:
    logo: logo
    repo: fontawesome/brands/github
    admonition:
      note: fontawesome/solid/note-sticky
      abstract: fontawesome/solid/book
      info: fontawesome/solid/circle-info
      tip: fontawesome/solid/lightbulb
      success: fontawesome/solid/check
      question: fontawesome/solid/circle-question
      warning: fontawesome/solid/triangle-exclamation
      failure: fontawesome/solid/bomb
      danger: fontawesome/solid/skull
      bug: fontawesome/solid/bug
      example: fontawesome/solid/flask
      quote: fontawesome/solid/quote-left

# Plugins
plugins:
  - search
  - tags
  - minify:
      minify_html: true
      minify_js: true
      minify_css: true
  - git-revision-date-localized:
      enable_creation_date: true
      type: date
  - glightbox
  - mermaid2
  - section-index

# Markdown Extensions
markdown_extensions:
  # Python Markdown Extensions
  - abbr
  - admonition
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - toc:
      permalink: true
      toc_depth: 4

  # PyMdown Extensions
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.betterem:
      smart_enable: all
  - pymdownx.caret
  - pymdownx.critic
  - pymdownx.details
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
      use_pygments: true
      pygments_style: github-dark
      linenums: true
      auto_title: true
  - pymdownx.inlinehilite
  - pymdownx.keys
  - pymdownx.magiclink:
      repo_url_shorthand: true
      user: your-org
      repo: salesforce-docs
  - pymdownx.mark
  - pymdownx.smartsymbols
  - pymdownx.snippets:
      check_paths: true
      base_path: ["docs/snippets"]
      auto_append: ["abbreviations.md"]
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
        - name: math
          class: arithmatex
          format: !!python/name:pymdownx.arithmatex.arithmatex_fenced_format
        - name: diagram
          class: diagram
          format: !!python/name:pymdownx.superfences.fence_div_format
        - name: api-ref
          class: api-reference
          format: !!python/name:pymdownx.superfences.fence_div_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
      clickable_checkbox: true
  - pymdownx.tilde
  - pymdownx.blocks.admonition
  - pymdownx.blocks.details
  - pymdownx.blocks.tab:
      alternate_style: true

# Additional Configuration
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/your-org
    - icon: fontawesome/brands/twitter
      link: https://twitter.com/your-org
  analytics:
    provider: google
    property: G-XXXXXXXXXX
  status:
    new: Recently added
    updated: Recently updated
    deprecated: Deprecated
    experimental: Experimental
  version:
    provider: mike

extra_css:
  - assets/stylesheets/extra.css

extra_javascript:
  - assets/javascripts/extra.js
  - https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js
  - https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.0.2/mermaid.min.js
  - https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.0.2/mermaid.fallback.min.js
  - https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.0.2/mermaid.init.min.js
  - https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.0.2/mermaid.min.js
  - https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.0.2/mermaid.fallback.min.js
EOF
