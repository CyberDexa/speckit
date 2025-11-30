# 🤖 Using Speckit with AI Coding Agents

This guide shows you how to go from idea to implementation with less frustration.

## The Problem You're Solving

When working with AI coding agents, you've probably experienced:

1. **Misunderstood requirements** - AI builds something different than you imagined
2. **Scope creep** - AI adds features you didn't want
3. **Wrong tech choices** - AI picks a stack you're not comfortable with
4. **Missing context** - AI asks the same questions repeatedly
5. **Lost progress** - Starting over because AI went down wrong path

**Speckit solves this** by creating a single source of truth for your project.

---

## Workflow Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Your Idea  │ ──► │   Speckit   │ ──► │   SPEC.md   │ ──► │  AI Agent   │
│             │     │  (refine)   │     │  (contract) │     │ (implement) │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

---

## Step 1: Capture Your Idea

### Quick Start (30 seconds)
```bash
cd ~/my-project
python ~/speckit/speckit.py quick "A CLI tool that tracks my daily tasks"
```

This generates a starter `SPEC.md` that you can refine.

### Full Spec (5-10 minutes)
```bash
python ~/speckit/speckit.py new
```

Answer the guided questions to create a comprehensive spec.

---

## Step 2: Review Your Spec

Open `SPEC.md` and check:

- [ ] **Overview** - Does the problem/solution match your vision?
- [ ] **Features** - Are must-haves truly essential? 
- [ ] **Non-goals** - Did you exclude enough to keep scope tight?
- [ ] **Tech stack** - Are you comfortable with these choices?
- [ ] **Phases** - Is Phase 1 small enough to validate quickly?

Edit directly if needed. The spec is for YOU, not for ceremony.

---

## Step 3: Start with AI

### Opening Prompt

```
I have a project I want to build. The full spec is in SPEC.md.

Please:
1. Read the entire spec carefully
2. Summarize your understanding in 2-3 sentences
3. List any clarifying questions before we start
4. Wait for my answers before implementing anything

Don't write any code yet.
```

This ensures AI understands before building.

### After AI Asks Questions

Answer the questions, then:

```
Great, let's start with Phase 1 only. 

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

## Step 4: Iterate Safely

### If AI Goes Off Track

```
Stop. This isn't matching the spec.

Look at the Non-Goals section - we explicitly said no {feature}.

Let's reset. Re-read SPEC.md and tell me what Phase 1 actually requires.
```

### If You Want to Change Direction

```
I want to modify the spec. Let's update these sections:

1. Change {X} to {Y}
2. Add {Z} to must-haves
3. Remove {W} from scope

Please update your understanding and we'll continue.
```

### Completing a Phase

```
Phase 1 is complete. Let's verify against success criteria:

[Paste the success criteria from SPEC.md]

Please confirm each item is done, or tell me what's missing.
```

---

## Pro Tips

### 1. Keep Phases Small
A phase should be completable in 1-2 hours. If it feels bigger, break it down.

```
Phase 1 feels too big. Let's split it:
- Phase 1a: Just the data model and database
- Phase 1b: Basic CRUD API
- Phase 1c: Simple frontend form

Let's start with 1a only.
```

### 2. Use Non-Goals Aggressively
Every time AI adds something you didn't ask for:

```
That's a non-goal. Add it to the Non-Goals section and remove it.
```

### 3. Validate Early
After Phase 1, actually use the thing:

```
Before Phase 2, I'm going to test Phase 1 manually.

[Test it]

Found some issues:
1. X doesn't work when Y
2. Z is confusing

Let's fix these before moving on.
```

### 4. Reference the Spec Constantly
When AI proposes something:

```
How does that fit with the spec? Specifically check:
- Does it match the user flow?
- Is it within scope?
- Does it use the agreed tech stack?
```

### 5. Save Working States
After each successful phase:

```
Phase 1 is working. Let's commit this state before Phase 2.

git add .
git commit -m "Phase 1 complete: basic functionality working"
```

---

## Common Prompts

### "Start a new project"
```
Read SPEC.md and implement Phase 1. Start with file structure, 
then implement each file. Pause after each major component.
```

### "Continue from where we left off"
```
We're working on [project]. The spec is in SPEC.md, currently on Phase 2.

Last session we completed: [X, Y, Z]
Next up: [remaining tasks from Phase 2]

Continue from there.
```

### "Something's broken"
```
There's an issue: [describe problem]

Relevant part of spec: [paste section]

Please fix while keeping alignment with the spec.
```

### "Add a new feature"
```
I want to add a feature that wasn't in the original spec.

New feature: [describe]

Please:
1. Suggest where this fits in the spec (P0, P1, or future?)
2. Identify any conflicts with existing requirements
3. Recommend if we should do this now or after MVP
```

### "Wrap up for the day"
```
Let's wrap up. Please provide:
1. Summary of what we completed
2. Current state (what's working, what's not)
3. Clear next steps for next session
4. Any decisions I need to make before we continue
```

---

## Example Session

```
You: I want to build a bookmark manager. Let me run speckit first.

[Run: python ~/speckit/speckit.py new]
[Answer questions, SPEC.md created]

You: Here's my project spec in SPEC.md. Please read it and 
     summarize your understanding.

AI: I understand you want a CLI bookmark manager that...
    Questions: 
    1. Should bookmarks sync across devices?
    2. What format for export?

You: 1. No sync, local only. 2. JSON export is fine.
     Add those to the spec. Now implement Phase 1.

AI: [Creates file structure]
    [Implements bookmark data model]
    [Creates add/list commands]
    
    Phase 1 complete. Would you like to test it?

You: Yes. Let me try it.
     
[Test: bookmark add "GitHub" https://github.com]
[Test: bookmark list]

You: Works! The output is hard to read though. Can you 
     add some formatting before we move to Phase 2?

AI: [Improves output formatting]

You: Perfect. Commit this as "Phase 1 complete" and 
     let's start Phase 2 tomorrow.
```

---

## Troubleshooting

### "AI keeps ignoring parts of my spec"
Re-paste the relevant section directly:

```
You're missing this requirement from the spec:

> "Must work offline - no external API calls"

Please fix your implementation to match.
```

### "AI's code is too complex"
```
This is overengineered for v1. Remember the constraints:
- Single file preferred
- Keep it simple

Simplify to the minimum that meets the spec.
```

### "I'm stuck on what to spec"
Start with the quick command and refine:

```bash
python ~/speckit/speckit.py quick "my idea in one sentence"
```

Then edit SPEC.md to add detail.

### "AI keeps asking things I already answered"
Point to the spec:

```
That's already in SPEC.md under [section]. 
Please reference the spec instead of asking again.
```

---

## Remember

1. **The spec is your anchor** - Always reference it
2. **Small phases = fast progress** - Validate early and often
3. **Non-goals are powerful** - Use them to prevent scope creep
4. **You're the product manager** - AI implements, you decide
5. **It's okay to update the spec** - Requirements evolve

Happy building! 🚀
