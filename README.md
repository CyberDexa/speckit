# 🛠️ Speckit

**From idea to implementation - without the frustration.**

Speckit is a personal tool for solo developers to structure their ideas into clear, actionable specs that AI coding agents can understand and implement effectively.

## Why Speckit?

As a solo developer, you've probably experienced:
- 🤯 Explaining your idea 10 times and still getting the wrong implementation
- 😤 AI making assumptions that completely miss the point
- 🔄 Endless back-and-forth trying to course-correct
- 💭 Having a clear vision but struggling to articulate it

**Speckit solves this** by helping you think through your idea systematically and generate a clear spec that any AI coding agent can follow.

## Quick Start

```bash
# Navigate to your project folder (or create one)
cd ~/my-project

# Generate a new spec interactively
python ~/speckit/speckit.py new

# Or generate from a one-liner idea
python ~/speckit/speckit.py quick "A CLI tool that converts markdown to PDF"

# View your spec
cat SPEC.md
```

## How It Works

1. **Capture** - Write down your raw idea
2. **Clarify** - Answer guided questions to fill in gaps
3. **Structure** - Generate a clear, AI-ready spec
4. **Implement** - Hand the spec to any AI coding agent

## Spec Structure

Every spec includes:

```
📋 SPEC.md
├── Overview (what it is, who it's for)
├── Core Features (must-haves vs nice-to-haves)
├── Technical Decisions (stack, constraints)
├── User Flows (step-by-step interactions)
├── Data Model (what data exists)
├── API/Interface Design (how things connect)
├── File Structure (expected project layout)
└── Implementation Phases (ordered tasks)
```

## Usage with AI Agents

Once you have your `SPEC.md`, use it like this:

```
"I have a spec for a project I want to build. Please read SPEC.md 
and implement Phase 1. Ask clarifying questions before starting."
```

## Pro Tips

1. **Be specific about constraints** - "Must work offline" or "No external APIs"
2. **Include non-goals** - What you explicitly DON'T want
3. **Define success** - How will you know it's done?
4. **Start small** - Implement in phases, validate each one

## Files

- `speckit.py` - Main CLI tool
- `templates/` - Spec templates for different project types
- `examples/` - Example specs for reference
- `AI_WORKFLOW.md` - Guide for using specs with AI agents

## Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/speckit.git ~/speckit

# Optional: Add alias for convenience
echo 'alias speckit="python3 ~/speckit/speckit.py"' >> ~/.zshrc
source ~/.zshrc

# Now use it anywhere
speckit new
speckit quick "my idea"
```

## License

MIT - Use it however you want.

---

Made for frustrated solo devs who just want to build cool stuff. 🚀
