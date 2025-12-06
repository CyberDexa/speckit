"""
Implementation Phase Module - Deployment and execution tools.

This module provides tools for:
- Testing strategy definition
- CI/CD pipeline planning
- Deployment configuration
- Quality gates
- Success criteria validation
"""

from typing import List, Dict, Any, Optional

from .core import Spec, Phase
from .utils import (
    Colors, print_header, print_subheader, print_section, print_tip,
    print_success, print_warning, print_info, get_input, get_choice,
    get_yes_no, format_list, format_checklist
)


# Testing frameworks by language/stack
TESTING_FRAMEWORKS = {
    "Python": {
        "unit": ["pytest", "unittest"],
        "integration": ["pytest", "behave"],
        "e2e": ["playwright", "selenium"]
    },
    "JavaScript": {
        "unit": ["Jest", "Vitest", "Mocha"],
        "integration": ["Jest", "Supertest"],
        "e2e": ["Playwright", "Cypress"]
    },
    "TypeScript": {
        "unit": ["Jest", "Vitest"],
        "integration": ["Jest", "Supertest"],
        "e2e": ["Playwright", "Cypress"]
    },
    "Go": {
        "unit": ["testing (built-in)"],
        "integration": ["testing + testify"],
        "e2e": ["testing"]
    },
    "Rust": {
        "unit": ["cargo test (built-in)"],
        "integration": ["cargo test"],
        "e2e": ["cargo test"]
    }
}

# CI/CD platforms
CI_CD_PLATFORMS = {
    "github_actions": {
        "name": "GitHub Actions",
        "file": ".github/workflows/ci.yml",
        "features": ["Built into GitHub", "Free for public repos", "Extensive marketplace"]
    },
    "gitlab_ci": {
        "name": "GitLab CI",
        "file": ".gitlab-ci.yml",
        "features": ["Built into GitLab", "Auto DevOps", "Integrated container registry"]
    },
    "circleci": {
        "name": "CircleCI",
        "file": ".circleci/config.yml",
        "features": ["Fast builds", "Docker support", "Parallelism"]
    },
    "none": {
        "name": "No CI/CD (manual)",
        "file": None,
        "features": ["Simple projects", "Local development only"]
    }
}

# Deployment platforms
DEPLOYMENT_PLATFORMS = {
    "vercel": {
        "name": "Vercel",
        "best_for": ["Next.js", "React", "Static sites"],
        "features": ["Zero config", "Edge functions", "Preview deployments"]
    },
    "railway": {
        "name": "Railway",
        "best_for": ["Full-stack apps", "APIs", "Databases"],
        "features": ["Easy setup", "Built-in databases", "Environment management"]
    },
    "netlify": {
        "name": "Netlify",
        "best_for": ["Static sites", "JAMstack", "Serverless functions"],
        "features": ["Form handling", "Split testing", "Edge handlers"]
    },
    "docker": {
        "name": "Docker (Self-hosted)",
        "best_for": ["Any project", "Microservices", "Custom infrastructure"],
        "features": ["Portable", "Reproducible", "Orchestration ready"]
    },
    "aws": {
        "name": "AWS",
        "best_for": ["Enterprise", "Scalable apps", "Complex infrastructure"],
        "features": ["Extensive services", "Global reach", "Enterprise support"]
    },
    "pypi": {
        "name": "PyPI",
        "best_for": ["Python packages", "Libraries"],
        "features": ["Standard Python distribution", "pip installable"]
    },
    "npm": {
        "name": "npm",
        "best_for": ["JavaScript packages", "Node modules"],
        "features": ["Standard JS distribution", "npm installable"]
    },
    "local": {
        "name": "Local / Manual",
        "best_for": ["Scripts", "Personal tools", "Development"],
        "features": ["Simple", "No infrastructure needed"]
    }
}


class ImplementationPhase:
    """
    Handles the implementation phase of spec creation.
    
    Guides users through implementation planning including
    testing strategy, CI/CD, deployment, and success criteria.
    """
    
    def __init__(self, spec: Spec):
        self.spec = spec
    
    def run_full_implementation(self) -> Spec:
        """Run the complete implementation planning workflow."""
        print_header("Implementation Phase", "🚀")
        print("Let's plan how to build, test, and deploy your project.\n")
        
        self.refine_phases()
        self.define_testing_strategy()
        self.plan_ci_cd()
        self.plan_deployment()
        self.define_quality_requirements()
        self.define_success_criteria()
        self.prepare_ai_instructions()
        
        print_success("Implementation planning complete!")
        return self.spec
    
    def refine_phases(self):
        """Refine and add details to implementation phases."""
        print_subheader("Implementation Phases", "📊")
        
        if not self.spec.phases:
            print_warning("No phases defined yet. Let's create them.")
            self._create_phases()
            return
        
        print("Current phases:")
        for phase in self.spec.phases:
            print(f"  {Colors.CYAN}Phase {phase.number}: {phase.name}{Colors.END}")
            for task in phase.tasks[:3]:
                print(f"    - {task}")
            if len(phase.tasks) > 3:
                print(f"    {Colors.DIM}... and {len(phase.tasks) - 3} more{Colors.END}")
        
        if get_yes_no("\nRefine phases with more detail?", default=True):
            for phase in self.spec.phases:
                print(f"\n{Colors.CYAN}Phase {phase.number}: {phase.name}{Colors.END}")
                
                # Add success criteria per phase
                if not phase.success_criteria:
                    if get_yes_no(f"Add success criteria for {phase.name}?", default=True):
                        criteria = get_input("Success criteria (one per line):", multiline=True)
                        phase.success_criteria = [c.strip() for c in criteria.split("\n") if c.strip()]
                
                # Add deliverables
                if not phase.deliverables:
                    if get_yes_no(f"Add deliverables for {phase.name}?", default=True):
                        deliverables = get_input("Deliverables (one per line):", multiline=True)
                        phase.deliverables = [d.strip() for d in deliverables.split("\n") if d.strip()]
                
                # Estimate duration
                if not phase.estimated_duration:
                    phase.estimated_duration = get_input(
                        f"Estimated duration for {phase.name}:",
                        default="1-2 days"
                    )
    
    def _create_phases(self):
        """Create phases if none exist."""
        if self.spec.features_must:
            print("\nCreating phases from your must-have features...")
            
            features = self.spec.features_must.copy()
            
            if len(features) <= 3:
                self.spec.add_phase(
                    name="MVP",
                    description="Complete core functionality",
                    tasks=features,
                    deliverables=["Working prototype"]
                )
            else:
                mid = len(features) // 2
                self.spec.add_phase(
                    name="Foundation",
                    description="Core infrastructure and basic features",
                    tasks=features[:mid],
                    deliverables=["Basic working version"]
                )
                self.spec.add_phase(
                    name="Feature Complete",
                    description="Complete remaining core features",
                    tasks=features[mid:],
                    deliverables=["Feature-complete version"]
                )
            
            self.spec.add_phase(
                name="Polish",
                description="Quality improvements and documentation",
                tasks=[
                    "Comprehensive error handling",
                    "Documentation",
                    "Testing",
                    "Performance optimization"
                ],
                deliverables=["Production-ready release"]
            )
        else:
            print("Let's define phases manually.\n")
            phase_num = 0
            while True:
                phase_num += 1
                name = get_input(f"Phase {phase_num} name:")
                description = get_input("Description:")
                tasks = get_input("Tasks (one per line):", multiline=True)
                
                self.spec.add_phase(
                    name=name,
                    description=description,
                    tasks=[t.strip() for t in tasks.split("\n") if t.strip()]
                )
                
                if not get_yes_no("Add another phase?", default=phase_num < 3):
                    break
    
    def define_testing_strategy(self):
        """Define the testing strategy."""
        print_subheader("Testing Strategy", "🧪")
        
        if not get_yes_no("Define testing strategy?", default=True):
            return
        
        print_tip("A good testing strategy ensures quality without slowing development")
        
        # Determine primary language
        all_tech = []
        for category in self.spec.tech_stack.values():
            all_tech.extend(category)
        
        primary_lang = None
        for tech in all_tech:
            for lang in TESTING_FRAMEWORKS.keys():
                if lang.lower() in tech.lower():
                    primary_lang = lang
                    break
            if primary_lang:
                break
        
        if primary_lang:
            print(f"\n{Colors.DIM}Detected primary language: {primary_lang}{Colors.END}")
            frameworks = TESTING_FRAMEWORKS.get(primary_lang, {})
        else:
            frameworks = {}
        
        testing_strategy = {
            "unit": [],
            "integration": [],
            "e2e": [],
            "manual": []
        }
        
        # Unit tests
        print_section("Unit Tests")
        print_tip("Test individual functions/methods in isolation")
        
        if get_yes_no("Include unit testing?", default=True):
            if frameworks.get("unit"):
                framework = get_choice(
                    "Unit testing framework:",
                    frameworks["unit"] + ["Other"]
                )
                if framework == "Other":
                    framework = get_input("Specify framework:")
                testing_strategy["unit"].append(f"Framework: {framework}")
            
            areas = get_input("What to unit test:", multiline=True, required=False)
            if areas:
                testing_strategy["unit"].extend([a.strip() for a in areas.split("\n") if a.strip()])
        
        # Integration tests
        print_section("Integration Tests")
        print_tip("Test how components work together")
        
        if get_yes_no("Include integration testing?", default=True):
            areas = get_input("What to integration test:", multiline=True, required=False)
            if areas:
                testing_strategy["integration"] = [a.strip() for a in areas.split("\n") if a.strip()]
        
        # E2E tests
        print_section("End-to-End Tests")
        print_tip("Test complete user flows")
        
        if get_yes_no("Include E2E testing?", default=False):
            if frameworks.get("e2e"):
                framework = get_choice(
                    "E2E testing framework:",
                    frameworks["e2e"] + ["Other"]
                )
                testing_strategy["e2e"].append(f"Framework: {framework}")
            
            flows = get_input("Critical flows to test:", multiline=True, required=False)
            if flows:
                testing_strategy["e2e"].extend([f.strip() for f in flows.split("\n") if f.strip()])
        
        # Manual tests
        print_section("Manual Testing")
        if get_yes_no("Define manual testing checklist?", default=True):
            manual = get_input("Manual testing items:", multiline=True, required=False)
            if manual:
                testing_strategy["manual"] = [m.strip() for m in manual.split("\n") if m.strip()]
        
        self.spec.testing_strategy = testing_strategy
    
    def plan_ci_cd(self):
        """Plan CI/CD pipeline."""
        print_subheader("CI/CD Pipeline", "⚙️")
        
        if not get_yes_no("Set up CI/CD?", default=True):
            return
        
        # Choose platform
        platforms = list(CI_CD_PLATFORMS.keys())
        platform_names = [CI_CD_PLATFORMS[p]["name"] for p in platforms]
        
        choice = get_choice("CI/CD platform:", platform_names)
        
        platform_key = None
        for key, info in CI_CD_PLATFORMS.items():
            if info["name"] == choice:
                platform_key = key
                break
        
        if platform_key and platform_key != "none":
            info = CI_CD_PLATFORMS[platform_key]
            print(f"\n{Colors.DIM}Config file: {info['file']}{Colors.END}")
            print(f"{Colors.DIM}Features: {', '.join(info['features'])}{Colors.END}")
        
        # Define pipeline steps
        print("\nDefine CI/CD pipeline steps:")
        
        common_steps = [
            "Install dependencies",
            "Run linting",
            "Run unit tests",
            "Run integration tests",
            "Build project",
            "Deploy to staging",
            "Deploy to production"
        ]
        
        selected = get_choice(
            "Pipeline steps:",
            common_steps + ["Other"],
            allow_multiple=True
        )
        
        if "Other" in selected:
            other = get_input("Additional steps:", multiline=True)
            selected = [s for s in selected if s != "Other"]
            selected.extend([s.strip() for s in other.split("\n") if s.strip()])
        
        self.spec.ci_cd_pipeline = selected
    
    def plan_deployment(self):
        """Plan deployment strategy."""
        print_subheader("Deployment Strategy", "🌐")
        
        # Choose platform based on project type
        if self.spec.project_type in ["CLI Tool", "Library/Package", "Automation Script"]:
            platforms = ["pypi", "npm", "docker", "local"]
        elif self.spec.project_type in ["Web App (Full-stack)", "API/Backend Service"]:
            platforms = ["vercel", "railway", "docker", "aws"]
        else:
            platforms = list(DEPLOYMENT_PLATFORMS.keys())
        
        platform_info = []
        for p in platforms:
            info = DEPLOYMENT_PLATFORMS.get(p, {})
            platform_info.append(f"{info.get('name', p)} - {', '.join(info.get('best_for', []))[:50]}")
        
        choice = get_choice("Deployment platform:", platform_info)
        platform_name = choice.split(" - ")[0]
        
        # Find the platform key
        for key, info in DEPLOYMENT_PLATFORMS.items():
            if info['name'] == platform_name:
                print(f"\n{Colors.DIM}Features: {', '.join(info['features'])}{Colors.END}")
                break
        
        # Deployment strategy
        strategy_options = [
            "Simple push to deploy",
            "Blue-green deployment",
            "Rolling deployment",
            "Manual deployment",
            "Other"
        ]
        
        strategy = get_choice("Deployment strategy:", strategy_options)
        if strategy == "Other":
            strategy = get_input("Describe your deployment strategy:")
        
        self.spec.deployment_strategy = f"{platform_name} - {strategy}"
    
    def define_quality_requirements(self):
        """Define quality requirements."""
        print_subheader("Quality Requirements", "✨")
        
        if not get_yes_no("Define quality requirements?", default=True):
            return
        
        # Performance
        print_section("Performance Requirements")
        if get_yes_no("Define performance requirements?", default=True):
            perf = get_input(
                "Performance requirements:",
                multiline=True,
                default="Response time < 200ms for API calls"
            )
            self.spec.performance_requirements = [
                p.strip() for p in perf.split("\n") if p.strip()
            ]
        
        # Security
        print_section("Security Requirements")
        if get_yes_no("Define security requirements?", default=True):
            common_security = [
                "Input validation on all user inputs",
                "Secure password hashing",
                "HTTPS only",
                "Authentication required for sensitive operations",
                "Rate limiting on API endpoints",
                "No sensitive data in logs"
            ]
            
            selected = get_choice(
                "Security requirements:",
                common_security + ["Other"],
                allow_multiple=True
            )
            
            if "Other" in selected:
                other = get_input("Other security requirements:", multiline=True)
                selected = [s for s in selected if s != "Other"]
                selected.extend([s.strip() for s in other.split("\n") if s.strip()])
            
            self.spec.security_requirements = selected
        
        # Accessibility
        print_section("Accessibility Requirements")
        if self.spec.project_type in ["Web App (Full-stack)", "Web App (Frontend only)", "Mobile App"]:
            if get_yes_no("Define accessibility requirements?", default=True):
                a11y = get_input(
                    "Accessibility requirements:",
                    multiline=True,
                    default="WCAG 2.1 AA compliance"
                )
                self.spec.accessibility_requirements = [
                    a.strip() for a in a11y.split("\n") if a.strip()
                ]
    
    def define_success_criteria(self):
        """Define project success criteria."""
        print_subheader("Success Criteria", "🎯")
        
        print_tip("How will you know the project is complete and successful?")
        
        if self.spec.features_must:
            print("\nBased on your must-have features, here are suggested criteria:")
            for feature in self.spec.features_must[:5]:
                print(f"  - ✓ {feature} is working")
        
        print("\nAdd your own success criteria:")
        print(f"{Colors.DIM}Example: 'Can complete main workflow in under 1 minute'{Colors.END}")
        
        criteria = get_input("Success criteria:", multiline=True)
        self.spec.success_criteria = [
            c.strip() for c in criteria.split("\n") if c.strip()
        ]
        
        # Add feature-based criteria if user wants
        if self.spec.features_must and get_yes_no("Include feature completion as criteria?", default=True):
            for feature in self.spec.features_must:
                self.spec.success_criteria.append(f"[Feature] {feature} working correctly")
    
    def prepare_ai_instructions(self):
        """Prepare instructions for AI implementation."""
        print_subheader("AI Instructions", "🤖")
        
        print_tip("These instructions guide AI agents when implementing your spec")
        
        # Context
        print_section("Project Context")
        context = get_input(
            "Any special context for AI?",
            multiline=True,
            required=False,
            default="Standard implementation following spec"
        )
        self.spec.ai_context = context
        
        # Questions AI should ask
        print_section("Clarifying Questions")
        print("What should AI clarify before starting?")
        
        common_questions = [
            "Best practices for this type of project",
            "Error handling approach",
            "Testing strategy details",
            "Performance optimization approach",
            "Security implementation details",
            "Code style preferences"
        ]
        
        selected = get_choice(
            "AI should clarify:",
            common_questions + ["None", "Other"],
            allow_multiple=True
        )
        
        questions = [q for q in selected if q not in ["None", "Other"]]
        if "Other" in selected:
            other = get_input("Other questions:", multiline=True)
            questions.extend([q.strip() for q in other.split("\n") if q.strip()])
        
        self.spec.ai_questions = questions
        
        # Warnings
        print_section("Important Warnings")
        if get_yes_no("Add warnings/constraints for AI?", default=True):
            common_warnings = [
                "Don't add features not in the spec",
                "Follow the defined file structure",
                "Use only specified technologies",
                "Keep code simple and readable",
                "Add comments for complex logic",
                "Handle errors gracefully"
            ]
            
            selected = get_choice(
                "Warnings for AI:",
                common_warnings + ["Other"],
                allow_multiple=True
            )
            
            if "Other" in selected:
                other = get_input("Other warnings:", multiline=True)
                selected = [w for w in selected if w != "Other"]
                selected.extend([w.strip() for w in other.split("\n") if w.strip()])
            
            self.spec.ai_warnings = selected


def run_implementation(spec: Spec) -> Spec:
    """Convenience function to run implementation phase."""
    implementer = ImplementationPhase(spec)
    return implementer.run_full_implementation()
