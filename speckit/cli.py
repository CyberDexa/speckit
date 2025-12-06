#!/usr/bin/env python3
"""
Speckit CLI - From idea to sophisticated implementation.

A comprehensive tool for solo developers to structure ideas into
production-ready specs with planning, design, and implementation phases.

Usage:
    speckit new                    Full interactive spec generation
    speckit quick "My idea"        Quick spec from one-liner  
    speckit plan                   Run planning phase only
    speckit design                 Run design phase only
    speckit implement              Run implementation phase only
    speckit templates              List available templates
    speckit examples               Show example specs
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .core import Spec, SpecBuilder
from .planning import PlanningPhase
from .design import DesignPhase
from .implementation import ImplementationPhase
from .generator import MarkdownGenerator
from .templates import list_templates, apply_template, get_template_for_project_type
from .utils import (
    Colors, print_header, print_subheader, print_success, print_error,
    print_warning, print_info, print_tip, get_input, get_choice, get_yes_no
)


def interactive_new(output_path: Optional[str] = None, template: Optional[str] = None):
    """Run full interactive spec generation with all phases."""
    print_header("SPECKIT - From Idea to Implementation", "🛠️")
    print("Let's create a comprehensive, AI-ready specification.\n")
    print(f"{Colors.DIM}This process covers: Planning → Design → Implementation{Colors.END}")
    print(f"{Colors.DIM}Tip: Press Ctrl+C anytime to exit without saving{Colors.END}\n")
    
    spec = Spec()
    
    try:
        # Apply template if specified
        if template:
            spec = apply_template(spec, template)
            print_info(f"Applied template: {template}")
        
        # Phase 1: Planning
        print_subheader("PHASE 1: PLANNING", "📋")
        planner = PlanningPhase(spec)
        spec = planner.run_full_planning()
        
        # Ask if user wants to continue to design
        if not get_yes_no("\nContinue to Design phase?", default=True):
            return _save_and_exit(spec, output_path)
        
        # Auto-apply template based on project type if not already applied
        if not template and spec.project_type:
            suggested_template = get_template_for_project_type(spec.project_type)
            if suggested_template:
                if get_yes_no(f"Apply '{suggested_template}' template for common settings?", default=True):
                    spec = apply_template(spec, suggested_template)
                    print_success(f"Applied {suggested_template} template")
        
        # Phase 2: Design
        print_subheader("PHASE 2: DESIGN", "🎨")
        designer = DesignPhase(spec)
        spec = designer.run_full_design()
        
        # Ask if user wants to continue to implementation
        if not get_yes_no("\nContinue to Implementation phase?", default=True):
            return _save_and_exit(spec, output_path)
        
        # Phase 3: Implementation
        print_subheader("PHASE 3: IMPLEMENTATION", "🚀")
        implementer = ImplementationPhase(spec)
        spec = implementer.run_full_implementation()
        
        # Save the spec
        _save_and_exit(spec, output_path)
        
    except KeyboardInterrupt:
        print_warning("\nInterrupted. Saving partial spec...")
        _save_and_exit(spec, output_path, partial=True)


def _save_and_exit(spec: Spec, output_path: Optional[str] = None, partial: bool = False):
    """Save the spec and show next steps."""
    output = Path(output_path) if output_path else Path.cwd() / "SPEC.md"
    
    # Generate and save markdown
    generator = MarkdownGenerator(spec)
    content = generator.generate()
    
    with open(output, "w") as f:
        f.write(content)
    
    # Also save JSON for future editing
    json_output = output.with_suffix(".json")
    spec.save_json(json_output)
    
    if partial:
        print_warning(f"Partial spec saved to: {output}")
    else:
        print_success(f"Spec saved to: {output}")
        print_info(f"JSON backup saved to: {json_output}")
    
    print(f"\n{Colors.BOLD}📊 Spec Summary:{Colors.END}")
    print(f"  • Project: {spec.name or 'Unnamed'}")
    print(f"  • Type: {spec.project_type or 'TBD'}")
    print(f"  • Complexity: {spec.complexity}")
    print(f"  • Phases: {len(spec.phases)}")
    print(f"  • Features: {len(spec.features_must)} must-have, {len(spec.features_should)} should-have")
    
    print(f"\n{Colors.BOLD}🚀 Next Steps:{Colors.END}")
    print(f"  1. Review your spec: {Colors.CYAN}cat SPEC.md{Colors.END}")
    print(f"  2. Open with AI agent and use this prompt:")
    print(f"\n{Colors.DIM}     \"I have a project spec in SPEC.md. Please:")
    print(f"      1. Read the entire spec carefully")
    print(f"      2. Summarize your understanding")
    print(f"      3. Ask clarifying questions")
    print(f"      4. Wait for my answers before starting Phase 1\"{Colors.END}")


def quick_spec(idea: str, output_path: Optional[str] = None):
    """Generate a quick spec from a one-liner idea."""
    print_header("SPECKIT - Quick Spec", "⚡")
    print(f"Generating spec for: {Colors.CYAN}{idea}{Colors.END}\n")
    
    builder = SpecBuilder(level="quick")
    spec = builder.build_quick(idea)
    
    output = Path(output_path) if output_path else Path.cwd() / "SPEC.md"
    
    generator = MarkdownGenerator(spec)
    content = generator.generate()
    
    with open(output, "w") as f:
        f.write(content)
    
    print_success(f"Quick spec saved to: {output}")
    print(f"\n{Colors.BOLD}This is a starter spec.{Colors.END}")
    print("Open it with your AI agent to refine the details.\n")
    
    print("Suggested prompt:")
    print(f"{Colors.DIM}\"I have a quick idea I want to build. The spec is in SPEC.md.")
    print(f"Please help me refine it by asking clarifying questions.\"{Colors.END}")


def run_phase(phase: str, input_path: Optional[str] = None, output_path: Optional[str] = None):
    """Run a specific phase on an existing or new spec."""
    spec = Spec()
    
    # Try to load existing spec
    if input_path:
        try:
            spec = Spec.load_json(Path(input_path))
            print_info(f"Loaded existing spec from {input_path}")
        except FileNotFoundError:
            print_warning(f"No spec found at {input_path}, starting fresh")
    
    try:
        if phase == "plan":
            print_header("Planning Phase", "📋")
            planner = PlanningPhase(spec)
            spec = planner.run_full_planning()
        elif phase == "design":
            print_header("Design Phase", "🎨")
            designer = DesignPhase(spec)
            spec = designer.run_full_design()
        elif phase == "implement":
            print_header("Implementation Phase", "🚀")
            implementer = ImplementationPhase(spec)
            spec = implementer.run_full_implementation()
        
        _save_and_exit(spec, output_path)
        
    except KeyboardInterrupt:
        print_warning("\nInterrupted.")


def show_templates():
    """Show available templates."""
    print_header("Available Templates", "📁")
    
    templates = list_templates()
    
    for tmpl in templates:
        print(f"  {Colors.CYAN}{tmpl['key']}{Colors.END}")
        print(f"    {tmpl['name']} - {tmpl['description']}")
        print()
    
    print(f"Use templates with: {Colors.CYAN}speckit new --template <name>{Colors.END}")


def show_examples():
    """Show example usage and specs."""
    print_header("Example Usage", "📚")
    
    examples = [
        {
            "title": "Full Spec Generation",
            "command": "speckit new",
            "description": "Interactive walkthrough of all phases"
        },
        {
            "title": "Quick Spec",
            "command": 'speckit quick "A CLI that converts markdown to PDF"',
            "description": "Generate a starter spec from a one-liner"
        },
        {
            "title": "With Template",
            "command": "speckit new --template api",
            "description": "Pre-fill with API project settings"
        },
        {
            "title": "Planning Only",
            "command": "speckit plan",
            "description": "Run just the planning phase"
        },
        {
            "title": "Design Existing Spec",
            "command": "speckit design --input SPEC.json",
            "description": "Add design to an existing spec"
        }
    ]
    
    for ex in examples:
        print(f"{Colors.CYAN}{ex['title']}{Colors.END}")
        print(f"  {Colors.DIM}${Colors.END} {ex['command']}")
        print(f"  {Colors.DIM}{ex['description']}{Colors.END}")
        print()
    
    print(f"\nFor full examples, check: {Colors.CYAN}examples/{Colors.END}")


def show_version():
    """Show version information."""
    from . import __version__
    print(f"Speckit v{__version__}")
    print("From idea to sophisticated implementation 🛠️")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Speckit - From idea to sophisticated implementation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  speckit new                        Full interactive spec generation
  speckit new --template webapp      Use a template
  speckit quick "My idea"            Generate quick spec
  speckit plan                       Run planning phase only
  speckit design                     Run design phase only  
  speckit implement                  Run implementation phase only
  speckit templates                  List available templates
  speckit examples                   Show example usage

For more info: https://github.com/CyberDexa/speckit
        """
    )
    
    parser.add_argument("--version", action="store_true", help="Show version")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # new command
    new_parser = subparsers.add_parser("new", help="Create a new spec interactively")
    new_parser.add_argument("-o", "--output", help="Output file path", default=None)
    new_parser.add_argument("-t", "--template", help="Template to use", default=None)
    
    # quick command
    quick_parser = subparsers.add_parser("quick", help="Generate quick spec from idea")
    quick_parser.add_argument("idea", help="Your idea in one sentence")
    quick_parser.add_argument("-o", "--output", help="Output file path", default=None)
    
    # plan command
    plan_parser = subparsers.add_parser("plan", help="Run planning phase only")
    plan_parser.add_argument("-i", "--input", help="Input spec JSON file", default=None)
    plan_parser.add_argument("-o", "--output", help="Output file path", default=None)
    
    # design command
    design_parser = subparsers.add_parser("design", help="Run design phase only")
    design_parser.add_argument("-i", "--input", help="Input spec JSON file", default=None)
    design_parser.add_argument("-o", "--output", help="Output file path", default=None)
    
    # implement command
    impl_parser = subparsers.add_parser("implement", help="Run implementation phase only")
    impl_parser.add_argument("-i", "--input", help="Input spec JSON file", default=None)
    impl_parser.add_argument("-o", "--output", help="Output file path", default=None)
    
    # templates command
    subparsers.add_parser("templates", help="List available templates")
    
    # examples command
    subparsers.add_parser("examples", help="Show example usage")
    
    args = parser.parse_args()
    
    if args.version:
        show_version()
        return
    
    if args.command == "new":
        interactive_new(args.output, args.template)
    elif args.command == "quick":
        quick_spec(args.idea, args.output)
    elif args.command == "plan":
        run_phase("plan", args.input, args.output)
    elif args.command == "design":
        run_phase("design", args.input, args.output)
    elif args.command == "implement":
        run_phase("implement", args.input, args.output)
    elif args.command == "templates":
        show_templates()
    elif args.command == "examples":
        show_examples()
    else:
        parser.print_help()
        print(f"\n{Colors.YELLOW}Quick start:{Colors.END} speckit new")


if __name__ == "__main__":
    main()
