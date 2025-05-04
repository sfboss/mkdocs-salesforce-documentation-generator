#!/bin/bash

# This script organizes the MkDocs Salesforce documentation structure
# Execute with: bash organize_docs.sh

# Create main directory structure
mkdir -p docs/{data-model,automation,security,integrations,customization,administration,development,monitoring}/
mkdir -p templates
mkdir -p scripts
mkdir -p data

# Create data model subdirectories
mkdir -p docs/data-model/{objects,fields,relationships}/

# Create automation subdirectories
mkdir -p docs/automation/{flows,processes,triggers,validation-rules,workflows}/

# Create security subdirectories
mkdir -p docs/security/{profiles,permissions,sharing}/

# Create integrations subdirectories  
mkdir -p docs/integrations/{apis,middleware,external-services}/

# Create customization subdirectories
mkdir -p docs/customization/{layouts,apps,components}/

# Create administration subdirectories
mkdir -p docs/administration/{users,licenses,settings}/

# Create development subdirectories
mkdir -p docs/development/{apex,testing,deployments}/

# Create monitoring subdirectories
mkdir -p docs/monitoring/{logs,metrics,reports}/

# Move existing content to the new structure
find . -name "*.md" -not -path "./site/*" -not -path "./venv/*" | while read file; do
  # Determine destination based on file content/name
  filename=$(basename "$file")
  if [[ "$file" == *"/data-model/"* ]]; then
    if [[ "$file" == *"/objects/"* ]]; then
      mkdir -p docs/data-model/objects/
      cp "$file" docs/data-model/objects/
    elif [[ "$file" == *"/fields/"* ]]; then
      mkdir -p docs/data-model/fields/
      cp "$file" docs/data-model/fields/
    elif [[ "$file" == *"/relationships/"* ]]; then
      mkdir -p docs/data-model/relationships/
      cp "$file" docs/data-model/relationships/
    else
      cp "$file" docs/data-model/
    fi
  elif [[ "$file" == *"/automation/"* ]]; then
    cp "$file" docs/automation/
  elif [[ "$file" == *"/security/"* ]]; then
    cp "$file" docs/security/
  elif [[ "$file" == *"/integrations/"* ]]; then
    cp "$file" docs/integrations/
  elif [[ "$file" == *"/customization/"* ]]; then
    cp "$file" docs/customization/
  elif [[ "$file" == *"/administration/"* ]]; then
    cp "$file" docs/administration/
  elif [[ "$file" == *"/development/"* ]]; then
    cp "$file" docs/development/
  elif [[ "$file" == *"/monitoring/"* ]]; then
    cp "$file" docs/monitoring/
  elif [[ "$filename" == "index.md" ]]; then
    cp "$file" docs/
  fi
done

# Move templates
find . -name "*.j2" -not -path "./site/*" -not -path "./venv/*" | while read file; do
  cp "$file" templates/
done

# Move Python scripts
find . -name "*.py" -not -path "./site/*" -not -path "./venv/*" | while read file; do
  cp "$file" scripts/
done

echo "Documentation structure organized. Review the new structure in docs/ and templates/ directories."
