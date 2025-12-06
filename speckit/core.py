"""
Core classes for Speckit - the foundation for spec generation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

from .utils import (
    Colors, print_header, print_section, print_tip, print_success,
    print_error, print_info, get_input, get_choice, get_yes_no,
    estimate_complexity, estimate_timeline, format_list, format_checklist,
    format_table, get_timestamp, slugify
)


@dataclass
class Requirement:
    """Represents a single requirement."""
    id: str
    description: str
    priority: str  # P0, P1, P2
    category: str  # functional, non-functional, constraint
    acceptance_criteria: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    estimated_effort: str = ""  # S, M, L, XL


@dataclass
class UserStory:
    """Represents a user story."""
    id: str
    as_a: str
    i_want: str
    so_that: str
    acceptance_criteria: List[str] = field(default_factory=list)
    priority: str = "P1"


@dataclass
class Component:
    """Represents a system component."""
    name: str
    description: str
    type: str  # frontend, backend, database, service, library
    technologies: List[str] = field(default_factory=list)
    responsibilities: List[str] = field(default_factory=list)
    interfaces: List[str] = field(default_factory=list)


@dataclass 
class APIEndpoint:
    """Represents an API endpoint."""
    method: str
    path: str
    description: str
    request_body: Optional[Dict] = None
    response: Optional[Dict] = None
    auth_required: bool = False


@dataclass
class DataEntity:
    """Represents a data entity/model."""
    name: str
    description: str
    fields: List[Dict[str, str]] = field(default_factory=list)
    relationships: List[str] = field(default_factory=list)


@dataclass
class Phase:
    """Represents an implementation phase."""
    number: int
    name: str
    description: str
    tasks: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    estimated_duration: str = ""


class Spec:
    """
    Represents a complete project specification.
    
    This is the central data structure that holds all project information
    from planning through design to implementation.
    """
    
    def __init__(self):
        # Meta
        self.name: str = ""
        self.slug: str = ""
        self.tagline: str = ""
        self.version: str = "1.0.0"
        self.created_at: str = get_timestamp()
        self.updated_at: str = get_timestamp()
        
        # Overview
        self.problem: str = ""
        self.solution: str = ""
        self.target_users: List[str] = []
        self.value_proposition: str = ""
        
        # Project Classification
        self.project_type: str = ""
        self.architecture_style: str = ""  # monolith, microservices, serverless, etc.
        self.tech_stack: Dict[str, List[str]] = {
            "frontend": [],
            "backend": [],
            "database": [],
            "infrastructure": [],
            "tools": []
        }
        
        # Planning
        self.requirements: List[Requirement] = []
        self.user_stories: List[UserStory] = []
        self.constraints: List[str] = []
        self.assumptions: List[str] = []
        self.risks: List[Dict[str, str]] = []
        self.dependencies_external: List[str] = []
        
        # Scope
        self.features_must: List[str] = []
        self.features_should: List[str] = []
        self.features_could: List[str] = []
        self.features_wont: List[str] = []  # Non-goals
        
        # Design
        self.components: List[Component] = []
        self.data_entities: List[DataEntity] = []
        self.api_endpoints: List[APIEndpoint] = []
        self.user_flows: List[Dict[str, Any]] = []
        self.architecture_diagram: str = ""
        self.file_structure: str = ""
        
        # Implementation
        self.phases: List[Phase] = []
        self.testing_strategy: Dict[str, List[str]] = {
            "unit": [],
            "integration": [],
            "e2e": [],
            "manual": []
        }
        self.deployment_strategy: str = ""
        self.ci_cd_pipeline: List[str] = []
        
        # Quality & Success
        self.success_criteria: List[str] = []
        self.performance_requirements: List[str] = []
        self.security_requirements: List[str] = []
        self.accessibility_requirements: List[str] = []
        
        # AI Instructions
        self.ai_context: str = ""
        self.ai_questions: List[str] = []
        self.ai_warnings: List[str] = []
        
        # Metadata
        self.complexity: str = ""
        self.timeline: Dict[str, str] = {}
        self.tags: List[str] = []
    
    def update_metadata(self):
        """Update computed metadata fields."""
        self.updated_at = get_timestamp()
        self.slug = slugify(self.name)
        all_features = self.features_must + self.features_should + self.features_could
        self.complexity = estimate_complexity(all_features, self.constraints)
        self.timeline = estimate_timeline(self.complexity, len(self.phases) or 3)
    
    def add_requirement(self, description: str, priority: str = "P1", 
                       category: str = "functional") -> Requirement:
        """Add a new requirement."""
        req_id = f"REQ-{len(self.requirements) + 1:03d}"
        req = Requirement(id=req_id, description=description, 
                         priority=priority, category=category)
        self.requirements.append(req)
        return req
    
    def add_user_story(self, as_a: str, i_want: str, so_that: str,
                       priority: str = "P1") -> UserStory:
        """Add a new user story."""
        story_id = f"US-{len(self.user_stories) + 1:03d}"
        story = UserStory(id=story_id, as_a=as_a, i_want=i_want, 
                         so_that=so_that, priority=priority)
        self.user_stories.append(story)
        return story
    
    def add_phase(self, name: str, description: str, tasks: List[str],
                  deliverables: List[str] = None) -> Phase:
        """Add an implementation phase."""
        phase_num = len(self.phases) + 1
        phase = Phase(
            number=phase_num,
            name=name,
            description=description,
            tasks=tasks,
            deliverables=deliverables or []
        )
        self.phases.append(phase)
        return phase
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert spec to dictionary for serialization."""
        self.update_metadata()
        return {
            "meta": {
                "name": self.name,
                "slug": self.slug,
                "tagline": self.tagline,
                "version": self.version,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "complexity": self.complexity,
                "timeline": self.timeline,
                "tags": self.tags
            },
            "overview": {
                "problem": self.problem,
                "solution": self.solution,
                "target_users": self.target_users,
                "value_proposition": self.value_proposition
            },
            "classification": {
                "project_type": self.project_type,
                "architecture_style": self.architecture_style,
                "tech_stack": self.tech_stack
            },
            "planning": {
                "requirements": [vars(r) for r in self.requirements],
                "user_stories": [vars(s) for s in self.user_stories],
                "constraints": self.constraints,
                "assumptions": self.assumptions,
                "risks": self.risks,
                "external_dependencies": self.dependencies_external
            },
            "scope": {
                "must_have": self.features_must,
                "should_have": self.features_should,
                "could_have": self.features_could,
                "wont_have": self.features_wont
            },
            "design": {
                "components": [vars(c) for c in self.components],
                "data_entities": [vars(e) for e in self.data_entities],
                "api_endpoints": [vars(e) for e in self.api_endpoints],
                "user_flows": self.user_flows,
                "architecture_diagram": self.architecture_diagram,
                "file_structure": self.file_structure
            },
            "implementation": {
                "phases": [vars(p) for p in self.phases],
                "testing_strategy": self.testing_strategy,
                "deployment_strategy": self.deployment_strategy,
                "ci_cd_pipeline": self.ci_cd_pipeline
            },
            "quality": {
                "success_criteria": self.success_criteria,
                "performance": self.performance_requirements,
                "security": self.security_requirements,
                "accessibility": self.accessibility_requirements
            },
            "ai": {
                "context": self.ai_context,
                "questions": self.ai_questions,
                "warnings": self.ai_warnings
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Spec':
        """Create a Spec from dictionary."""
        spec = cls()
        
        # Meta
        meta = data.get("meta", {})
        spec.name = meta.get("name", "")
        spec.slug = meta.get("slug", "")
        spec.tagline = meta.get("tagline", "")
        spec.version = meta.get("version", "1.0.0")
        spec.created_at = meta.get("created_at", get_timestamp())
        spec.tags = meta.get("tags", [])
        
        # Overview
        overview = data.get("overview", {})
        spec.problem = overview.get("problem", "")
        spec.solution = overview.get("solution", "")
        spec.target_users = overview.get("target_users", [])
        spec.value_proposition = overview.get("value_proposition", "")
        
        # Classification
        classification = data.get("classification", {})
        spec.project_type = classification.get("project_type", "")
        spec.architecture_style = classification.get("architecture_style", "")
        spec.tech_stack = classification.get("tech_stack", spec.tech_stack)
        
        # Planning
        planning = data.get("planning", {})
        spec.constraints = planning.get("constraints", [])
        spec.assumptions = planning.get("assumptions", [])
        spec.risks = planning.get("risks", [])
        spec.dependencies_external = planning.get("external_dependencies", [])
        
        # Scope
        scope = data.get("scope", {})
        spec.features_must = scope.get("must_have", [])
        spec.features_should = scope.get("should_have", [])
        spec.features_could = scope.get("could_have", [])
        spec.features_wont = scope.get("wont_have", [])
        
        # Design
        design = data.get("design", {})
        spec.user_flows = design.get("user_flows", [])
        spec.architecture_diagram = design.get("architecture_diagram", "")
        spec.file_structure = design.get("file_structure", "")
        
        # Implementation
        impl = data.get("implementation", {})
        spec.testing_strategy = impl.get("testing_strategy", spec.testing_strategy)
        spec.deployment_strategy = impl.get("deployment_strategy", "")
        spec.ci_cd_pipeline = impl.get("ci_cd_pipeline", [])
        
        # Quality
        quality = data.get("quality", {})
        spec.success_criteria = quality.get("success_criteria", [])
        spec.performance_requirements = quality.get("performance", [])
        spec.security_requirements = quality.get("security", [])
        spec.accessibility_requirements = quality.get("accessibility", [])
        
        # AI
        ai = data.get("ai", {})
        spec.ai_context = ai.get("context", "")
        spec.ai_questions = ai.get("questions", [])
        spec.ai_warnings = ai.get("warnings", [])
        
        spec.update_metadata()
        return spec
    
    def save_json(self, filepath: Path):
        """Save spec as JSON."""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_json(cls, filepath: Path) -> 'Spec':
        """Load spec from JSON."""
        with open(filepath, 'r') as f:
            return cls.from_dict(json.load(f))


class SpecBuilder:
    """
    Builder class for creating specs through guided workflows.
    
    Supports different levels of detail:
    - Quick: Minimal spec for simple projects
    - Standard: Balanced spec for most projects
    - Comprehensive: Full spec for complex projects
    """
    
    def __init__(self, level: str = "standard"):
        self.level = level  # quick, standard, comprehensive
        self.spec = Spec()
    
    def build_quick(self, idea: str) -> Spec:
        """Build a quick spec from a one-liner idea."""
        self.spec.name = idea[:50] + "..." if len(idea) > 50 else idea
        self.spec.tagline = idea
        self.spec.problem = "To be refined with AI"
        self.spec.solution = idea
        self.spec.target_users = ["Me (solo developer)"]
        
        self.spec.features_must = [
            "Core functionality as described",
            "Basic error handling", 
            "Clear usage instructions"
        ]
        
        self.spec.add_phase(
            name="MVP",
            description="Basic working version",
            tasks=["Implement core functionality", "Add minimal error handling"],
            deliverables=["Working prototype"]
        )
        
        self.spec.add_phase(
            name="Polish",
            description="Refinement and documentation",
            tasks=["Improve error handling", "Add documentation", "Handle edge cases"],
            deliverables=["Production-ready code", "README"]
        )
        
        self.spec.ai_context = f"""This is a quick spec for: "{idea}"

Please help refine it by:
1. Asking clarifying questions about the idea
2. Suggesting appropriate tech stack based on requirements
3. Identifying potential challenges before implementation
4. Proposing a file structure for the project
5. Breaking down Phase 1 into specific tasks"""
        
        self.spec.update_metadata()
        return self.spec
    
    def set_overview(self, name: str, tagline: str, problem: str, 
                     solution: str, target_users: List[str]):
        """Set the project overview."""
        self.spec.name = name
        self.spec.tagline = tagline
        self.spec.problem = problem
        self.spec.solution = solution
        self.spec.target_users = target_users
        return self
    
    def set_classification(self, project_type: str, architecture: str,
                          tech_stack: Dict[str, List[str]]):
        """Set project classification."""
        self.spec.project_type = project_type
        self.spec.architecture_style = architecture
        self.spec.tech_stack = tech_stack
        return self
    
    def set_scope(self, must: List[str], should: List[str] = None,
                  could: List[str] = None, wont: List[str] = None):
        """Set project scope using MoSCoW prioritization."""
        self.spec.features_must = must
        self.spec.features_should = should or []
        self.spec.features_could = could or []
        self.spec.features_wont = wont or []
        return self
    
    def add_constraint(self, constraint: str):
        """Add a project constraint."""
        self.spec.constraints.append(constraint)
        return self
    
    def add_risk(self, risk: str, impact: str, mitigation: str):
        """Add a project risk."""
        self.spec.risks.append({
            "risk": risk,
            "impact": impact,
            "mitigation": mitigation
        })
        return self
    
    def finalize(self) -> Spec:
        """Finalize and return the spec."""
        self.spec.update_metadata()
        return self.spec
