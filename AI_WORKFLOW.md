# 🤖 Using Speckit 2.0 with AI Coding Agents

This guide shows you how to go from idea to sophisticated implementation with AI assistance.

## The Problem Speckit Solves

When working with AI coding agents, you've probably experienced:

1. **Misunderstood requirements** - AI builds something different than you imagined
2. **Scope creep** - AI adds features you didn't want
3. **Wrong tech choices** - AI picks a stack you're not comfortable with
4. **Missing context** - AI asks the same questions repeatedly
5. **Lost progress** - Starting over because AI went down wrong path
6. **Incomplete implementations** - Features half-done or missing edge cases

**Speckit solves this** by creating a comprehensive, structured spec that serves as a contract between you and the AI.

---

## Workflow Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Your Idea  │ ──► │   Speckit   │ ──► │   SPEC.md   │ ──► │  AI Agent   │
│             │     │ (3 phases)  │     │  (contract) │     │ (implement) │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    ▼      ▼      ▼
                  Plan  Design  Implement
```

---

## Step 1: Create Your Spec

### Full Spec (10-15 minutes) - Recommended
```bash
cd ~/my-project
python -m speckit.cli new
```

This walks you through all three phases:
1. **Planning**: Capture requirements, scope, risks
2. **Design**: Architecture, components, APIs
3. **Implementation**: Phases, testing, deployment

### Quick Spec (30 seconds)
```bash
python -m speckit.cli quick "A CLI tool that tracks my daily tasks"
```

### With Template
```bash
python -m speckit.cli new --template api
```

---

## Step 2: Review Your Spec

Before handing to AI, verify:

### Planning Section
- [ ] **Problem/Solution** - Does it match your vision?
- [ ] **Must-haves** - Are these truly essential for MVP?
- [ ] **Won't-haves** - Did you exclude enough?
- [ ] **Risks** - Are major risks identified?

### Design Section
- [ ] **Architecture** - Is this appropriate for scope?
- [ ] **Tech stack** - Are you comfortable with these?
- [ ] **Components** - Are responsibilities clear?

### Implementation Section
- [ ] **Phases** - Is Phase 1 small enough to validate?
- [ ] **Success criteria** - Will you know when it's done?

---

## Step 3: Start with AI

### The Opening Prompt

```
I have a project I want to build. The full specification is in SPEC.md.

Please:
1. Read the ENTIRE spec carefully (all sections)
2. Summarize your understanding in 2-3 sentences
3. List any clarifying questions before we start
4. Wait for my answers before implementing anything

Do not write any code yet.
```

### After AI Asks Questions

Answer thoroughly, then:

```
Great. Now let's start with Phase 1 ONLY.

Please:
1. Propose the file structure for Phase 1
2. Explain your implementation approach
3. Wait for my approval before writing code
```

### Approving the Approach

```
That approach looks good. Please implement Phase 1.
After each file, pause and let me review before continuing.
```

---

## Step 4: During Implementation

### Keep AI Focused

When AI goes off-track:

```
Stop. Look at the spec.
The Non-Goals section explicitly says no [feature].
Let's stay focused on Phase 1 requirements only.
```

### Reference the Spec Constantly

```
How does that fit with the spec? Check:
- Is it in the Must-Have features?
- Does it match the defined architecture?
- Is it within the current phase scope?
```

### Complete One Phase at a Time

```
Let's verify Phase 1 is complete before moving on.

From SPEC.md, Phase 1 success criteria:
- [ ] [criterion 1]
- [ ] [criterion 2]

Please confirm each is done.
```

---

## Step 5: Phase Transitions

### Completing a Phase

```
Phase 1 looks complete. Before Phase 2:
1. Let me test the current implementation
2. I'll report any issues
3. Then we'll review Phase 2 requirements

[Test it]

Found these issues: [list issues]
Let's fix these before moving on.
```

### Starting Next Phase

```
Phase 1 is working. Let's commit:

git add .
git commit -m "Phase 1 complete: [summary]"

Now, let's review Phase 2 from SPEC.md.
```

---

## Common Prompts

### "AI keeps adding unwanted features"

```
Stop. You're adding [feature] which is NOT in the spec.
Check the Won't Have section. Remove this.
```

### "AI's code is too complex"

```
This is overengineered. The Constraints section says:
> "Keep it simple and readable"
Simplify to the minimum that meets Phase 1.
```

### "Need to change requirements"

```
I want to modify the spec. Updates:
1. Move [X] from Must-Have to Could-Have
2. Add [Y] to Won't-Have

Please acknowledge and update your understanding.
```

### "Starting a new session"

```
I'm continuing work on [project].

Context:
- Spec: SPEC.md
- Last session: Completed [X, Y, Z]
- Current phase: Phase [N]

Please confirm and continue.
```

### "Wrapping up"

```
Let's wrap up. Please provide:
1. Summary of what we completed
2. Current state (working/not working)
3. Next steps for next session
```

---

## Pro Tips

### 1. Keep Phases Small
Each phase should be completable in 1-2 hours.

### 2. Use Non-Goals Aggressively
Every time AI adds something you didn't ask for, point to Non-Goals.

### 3. Validate Early
After Phase 1, actually use the thing before Phase 2.

### 4. Save Working States
Commit after each successful phase.

### 5. The Spec is Your Anchor
Always reference it. Update it when requirements change.

---

## Example Session

```
You: I want to build a bookmark manager. Let me create a spec first.

[Run: python -m speckit.cli new]
[Answer questions through all three phases]
[SPEC.md generated]

You: Here's my project spec in SPEC.md. Please read it and 
     summarize your understanding.

AI: I understand you want a CLI bookmark manager that...
    Questions: 
    1. Should bookmarks sync across devices?
    2. What format for export?

You: 1. No sync, local only. 2. JSON export is fine.
     Now implement Phase 1.

AI: [Creates file structure]
    [Implements bookmark data model]
    [Creates add/list commands]
    
    Phase 1 complete.

You: Let me test it.
     
[Test: bookmark add "GitHub" https://github.com]
[Test: bookmark list]

You: Works! Commit as "Phase 1 complete" and 
     we'll start Phase 2 tomorrow.
```

---

## Remember

1. **The spec is your anchor** - Always reference it
2. **Small phases = fast progress** - Validate early
3. **Non-goals are powerful** - Prevent scope creep
4. **You're the product manager** - AI implements, you decide
5. **It's okay to update the spec** - Requirements evolve

Happy building! 🚀

*Speckit 2.0*
