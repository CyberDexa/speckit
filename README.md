# 🛠️ Speckit 2.0

**From idea to sophisticated implementation - without the frustration.**

Speckit is a comprehensive tool for solo developers to structure ideas into production-ready specs that AI coding agents can understand and implement effectively.

## 🆕 What's New in 2.0

- **Three-Phase Workflow**: Planning → Design → Implementation
- **Sophisticated Templates**: Pre-configured specs for CLI, Web Apps, APIs, Libraries, SaaS
- **Requirements Engineering**: MoSCoW prioritization, user stories, risk assessment
- **Architecture Design**: Component diagrams, Mermaid integration, API contracts
- **Implementation Planning**: Testing strategy, CI/CD pipelines, deployment configuration
- **AI-Optimized Output**: Structured specs that AI agents understand and execute well

## 🚀 Quick Start

```bash
# Navigate to your project folder
cd ~/my-project

# Full interactive spec (recommended for new projects)
python -m speckit.cli new

# Quick spec from a one-liner
python -m speckit.cli quick "A CLI tool that converts markdown to PDF"

# Use a template
python -m speckit.cli new --template api

# Run individual phases
python -m speckit.cli plan
python -m speckit.cli design
python -m speckit.cli implement
```

## 📋 How It Works

### The Three Phases

```
┌──────────────────────────────────────────────────────────────────────┐
│                         SPECKIT WORKFLOW                              │
├──────────────┬──────────────────┬──────────────────┬────────────────┤
│   📋 PLAN    │    🎨 DESIGN     │   🚀 IMPLEMENT   │   🤖 BUILD     │
├──────────────┼──────────────────┼──────────────────┼────────────────┤
│ • Overview   │ • Architecture   │ • Phases         │ Hand spec to   │
│ • Users      │ • Components     │ • Testing        │ AI agent for   │
│ • Features   │ • Data Model     │ • CI/CD          │ implementation │
│ • Scope      │ • APIs           │ • Deployment     │                │
│ • Risks      │ • User Flows     │ • Success        │                │
│ • Timeline   │ • File Structure │   Criteria       │                │
└──────────────┴──────────────────┴──────────────────┴────────────────┘
```

### Phase 1: Planning 📋

Capture and validate your idea:
- **Problem & Solution**: What you're building and why
- **Target Users**: Who will use this
- **Requirements**: Functional and non-functional needs
- **Scope (MoSCoW)**: Must/Should/Could/Won't have
- **Risks**: What could go wrong and how to mitigate
- **Timeline**: Complexity-based estimation

### Phase 2: Design 🎨

Make technical decisions:
- **Architecture**: Monolith, Microservices, Serverless, etc.
- **Tech Stack**: Frontend, Backend, Database, Infrastructure
- **Components**: System building blocks and responsibilities
- **Data Model**: Entities, fields, relationships
- **API Design**: Endpoints, request/response formats
- **User Flows**: Step-by-step interaction paths
- **File Structure**: Project organization

### Phase 3: Implementation 🚀

Plan the build:
- **Phases**: Break down into manageable chunks
- **Testing Strategy**: Unit, integration, E2E, manual
- **CI/CD Pipeline**: Build, test, deploy automation
- **Deployment**: Platform and strategy
- **Quality Requirements**: Performance, security, accessibility
- **Success Criteria**: Definition of "done"
- **AI Instructions**: Guidance for AI implementation

## 📁 Output

Speckit generates two files:

### SPEC.md
A comprehensive, AI-ready specification document containing:
- Project overview and context
- Feature prioritization (MoSCoW)
- Technical architecture with diagrams
- Data models and API specifications
- Implementation phases with checklists
- Testing and deployment plans
- AI-specific instructions

### SPEC.json
Machine-readable format for:
- Editing and re-running phases
- Importing into other tools
- Version control and diffing

## 🎯 Templates

Pre-configured specs for common project types:

| Template | Best For |
|----------|----------|
| `cli` | Command-line tools and scripts |
| `webapp` | Full-stack web applications |
| `api` | REST/GraphQL backend services |
| `library` | Reusable packages and libraries |
| `saas` | Software-as-a-Service applications |

```bash
# Use a template
python -m speckit.cli new --template webapp
python -m speckit.cli templates  # List all templates
```

## 💡 Pro Tips

### 1. Be Strict About Scope
The "Won't Have" section is crucial. Be explicit about what's out of scope.

### 2. Keep Phases Small
Each phase should be completable in 1-2 days.

### 3. Define Success Clearly
Measurable criteria help you know when you're done.

### 4. Use Templates as Starting Points
Templates give you structure; customize for your needs.

## 🤖 Using with AI Agents

See [AI_WORKFLOW.md](./AI_WORKFLOW.md) for the complete guide.

### Quick Start with AI

After generating your spec:

```
I have a project spec in SPEC.md. Please:
1. Read the entire spec carefully
2. Summarize your understanding in 2-3 sentences
3. List any clarifying questions
4. Wait for my answers before starting Phase 1
```

## 📂 Project Structure

```
speckit/
├── speckit/
│   ├── __init__.py      # Package initialization
│   ├── cli.py           # Command-line interface
│   ├── core.py          # Core data structures
│   ├── planning.py      # Planning phase logic
│   ├── design.py        # Design phase logic
│   ├── implementation.py # Implementation phase logic
│   ├── generator.py     # Markdown generation
│   ├── templates.py     # Project templates
│   └── utils.py         # Utility functions
├── examples/            # Example specifications
├── AI_WORKFLOW.md       # AI usage guide
└── README.md            # This file
```

## 🔧 Installation

```bash
# Clone the repo
git clone https://github.com/CyberDexa/speckit.git ~/speckit

# Optional: Create an alias
echo 'alias speckit="python3 -m speckit.cli"' >> ~/.zshrc
source ~/.zshrc

# Now use it anywhere
speckit new
speckit quick "my idea"
```

## 📚 Examples

Check the `examples/` folder for complete specifications.

## 🤝 Philosophy

1. **Specs are for humans first, AI second**
2. **Constraints liberate** - Well-defined boundaries prevent scope creep
3. **Small phases, fast feedback** - Validate early and often
4. **Non-goals are goals** - Explicitly stating what you won't do is powerful
5. **The spec is a contract** - Reference it constantly during implementation

## 📝 License

MIT - Use it however you want.

---

Made for developers who want to build sophisticated projects without the chaos. 🚀
