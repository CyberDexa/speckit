# Markdown to PDF CLI

> A command-line tool that converts Markdown files to styled PDFs

**Generated:** 2024-01-15 14:00  
**Type:** CLI Tool  
**Stack:** Python

---

## 🎯 Overview

### Problem
I write documentation and notes in Markdown but sometimes need PDF versions for sharing with non-technical people. Existing tools are complex, have too many dependencies, or produce ugly output.

### Solution
A simple CLI that takes a Markdown file and produces a clean, well-styled PDF with sensible defaults.

### Target User
Me. Fellow developers who write Markdown.

---

## ✨ Features

### Must Have (P0)
- Convert single .md file to .pdf
- Sensible default styling (readable, professional)
- Code block syntax highlighting
- Support for images (local paths)
- Table support

### Nice to Have (P1)
- Custom CSS styling
- Table of contents generation
- Header/footer with page numbers
- Watch mode (auto-regenerate)
- Batch convert (whole folder)

### Non-Goals (Out of Scope)
- GUI interface
- Live preview
- Markdown editing
- Cloud service integration

---

## 🔧 Technical Decisions

### Language
Python 3.9+

### Key Libraries
- `markdown` - Markdown parsing
- `weasyprint` - HTML to PDF (or `pdfkit`)
- `pygments` - Syntax highlighting

### Constraints
- Single pip install (no external binaries if possible)
- Works offline
- Cross-platform (macOS, Linux, Windows)

---

## 🚶 User Flows

### Basic Usage
```bash
md2pdf document.md
# → Creates document.pdf in same directory
```

### With Options
```bash
md2pdf document.md -o output.pdf --style github
# → Creates output.pdf with GitHub-style formatting
```

### Batch Convert
```bash
md2pdf ./docs/*.md --output-dir ./pdfs
# → Converts all .md files to PDFs in ./pdfs/
```

### Help
```bash
md2pdf --help

Usage: md2pdf [OPTIONS] INPUT...

Convert Markdown files to PDF.

Arguments:
  INPUT  Markdown file(s) to convert

Options:
  -o, --output PATH      Output file path
  --output-dir PATH      Output directory (for batch)
  -s, --style STYLE      Style preset (default, github, academic)
  --css PATH             Custom CSS file
  --toc                  Generate table of contents
  --no-highlight         Disable code highlighting
  -w, --watch            Watch for changes
  -v, --verbose          Verbose output
  --version              Show version
  -h, --help             Show this help
```

---

## 📁 File Structure

```
md2pdf/
├── md2pdf/
│   ├── __init__.py
│   ├── __main__.py      # Entry: python -m md2pdf
│   ├── cli.py           # Argument parsing
│   ├── converter.py     # Core conversion logic
│   ├── styles.py        # Style presets
│   └── assets/
│       ├── default.css
│       ├── github.css
│       └── academic.css
├── tests/
│   ├── test_converter.py
│   └── fixtures/
│       └── sample.md
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## 📊 Implementation Phases

### Phase 1: Basic Conversion
- [ ] Set up project structure
- [ ] Implement Markdown to HTML
- [ ] Implement HTML to PDF
- [ ] Basic CLI (input file → output file)
- [ ] Test with sample Markdown

### Phase 2: Styling
- [ ] Create default CSS
- [ ] Add syntax highlighting for code
- [ ] Support images (convert paths)
- [ ] Add style presets (github, academic)

### Phase 3: CLI Polish
- [ ] Add all CLI options
- [ ] Custom CSS support
- [ ] Batch conversion
- [ ] Proper error messages
- [ ] Progress output

### Phase 4: Distribution
- [ ] Write README
- [ ] Add tests
- [ ] Publish to PyPI
- [ ] Create release

---

## 🎯 Success Criteria

- [ ] `md2pdf README.md` produces README.pdf
- [ ] Code blocks are syntax highlighted
- [ ] Tables render correctly
- [ ] PDF looks professional (not ugly default)
- [ ] Works with my actual documentation

---

## 💬 Instructions for AI

Start with Phase 1. Get basic conversion working with hardcoded style.

Implementation notes:
- Prefer weasyprint over pdfkit (fewer dependencies)
- Use python-markdown with extensions (tables, fenced_code)
- Pygments for syntax highlighting

Test with this sample:
```markdown
# Test Document

This is a paragraph with **bold** and *italic*.

## Code Example

\`\`\`python
def hello():
    print("Hello, world!")
\`\`\`

## Table

| Name | Value |
|------|-------|
| Foo  | 123   |
| Bar  | 456   |
```

---

*Generated with Speckit 🛠️*
