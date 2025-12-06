"""
Project Templates - Pre-configured specs for common project types.

Provides sophisticated templates for:
- CLI Tools
- Web Applications
- APIs/Backend Services
- Libraries/Packages
- SaaS Applications
- Microservices
"""

from typing import Dict, Any, List, Optional
from .core import Spec, Component, Phase


# Template definitions
TEMPLATES = {
    "cli": {
        "name": "CLI Tool",
        "description": "Command-line interface tool",
        "architecture": "Monolithic",
        "tech_stack": {
            "backend": ["Python", "Click/Argparse"],
            "tools": ["pytest", "black", "mypy"]
        },
        "components": [
            {
                "name": "CLI Interface",
                "type": "backend",
                "description": "Command-line argument parsing and user interaction",
                "responsibilities": ["Parse arguments", "Display output", "Handle errors"]
            },
            {
                "name": "Core Logic",
                "type": "backend", 
                "description": "Main business logic and processing",
                "responsibilities": ["Process data", "Execute commands", "Manage state"]
            }
        ],
        "phases": [
            {
                "name": "Foundation",
                "description": "Basic CLI structure and core functionality",
                "tasks": ["Set up project structure", "Implement CLI argument parsing", "Create main command(s)"],
                "deliverables": ["Working CLI with basic commands"]
            },
            {
                "name": "Core Features",
                "description": "Full feature implementation",
                "tasks": ["Implement all core features", "Add configuration support", "Error handling"],
                "deliverables": ["Feature-complete CLI"]
            },
            {
                "name": "Polish",
                "description": "Documentation and distribution",
                "tasks": ["Write documentation", "Add tests", "Package for distribution"],
                "deliverables": ["Documented, tested, distributable CLI"]
            }
        ],
        "file_structure": """project/
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── core.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_core.py
├── README.md
├── pyproject.toml
└── LICENSE""",
        "constraints": [
            "Must be installable via pip",
            "Clear and helpful error messages",
            "Works across Python 3.9+"
        ],
        "testing": {
            "unit": ["Core logic functions", "Utility functions"],
            "integration": ["CLI command execution", "Configuration loading"],
            "manual": ["Install and run basic commands", "Test error scenarios"]
        }
    },
    
    "webapp": {
        "name": "Web Application (Full-stack)",
        "description": "Full-stack web application with frontend and backend",
        "architecture": "Layered",
        "tech_stack": {
            "frontend": ["React/Next.js", "Tailwind CSS"],
            "backend": ["Python/FastAPI or Node.js/Express"],
            "database": ["PostgreSQL"],
            "infrastructure": ["Docker", "Vercel/Railway"]
        },
        "components": [
            {
                "name": "Frontend",
                "type": "frontend",
                "description": "User interface and client-side logic",
                "responsibilities": ["Render UI", "Handle user input", "API communication"]
            },
            {
                "name": "Backend API",
                "type": "backend",
                "description": "REST/GraphQL API server",
                "responsibilities": ["Handle requests", "Business logic", "Data validation"]
            },
            {
                "name": "Database",
                "type": "database",
                "description": "Data persistence layer",
                "responsibilities": ["Store data", "Query data", "Maintain integrity"]
            }
        ],
        "phases": [
            {
                "name": "Foundation",
                "description": "Project setup and basic structure",
                "tasks": ["Set up frontend project", "Set up backend project", "Database schema design", "Basic routing"],
                "deliverables": ["Running frontend and backend", "Database connection"]
            },
            {
                "name": "Core Features",
                "description": "Main functionality implementation",
                "tasks": ["Implement core UI components", "Build API endpoints", "Database models and queries", "Connect frontend to backend"],
                "deliverables": ["Working core features end-to-end"]
            },
            {
                "name": "Authentication & Authorization",
                "description": "User management and security",
                "tasks": ["User registration/login", "Session management", "Protected routes", "Role-based access"],
                "deliverables": ["Secure user authentication"]
            },
            {
                "name": "Polish & Deploy",
                "description": "Production readiness",
                "tasks": ["Error handling", "Loading states", "Responsive design", "Testing", "Deployment setup"],
                "deliverables": ["Production-ready application"]
            }
        ],
        "file_structure": """project/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── styles/
│   │   └── lib/
│   ├── public/
│   └── package.json
├── backend/
│   ├── src/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   └── requirements.txt
├── docker-compose.yml
└── README.md""",
        "constraints": [
            "Mobile-responsive design",
            "Fast load times (< 3s)",
            "Secure authentication"
        ],
        "testing": {
            "unit": ["React components", "API handlers", "Utility functions"],
            "integration": ["API endpoints", "Database operations"],
            "e2e": ["User registration flow", "Core user journeys"],
            "manual": ["Cross-browser testing", "Mobile testing"]
        }
    },
    
    "api": {
        "name": "API/Backend Service",
        "description": "REST or GraphQL API service",
        "architecture": "Layered",
        "tech_stack": {
            "backend": ["Python/FastAPI", "SQLAlchemy"],
            "database": ["PostgreSQL"],
            "infrastructure": ["Docker", "Railway/AWS"]
        },
        "components": [
            {
                "name": "API Layer",
                "type": "backend",
                "description": "HTTP request handling and routing",
                "responsibilities": ["Route requests", "Input validation", "Response formatting"]
            },
            {
                "name": "Service Layer",
                "type": "backend",
                "description": "Business logic",
                "responsibilities": ["Business rules", "Data transformation", "Orchestration"]
            },
            {
                "name": "Data Layer",
                "type": "backend",
                "description": "Data access and persistence",
                "responsibilities": ["Database queries", "Data mapping", "Caching"]
            },
            {
                "name": "Database",
                "type": "database",
                "description": "Data storage",
                "responsibilities": ["Data persistence", "Integrity constraints"]
            }
        ],
        "phases": [
            {
                "name": "Foundation",
                "description": "API structure and database setup",
                "tasks": ["Project setup", "Database schema", "Basic CRUD endpoints", "Error handling middleware"],
                "deliverables": ["Running API with basic endpoints"]
            },
            {
                "name": "Core Features",
                "description": "Full API implementation",
                "tasks": ["All business logic endpoints", "Data validation", "Query optimization"],
                "deliverables": ["Feature-complete API"]
            },
            {
                "name": "Security & Production",
                "description": "Security and deployment readiness",
                "tasks": ["Authentication/authorization", "Rate limiting", "Logging", "API documentation", "Docker setup"],
                "deliverables": ["Secure, documented, deployable API"]
            }
        ],
        "file_structure": """project/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   └── middleware/
│   ├── models/
│   ├── services/
│   ├── repositories/
│   ├── schemas/
│   └── core/
│       ├── config.py
│       └── database.py
├── tests/
│   ├── unit/
│   └── integration/
├── migrations/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md""",
        "constraints": [
            "RESTful design principles",
            "OpenAPI documentation",
            "Response time < 200ms"
        ],
        "testing": {
            "unit": ["Service functions", "Utility functions"],
            "integration": ["API endpoints", "Database operations"],
            "manual": ["API testing with Postman/curl"]
        }
    },
    
    "library": {
        "name": "Library/Package",
        "description": "Reusable library or package",
        "architecture": "Monolithic",
        "tech_stack": {
            "backend": ["Python/JavaScript/TypeScript"],
            "tools": ["pytest/jest", "documentation generator"]
        },
        "components": [
            {
                "name": "Core Module",
                "type": "library",
                "description": "Main library functionality",
                "responsibilities": ["Core features", "Public API"]
            },
            {
                "name": "Utilities",
                "type": "library",
                "description": "Helper functions and utilities",
                "responsibilities": ["Common operations", "Internal helpers"]
            }
        ],
        "phases": [
            {
                "name": "Core API",
                "description": "Design and implement public API",
                "tasks": ["Define public interface", "Implement core functions", "Basic error handling"],
                "deliverables": ["Working core functionality"]
            },
            {
                "name": "Complete Features",
                "description": "Full functionality",
                "tasks": ["Additional features", "Edge case handling", "Performance optimization"],
                "deliverables": ["Feature-complete library"]
            },
            {
                "name": "Documentation & Release",
                "description": "Prepare for distribution",
                "tasks": ["API documentation", "Usage examples", "Tests", "Package configuration"],
                "deliverables": ["Published package with documentation"]
            }
        ],
        "file_structure": """project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── core.py
│       ├── utils.py
│       └── exceptions.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
├── docs/
│   └── api.md
├── examples/
│   └── basic_usage.py
├── pyproject.toml
├── README.md
└── LICENSE""",
        "constraints": [
            "Clean, well-documented public API",
            "Minimal dependencies",
            "High test coverage (>80%)"
        ],
        "testing": {
            "unit": ["All public functions", "Edge cases"],
            "integration": ["Module interactions"],
            "manual": ["Install and use examples"]
        }
    },
    
    "saas": {
        "name": "SaaS Application",
        "description": "Software as a Service application with multi-tenancy",
        "architecture": "Microservices or Layered",
        "tech_stack": {
            "frontend": ["React/Next.js", "Tailwind CSS"],
            "backend": ["Python/FastAPI or Node.js"],
            "database": ["PostgreSQL", "Redis"],
            "infrastructure": ["Docker", "Kubernetes/Railway", "Stripe"]
        },
        "components": [
            {
                "name": "Web App",
                "type": "frontend",
                "description": "Main web application interface",
                "responsibilities": ["User interface", "Dashboard", "Settings"]
            },
            {
                "name": "API Gateway",
                "type": "backend",
                "description": "API routing and authentication",
                "responsibilities": ["Request routing", "Auth", "Rate limiting"]
            },
            {
                "name": "Core Service",
                "type": "backend",
                "description": "Main application logic",
                "responsibilities": ["Business logic", "Data processing"]
            },
            {
                "name": "Billing Service",
                "type": "backend",
                "description": "Subscription and payment handling",
                "responsibilities": ["Subscriptions", "Invoicing", "Payment processing"]
            },
            {
                "name": "Database",
                "type": "database",
                "description": "Multi-tenant data storage",
                "responsibilities": ["Tenant isolation", "Data persistence"]
            }
        ],
        "phases": [
            {
                "name": "Foundation",
                "description": "Core infrastructure",
                "tasks": ["Project setup", "Authentication system", "Multi-tenancy setup", "Basic UI"],
                "deliverables": ["Users can sign up and log in"]
            },
            {
                "name": "Core Product",
                "description": "Main product features",
                "tasks": ["Core feature implementation", "Dashboard", "Settings", "Data management"],
                "deliverables": ["Working core product"]
            },
            {
                "name": "Billing & Subscriptions",
                "description": "Payment integration",
                "tasks": ["Stripe integration", "Subscription plans", "Billing portal", "Usage tracking"],
                "deliverables": ["Working subscription system"]
            },
            {
                "name": "Growth Features",
                "description": "Scale and optimize",
                "tasks": ["Analytics", "Admin dashboard", "Email notifications", "Performance optimization"],
                "deliverables": ["Production-ready SaaS"]
            }
        ],
        "file_structure": """project/
├── apps/
│   ├── web/
│   │   ├── src/
│   │   └── package.json
│   └── api/
│       ├── src/
│       └── requirements.txt
├── packages/
│   └── shared/
├── infrastructure/
│   ├── docker/
│   └── kubernetes/
├── docker-compose.yml
└── README.md""",
        "constraints": [
            "Multi-tenant data isolation",
            "99.9% uptime target",
            "GDPR compliant",
            "Secure payment handling"
        ],
        "testing": {
            "unit": ["Business logic", "Billing calculations"],
            "integration": ["API flows", "Payment processing"],
            "e2e": ["User signup to payment flow"],
            "manual": ["Billing scenarios", "Admin features"]
        }
    }
}


def get_template(template_name: str) -> Optional[Dict[str, Any]]:
    """Get a template by name."""
    return TEMPLATES.get(template_name.lower())


def list_templates() -> List[Dict[str, str]]:
    """List all available templates."""
    return [
        {"key": key, "name": tmpl["name"], "description": tmpl["description"]}
        for key, tmpl in TEMPLATES.items()
    ]


def apply_template(spec: Spec, template_name: str) -> Spec:
    """Apply a template to a Spec object."""
    template = get_template(template_name)
    if not template:
        return spec
    
    # Apply architecture
    spec.architecture_style = template.get("architecture", "Monolithic")
    
    # Apply tech stack
    if template.get("tech_stack"):
        spec.tech_stack = template["tech_stack"]
    
    # Apply components
    if template.get("components"):
        for comp_data in template["components"]:
            comp = Component(
                name=comp_data["name"],
                description=comp_data["description"],
                type=comp_data["type"],
                responsibilities=comp_data.get("responsibilities", [])
            )
            spec.components.append(comp)
    
    # Apply phases
    if template.get("phases"):
        for i, phase_data in enumerate(template["phases"], 1):
            phase = Phase(
                number=i,
                name=phase_data["name"],
                description=phase_data["description"],
                tasks=phase_data.get("tasks", []),
                deliverables=phase_data.get("deliverables", [])
            )
            spec.phases.append(phase)
    
    # Apply file structure
    if template.get("file_structure"):
        spec.file_structure = template["file_structure"]
    
    # Apply constraints
    if template.get("constraints"):
        spec.constraints.extend(template["constraints"])
    
    # Apply testing strategy
    if template.get("testing"):
        spec.testing_strategy = template["testing"]
    
    return spec


def get_template_for_project_type(project_type: str) -> Optional[str]:
    """Map project type to template name."""
    mapping = {
        "CLI Tool": "cli",
        "Web App (Full-stack)": "webapp",
        "Web App (Frontend only)": "webapp",
        "API/Backend Service": "api",
        "Library/Package": "library",
        "SaaS Application": "saas",
        "Automation Script": "cli",
    }
    return mapping.get(project_type)
