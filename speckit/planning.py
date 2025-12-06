"""
Planning Phase Module - Comprehensive project planning tools.

This module provides tools for:
- Requirements gathering and analysis
- User story creation
- Risk assessment
- Dependency mapping
- Timeline estimation
- Stakeholder analysis
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .core import Spec, Requirement, UserStory
from .utils import (
    Colors, print_header, print_subheader, print_section, print_tip,
    print_success, print_warning, print_info, get_input, get_choice,
    get_yes_no, get_rating, format_list, format_table
)


class PlanningPhase:
    """
    Handles the planning phase of spec creation.
    
    Guides users through comprehensive project planning including
    requirements, risks, dependencies, and timeline estimation.
    """
    
    def __init__(self, spec: Spec):
        self.spec = spec
    
    def run_full_planning(self) -> Spec:
        """Run the complete planning workflow."""
        print_header("Planning Phase", "📋")
        print("Let's plan your project thoroughly before diving into design.\n")
        
        self.gather_overview()
        self.gather_target_users()
        self.gather_requirements()
        self.gather_user_stories()
        self.gather_constraints()
        self.gather_assumptions()
        self.assess_risks()
        self.map_dependencies()
        self.define_scope()
        self.estimate_timeline()
        
        print_success("Planning phase complete!")
        return self.spec
    
    def gather_overview(self):
        """Gather basic project overview."""
        print_subheader("Project Overview", "🎯")
        
        print_tip("Start with the essentials - what problem are you solving?")
        
        self.spec.name = get_input("Project name:")
        
        self.spec.tagline = get_input(
            "One-line description (elevator pitch):",
            default="A tool that..."
        )
        
        print_section("The Problem")
        print_tip("What frustration, pain point, or need does this address?")
        self.spec.problem = get_input("What problem does this solve?", multiline=True)
        
        print_section("The Solution")
        print_tip("How does your idea solve this problem? What's unique about it?")
        self.spec.solution = get_input("How will this solve the problem?", multiline=True)
        
        print_section("Value Proposition")
        print_tip("Why would someone use this over alternatives?")
        self.spec.value_proposition = get_input(
            "What value does this provide?",
            default="It's simpler and more focused than alternatives"
        )
    
    def gather_target_users(self):
        """Identify and analyze target users."""
        print_subheader("Target Users", "👥")
        
        print_tip("Who will use this? Be specific - 'developers' is too broad")
        
        user_types = [
            "Solo developers",
            "Development teams",
            "Non-technical users",
            "Power users / Experts",
            "Myself only",
            "Other (specify)"
        ]
        
        selected = get_choice(
            "Who is this primarily for?",
            user_types,
            allow_multiple=True
        )
        
        if "Other (specify)" in selected:
            other = get_input("Describe your target users:")
            selected = [u for u in selected if u != "Other (specify)"]
            selected.append(other)
        
        self.spec.target_users = selected
        
        # User context
        if get_yes_no("Want to add more context about users?", default=False):
            print("\nDescribe user context (technical level, environment, etc.):")
            context = get_input("User context:", multiline=True)
            self.spec.target_users.append(f"Context: {context}")
    
    def gather_requirements(self):
        """Gather detailed requirements."""
        print_subheader("Requirements", "📝")
        
        print_tip("Requirements are specific, measurable things your project must do")
        
        # Functional requirements
        print_section("Functional Requirements")
        print("What specific capabilities must the system have?")
        print(f"{Colors.DIM}Example: 'System must validate email addresses'{Colors.END}")
        
        func_reqs = get_input("Functional requirements:", multiline=True)
        for req in func_reqs.split("\n"):
            if req.strip():
                self.spec.add_requirement(req.strip(), "P0", "functional")
        
        # Non-functional requirements
        if get_yes_no("Add non-functional requirements (performance, security)?", default=True):
            print_section("Non-Functional Requirements")
            print("Quality attributes like performance, security, usability:")
            
            nf_categories = {
                "Performance": "Response time, throughput, resource usage",
                "Security": "Authentication, authorization, data protection",
                "Usability": "Ease of use, accessibility, documentation",
                "Reliability": "Uptime, error handling, data integrity",
                "Scalability": "Growth handling, load management",
                "Maintainability": "Code quality, documentation, testing"
            }
            
            for category, description in nf_categories.items():
                print(f"\n{Colors.CYAN}{category}{Colors.END}: {Colors.DIM}{description}{Colors.END}")
                req = get_input(f"{category} requirements:", required=False)
                if req:
                    for r in req.split("\n"):
                        if r.strip():
                            self.spec.add_requirement(
                                f"[{category}] {r.strip()}", 
                                "P1", 
                                "non-functional"
                            )
    
    def gather_user_stories(self):
        """Create user stories."""
        print_subheader("User Stories", "📖")
        
        if not get_yes_no("Create user stories?", default=True):
            return
        
        print_tip("User stories capture what users want to do and why")
        print(f"{Colors.DIM}Format: As a [user], I want [feature] so that [benefit]{Colors.END}\n")
        
        story_count = 0
        while True:
            story_count += 1
            print(f"\n{Colors.CYAN}User Story #{story_count}{Colors.END}")
            
            as_a = get_input("As a [type of user]:")
            i_want = get_input("I want [feature/capability]:")
            so_that = get_input("So that [benefit/value]:")
            
            priority = get_choice(
                "Priority:",
                ["P0 - Must have", "P1 - Should have", "P2 - Nice to have"],
                default=2
            )
            priority_code = priority.split(" - ")[0]
            
            story = self.spec.add_user_story(as_a, i_want, so_that, priority_code)
            
            # Acceptance criteria
            if get_yes_no("Add acceptance criteria?", default=True):
                print("Enter acceptance criteria (one per line):")
                criteria = get_input("Criteria:", multiline=True)
                story.acceptance_criteria = [
                    c.strip() for c in criteria.split("\n") if c.strip()
                ]
            
            if not get_yes_no("Add another user story?", default=story_count < 3):
                break
    
    def gather_constraints(self):
        """Gather project constraints."""
        print_subheader("Constraints", "🔒")
        
        print_tip("Constraints are limitations you must work within")
        
        common_constraints = [
            "Must work offline",
            "No paid services/APIs",
            "Single file preferred",
            "Must be fast/lightweight",
            "Cross-platform support required",
            "No database required",
            "Privacy-focused (no telemetry)",
            "Beginner-friendly code required",
            "Must use existing codebase",
            "Limited development time",
            "Specific technology required"
        ]
        
        selected = get_choice(
            "Common constraints (select all that apply):",
            common_constraints + ["None", "Other (specify)"],
            allow_multiple=True
        )
        
        constraints = [c for c in selected if c not in ["None", "Other (specify)"]]
        
        if "Other (specify)" in selected:
            print("\nEnter additional constraints:")
            other = get_input("Other constraints:", multiline=True)
            constraints.extend([c.strip() for c in other.split("\n") if c.strip()])
        
        self.spec.constraints = constraints
        
        # Technical constraints
        if get_yes_no("Add technical constraints?", default=False):
            print("\nTechnical constraints (versions, compatibility, etc.):")
            tech = get_input("Technical constraints:", multiline=True)
            self.spec.constraints.extend([
                f"[Tech] {c.strip()}" for c in tech.split("\n") if c.strip()
            ])
    
    def gather_assumptions(self):
        """Document project assumptions."""
        print_subheader("Assumptions", "💭")
        
        if not get_yes_no("Document assumptions?", default=True):
            return
        
        print_tip("Assumptions are things you believe to be true but haven't verified")
        print(f"{Colors.DIM}Example: 'Users have Python 3.9+ installed'{Colors.END}")
        
        assumptions = get_input("What are you assuming?", multiline=True)
        self.spec.assumptions = [
            a.strip() for a in assumptions.split("\n") if a.strip()
        ]
    
    def assess_risks(self):
        """Perform risk assessment."""
        print_subheader("Risk Assessment", "⚠️")
        
        if not get_yes_no("Perform risk assessment?", default=True):
            return
        
        print_tip("Identify what could go wrong and how to handle it")
        
        common_risks = [
            ("Scope creep", "Project grows beyond original vision"),
            ("Technical complexity", "Implementation harder than expected"),
            ("Time underestimation", "Takes longer than planned"),
            ("Dependency issues", "Third-party tools/APIs change or fail"),
            ("Performance problems", "System too slow or resource-heavy"),
            ("Security vulnerabilities", "Potential security issues"),
        ]
        
        print("\nCommon project risks:")
        for i, (risk, desc) in enumerate(common_risks, 1):
            print(f"  {Colors.CYAN}{i}.{Colors.END} {risk} - {Colors.DIM}{desc}{Colors.END}")
        
        selected_indices = get_input(
            "\nWhich risks apply? (comma-separated numbers, or 'none'):",
            default="1,2,3"
        )
        
        if selected_indices.lower() != 'none':
            try:
                indices = [int(x.strip()) - 1 for x in selected_indices.split(",")]
                for i in indices:
                    if 0 <= i < len(common_risks):
                        risk_name, risk_desc = common_risks[i]
                        
                        impact = get_choice(
                            f"Impact of '{risk_name}':",
                            ["Low", "Medium", "High"],
                            default=2
                        )
                        
                        mitigation = get_input(
                            f"How will you mitigate '{risk_name}'?",
                            default="Monitor and address early"
                        )
                        
                        self.spec.risks.append({
                            "risk": risk_name,
                            "description": risk_desc,
                            "impact": impact,
                            "mitigation": mitigation
                        })
            except ValueError:
                pass
        
        # Custom risks
        if get_yes_no("Add custom risks?", default=False):
            while True:
                risk = get_input("Risk description:")
                impact = get_choice("Impact:", ["Low", "Medium", "High"])
                mitigation = get_input("Mitigation strategy:")
                
                self.spec.risks.append({
                    "risk": risk,
                    "impact": impact,
                    "mitigation": mitigation
                })
                
                if not get_yes_no("Add another risk?", default=False):
                    break
    
    def map_dependencies(self):
        """Map external dependencies."""
        print_subheader("External Dependencies", "🔗")
        
        if not get_yes_no("Map external dependencies?", default=True):
            return
        
        print_tip("What external services, APIs, or tools does this depend on?")
        
        dependency_types = [
            "Third-party APIs",
            "External services",
            "Open source libraries",
            "Development tools",
            "Infrastructure/hosting",
            "Data sources"
        ]
        
        print("\nDependency categories:")
        for dtype in dependency_types:
            deps = get_input(f"{dtype}:", required=False)
            if deps:
                for dep in deps.split(","):
                    if dep.strip():
                        self.spec.dependencies_external.append(
                            f"[{dtype}] {dep.strip()}"
                        )
    
    def define_scope(self):
        """Define project scope using MoSCoW prioritization."""
        print_subheader("Scope Definition (MoSCoW)", "🎯")
        
        print_tip("Prioritize features to keep scope manageable")
        print(f"{Colors.DIM}MoSCoW: Must have, Should have, Could have, Won't have{Colors.END}\n")
        
        # Must have (P0)
        print_section("Must Have (P0) - Critical for MVP")
        print("Without these, the project fails. Be strict!")
        must = get_input("Must-have features:", multiline=True)
        self.spec.features_must = [f.strip() for f in must.split("\n") if f.strip()]
        
        # Should have (P1)
        print_section("Should Have (P1) - Important but not critical")
        print("Important features for complete product:")
        should = get_input("Should-have features:", multiline=True, required=False)
        self.spec.features_should = [f.strip() for f in should.split("\n") if f.strip()]
        
        # Could have (P2)
        print_section("Could Have (P2) - Nice to have")
        print("Features for future iterations:")
        could = get_input("Could-have features:", multiline=True, required=False)
        self.spec.features_could = [f.strip() for f in could.split("\n") if f.strip()]
        
        # Won't have
        print_section("Won't Have - Explicitly out of scope")
        print_tip("This is IMPORTANT - it prevents scope creep!")
        wont = get_input("What is explicitly OUT of scope?", multiline=True, required=False)
        self.spec.features_wont = [f.strip() for f in wont.split("\n") if f.strip()]
    
    def estimate_timeline(self):
        """Estimate project timeline."""
        print_subheader("Timeline Estimation", "📅")
        
        # Auto-calculate based on complexity
        self.spec.update_metadata()
        
        print(f"\nBased on your scope, estimated complexity: {Colors.CYAN}{self.spec.complexity}{Colors.END}")
        print(f"Suggested timeline: {Colors.CYAN}{self.spec.timeline['with_buffer']}{Colors.END} (with 20% buffer)")
        
        if get_yes_no("Customize timeline?", default=False):
            custom = get_input("Your estimated timeline:")
            self.spec.timeline['custom'] = custom
        
        # Define phases
        if get_yes_no("Define implementation phases now?", default=True):
            self._define_phases()
    
    def _define_phases(self):
        """Helper to define implementation phases."""
        print("\n" + "─" * 40)
        print("Let's break the project into phases.\n")
        
        if self.spec.features_must and get_yes_no(
            "Auto-generate phases from features?", default=True
        ):
            # Auto-generate
            features = self.spec.features_must.copy()
            
            if len(features) <= 2:
                self.spec.add_phase(
                    name="Core Implementation",
                    description="Build all core functionality",
                    tasks=features,
                    deliverables=["Working MVP"]
                )
            else:
                # Split into foundation and completion
                mid = len(features) // 2
                self.spec.add_phase(
                    name="Foundation",
                    description="Core infrastructure and basic features",
                    tasks=features[:mid],
                    deliverables=["Basic working version"]
                )
                self.spec.add_phase(
                    name="Core Complete",
                    description="Remaining core features",
                    tasks=features[mid:],
                    deliverables=["Feature-complete MVP"]
                )
            
            # Polish phase
            self.spec.add_phase(
                name="Polish & Documentation",
                description="Refinement and documentation",
                tasks=[
                    "Error handling improvements",
                    "Documentation",
                    "Testing",
                    "Edge case handling"
                ],
                deliverables=["Production-ready release"]
            )
            
            # Enhancement phase if there are nice-to-haves
            if self.spec.features_should:
                self.spec.add_phase(
                    name="Enhancements",
                    description="Additional features",
                    tasks=self.spec.features_should[:5],
                    deliverables=["Enhanced version"]
                )
        else:
            # Manual phase definition
            phase_num = 0
            while True:
                phase_num += 1
                print(f"\n{Colors.CYAN}Phase {phase_num}{Colors.END}")
                
                name = get_input("Phase name:", default=f"Phase {phase_num}")
                description = get_input("Description:")
                tasks = get_input("Tasks (one per line):", multiline=True)
                deliverables = get_input("Deliverables (one per line):", multiline=True, required=False)
                
                self.spec.add_phase(
                    name=name,
                    description=description,
                    tasks=[t.strip() for t in tasks.split("\n") if t.strip()],
                    deliverables=[d.strip() for d in deliverables.split("\n") if d.strip()]
                )
                
                if not get_yes_no("Add another phase?", default=phase_num < 3):
                    break


def run_planning(spec: Spec) -> Spec:
    """Convenience function to run planning phase."""
    planner = PlanningPhase(spec)
    return planner.run_full_planning()
