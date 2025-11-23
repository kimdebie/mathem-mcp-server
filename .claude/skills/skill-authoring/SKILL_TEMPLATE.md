# Skill Template

Copy this template to create a new Skill. Replace placeholders with your content.

```markdown
---
name: Your Skill Name
description: Brief description of what this Skill does and when to use it. Include key terms and trigger words that Claude should recognize.
---

# Your Skill Name

[One-paragraph overview of what this Skill provides]

## When to use this Skill

- [Specific use case 1]
- [Specific use case 2]
- [Specific use case 3]

## Quick start

[Fastest path to using this Skill - minimal example]

## [Main Section 1]

[Core instructions or guidance]

### [Subsection if needed]

[Additional details]

## [Main Section 2]

[More instructions or patterns]

## Common patterns

[Template patterns, examples, or workflows that Claude should follow]

## Tips for success

1. [Practical tip 1]
2. [Practical tip 2]
3. [Practical tip 3]

## Advanced topics

[Optional: Link to additional reference files if needed]

For detailed guidance on [topic], see [REFERENCE.md](REFERENCE.md)
```

## Template usage notes

**YAML frontmatter:**
- `name`: Max 64 characters, use gerund form (e.g., "Processing PDFs")
- `description`: Max 1024 characters, third person, include what + when

**Body structure:**
- Jump straight into content (no heading as first line)
- Use clear section headings (##)
- Keep total under 500 lines
- Break into separate files if approaching limit

**Content guidelines:**
- Be concise - assume Claude is already smart
- Provide concrete examples over abstract explanations
- Use consistent terminology throughout
- Include actionable tips and practical guidance
- Link to additional files for optional/advanced content

**File references:**
- Keep one level deep (all files link from SKILL.md)
- Use forward slashes in paths (Unix-style)
- Provide clear navigation to bundled resources

## Minimal working example

For the simplest possible Skill:

```markdown
---
name: Commit Messages
description: Generate conventional commit messages by analyzing git diffs. Use when writing commit messages or reviewing staged changes.
---

# Commit Messages

Generate commit messages following the conventional commits format.

## Format

```
type(scope): brief description

Detailed explanation of changes
```

## Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **refactor**: Code refactoring
- **test**: Test additions or changes
- **chore**: Maintenance tasks

## Example

```
feat(auth): implement JWT-based authentication

Add login endpoint with JWT token generation
Include token validation middleware
Update user model to store refresh tokens
```

## Process

1. Review `git diff --staged`
2. Identify the type and scope
3. Write brief description (50 chars max)
4. Add detailed explanation in body
```

This minimal Skill is complete and functional at ~30 lines.
