---
name: Skill Authoring
description: Create and refine Agent Skills (custom capabilities for Claude). Use when creating new Skills, understanding Skill architecture, following best practices, or debugging Skill discovery and loading issues. References canonical Anthropic documentation.
---

# Skill Authoring

This Skill helps you create effective Agent Skills for Claude. Skills are modular capabilities that extend Claude's functionality through instructions, code, and resources that load progressively as needed.

## When to use this Skill

- Creating a new Agent Skill from scratch
- Understanding how Skills work (progressive disclosure, filesystem architecture)
- Following best practices for Skill authoring
- Debugging Skill discovery or loading issues
- Reviewing and refining existing Skills

## Quick start

**To create your first Skill:**

1. Create a directory: `.claude/skills/your-skill-name/`
2. Add a `SKILL.md` file with YAML frontmatter
3. Start with the template: see [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md)
4. For a complete example: see [SIMPLE_EXAMPLE.md](SIMPLE_EXAMPLE.md)

**Minimum required structure:**

```yaml
---
name: Your Skill Name
description: What this Skill does and when to use it
---

# Your Skill Name

[Instructions for Claude to follow]
```

## Core concepts

### Progressive disclosure

Skills load content in three levels to minimize context usage:

**Level 1: Metadata (always loaded)**
- Only the `name` and `description` from YAML frontmatter
- Loaded at startup into system prompt (~100 tokens per Skill)
- Used for Skill discovery

**Level 2: Instructions (loaded when triggered)**
- The body of SKILL.md
- Claude reads this via bash when the Skill becomes relevant
- Keep under 500 lines for optimal performance

**Level 3: Resources (loaded as needed)**
- Additional files referenced from SKILL.md
- Scripts, examples, reference docs, data files
- Loaded only when Claude needs them

**Key principle:** Only relevant content occupies context at any time.

### Filesystem-based architecture

Skills exist as directories in a code execution environment. Claude navigates them using bash commands:

- **Files are read on-demand** via bash Read tools
- **Scripts are executed** without loading their code into context
- **No context penalty** for bundled files until they're accessed
- **All file paths** must use forward slashes (Unix-style)

### Reference depth rule

**All reference files must link directly from SKILL.md** (one level deep only).

**Good (one level):**
```
SKILL.md references → FORMS.md
SKILL.md references → REFERENCE.md
```

**Bad (nested references):**
```
SKILL.md references → advanced.md references → details.md
```

When references are nested too deeply, Claude may partially read files, resulting in incomplete information.

## YAML frontmatter requirements

Every SKILL.md must include exactly two fields in YAML frontmatter:

```yaml
---
name: Your Skill Name        # Max 64 characters
description: Brief description of what this Skill does and when to use it  # Max 1024 characters
---
```

**No other fields are supported.**

### Writing effective descriptions

The description enables Skill discovery. Include both **what** the Skill does and **when** to use it.

**Always write in third person** (the description is injected into system prompt):

✓ **Good:** "Processes Excel files and generates reports. Use when analyzing spreadsheets, tabular data, or .xlsx files."

✗ **Avoid:** "I can help you process Excel files"

✗ **Avoid:** "You can use this to process Excel files"

**Be specific and include key terms:**

✓ **Good:** "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."

✗ **Bad:** "Helps with documents"

### Token budgets

- **SKILL.md body:** Keep under 500 lines for optimal performance
- **Metadata:** ~100 tokens per Skill (always loaded)
- **Additional files:** No limit (loaded only as needed)

If SKILL.md approaches 500 lines, split content into separate files and reference them.

## Common patterns

### Template pattern

Provide templates for consistent output formats:

````markdown
## Report structure

Use this template:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data

## Recommendations
1. Specific actionable recommendation
```
````

### Examples pattern

Show input/output pairs to clarify desired style:

````markdown
## Commit message format

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

Follow this style for all commit messages.
````

### Workflow pattern

Break complex operations into clear sequential steps:

````markdown
## Document editing workflow

1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow"
   **Editing existing content?** → Follow "Editing workflow"

2. Creation workflow:
   - Use docx-js library
   - Build document from scratch

3. Editing workflow:
   - Unpack existing document
   - Modify XML directly
   - Validate after each change
````

### Conditional details pattern

Show basic content inline, link to advanced topics:

```markdown
## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

**For tracked changes:** See [REDLINING.md](REDLINING.md)
**For OOXML details:** See [OOXML.md](OOXML.md)
```

Claude reads the additional files only when needed.

## File organization

### Simple Skill (single file)

```
my-skill/
└── SKILL.md
```

Use when all content fits comfortably under 500 lines.

### Skill with references (one level deep)

```
my-skill/
├── SKILL.md (overview + navigation)
├── REFERENCE.md (API reference)
├── EXAMPLES.md (usage examples)
└── scripts/
    └── validate.py (utility script)
```

All files link directly from SKILL.md.

### Domain-organized Skill

```
bigquery-skill/
├── SKILL.md (overview + navigation)
└── reference/
    ├── finance.md
    ├── sales.md
    └── product.md
```

When user asks about sales, Claude only loads sales.md, not finance or product.

## Common anti-patterns to avoid

### Don't use Windows-style paths

✓ **Good:** `scripts/helper.py`, `reference/guide.md`

✗ **Bad:** `scripts\helper.py`, `reference\guide.md`

### Don't nest references deeply

✓ **Good:** All files referenced directly from SKILL.md

✗ **Bad:** SKILL.md → advanced.md → details.md

### Don't offer too many options

✓ **Good:** "Use pdfplumber for text extraction. For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."

✗ **Bad:** "You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or..."

### Don't include time-sensitive information

✓ **Good:** Use a "Legacy patterns" collapsible section

✗ **Bad:** "If you're doing this before August 2025, use the old API."

### Don't be verbose when concise works

✓ **Good:** "Use pdfplumber to extract text from PDFs."

✗ **Bad:** "PDF (Portable Document Format) files are a common file format that contains text, images, and other content. To extract text from a PDF, you'll need to use a library..."

**Remember:** Claude is already very smart. Only add context Claude doesn't already have.

## Detailed documentation

For comprehensive guidance, use WebFetch to read the canonical Anthropic documentation:

**Skills overview (architecture, how Skills work):**
https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview

**Best practices (authoring guidance, patterns, evaluation):**
https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices

These docs cover:
- How progressive disclosure works in detail
- Security considerations
- Skills with executable code
- Evaluation-driven development
- Iterative development with Claude
- Advanced patterns (workflows, feedback loops, validation)
- Platform-specific guidance (API, Claude Code, claude.ai)

## Resources

**Quick start:**
- Template: [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md) - Copy-paste ready starter
- Example: [SIMPLE_EXAMPLE.md](SIMPLE_EXAMPLE.md) - Well-structured Skill example

**Quality assurance:**
- Checklist: [CHECKLIST.md](CHECKLIST.md) - Pre-publish verification

**Comprehensive docs:**
- Use WebFetch with URLs above for detailed guidance

## Development workflow

1. **Identify gaps:** Run Claude on tasks without a Skill, document failures
2. **Create evaluations:** Build 3+ test scenarios
3. **Establish baseline:** Measure performance without the Skill
4. **Write minimal instructions:** Create just enough to pass evaluations
5. **Iterate:** Test, measure, refine

**Work with Claude to create Skills:**
- Use one instance of Claude ("Claude A") to design and refine the Skill
- Test with another instance ("Claude B") that has the Skill loaded
- Observe Claude B's behavior on real tasks
- Bring insights back to Claude A for improvements

## Key principles

1. **Concise is key** - The context window is a public good
2. **Set appropriate degrees of freedom** - Match specificity to task fragility
3. **Test with all models** - Haiku, Sonnet, and Opus have different needs
4. **Use progressive disclosure** - Load only what's needed when it's needed
5. **Keep references one level deep** - All files link directly from SKILL.md
