# Skill Quality Checklist

Use this checklist before publishing a Skill. Copy into your response when reviewing Skills.

## Core quality

### YAML frontmatter
- [ ] `name` field present (max 64 characters)
- [ ] `description` field present (max 1024 characters)
- [ ] Description written in third person (not "I" or "you")
- [ ] Description includes what the Skill does
- [ ] Description includes when to use the Skill
- [ ] Description includes key terms and trigger words
- [ ] No unsupported fields in frontmatter

### Structure and organization
- [ ] SKILL.md body is under 500 lines
- [ ] Content is concise (assumes Claude is smart)
- [ ] Additional details split into separate files if needed
- [ ] All file references are one level deep (no nested references)
- [ ] File paths use forward slashes (Unix-style, not Windows)
- [ ] Files are named descriptively (not doc1.md, file2.md)

### Content quality
- [ ] No time-sensitive information (or in "old patterns" section)
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] Clear workflows with sequential steps
- [ ] Instructions match appropriate degree of freedom for task
- [ ] Practical, actionable guidance included

### Navigation and discovery
- [ ] Clear "When to use this Skill" section
- [ ] Quick start or minimal example provided
- [ ] References to additional files are clear and explicit
- [ ] Longer reference files include table of contents
- [ ] Organization supports progressive disclosure

## Code and scripts (if applicable)

### Error handling
- [ ] Scripts solve problems rather than punt to Claude
- [ ] Error handling is explicit and helpful
- [ ] Error messages guide Claude toward fixes
- [ ] No "voodoo constants" (all values justified with comments)

### Dependencies and environment
- [ ] Required packages listed in instructions
- [ ] Package availability verified in code execution environment
- [ ] No assumptions about installed packages
- [ ] Scripts are well-documented

### Validation and quality
- [ ] Validation/verification steps for critical operations
- [ ] Feedback loops included for quality-critical tasks
- [ ] Intermediate outputs are verifiable (e.g., plan files)
- [ ] Scripts provide clear success/failure indicators

## Testing and validation

### Evaluation
- [ ] At least three evaluation scenarios created
- [ ] Evaluations test real use cases, not edge cases only
- [ ] Baseline performance measured without the Skill
- [ ] Skill improves performance on evaluations

### Model testing
- [ ] Tested with Claude Haiku (fast, economical)
- [ ] Tested with Claude Sonnet (balanced)
- [ ] Tested with Claude Opus (powerful reasoning)
- [ ] Works well across all target models

### Real-world testing
- [ ] Tested with real usage scenarios
- [ ] Observed how Claude navigates the Skill
- [ ] Verified Claude finds and uses bundled files correctly
- [ ] Team feedback incorporated (if applicable)

### Discovery testing
- [ ] Skill activates when expected (description is effective)
- [ ] Skill doesn't activate on unrelated requests
- [ ] Claude loads appropriate reference files
- [ ] Claude doesn't load unnecessary files

## Common anti-patterns (avoid these)

- [ ] No Windows-style paths (backslashes)
- [ ] No deeply nested references (keep one level deep)
- [ ] No offering too many options without a default
- [ ] No time-sensitive content without "legacy" sections
- [ ] No verbose explanations of basic concepts
- [ ] No assuming tools or packages are pre-installed
- [ ] No magic numbers in scripts (all constants documented)
- [ ] No punting error handling to Claude

## Documentation and resources

### Internal documentation
- [ ] Instructions are clear and unambiguous
- [ ] Examples demonstrate expected patterns
- [ ] Templates are copy-paste ready
- [ ] Workflow steps are numbered and sequential

### External references (if applicable)
- [ ] WebFetch URLs are correct and accessible
- [ ] URLs point to canonical, stable documentation
- [ ] Instructions explain when to fetch external docs
- [ ] No duplication of content available via WebFetch

## Pre-publication final checks

- [ ] Skill name is unique and descriptive
- [ ] Directory structure follows conventions
- [ ] All referenced files exist at correct paths
- [ ] No broken internal links
- [ ] No placeholder content (TODOs, FIXMEs)
- [ ] Code examples are syntactically correct
- [ ] File sizes are reasonable (no huge files)
- [ ] Skill demonstrates the patterns it teaches (if meta-Skill)

## Quick reference: Maximum limits

- **name:** 64 characters
- **description:** 1024 characters
- **SKILL.md body:** 500 lines (recommended)
- **Reference files:** No limit (loaded on-demand)
- **Metadata token cost:** ~100 tokens per Skill (always loaded)

## Scoring guide

**Essential items (must pass):**
- All items under "Core quality > YAML frontmatter"
- All items under "Core quality > Structure and organization"
- All items under "Testing and validation > Discovery testing"

**Important items (should pass most):**
- Items under "Core quality > Content quality"
- Items under "Testing and validation > Real-world testing"
- Items under "Common anti-patterns"

**Nice to have:**
- Items under "Code and scripts" (if applicable)
- Items under "Testing and validation > Model testing"
- Items under "Documentation and resources"

## Usage notes

**For self-review:**
Go through this checklist before sharing or publishing a Skill.

**For pair review:**
Share this checklist with a colleague and review together.

**For automated checks:**
Some items can be verified programmatically:
- YAML frontmatter presence and field names
- Character limits on name and description
- File path conventions (forward vs. back slashes)
- File existence for references
- Line count in SKILL.md

**For iterative development:**
Don't expect to pass every item on first draft. Use this as a guide for improvement across iterations.
