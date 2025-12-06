"""
Design Phase Module - Architecture and technical design tools.

This module provides tools for:
- Architecture design and diagrams
- Component design
- API contract definition
- Data model design
- User flow mapping
- File structure planning
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .core import Spec, Component, DataEntity, APIEndpoint
from .utils import (
    Colors, print_header, print_subheader, print_section, print_tip,
    print_success, print_warning, print_info, get_input, get_choice,
    get_yes_no, format_list, format_table
)


# Architecture patterns and their characteristics
ARCHITECTURE_PATTERNS = {
    "monolith": {
        "name": "Monolithic",
        "description": "Single deployable unit, simpler to develop and deploy",
        "best_for": ["Small to medium projects", "Solo developers", "Quick MVPs"],
        "components": ["Application", "Database"],
    },
    "layered": {
        "name": "Layered (N-Tier)",
        "description": "Separated into presentation, business, and data layers",
        "best_for": ["Traditional web apps", "Clear separation of concerns"],
        "components": ["Presentation Layer", "Business Layer", "Data Layer", "Database"],
    },
    "microservices": {
        "name": "Microservices",
        "description": "Independent services communicating via APIs",
        "best_for": ["Large teams", "Scalable systems", "Complex domains"],
        "components": ["API Gateway", "Service A", "Service B", "Message Queue", "Database(s)"],
    },
    "serverless": {
        "name": "Serverless",
        "description": "Functions as a service, no server management",
        "best_for": ["Event-driven systems", "Variable workloads", "Cost optimization"],
        "components": ["Functions", "API Gateway", "Storage", "Event Sources"],
    },
    "jamstack": {
        "name": "JAMstack",
        "description": "JavaScript, APIs, Markup - static first approach",
        "best_for": ["Websites", "Blogs", "Marketing sites"],
        "components": ["Static Site", "CDN", "API Services", "Headless CMS"],
    },
    "event-driven": {
        "name": "Event-Driven",
        "description": "Components communicate through events",
        "best_for": ["Real-time systems", "Decoupled architectures"],
        "components": ["Event Producers", "Event Bus", "Event Consumers", "Event Store"],
    }
}

# Project type to architecture mapping
PROJECT_ARCHITECTURES = {
    "CLI Tool": ["monolith"],
    "Web App (Full-stack)": ["monolith", "layered", "jamstack"],
    "Web App (Frontend only)": ["jamstack"],
    "API/Backend Service": ["monolith", "layered", "microservices"],
    "Desktop App": ["monolith", "layered"],
    "Mobile App": ["layered"],
    "Browser Extension": ["monolith"],
    "Library/Package": ["monolith"],
    "Automation Script": ["monolith"],
    "SaaS Application": ["microservices", "serverless", "layered"],
}

# Tech stack suggestions
TECH_STACKS = {
    "CLI Tool": {
        "backend": ["Python", "Node.js", "Go", "Rust"],
        "tools": ["argparse", "click", "commander.js"]
    },
    "Web App (Full-stack)": {
        "frontend": ["React", "Vue", "Svelte", "Next.js", "Nuxt"],
        "backend": ["Node.js/Express", "Python/FastAPI", "Python/Django", "Go/Gin"],
        "database": ["PostgreSQL", "MongoDB", "SQLite", "MySQL"],
        "infrastructure": ["Vercel", "Railway", "Docker", "AWS"]
    },
    "API/Backend Service": {
        "backend": ["Python/FastAPI", "Node.js/Express", "Go/Gin", "Rust/Actix"],
        "database": ["PostgreSQL", "MongoDB", "Redis", "SQLite"],
        "infrastructure": ["Docker", "Kubernetes", "AWS Lambda", "Railway"]
    },
}


class DesignPhase:
    """
    Handles the design phase of spec creation.
    
    Guides users through technical design decisions including
    architecture, components, data models, and APIs.
    """
    
    def __init__(self, spec: Spec):
        self.spec = spec
    
    def run_full_design(self) -> Spec:
        """Run the complete design workflow."""
        print_header("Design Phase", "🎨")
        print("Let's design the technical architecture of your project.\n")
        
        self.choose_project_type()
        self.choose_architecture()
        self.choose_tech_stack()
        self.design_components()
        self.design_data_model()
        self.design_api()
        self.map_user_flows()
        self.plan_file_structure()
        self.generate_architecture_diagram()
        
        print_success("Design phase complete!")
        return self.spec
    
    def choose_project_type(self):
        """Choose the project type."""
        print_subheader("Project Type", "📦")
        
        project_types = [
            "CLI Tool",
            "Web App (Full-stack)",
            "Web App (Frontend only)", 
            "API/Backend Service",
            "Desktop App",
            "Mobile App",
            "Browser Extension",
            "Library/Package",
            "Automation Script",
            "SaaS Application",
            "Other"
        ]
        
        self.spec.project_type = get_choice(
            "What type of project is this?",
            project_types
        )
        
        if self.spec.project_type == "Other":
            self.spec.project_type = get_input("Describe your project type:")
    
    def choose_architecture(self):
        """Choose architecture pattern."""
        print_subheader("Architecture Pattern", "🏗️")
        
        # Get suggested architectures based on project type
        suggested = PROJECT_ARCHITECTURES.get(self.spec.project_type, ["monolith"])
        
        print("Architecture patterns suited for your project type:\n")
        
        options = []
        for arch_key in suggested:
            arch = ARCHITECTURE_PATTERNS.get(arch_key, {})
            options.append(f"{arch.get('name', arch_key)} - {arch.get('description', '')}")
        
        options.append("Other (I'll describe)")
        
        choice = get_choice("Select architecture:", options)
        
        if "Other" in choice:
            self.spec.architecture_style = get_input("Describe your architecture:")
        else:
            # Extract architecture name
            arch_name = choice.split(" - ")[0]
            self.spec.architecture_style = arch_name
            
            # Find the architecture key
            for key, arch in ARCHITECTURE_PATTERNS.items():
                if arch['name'] == arch_name:
                    print(f"\n{Colors.DIM}Best for: {', '.join(arch['best_for'])}{Colors.END}")
                    print(f"{Colors.DIM}Typical components: {', '.join(arch['components'])}{Colors.END}")
                    break
    
    def choose_tech_stack(self):
        """Choose the technology stack."""
        print_subheader("Technology Stack", "🔧")
        
        # Get suggestions based on project type
        suggestions = TECH_STACKS.get(self.spec.project_type, {})
        
        tech_stack = {
            "frontend": [],
            "backend": [],
            "database": [],
            "infrastructure": [],
            "tools": []
        }
        
        # Frontend
        if suggestions.get("frontend"):
            print_section("Frontend")
            frontend = get_choice(
                "Frontend technology:",
                suggestions["frontend"] + ["None", "Other"],
                allow_multiple=True
            )
            if "Other" in frontend:
                other = get_input("Specify frontend:")
                frontend = [f for f in frontend if f not in ["None", "Other"]]
                frontend.append(other)
            tech_stack["frontend"] = [f for f in frontend if f != "None"]
        
        # Backend
        if suggestions.get("backend"):
            print_section("Backend")
            backend = get_choice(
                "Backend technology:",
                suggestions["backend"] + ["None", "Other"],
                allow_multiple=True
            )
            if "Other" in backend:
                other = get_input("Specify backend:")
                backend = [b for b in backend if b not in ["None", "Other"]]
                backend.append(other)
            tech_stack["backend"] = [b for b in backend if b != "None"]
        
        # Database
        if suggestions.get("database"):
            print_section("Database")
            db = get_choice(
                "Database:",
                suggestions["database"] + ["None", "Other"]
            )
            if db == "Other":
                db = get_input("Specify database:")
            if db != "None":
                tech_stack["database"] = [db]
        
        # Infrastructure
        if suggestions.get("infrastructure"):
            print_section("Infrastructure / Hosting")
            infra = get_choice(
                "Deployment platform:",
                suggestions["infrastructure"] + ["TBD", "Other"]
            )
            if infra == "Other":
                infra = get_input("Specify platform:")
            if infra != "TBD":
                tech_stack["infrastructure"] = [infra]
        
        # Additional tools
        if get_yes_no("Specify additional tools/libraries?", default=False):
            tools = get_input("Additional tools (comma-separated):")
            tech_stack["tools"] = [t.strip() for t in tools.split(",") if t.strip()]
        
        self.spec.tech_stack = tech_stack
    
    def design_components(self):
        """Design system components."""
        print_subheader("Component Design", "🧩")
        
        if not get_yes_no("Design system components?", default=True):
            return
        
        print_tip("Components are the main building blocks of your system")
        
        # Suggest components based on architecture
        arch_key = None
        for key, arch in ARCHITECTURE_PATTERNS.items():
            if arch['name'] == self.spec.architecture_style:
                arch_key = key
                break
        
        if arch_key:
            suggested = ARCHITECTURE_PATTERNS[arch_key].get('components', [])
            print(f"\n{Colors.DIM}Suggested components for {self.spec.architecture_style}: {', '.join(suggested)}{Colors.END}\n")
        
        component_num = 0
        while True:
            component_num += 1
            print(f"\n{Colors.CYAN}Component #{component_num}{Colors.END}")
            
            name = get_input("Component name:")
            description = get_input("Description (what does it do?):")
            
            comp_type = get_choice(
                "Component type:",
                ["Frontend", "Backend", "Database", "Service", "Library", "Infrastructure", "Other"]
            )
            
            technologies = get_input("Technologies used (comma-separated):", required=False)
            tech_list = [t.strip() for t in technologies.split(",") if t.strip()]
            
            responsibilities = get_input("Main responsibilities (one per line):", multiline=True, required=False)
            resp_list = [r.strip() for r in responsibilities.split("\n") if r.strip()]
            
            component = Component(
                name=name,
                description=description,
                type=comp_type.lower(),
                technologies=tech_list,
                responsibilities=resp_list
            )
            self.spec.components.append(component)
            
            if not get_yes_no("Add another component?", default=component_num < 3):
                break
    
    def design_data_model(self):
        """Design the data model."""
        print_subheader("Data Model Design", "💾")
        
        needs_data = get_yes_no("Does this project manage persistent data?", default=True)
        if not needs_data:
            return
        
        print_tip("Define the main entities/models in your system")
        
        entity_num = 0
        while True:
            entity_num += 1
            print(f"\n{Colors.CYAN}Entity #{entity_num}{Colors.END}")
            
            name = get_input("Entity name (e.g., User, Product, Order):")
            description = get_input("Description:")
            
            # Fields
            print(f"\nDefine fields for {name}:")
            print(f"{Colors.DIM}Format: field_name: type (e.g., 'email: string', 'age: integer'){Colors.END}")
            
            fields = []
            fields_input = get_input("Fields (one per line):", multiline=True)
            for field_str in fields_input.split("\n"):
                if ":" in field_str:
                    parts = field_str.split(":", 1)
                    fields.append({
                        "name": parts[0].strip(),
                        "type": parts[1].strip()
                    })
                elif field_str.strip():
                    fields.append({
                        "name": field_str.strip(),
                        "type": "string"
                    })
            
            # Relationships
            relationships = []
            if get_yes_no("Does this entity have relationships?", default=False):
                rels = get_input(
                    "Relationships (e.g., 'has many Orders', 'belongs to User'):",
                    multiline=True
                )
                relationships = [r.strip() for r in rels.split("\n") if r.strip()]
            
            entity = DataEntity(
                name=name,
                description=description,
                fields=fields,
                relationships=relationships
            )
            self.spec.data_entities.append(entity)
            
            if not get_yes_no("Add another entity?", default=entity_num < 3):
                break
    
    def design_api(self):
        """Design the API."""
        print_subheader("API Design", "🔌")
        
        has_api = get_yes_no("Does this project have an API?", default=True)
        if not has_api:
            return
        
        print_tip("Define the main API endpoints")
        
        endpoint_num = 0
        while True:
            endpoint_num += 1
            print(f"\n{Colors.CYAN}Endpoint #{endpoint_num}{Colors.END}")
            
            method = get_choice(
                "HTTP Method:",
                ["GET", "POST", "PUT", "PATCH", "DELETE"]
            )
            
            path = get_input("Path (e.g., /api/users, /api/products/:id):")
            description = get_input("Description:")
            
            auth_required = get_yes_no("Requires authentication?", default=False)
            
            # Request body for POST/PUT/PATCH
            request_body = None
            if method in ["POST", "PUT", "PATCH"]:
                if get_yes_no("Define request body?", default=True):
                    print(f"{Colors.DIM}Describe the request body structure:{Colors.END}")
                    body = get_input("Request body:", multiline=True)
                    request_body = {"description": body}
            
            # Response
            response = None
            if get_yes_no("Define response?", default=True):
                print(f"{Colors.DIM}Describe the response structure:{Colors.END}")
                resp = get_input("Response:", multiline=True)
                response = {"description": resp}
            
            endpoint = APIEndpoint(
                method=method,
                path=path,
                description=description,
                request_body=request_body,
                response=response,
                auth_required=auth_required
            )
            self.spec.api_endpoints.append(endpoint)
            
            if not get_yes_no("Add another endpoint?", default=endpoint_num < 5):
                break
    
    def map_user_flows(self):
        """Map out user flows."""
        print_subheader("User Flows", "🚶")
        
        if not get_yes_no("Define user flows?", default=True):
            return
        
        print_tip("User flows describe how users interact with your system")
        
        flow_num = 0
        while True:
            flow_num += 1
            print(f"\n{Colors.CYAN}User Flow #{flow_num}{Colors.END}")
            
            name = get_input("Flow name (e.g., 'User Registration', 'Checkout'):")
            description = get_input("Brief description:")
            
            print(f"\nDescribe the steps in this flow:")
            print(f"{Colors.DIM}e.g., '1. User visits homepage', '2. Clicks sign up'{Colors.END}")
            steps = get_input("Steps:", multiline=True)
            
            # Parse steps
            step_list = []
            for step in steps.split("\n"):
                if step.strip():
                    step_list.append(step.strip())
            
            self.spec.user_flows.append({
                "name": name,
                "description": description,
                "steps": step_list
            })
            
            if not get_yes_no("Add another user flow?", default=flow_num < 2):
                break
    
    def plan_file_structure(self):
        """Plan the file/folder structure."""
        print_subheader("File Structure", "📁")
        
        if not get_yes_no("Define file structure?", default=True):
            return
        
        print_tip("Outline the project's folder and file organization")
        
        # Suggest based on project type
        structures = self._get_suggested_structure()
        
        if structures and get_yes_no("Use suggested structure as starting point?", default=True):
            print(f"\n{Colors.DIM}Suggested structure:{Colors.END}")
            print(structures)
            
            if get_yes_no("\nModify this structure?", default=False):
                modified = get_input("Your file structure:", multiline=True)
                self.spec.file_structure = modified
            else:
                self.spec.file_structure = structures
        else:
            print("\nEnter your file structure:")
            print(f"{Colors.DIM}Use indentation to show hierarchy{Colors.END}")
            self.spec.file_structure = get_input("File structure:", multiline=True)
    
    def _get_suggested_structure(self) -> str:
        """Get suggested file structure based on project type."""
        structures = {
            "CLI Tool": """project/
├── src/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── core.py
│   └── utils.py
├── tests/
│   └── test_core.py
├── README.md
├── pyproject.toml
└── LICENSE""",
            
            "Web App (Full-stack)": """project/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── styles/
│   │   └── App.jsx
│   ├── public/
│   └── package.json
├── backend/
│   ├── src/
│   │   ├── routes/
│   │   ├── models/
│   │   ├── services/
│   │   └── app.py
│   └── requirements.txt
├── docker-compose.yml
└── README.md""",
            
            "API/Backend Service": """project/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   └── middleware/
│   ├── models/
│   ├── services/
│   ├── utils/
│   └── app.py
├── tests/
│   ├── unit/
│   └── integration/
├── config/
├── migrations/
├── Dockerfile
├── requirements.txt
└── README.md""",
            
            "Library/Package": """project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/
├── docs/
├── examples/
├── pyproject.toml
├── README.md
└── LICENSE"""
        }
        
        return structures.get(self.spec.project_type, "")
    
    def generate_architecture_diagram(self):
        """Generate architecture diagram in Mermaid format."""
        print_subheader("Architecture Diagram", "📊")
        
        if not get_yes_no("Generate architecture diagram?", default=True):
            return
        
        print_tip("We'll create a Mermaid diagram you can render anywhere")
        
        # Auto-generate based on components
        if self.spec.components:
            diagram = self._generate_mermaid_diagram()
            self.spec.architecture_diagram = diagram
            
            print(f"\n{Colors.DIM}Generated diagram:{Colors.END}")
            print(diagram)
            
            if get_yes_no("\nModify this diagram?", default=False):
                self.spec.architecture_diagram = get_input("Your Mermaid diagram:", multiline=True)
        else:
            print("Enter your architecture diagram in Mermaid format:")
            print(f"{Colors.DIM}Example: graph TD; A-->B{Colors.END}")
            self.spec.architecture_diagram = get_input("Diagram:", multiline=True)
    
    def _generate_mermaid_diagram(self) -> str:
        """Generate Mermaid diagram from components."""
        lines = ["```mermaid", "graph TD"]
        
        # Create nodes for each component
        node_ids = {}
        for i, comp in enumerate(self.spec.components):
            node_id = f"C{i+1}"
            node_ids[comp.name] = node_id
            
            # Choose shape based on type
            if comp.type == "database":
                lines.append(f"    {node_id}[({comp.name})]")
            elif comp.type == "service":
                lines.append(f"    {node_id}{{{{{comp.name}}}}}")
            elif comp.type == "frontend":
                lines.append(f"    {node_id}[{comp.name}]")
            else:
                lines.append(f"    {node_id}[{comp.name}]")
        
        # Add connections based on common patterns
        components = [c.name.lower() for c in self.spec.components]
        
        # Frontend -> Backend
        for i, comp in enumerate(self.spec.components):
            if comp.type == "frontend":
                for j, other in enumerate(self.spec.components):
                    if other.type in ["backend", "service"]:
                        lines.append(f"    C{i+1} --> C{j+1}")
        
        # Backend -> Database
        for i, comp in enumerate(self.spec.components):
            if comp.type in ["backend", "service"]:
                for j, other in enumerate(self.spec.components):
                    if other.type == "database":
                        lines.append(f"    C{i+1} --> C{j+1}")
        
        lines.append("```")
        return "\n".join(lines)


def run_design(spec: Spec) -> Spec:
    """Convenience function to run design phase."""
    designer = DesignPhase(spec)
    return designer.run_full_design()
