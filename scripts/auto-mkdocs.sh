#!/bin/bash

# Exit on error
set -e

# Configuration
PROJECT_NAME="salesforce-org-documentation"
DOCS_DIR="docs"

# Create project directory
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install mkdocs mkdocs-material mkdocs-mermaid2-plugin mkdocs-git-revision-date-plugin mkdocs-awesome-pages-plugin mkdocs-macros-plugin

# Initialize MkDocs
mkdocs new .

# Create documentation structure
mkdir -p docs/{data-model,automation,security,integrations,customization,administration,development,monitoring}

# Create placeholder files for each section
# Data Model
mkdir -p docs/data-model/{objects,relationships,fields}
touch docs/data-model/objects/standard-objects.md
touch docs/data-model/objects/custom-objects.md
touch docs/data-model/relationships/erd.md
touch docs/data-model/fields/data-dictionary.md
touch docs/data-model/fields/formula-fields.md
touch docs/data-model/fields/field-dependencies.md

# Automation
mkdir -p docs/automation/{flows,processes,triggers,validation-rules,workflows}
touch docs/automation/flows/record-triggered.md
touch docs/automation/flows/scheduled.md
touch docs/automation/processes/process-builder.md
touch docs/automation/triggers/apex-triggers.md
touch docs/automation/validation-rules/rules-matrix.md
touch docs/automation/workflows/email-alerts.md

# Security
mkdir -p docs/security/{profiles,permissions,sharing}
touch docs/security/profiles/profile-matrix.md
touch docs/security/permissions/permission-sets.md
touch docs/security/sharing/sharing-rules.md
touch docs/security/sharing/role-hierarchy.md

# Integrations
mkdir -p docs/integrations/{apis,middleware,external-services}
touch docs/integrations/apis/rest-services.md
touch docs/integrations/apis/soap-services.md
touch docs/integrations/middleware/mulesoft.md
touch docs/integrations/external-services/named-credentials.md

# Customization
mkdir -p docs/customization/{layouts,apps,components}
touch docs/customization/layouts/page-layouts.md
touch docs/customization/layouts/record-types.md
touch docs/customization/apps/lightning-apps.md
touch docs/customization/components/lightning-components.md

# Administration
mkdir -p docs/administration/{users,licenses,settings}
touch docs/administration/users/user-management.md
touch docs/administration/licenses/license-usage.md
touch docs/administration/settings/custom-settings.md
touch docs/administration/settings/custom-metadata.md

# Development
mkdir -p docs/development/{apex,testing,deployments}
touch docs/development/apex/code-coverage.md
touch docs/development/testing/test-classes.md
touch docs/development/deployments/deployment-strategy.md

# Monitoring
mkdir -p docs/monitoring/{logs,metrics,reports}
touch docs/monitoring/logs/debug-logs.md
touch docs/monitoring/metrics/usage-metrics.md
touch docs/monitoring/reports/report-inventory.md

# Create mkdocs.yml
cat > mkdocs.yml << 'EOL'
site_name: Salesforce Org Documentation
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.highlight
    - search.share
    - content.code.copy
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/toggle-switch
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/toggle-switch-off-outline
        name: Switch to light mode

plugins:
  - search
  - mermaid2
  - git-revision-date
  - awesome-pages
  - macros

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.tabbed:
      alternate_style: true
  - tables
  - toc:
      permalink: true

nav:
  - Home: index.md
  - Data Model:
    - Objects:
      - Standard Objects: data-model/objects/standard-objects.md
      - Custom Objects: data-model/objects/custom-objects.md
    - Relationships:
      - ERD: data-model/relationships/erd.md
    - Fields:
      - Data Dictionary: data-model/fields/data-dictionary.md
      - Formula Fields: data-model/fields/formula-fields.md
      - Field Dependencies: data-model/fields/field-dependencies.md
  - Automation:
    - Flows:
      - Record-Triggered: automation/flows/record-triggered.md
      - Scheduled: automation/flows/scheduled.md
    - Process Builder: automation/processes/process-builder.md
    - Triggers: automation/triggers/apex-triggers.md
    - Validation Rules: automation/validation-rules/rules-matrix.md
    - Workflows: automation/workflows/email-alerts.md
  - Security:
    - Profiles: security/profiles/profile-matrix.md
    - Permissions: security/permissions/permission-sets.md
    - Sharing:
      - Sharing Rules: security/sharing/sharing-rules.md
      - Role Hierarchy: security/sharing/role-hierarchy.md
  - Integrations:
    - APIs:
      - REST Services: integrations/apis/rest-services.md
      - SOAP Services: integrations/apis/soap-services.md
    - Middleware: integrations/middleware/mulesoft.md
    - External Services: integrations/external-services/named-credentials.md
  - Customization:
    - Layouts:
      - Page Layouts: customization/layouts/page-layouts.md
      - Record Types: customization/layouts/record-types.md
    - Apps: customization/apps/lightning-apps.md
    - Components: customization/components/lightning-components.md
  - Administration:
    - Users: administration/users/user-management.md
    - Licenses: administration/licenses/license-usage.md
    - Settings:
      - Custom Settings: administration/settings/custom-settings.md
      - Custom Metadata: administration/settings/custom-metadata.md
  - Development:
    - Apex: development/apex/code-coverage.md
    - Testing: development/testing/test-classes.md
    - Deployments: development/deployments/deployment-strategy.md
  - Monitoring:
    - Logs: monitoring/logs/debug-logs.md
    - Metrics: monitoring/metrics/usage-metrics.md
    - Reports: monitoring/reports/report-inventory.md

EOL

# Create index.md with template content
cat > docs/index.md << 'EOL'
# Salesforce Org Documentation

Welcome to the comprehensive documentation for our Salesforce organization. This documentation provides detailed information about our implementation, customizations, and best practices.

## Documentation Structure

### Data Model
- Complete object model documentation
- Field-level details and relationships
- ERD diagrams and dependencies

### Automation
- Flow and Process Builder inventory
- Validation rules and workflows
- Trigger framework and implementation

### Security
- Profile and permission set matrix
- Sharing model documentation
- Security best practices

### Integrations
- API documentation
- Integration patterns
- External system connections

### Customization
- Page layouts and record types
- Lightning components
- Custom applications

### Administration
- User management
- License tracking
- Org configuration

### Development
- Apex code documentation
- Test coverage
- Deployment procedures

### Monitoring
- System logs
- Usage metrics
- Reports and dashboards

## Getting Started

Use the navigation menu to explore different aspects of the organization. Each section contains detailed documentation, diagrams, and best practices.

EOL

# Create template for placeholder pages
for file in $(find docs -name "*.md" ! -name "index.md"); do
  filename=$(basename "$file" .md)
  title=$(echo "$filename" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++)sub(/./,toupper(substr($i,1,1)),$i)}1')
  
  cat > "$file" << EOL
# $title

## Overview

[Provide overview of $title]

## Details

[Add specific details about $title]

## Related Items

[List related components or documentation]

## Best Practices

[Document best practices for $title]

## References

[Add relevant references and links]
EOL
done

# Initialize git repository
git init
touch .gitignore
echo "venv/" >> .gitignore
echo "site/" >> .gitignore

# Create README
cat > README.md << 'EOL'
# Salesforce Org Documentation

This repository contains the comprehensive documentation for our Salesforce organization, built using MkDocs.

## Setup

1. Clone this repository
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the documentation locally: `mkdocs serve`

## Structure

The documentation is organized into the following main sections:

- Data Model
- Automation
- Security
- Integrations
- Customization
- Administration
- Development
- Monitoring

## Contributing

1. Create a new branch for your changes
2. Make your updates
3. Submit a pull request

## Building

To build the documentation site:

```bash
mkdocs build
```

The built site will be in the `site` directory.
EOL

# Create requirements.txt
cat > requirements.txt << 'EOL'
mkdocs
mkdocs-material
mkdocs-mermaid2-plugin
mkdocs-git-revision-date-plugin
mkdocs-awesome-pages-plugin
mkdocs-macros-plugin
EOL

echo "Documentation setup complete! To start the documentation server:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run: mkdocs serve"
echo "3. Visit: http://127.0.0.1:8000"
