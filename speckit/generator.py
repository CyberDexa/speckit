"""
Markdown Generator - Creates sophisticated SPEC.md from Spec objects.

Generates comprehensive, AI-ready specification documents with:
- Project overview and context
- Technical architecture details
- Implementation phases with checklists
- AI-specific instructions
"""

from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path

from .core import Spec, Phase, Component, DataEntity, APIEndpoint


class MarkdownGenerator:
    """
    Generates sophisticated Markdown specification documents.
    """
    
    def __init__(self, spec: Spec):
        self.spec = spec
    
    def generate(self) -> str:
        """Generate the complete SPEC.md content."""
        sections = [
            self._header(),
            self._overview(),
            self._scope(),
            self._technical_architecture(),
            self._data_model(),
            self._api_specification(),
            self._user_flows(),
            self._file_structure(),
            self._implementation_phases(),
            self._testing_strategy(),
            self._deployment(),
            self._quality_requirements(),
            self._success_criteria(),
            self._ai_instructions(),
            self._appendix(),
            self._footer()
        ]
        
        return "\n".join(section for section in sections if section)
    
    def _header(self) -> str:
        """Generate document header."""
        s = self.spec
        
        # Format tech stack
        tech_parts = []
        for category, items in s.tech_stack.items():
            if items:
                tech_parts.extend(items)
        tech_str = ", ".join(tech_parts) if tech_parts else "TBD"
        
        return f"""# {s.name}

> {s.tagline}

| Property | Value |
|----------|-------|
| **Version** | {s.version} |
| **Type** | {s.project_type} |
| **Architecture** | {s.architecture_style or 'TBD'} |
| **Complexity** | {s.complexity} |
| **Timeline** | {s.timeline.get('with_buffer', 'TBD')} |
| **Created** | {s.created_at} |
| **Updated** | {s.updated_at} |

**Tech Stack:** {tech_str}

---
"""
    
    def _overview(self) -> str:
        """Generate overview section."""
        s = self.spec
        
        users_str = "\n".join(f"- {u}" for u in s.target_users) if s.target_users else "- TBD"
        
        return f"""## 🎯 Overview

### Problem Statement
{s.problem or '_To be defined_'}

### Solution
{s.solution or '_To be defined_'}

### Value Proposition
{s.value_proposition or '_To be defined_'}

### Target Users
{users_str}

---
"""
    
    def _scope(self) -> str:
        """Generate scope section with MoSCoW prioritization."""
        s = self.spec
        
        must = self._format_list(s.features_must) if s.features_must else "_None defined_"
        should = self._format_list(s.features_should) if s.features_should else "_None defined_"
        could = self._format_list(s.features_could) if s.features_could else "_None defined_"
        wont = self._format_list(s.features_wont) if s.features_wont else "_None defined - CAUTION: Set boundaries!_"
        
        # Requirements summary
        req_section = ""
        if s.requirements:
            p0_reqs = [r for r in s.requirements if r.priority == "P0"]
            p1_reqs = [r for r in s.requirements if r.priority == "P1"]
            
            if p0_reqs or p1_reqs:
                req_section = "\n### Key Requirements\n\n"
                if p0_reqs:
                    req_section += "**Critical (P0):**\n"
                    for req in p0_reqs:
                        req_section += f"- `{req.id}` {req.description}\n"
                if p1_reqs:
                    req_section += "\n**Important (P1):**\n"
                    for req in p1_reqs[:5]:
                        req_section += f"- `{req.id}` {req.description}\n"
                    if len(p1_reqs) > 5:
                        req_section += f"- _...and {len(p1_reqs) - 5} more_\n"
        
        # User stories summary
        story_section = ""
        if s.user_stories:
            story_section = "\n### User Stories\n\n"
            for story in s.user_stories[:5]:
                story_section += f"- **{story.id}** [{story.priority}]: As a {story.as_a}, I want {story.i_want}, so that {story.so_that}\n"
            if len(s.user_stories) > 5:
                story_section += f"\n_...and {len(s.user_stories) - 5} more user stories_\n"
        
        return f"""## ✨ Scope (MoSCoW)

### Must Have (P0) - Critical
{must}

### Should Have (P1) - Important  
{should}

### Could Have (P2) - Nice to Have
{could}

### Won't Have - Out of Scope ⚠️
{wont}
{req_section}{story_section}
---
"""
    
    def _technical_architecture(self) -> str:
        """Generate technical architecture section."""
        s = self.spec
        
        # Tech stack formatted
        stack_section = ""
        for category, items in s.tech_stack.items():
            if items:
                stack_section += f"- **{category.title()}:** {', '.join(items)}\n"
        
        if not stack_section:
            stack_section = "_TBD - To be decided with AI_"
        
        # Components
        comp_section = ""
        if s.components:
            comp_section = "\n### Components\n\n"
            for comp in s.components:
                comp_section += f"#### {comp.name}\n"
                comp_section += f"- **Type:** {comp.type}\n"
                comp_section += f"- **Description:** {comp.description}\n"
                if comp.technologies:
                    comp_section += f"- **Technologies:** {', '.join(comp.technologies)}\n"
                if comp.responsibilities:
                    comp_section += f"- **Responsibilities:**\n"
                    for resp in comp.responsibilities:
                        comp_section += f"  - {resp}\n"
                comp_section += "\n"
        
        # Architecture diagram
        diagram_section = ""
        if s.architecture_diagram:
            diagram_section = f"\n### Architecture Diagram\n\n{s.architecture_diagram}\n"
        
        # Constraints
        constraints = self._format_list(s.constraints) if s.constraints else "_None defined_"
        
        # Assumptions
        assumptions = self._format_list(s.assumptions) if s.assumptions else "_None defined_"
        
        # Risks
        risk_section = ""
        if s.risks:
            risk_section = "\n### Risk Assessment\n\n"
            risk_section += "| Risk | Impact | Mitigation |\n"
            risk_section += "|------|--------|------------|\n"
            for risk in s.risks:
                risk_section += f"| {risk.get('risk', 'N/A')} | {risk.get('impact', 'N/A')} | {risk.get('mitigation', 'N/A')} |\n"
        
        return f"""## 🏗️ Technical Architecture

### Style
**{s.architecture_style or 'TBD'}**

### Tech Stack
{stack_section}
{comp_section}{diagram_section}
### Constraints
{constraints}

### Assumptions
{assumptions}
{risk_section}
---
"""
    
    def _data_model(self) -> str:
        """Generate data model section."""
        s = self.spec
        
        if not s.data_entities:
            return ""
        
        content = "## 💾 Data Model\n\n"
        
        for entity in s.data_entities:
            content += f"### {entity.name}\n"
            content += f"{entity.description}\n\n"
            
            if entity.fields:
                content += "| Field | Type |\n"
                content += "|-------|------|\n"
                for field in entity.fields:
                    content += f"| {field.get('name', 'N/A')} | {field.get('type', 'N/A')} |\n"
                content += "\n"
            
            if entity.relationships:
                content += "**Relationships:**\n"
                for rel in entity.relationships:
                    content += f"- {rel}\n"
                content += "\n"
        
        content += "---\n"
        return content
    
    def _api_specification(self) -> str:
        """Generate API specification section."""
        s = self.spec
        
        if not s.api_endpoints:
            return ""
        
        content = "## 🔌 API Specification\n\n"
        content += "| Method | Endpoint | Description | Auth |\n"
        content += "|--------|----------|-------------|------|\n"
        
        for ep in s.api_endpoints:
            auth = "🔒" if ep.auth_required else "-"
            content += f"| `{ep.method}` | `{ep.path}` | {ep.description} | {auth} |\n"
        
        content += "\n### Endpoint Details\n\n"
        
        for ep in s.api_endpoints:
            content += f"#### `{ep.method} {ep.path}`\n"
            content += f"{ep.description}\n\n"
            
            if ep.auth_required:
                content += "**Authentication:** Required 🔒\n\n"
            
            if ep.request_body:
                content += "**Request Body:**\n```\n"
                content += ep.request_body.get('description', 'See implementation')
                content += "\n```\n\n"
            
            if ep.response:
                content += "**Response:**\n```\n"
                content += ep.response.get('description', 'See implementation')
                content += "\n```\n\n"
        
        content += "---\n"
        return content
    
    def _user_flows(self) -> str:
        """Generate user flows section."""
        s = self.spec
        
        if not s.user_flows:
            return ""
        
        content = "## 🚶 User Flows\n\n"
        
        for flow in s.user_flows:
            content += f"### {flow.get('name', 'Flow')}\n"
            if flow.get('description'):
                content += f"{flow['description']}\n\n"
            
            content += "```\n"
            for i, step in enumerate(flow.get('steps', []), 1):
                content += f"{i}. {step}\n"
            content += "```\n\n"
        
        content += "---\n"
        return content
    
    def _file_structure(self) -> str:
        """Generate file structure section."""
        s = self.spec
        
        if not s.file_structure:
            return ""
        
        return f"""## 📁 File Structure

```
{s.file_structure}
```

---
"""
    
    def _implementation_phases(self) -> str:
        """Generate implementation phases section."""
        s = self.spec
        
        if not s.phases:
            return """## 📊 Implementation Phases

_No phases defined yet. Work with AI to break down the project into phases._

---
"""
        
        content = "## 📊 Implementation Phases\n\n"
        
        for phase in s.phases:
            content += f"### Phase {phase.number}: {phase.name}\n"
            content += f"_{phase.description}_\n\n"
            
            if phase.estimated_duration:
                content += f"**Estimated Duration:** {phase.estimated_duration}\n\n"
            
            content += "**Tasks:**\n"
            for task in phase.tasks:
                content += f"- [ ] {task}\n"
            content += "\n"
            
            if phase.deliverables:
                content += "**Deliverables:**\n"
                for deliverable in phase.deliverables:
                    content += f"- {deliverable}\n"
                content += "\n"
            
            if phase.success_criteria:
                content += "**Success Criteria:**\n"
                for criterion in phase.success_criteria:
                    content += f"- {criterion}\n"
                content += "\n"
        
        content += "---\n"
        return content
    
    def _testing_strategy(self) -> str:
        """Generate testing strategy section."""
        s = self.spec
        
        has_testing = any(s.testing_strategy.values())
        if not has_testing:
            return ""
        
        content = "## 🧪 Testing Strategy\n\n"
        
        if s.testing_strategy.get('unit'):
            content += "### Unit Tests\n"
            for item in s.testing_strategy['unit']:
                content += f"- {item}\n"
            content += "\n"
        
        if s.testing_strategy.get('integration'):
            content += "### Integration Tests\n"
            for item in s.testing_strategy['integration']:
                content += f"- {item}\n"
            content += "\n"
        
        if s.testing_strategy.get('e2e'):
            content += "### End-to-End Tests\n"
            for item in s.testing_strategy['e2e']:
                content += f"- {item}\n"
            content += "\n"
        
        if s.testing_strategy.get('manual'):
            content += "### Manual Testing Checklist\n"
            for item in s.testing_strategy['manual']:
                content += f"- [ ] {item}\n"
            content += "\n"
        
        content += "---\n"
        return content
    
    def _deployment(self) -> str:
        """Generate deployment section."""
        s = self.spec
        
        if not s.deployment_strategy and not s.ci_cd_pipeline:
            return ""
        
        content = "## 🚀 Deployment\n\n"
        
        if s.deployment_strategy:
            content += f"### Strategy\n{s.deployment_strategy}\n\n"
        
        if s.ci_cd_pipeline:
            content += "### CI/CD Pipeline\n"
            for step in s.ci_cd_pipeline:
                content += f"1. {step}\n"
            content += "\n"
        
        content += "---\n"
        return content
    
    def _quality_requirements(self) -> str:
        """Generate quality requirements section."""
        s = self.spec
        
        has_quality = (s.performance_requirements or s.security_requirements or 
                      s.accessibility_requirements)
        if not has_quality:
            return ""
        
        content = "## ✨ Quality Requirements\n\n"
        
        if s.performance_requirements:
            content += "### Performance\n"
            for req in s.performance_requirements:
                content += f"- {req}\n"
            content += "\n"
        
        if s.security_requirements:
            content += "### Security\n"
            for req in s.security_requirements:
                content += f"- {req}\n"
            content += "\n"
        
        if s.accessibility_requirements:
            content += "### Accessibility\n"
            for req in s.accessibility_requirements:
                content += f"- {req}\n"
            content += "\n"
        
        content += "---\n"
        return content
    
    def _success_criteria(self) -> str:
        """Generate success criteria section."""
        s = self.spec
        
        if not s.success_criteria:
            return """## 🎯 Success Criteria

_No success criteria defined yet._

---
"""
        
        content = "## 🎯 Success Criteria\n\n"
        content += "The project is complete when:\n\n"
        
        for criterion in s.success_criteria:
            content += f"- [ ] {criterion}\n"
        
        content += "\n---\n"
        return content
    
    def _ai_instructions(self) -> str:
        """Generate AI instructions section."""
        s = self.spec
        
        content = """## 🤖 Instructions for AI

When implementing this specification:

"""
        
        # Standard instructions
        content += """### Before Starting
1. **Read the entire spec** before writing any code
2. **Summarize your understanding** in 2-3 sentences
3. **Ask clarifying questions** if anything is ambiguous
4. **Confirm the approach** before implementing

### During Implementation
1. **Implement one phase at a time** - validate before moving on
2. **Follow the file structure** defined above
3. **Respect all constraints** listed in Technical Architecture
4. **Use only specified technologies** unless discussing alternatives
5. **Add comments** for complex logic
6. **Handle errors gracefully** with meaningful messages

### After Each Phase
1. **Run tests** if defined
2. **Check against success criteria**
3. **Summarize what was done**
4. **Identify any blockers** before moving on

"""
        
        # Clarifying questions
        if s.ai_questions:
            content += "### Questions to Address Before Starting\n"
            for question in s.ai_questions:
                content += f"- {question}\n"
            content += "\n"
        
        # Warnings
        if s.ai_warnings:
            content += "### ⚠️ Important Warnings\n"
            for warning in s.ai_warnings:
                content += f"- {warning}\n"
            content += "\n"
        
        # Context
        if s.ai_context and s.ai_context != "Standard implementation following spec":
            content += f"### Additional Context\n{s.ai_context}\n\n"
        
        # Suggested first prompt
        content += f"""### Suggested First Prompt

```
I have a project spec I'd like you to implement: "{s.name}"

Please:
1. Read SPEC.md carefully  
2. Summarize your understanding in 2-3 sentences
3. List any clarifying questions
4. Wait for my answers before starting Phase 1
```

"""
        
        content += "---\n"
        return content
    
    def _appendix(self) -> str:
        """Generate appendix with additional details."""
        s = self.spec
        
        has_appendix = s.dependencies_external or (len(s.requirements) > 5)
        if not has_appendix:
            return ""
        
        content = "## 📎 Appendix\n\n"
        
        if s.dependencies_external:
            content += "### External Dependencies\n"
            for dep in s.dependencies_external:
                content += f"- {dep}\n"
            content += "\n"
        
        if len(s.requirements) > 5:
            content += "### All Requirements\n\n"
            content += "| ID | Priority | Category | Description |\n"
            content += "|----|----------|----------|-------------|\n"
            for req in s.requirements:
                content += f"| {req.id} | {req.priority} | {req.category} | {req.description} |\n"
            content += "\n"
        
        content += "---\n"
        return content
    
    def _footer(self) -> str:
        """Generate document footer."""
        return f"""
*Generated with Speckit 2.0 🛠️*
*Spec Version: {self.spec.version}*
"""
    
    def _format_list(self, items: List[str], bullet: str = "-") -> str:
        """Format a list with bullets."""
        if not items:
            return "_None_"
        return "\n".join(f"{bullet} {item}" for item in items)
    
    def save(self, filepath: Path):
        """Save the generated markdown to a file."""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        content = self.generate()
        with open(filepath, 'w') as f:
            f.write(content)
        
        return filepath


def generate_spec_markdown(spec: Spec) -> str:
    """Convenience function to generate markdown from spec."""
    generator = MarkdownGenerator(spec)
    return generator.generate()


def save_spec_markdown(spec: Spec, filepath: Path) -> Path:
    """Convenience function to save spec markdown."""
    generator = MarkdownGenerator(spec)
    return generator.save(filepath)
