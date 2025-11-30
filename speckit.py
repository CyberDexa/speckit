#!/usr/bin/env python3
"""
Speckit - From idea to implementation without the frustration.

A tool for solo developers to structure ideas into clear, AI-ready specs.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 50}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}  {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 50}{Colors.END}\n")

def print_section(text):
    print(f"\n{Colors.BOLD}{Colors.YELLOW}▸ {text}{Colors.END}")

def print_tip(text):
    print(f"{Colors.DIM}  💡 {text}{Colors.END}")

def print_success(text):
    print(f"\n{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"\n{Colors.RED}✗ {text}{Colors.END}")

def get_input(prompt, required=True, multiline=False, default=None):
    """Get input from user with optional multiline support."""
    if default:
        prompt = f"{prompt} [{default}]"
    
    print(f"{Colors.BLUE}{prompt}{Colors.END}")
    
    if multiline:
        print(f"{Colors.DIM}  (Enter an empty line to finish){Colors.END}")
        lines = []
        while True:
            line = input("  ")
            if line == "":
                break
            lines.append(line)
        value = "\n".join(lines)
    else:
        value = input("  → ").strip()
    
    if not value and default:
        return default
    
    if required and not value:
        print_error("This field is required. Please try again.")
        return get_input(prompt, required, multiline, default)
    
    return value

def get_choice(prompt, options, allow_multiple=False):
    """Get a choice from a list of options."""
    print(f"\n{Colors.BLUE}{prompt}{Colors.END}")
    for i, option in enumerate(options, 1):
        print(f"  {Colors.CYAN}{i}.{Colors.END} {option}")
    
    if allow_multiple:
        print(f"{Colors.DIM}  (Enter numbers separated by commas, e.g., 1,3,4){Colors.END}")
        choices = input("  → ").strip()
        try:
            indices = [int(x.strip()) - 1 for x in choices.split(",")]
            return [options[i] for i in indices if 0 <= i < len(options)]
        except (ValueError, IndexError):
            return [options[0]]
    else:
        try:
            choice = int(input("  → ").strip()) - 1
            return options[choice] if 0 <= choice < len(options) else options[0]
        except (ValueError, IndexError):
            return options[0]

def get_yes_no(prompt, default=True):
    """Get a yes/no answer."""
    default_str = "Y/n" if default else "y/N"
    print(f"{Colors.BLUE}{prompt} [{default_str}]{Colors.END}")
    answer = input("  → ").strip().lower()
    if not answer:
        return default
    return answer in ('y', 'yes', 'true', '1')


class Spec:
    """Represents a project specification."""
    
    def __init__(self):
        self.data = {
            "name": "",
            "tagline": "",
            "problem": "",
            "solution": "",
            "target_user": "",
            "project_type": "",
            "tech_stack": [],
            "constraints": [],
            "features_must": [],
            "features_nice": [],
            "non_goals": [],
            "user_flows": [],
            "data_models": [],
            "api_endpoints": [],
            "file_structure": [],
            "phases": [],
            "success_criteria": [],
            "questions_for_ai": [],
        }
    
    def gather_overview(self):
        """Gather basic project overview."""
        print_header("📋 Let's capture your idea")
        
        print_tip("Don't overthink it - just describe what you want to build")
        self.data["name"] = get_input("Project name:")
        
        self.data["tagline"] = get_input(
            "One-line description (what is it?):",
            default="A tool that..."
        )
        
        print_section("The Problem")
        print_tip("What frustration or need does this solve?")
        self.data["problem"] = get_input("What problem does this solve?", multiline=True)
        
        print_section("The Solution")
        print_tip("How does your idea solve this problem?")
        self.data["solution"] = get_input("How will this work?", multiline=True)
        
        print_section("Target User")
        print_tip("Who will use this? 'Me' is a valid answer!")
        self.data["target_user"] = get_input("Who is this for?", default="Me (solo developer)")
    
    def gather_project_type(self):
        """Determine project type and tech stack."""
        print_header("🔧 Technical Decisions")
        
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
            "Other"
        ]
        
        self.data["project_type"] = get_choice(
            "What type of project is this?",
            project_types
        )
        
        # Suggest tech stacks based on project type
        stack_suggestions = {
            "CLI Tool": ["Python", "Node.js", "Go", "Rust", "Bash"],
            "Web App (Full-stack)": ["Next.js", "Python + FastAPI + React", "Node.js + Express + React", "Django", "Ruby on Rails"],
            "Web App (Frontend only)": ["React", "Vue", "Svelte", "Plain HTML/CSS/JS", "Astro"],
            "API/Backend Service": ["Python + FastAPI", "Node.js + Express", "Go", "Python + Flask", "Rust + Actix"],
            "Desktop App": ["Electron", "Tauri", "Python + Tkinter", "Swift (macOS)", ".NET MAUI"],
            "Mobile App": ["React Native", "Flutter", "Swift (iOS)", "Kotlin (Android)"],
            "Browser Extension": ["JavaScript", "TypeScript"],
            "Library/Package": ["Python", "JavaScript/TypeScript", "Rust", "Go"],
            "Automation Script": ["Python", "Bash", "Node.js"],
        }
        
        suggestions = stack_suggestions.get(self.data["project_type"], ["Python", "JavaScript", "Other"])
        
        print_section("Tech Stack")
        print_tip("Pick what you're comfortable with, or let AI suggest")
        
        self.data["tech_stack"] = get_choice(
            "What tech stack? (select all that apply)",
            suggestions + ["Let AI decide", "Other (specify later)"],
            allow_multiple=True
        )
        
        print_section("Constraints")
        print_tip("Any limitations or requirements to keep in mind?")
        
        common_constraints = [
            "Must work offline",
            "No paid services/APIs",
            "Single file preferred",
            "Must be fast/lightweight",
            "Cross-platform support",
            "No database required",
            "Privacy-focused (no telemetry)",
            "Must be beginner-friendly code",
        ]
        
        selected = get_choice(
            "Any constraints? (select all that apply)",
            common_constraints + ["None", "Other (I'll specify)"],
            allow_multiple=True
        )
        
        if "Other (I'll specify)" in selected:
            other = get_input("Specify other constraints:", multiline=True)
            selected.append(other)
        
        self.data["constraints"] = [c for c in selected if c not in ["None", "Other (I'll specify)"]]
    
    def gather_features(self):
        """Gather feature requirements."""
        print_header("✨ Features")
        
        print_section("Must-Have Features")
        print_tip("Core features - without these, the project fails")
        print("Enter each feature on a new line:")
        self.data["features_must"] = [
            f.strip() for f in get_input("Must-have features:", multiline=True).split("\n")
            if f.strip()
        ]
        
        print_section("Nice-to-Have Features")
        print_tip("Would be great, but not essential for v1")
        print("Enter each feature on a new line:")
        self.data["features_nice"] = [
            f.strip() for f in get_input("Nice-to-have features:", required=False, multiline=True).split("\n")
            if f.strip()
        ]
        
        print_section("Non-Goals")
        print_tip("What do you explicitly NOT want? This helps AI avoid scope creep")
        self.data["non_goals"] = [
            f.strip() for f in get_input("What is OUT of scope?", required=False, multiline=True).split("\n")
            if f.strip()
        ]
    
    def gather_user_flows(self):
        """Gather user interaction flows."""
        print_header("🚶 User Flows")
        print_tip("Describe how someone will actually use this")
        
        if get_yes_no("Do you want to define user flows?", default=True):
            print("\nDescribe the main user journey step by step:")
            print(f"{Colors.DIM}Example: 1. User runs command, 2. Enters their idea, 3. Gets a spec file{Colors.END}")
            
            flow = get_input("Main user flow:", multiline=True)
            self.data["user_flows"] = [{"name": "Main Flow", "steps": flow}]
            
            while get_yes_no("Add another user flow?", default=False):
                name = get_input("Flow name (e.g., 'Error handling', 'Advanced usage'):")
                steps = get_input(f"Steps for '{name}':", multiline=True)
                self.data["user_flows"].append({"name": name, "steps": steps})
    
    def gather_data_model(self):
        """Gather data model information."""
        print_header("💾 Data & Storage")
        
        needs_data = get_yes_no("Does this project need to store/manage data?", default=True)
        
        if needs_data:
            print_tip("Describe what data exists and its structure")
            print("\nExample: User has name, email, preferences. Project has title, files, created date.")
            
            data = get_input("What data/entities exist?", multiline=True)
            self.data["data_models"] = data
            
            storage_options = [
                "Files (JSON, YAML, etc.)",
                "SQLite database",
                "PostgreSQL/MySQL",
                "In-memory only",
                "Browser localStorage",
                "Let AI decide",
            ]
            storage = get_choice("How should data be stored?", storage_options)
            self.data["constraints"].append(f"Storage: {storage}")
    
    def gather_phases(self):
        """Break down into implementation phases."""
        print_header("📊 Implementation Phases")
        print_tip("Breaking into phases helps AI (and you) stay focused")
        
        if self.data["features_must"]:
            print("\nBased on your must-have features, let's create phases.")
            print("You can group features into phases or let me suggest.")
            
            if get_yes_no("Should I auto-generate phases from your features?", default=True):
                # Auto-generate phases
                features = self.data["features_must"]
                if len(features) <= 3:
                    self.data["phases"] = [
                        {"name": "Phase 1: Core Implementation", "tasks": features}
                    ]
                else:
                    mid = len(features) // 2
                    self.data["phases"] = [
                        {"name": "Phase 1: Foundation", "tasks": features[:mid]},
                        {"name": "Phase 2: Complete Core", "tasks": features[mid:]},
                    ]
                
                if self.data["features_nice"]:
                    self.data["phases"].append({
                        "name": "Phase 3: Enhancements",
                        "tasks": self.data["features_nice"][:3]
                    })
                
                print("\nGenerated phases:")
                for phase in self.data["phases"]:
                    print(f"  {Colors.CYAN}{phase['name']}{Colors.END}")
                    for task in phase["tasks"]:
                        print(f"    - {task}")
            else:
                self.data["phases"] = []
                phase_num = 1
                while True:
                    name = get_input(f"Phase {phase_num} name:", default=f"Phase {phase_num}")
                    tasks = get_input(f"Tasks for {name}:", multiline=True)
                    self.data["phases"].append({
                        "name": name,
                        "tasks": [t.strip() for t in tasks.split("\n") if t.strip()]
                    })
                    if not get_yes_no("Add another phase?", default=phase_num < 3):
                        break
                    phase_num += 1
    
    def gather_success_criteria(self):
        """Define what success looks like."""
        print_header("🎯 Success Criteria")
        print_tip("How will you know when it's done and working?")
        
        print("\nExample: 'I can run the command and get a spec file in under 10 seconds'")
        criteria = get_input("What does 'done' look like?", multiline=True)
        self.data["success_criteria"] = [
            c.strip() for c in criteria.split("\n") if c.strip()
        ]
    
    def gather_ai_questions(self):
        """Identify questions the AI should ask."""
        print_header("❓ Questions for AI")
        print_tip("What should the AI clarify before implementing?")
        
        suggestions = [
            "Best practices for this type of project",
            "Error handling approach",
            "Testing strategy",
            "Performance considerations",
            "Security considerations",
        ]
        
        selected = get_choice(
            "What should AI ask about before starting?",
            suggestions + ["None - I've covered everything", "Other"],
            allow_multiple=True
        )
        
        self.data["questions_for_ai"] = [
            q for q in selected 
            if q not in ["None - I've covered everything", "Other"]
        ]
    
    def generate_spec_markdown(self):
        """Generate the final SPEC.md content."""
        d = self.data
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        spec = f"""# {d['name']}

> {d['tagline']}

**Generated:** {now}  
**Type:** {d['project_type']}  
**Stack:** {', '.join(d['tech_stack']) if d['tech_stack'] else 'TBD'}

---

## 🎯 Overview

### Problem
{d['problem']}

### Solution
{d['solution']}

### Target User
{d['target_user']}

---

## ✨ Features

### Must Have (P0)
{self._format_list(d['features_must'])}

### Nice to Have (P1)
{self._format_list(d['features_nice']) if d['features_nice'] else '_None defined_'}

### Non-Goals (Out of Scope)
{self._format_list(d['non_goals']) if d['non_goals'] else '_None defined - be careful of scope creep!_'}

---

## 🔧 Technical Decisions

### Tech Stack
{self._format_list(d['tech_stack'])}

### Constraints
{self._format_list(d['constraints']) if d['constraints'] else '_No specific constraints_'}

---

## 🚶 User Flows

"""
        for flow in d['user_flows']:
            spec += f"### {flow['name']}\n\n"
            spec += f"```\n{flow['steps']}\n```\n\n"
        
        if d['data_models']:
            spec += f"""---

## 💾 Data Model

{d['data_models']}

"""
        
        spec += """---

## 📊 Implementation Phases

"""
        for phase in d['phases']:
            spec += f"### {phase['name']}\n\n"
            for task in phase['tasks']:
                spec += f"- [ ] {task}\n"
            spec += "\n"
        
        spec += f"""---

## 🎯 Success Criteria

{self._format_list(d['success_criteria'])}

---

## 💬 Instructions for AI

When implementing this spec:

1. **Read the entire spec first** before writing any code
2. **Ask clarifying questions** if anything is ambiguous
3. **Implement one phase at a time** and validate before moving on
4. **Respect the constraints** listed above
5. **Check against success criteria** before marking complete

### Questions to Address
{self._format_list(d['questions_for_ai']) if d['questions_for_ai'] else '_No specific questions - proceed with best judgment_'}

### Suggested First Prompt
```
I have a project spec I'd like you to implement. Please read SPEC.md carefully, 
then ask any clarifying questions before we start with Phase 1.
```

---

*Generated with Speckit 🛠️*
"""
        return spec
    
    def _format_list(self, items):
        if not items:
            return "_None_"
        return "\n".join(f"- {item}" for item in items)


def interactive_new(output_path=None):
    """Run interactive spec generation."""
    print_header("🛠️  SPECKIT - Idea to Implementation")
    print("Let's turn your idea into a clear, actionable spec.\n")
    print(f"{Colors.DIM}Tip: You can skip optional questions by pressing Enter{Colors.END}")
    
    spec = Spec()
    
    try:
        spec.gather_overview()
        spec.gather_project_type()
        spec.gather_features()
        spec.gather_user_flows()
        spec.gather_data_model()
        spec.gather_phases()
        spec.gather_success_criteria()
        spec.gather_ai_questions()
    except KeyboardInterrupt:
        print_error("\nCancelled. No spec was saved.")
        return
    
    # Generate and save
    output = output_path or Path.cwd() / "SPEC.md"
    content = spec.generate_spec_markdown()
    
    with open(output, "w") as f:
        f.write(content)
    
    print_success(f"Spec saved to: {output}")
    print(f"\n{Colors.BOLD}Next Steps:{Colors.END}")
    print(f"  1. Review your spec: {Colors.CYAN}cat SPEC.md{Colors.END}")
    print(f"  2. Open with AI agent and paste:")
    print(f"     {Colors.DIM}\"Please read SPEC.md and implement Phase 1\"{Colors.END}")


def quick_spec(idea, output_path=None):
    """Generate a quick spec from a one-liner."""
    print_header("🛠️  SPECKIT - Quick Spec")
    print(f"Generating spec for: {Colors.CYAN}{idea}{Colors.END}\n")
    
    # Create a minimal spec
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    spec = f"""# Quick Spec

> {idea}

**Generated:** {now}  
**Type:** TBD  
**Stack:** TBD (AI to suggest)

---

## 🎯 Overview

### The Idea
{idea}

### Problem & Solution
_To be refined with AI_

---

## ✨ Features

### Must Have
- [ ] Core functionality as described above
- [ ] Basic error handling
- [ ] Clear usage instructions

### Nice to Have
- [ ] Additional features TBD

### Non-Goals
_None defined yet - discuss with AI to set boundaries_

---

## 📊 Implementation Phases

### Phase 1: MVP
- [ ] Basic working version of the idea
- [ ] Minimal but functional

### Phase 2: Polish
- [ ] Error handling
- [ ] Documentation
- [ ] Edge cases

---

## 💬 Instructions for AI

This is a quick spec - please help refine it:

1. **Ask clarifying questions** about the idea
2. **Suggest appropriate tech stack** based on requirements  
3. **Identify potential challenges** before implementation
4. **Propose a file structure** for the project
5. **Break down Phase 1** into specific tasks

### Suggested First Prompt
```
I have a quick idea I want to build: "{idea}"

Please help me:
1. Understand what I'm trying to build
2. Ask any clarifying questions
3. Suggest the best tech stack
4. Outline the implementation approach
```

---

*Generated with Speckit 🛠️*
"""
    
    output = output_path or Path.cwd() / "SPEC.md"
    with open(output, "w") as f:
        f.write(spec)
    
    print_success(f"Quick spec saved to: {output}")
    print(f"\n{Colors.BOLD}This is a starter spec. Open it with your AI agent to refine it.{Colors.END}")


def show_examples():
    """Show example specs."""
    print_header("📚 Example Specs")
    
    examples = [
        ("CLI Todo App", "A simple command-line todo list manager"),
        ("URL Shortener", "A web service that shortens URLs"),
        ("Markdown Blog", "A static site generator for markdown blog posts"),
    ]
    
    print("Example project ideas and how to spec them:\n")
    for name, desc in examples:
        print(f"  {Colors.CYAN}{name}{Colors.END}")
        print(f"  {Colors.DIM}{desc}{Colors.END}")
        print(f"  → speckit quick \"{desc}\"\n")
    
    print(f"\nFor full examples, see: {Colors.CYAN}~/speckit/examples/{Colors.END}")


def main():
    parser = argparse.ArgumentParser(
        description="Speckit - From idea to implementation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  speckit new                    Interactive spec generation
  speckit quick "My idea"        Generate quick spec from one-liner
  speckit examples               Show example specs

For more info: https://github.com/yourname/speckit
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # new command
    new_parser = subparsers.add_parser("new", help="Create a new spec interactively")
    new_parser.add_argument("-o", "--output", help="Output file path", default=None)
    
    # quick command
    quick_parser = subparsers.add_parser("quick", help="Generate a quick spec from idea")
    quick_parser.add_argument("idea", help="Your idea in one sentence")
    quick_parser.add_argument("-o", "--output", help="Output file path", default=None)
    
    # examples command
    subparsers.add_parser("examples", help="Show example specs")
    
    # templates command
    templates_parser = subparsers.add_parser("templates", help="List available templates")
    
    args = parser.parse_args()
    
    if args.command == "new":
        interactive_new(args.output)
    elif args.command == "quick":
        quick_spec(args.idea, args.output)
    elif args.command == "examples":
        show_examples()
    elif args.command == "templates":
        print_header("📁 Available Templates")
        print("  • webapp - Full-stack web application")
        print("  • cli - Command-line tool")
        print("  • api - REST API service")
        print("  • script - Automation script")
        print(f"\n  Use: {Colors.CYAN}speckit new --template webapp{Colors.END}")
    else:
        parser.print_help()
        print(f"\n{Colors.YELLOW}Quick start:{Colors.END} speckit new")


if __name__ == "__main__":
    main()
