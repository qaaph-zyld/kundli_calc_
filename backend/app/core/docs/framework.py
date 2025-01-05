"""
Documentation Framework
PGF Protocol: DOC_001
Gate: GATE_8
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, Union, Type
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
import inspect
import ast
import re
from pathlib import Path
import json
import yaml
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

class DocType(str, Enum):
    """Documentation types"""
    API = "api"
    CODE = "code"
    ARCHITECTURE = "architecture"
    DEPLOYMENT = "deployment"
    SECURITY = "security"
    TESTING = "testing"

class DocFormat(str, Enum):
    """Documentation formats"""
    MARKDOWN = "markdown"
    HTML = "html"
    PDF = "pdf"
    YAML = "yaml"
    JSON = "json"

class DocSection(BaseModel):
    """Documentation section"""
    
    title: str
    content: str
    subsections: List['DocSection'] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Documentation(BaseModel):
    """Documentation model"""
    
    title: str
    version: str
    description: Optional[str] = None
    doc_type: DocType
    format: DocFormat
    sections: List[DocSection] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class DocGenerator:
    """Documentation generator"""
    
    def __init__(self, app: FastAPI):
        self.app = app
        self._setup_paths()
    
    def _setup_paths(self) -> None:
        """Setup documentation paths"""
        self.docs_path = Path("docs")
        self.api_docs_path = self.docs_path / "api"
        self.code_docs_path = self.docs_path / "code"
        self.arch_docs_path = self.docs_path / "architecture"
        
        # Create directories
        for path in [self.docs_path, self.api_docs_path, 
                    self.code_docs_path, self.arch_docs_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def generate_api_docs(self) -> Documentation:
        """Generate API documentation"""
        openapi_schema = get_openapi(
            title=self.app.title,
            version=self.app.version,
            openapi_version="3.0.2",
            description=self.app.description,
            routes=self.app.routes
        )
        
        # Convert OpenAPI schema to documentation sections
        sections = []
        
        # Info section
        info_section = DocSection(
            title="API Information",
            content=f"# {openapi_schema['info']['title']}\n\n"
                    f"Version: {openapi_schema['info']['version']}\n\n"
                    f"{openapi_schema['info'].get('description', '')}"
        )
        sections.append(info_section)
        
        # Endpoints section
        endpoints_section = DocSection(
            title="Endpoints",
            content="# API Endpoints\n\n",
            subsections=[]
        )
        
        for path, path_item in openapi_schema['paths'].items():
            for method, operation in path_item.items():
                endpoint_doc = DocSection(
                    title=f"{method.upper()} {path}",
                    content=self._format_endpoint_doc(operation),
                    metadata={
                        "method": method,
                        "path": path,
                        "tags": operation.get("tags", [])
                    }
                )
                endpoints_section.subsections.append(endpoint_doc)
        
        sections.append(endpoints_section)
        
        # Models section
        models_section = DocSection(
            title="Data Models",
            content="# Data Models\n\n",
            subsections=[]
        )
        
        for schema_name, schema in openapi_schema['components']['schemas'].items():
            model_doc = DocSection(
                title=schema_name,
                content=self._format_model_doc(schema_name, schema),
                metadata={"schema": schema}
            )
            models_section.subsections.append(model_doc)
        
        sections.append(models_section)
        
        # Create documentation
        api_docs = Documentation(
            title=f"{self.app.title} API Documentation",
            version=self.app.version,
            description=self.app.description,
            doc_type=DocType.API,
            format=DocFormat.MARKDOWN,
            sections=sections,
            metadata={
                "generated_at": datetime.utcnow().isoformat(),
                "openapi_version": openapi_schema['openapi']
            }
        )
        
        # Save documentation
        self._save_documentation(api_docs, self.api_docs_path / "api_docs.md")
        
        return api_docs
    
    def generate_code_docs(self, source_dir: Path) -> Documentation:
        """Generate code documentation"""
        sections = []
        
        # Process Python files
        for py_file in source_dir.rglob("*.py"):
            with open(py_file, "r") as f:
                module = ast.parse(f.read())
            
            module_doc = self._process_module(module, py_file)
            if module_doc:
                sections.append(module_doc)
        
        code_docs = Documentation(
            title="Code Documentation",
            version="1.0.0",
            doc_type=DocType.CODE,
            format=DocFormat.MARKDOWN,
            sections=sections,
            metadata={
                "generated_at": datetime.utcnow().isoformat(),
                "source_dir": str(source_dir)
            }
        )
        
        # Save documentation
        self._save_documentation(code_docs, self.code_docs_path / "code_docs.md")
        
        return code_docs
    
    def generate_architecture_docs(self) -> Documentation:
        """Generate architecture documentation"""
        sections = [
            DocSection(
                title="System Architecture",
                content="""# System Architecture

## Overview
This document describes the high-level architecture of the Vedic Astrology System.

## Components
1. FastAPI Backend
   - API Layer
   - Service Layer
   - Data Layer
   - Core Components

2. Frontend
   - React Components
   - State Management
   - API Integration

3. Infrastructure
   - Deployment
   - Scaling
   - Monitoring""",
                subsections=[
                    DocSection(
                        title="Backend Architecture",
                        content=self._generate_backend_arch_doc()
                    ),
                    DocSection(
                        title="Data Flow",
                        content=self._generate_data_flow_doc()
                    ),
                    DocSection(
                        title="Security Architecture",
                        content=self._generate_security_arch_doc()
                    )
                ]
            )
        ]
        
        arch_docs = Documentation(
            title="Architecture Documentation",
            version="1.0.0",
            doc_type=DocType.ARCHITECTURE,
            format=DocFormat.MARKDOWN,
            sections=sections,
            metadata={
                "generated_at": datetime.utcnow().isoformat()
            }
        )
        
        # Save documentation
        self._save_documentation(arch_docs, self.arch_docs_path / "architecture_docs.md")
        
        return arch_docs
    
    def _format_endpoint_doc(self, operation: Dict[str, Any]) -> str:
        """Format endpoint documentation"""
        doc = f"## {operation.get('summary', 'No summary')}\n\n"
        
        if operation.get('description'):
            doc += f"{operation['description']}\n\n"
        
        if operation.get('parameters'):
            doc += "### Parameters\n\n"
            for param in operation['parameters']:
                doc += f"- `{param['name']}` ({param['in']}): {param.get('description', 'No description')}\n"
            doc += "\n"
        
        if operation.get('requestBody'):
            doc += "### Request Body\n\n"
            content = operation['requestBody']['content']
            for media_type, schema in content.items():
                doc += f"**Media Type**: `{media_type}`\n\n"
                if 'schema' in schema:
                    doc += "**Schema**:\n```json\n"
                    doc += json.dumps(schema['schema'], indent=2)
                    doc += "\n```\n\n"
        
        if operation.get('responses'):
            doc += "### Responses\n\n"
            for status, response in operation['responses'].items():
                doc += f"#### {status}\n\n"
                if response.get('description'):
                    doc += f"{response['description']}\n\n"
                if 'content' in response:
                    for media_type, schema in response['content'].items():
                        doc += f"**Media Type**: `{media_type}`\n\n"
                        if 'schema' in schema:
                            doc += "**Schema**:\n```json\n"
                            doc += json.dumps(schema['schema'], indent=2)
                            doc += "\n```\n\n"
        
        return doc
    
    def _format_model_doc(self, name: str, schema: Dict[str, Any]) -> str:
        """Format model documentation"""
        doc = f"## {name}\n\n"
        
        if schema.get('description'):
            doc += f"{schema['description']}\n\n"
        
        if schema.get('properties'):
            doc += "### Properties\n\n"
            for prop_name, prop in schema['properties'].items():
                doc += f"- `{prop_name}`"
                if prop.get('type'):
                    doc += f" ({prop['type']})"
                if prop.get('description'):
                    doc += f": {prop['description']}"
                doc += "\n"
        
        return doc
    
    def _process_module(self, module: ast.Module, file_path: Path) -> Optional[DocSection]:
        """Process Python module"""
        # Get module docstring
        module_doc = ast.get_docstring(module)
        if not module_doc:
            return None
        
        # Process classes and functions
        subsections = []
        for node in module.body:
            if isinstance(node, ast.ClassDef):
                class_doc = self._process_class(node)
                if class_doc:
                    subsections.append(class_doc)
            elif isinstance(node, ast.FunctionDef):
                func_doc = self._process_function(node)
                if func_doc:
                    subsections.append(func_doc)
        
        return DocSection(
            title=file_path.stem,
            content=f"# {file_path.stem}\n\n{module_doc}",
            subsections=subsections,
            metadata={"file_path": str(file_path)}
        )
    
    def _process_class(self, node: ast.ClassDef) -> Optional[DocSection]:
        """Process Python class"""
        class_doc = ast.get_docstring(node)
        if not class_doc:
            return None
        
        # Process methods
        subsections = []
        for body_node in node.body:
            if isinstance(body_node, ast.FunctionDef):
                method_doc = self._process_function(body_node)
                if method_doc:
                    subsections.append(method_doc)
        
        return DocSection(
            title=node.name,
            content=f"## Class: {node.name}\n\n{class_doc}",
            subsections=subsections,
            metadata={"type": "class"}
        )
    
    def _process_function(self, node: ast.FunctionDef) -> Optional[DocSection]:
        """Process Python function"""
        func_doc = ast.get_docstring(node)
        if not func_doc:
            return None
        
        return DocSection(
            title=node.name,
            content=f"### {'Method' if node.name.startswith('_') else 'Function'}: {node.name}\n\n{func_doc}",
            metadata={"type": "function"}
        )
    
    def _generate_backend_arch_doc(self) -> str:
        """Generate backend architecture documentation"""
        return """## Backend Architecture

### API Layer
- FastAPI application
- Route handlers
- Request/Response models
- Middleware

### Service Layer
- Business logic
- Service coordination
- External integrations

### Data Layer
- Data models
- Repositories
- Database interactions

### Core Components
- Security
- Caching
- Performance monitoring
- Testing framework"""
    
    def _generate_data_flow_doc(self) -> str:
        """Generate data flow documentation"""
        return """## Data Flow

1. Request Flow
   - Client request
   - Authentication/Authorization
   - Input validation
   - Business logic
   - Response formatting

2. Data Processing
   - Validation pipeline
   - Transformation pipeline
   - Enrichment pipeline
   - Storage pipeline

3. Caching Strategy
   - Cache levels
   - Invalidation rules
   - Performance optimization"""
    
    def _generate_security_arch_doc(self) -> str:
        """Generate security architecture documentation"""
        return """## Security Architecture

1. Authentication
   - JWT tokens
   - Token validation
   - Session management

2. Authorization
   - Role-based access control
   - Permission management
   - Resource protection

3. Data Protection
   - Input sanitization
   - Output encoding
   - Encryption
   - Secure communication"""
    
    def _save_documentation(self, doc: Documentation, path: Path) -> None:
        """Save documentation to file"""
        if doc.format == DocFormat.MARKDOWN:
            content = self._generate_markdown(doc)
            path = path.with_suffix('.md')
        elif doc.format == DocFormat.HTML:
            content = self._generate_html(doc)
            path = path.with_suffix('.html')
        elif doc.format == DocFormat.YAML:
            content = yaml.dump(doc.dict())
            path = path.with_suffix('.yaml')
        else:
            content = doc.json(indent=2)
            path = path.with_suffix('.json')
        
        with open(path, 'w') as f:
            f.write(content)
    
    def _generate_markdown(self, doc: Documentation) -> str:
        """Generate markdown documentation"""
        content = [
            f"# {doc.title}",
            f"\nVersion: {doc.version}",
            f"\n{doc.description or ''}\n"
        ]
        
        for section in doc.sections:
            content.append(f"\n{section.content}")
            for subsection in section.subsections:
                content.append(f"\n{subsection.content}")
        
        return "\n".join(content)
    
    def _generate_html(self, doc: Documentation) -> str:
        """Generate HTML documentation"""
        import markdown
        md_content = self._generate_markdown(doc)
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{doc.title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        pre {{
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
        }}
        code {{
            background-color: #f5f5f5;
            padding: 2px 5px;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    {markdown.markdown(md_content)}
</body>
</html>
"""
