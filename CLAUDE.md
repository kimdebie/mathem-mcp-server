# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is an **agent workspace** for managing household groceries and recipes. It combines:

1. **Agent Skills** (`.claude/skills/`) - Pre-built workflows for grocery shopping and recipe management that agents MUST use
2. **MCP Server** (`mathem.py`) - Technical implementation providing Mathem.se grocery store integration
3. **Notion Integration** - Recipe database for collaborative household meal planning

**IMPORTANT: When the user requests grocery shopping, recipe management, or meal planning tasks, you MUST use the appropriate skill from `.claude/skills/`. DO NOT attempt to implement these workflows manually.**

## Agent Skills (MUST USE)

The following skills are available and MUST be used for their respective tasks:

### 1. `ordering-groceries` skill
**Use when:** User wants to order groceries, shop for recipes, or add ingredients to basket
**How to invoke:** Use the Skill tool with skill name "ordering-groceries"

### 2. `writing-recipes` skill
**Use when:** User wants to add, create, or save a recipe to Notion
**How to invoke:** Use the Skill tool with skill name "writing-recipes"

## Quick Start for Agents

When a user asks to:
- **Order groceries or shop for a recipe** → Use `Skill("ordering-groceries")`
- **Add a recipe to Notion** → Use `Skill("writing-recipes")`

**Do not attempt to manually implement these workflows.** The skills contain detailed instructions, household preferences, and edge case handling that must be followed exactly.

## Example Interactions

**User:** "I want to make pasta carbonara tonight"
**Agent:** Uses `Skill("ordering-groceries")` to retrieve the recipe from Notion, search Mathem.se for ingredients, and add them to the basket

**User:** "Add this recipe from URL to my collection"
**Agent:** Uses `Skill("writing-recipes")` to fetch, restructure chronologically, simplify, and save to Notion

**User:** "Help me come up with a seasonal dinner idea"
**Agent:** Uses `Skill("writing-recipes")` which includes recipe ideation workflow for Stockholm seasonal ingredients

---

## Technical Implementation Details

The sections below describe the underlying MCP server implementation. **Most agents working with this repository will not need to modify this code** - they should use the skills instead.

### Development Commands

#### Setup and Dependencies
```bash
# Install dependencies
uv sync

# Setup Mathem.se authentication (required for basket operations)
cp cookie.txt.example cookie.txt
# Then manually add your Mathem.se session cookies to cookie.txt

# Setup Notion MCP authentication (for recipe management)
cp .env.example .env
# Then add your Notion API token to .env
# Get your token from: https://www.notion.so/profile/integrations
```

#### Running Tests
```bash
# Run all tests with pytest
uv run pytest

# Run tests directly with the test file
uv run test.py
```

#### Running the Server
```bash
# Start the MCP server (typically not needed when using skills)
uv run mathem.py
```

### Core Components

**mathem.py** - Main MCP server implementation containing:
- **MCP Tools**: Three @mcp.tool decorated functions that expose capabilities to AI assistants
  - `search_mathem_ingredients(query, limit=10)` - Searches Mathem.se. **Query must be in Swedish** (e.g., "kaffe", "mjölk", "ägg"). Returns up to 10 products by default (configurable via limit parameter, max 40) with id, name, brand, price, unit_price, and optional labels/offers.
  - `add_to_mathem_basket(product_id, quantity)` - Adds products to basket using Mathem's API with cookie authentication. Requires valid cookie.txt file.
  - `get_mathem_basket()` - Retrieves current basket contents using Mathem's API with cookie authentication. Requires valid cookie.txt file.

- **Helper Functions**:
  - `search_ingredients(query)` - Calls the API search endpoint and parses the JSON response
  - `add_to_basket(product_id, quantity)` - Posts to Mathem's cart API with cookie-based authentication
  - `get_basket()` - Retrieves basket contents from Mathem's cart API with cookie-based authentication
  - `read_cookie_from_file()` - Reads authentication cookies from cookie.txt file

### Authentication Flow

The server uses cookie-based authentication for basket operations:
1. User manually extracts session cookies from logged-in Mathem.se session in browser
2. Cookies stored in `cookie.txt` (not committed to git)
3. `add_to_basket()` reads cookie.txt and includes cookies in API request headers
4. Without valid cookies, search still works but basket operations fail

### API Integration Strategy

The server uses Mathem's official tienda-web-api endpoints for all operations:
1. **Search**: `GET https://www.mathem.se/tienda-web-api/v1/search/?q={query}` - Returns JSON with product data
2. **Add to cart**: `POST https://www.mathem.se/tienda-web-api/v1/cart/items/` - Adds items to basket (requires authentication)
3. **View cart**: `GET https://www.mathem.se/tienda-web-api/v1/cart/` - Retrieves current basket contents (requires authentication)

### Testing

Tests in `test.py` access MCP tools via `.fn()` attribute (e.g., `mathem.search_mathem_ingredients.fn()`). This bypasses the MCP protocol layer and directly calls the underlying Python functions.
---

## Important Reminders for Agents

1. **ALWAYS use the skills** (`.claude/skills/`) for grocery shopping and recipe management tasks
2. **DO NOT manually implement** the workflows described in the skills - they contain critical household preferences and edge case handling
3. **The skills are mandatory** - attempting to manually orchestrate Notion/Mathem interactions will miss important requirements like:
   - Checking standard ingredients database
   - Filtering pantry staples
   - Applying vegetarian/organic/portion rules
   - Checking basket for duplicates
   - Proper chronological recipe formatting
4. **For code development tasks** (modifying `mathem.py`, tests, etc.) - work directly with the code as usual
