# Mathem MCP Server 🛒

I built this to help my household order groceries from Mathem.se using Claude. It's an MCP server that lets AI assistants search for products and add them directly to your Mathem basket. Combined with Notion for recipe management, it handles the full workflow from "what should we eat this week?" to having ingredients in the cart.

This started as a fork of [sleipner42/mathem-mcp-server](https://github.com/sleipner42/mathem-mcp-server) which I then tweaked and extended for my household's workflow. Big thanks to the original author for getting this started.

This is primarily a personal household tool and very much a WIP, but I'm sharing it in case it's useful to others. If you also use Mathem.se and want to automate your grocery shopping with Claude, give it a try.

## What this repo contains

This is actually two things:

1. **An MCP server** (`mathem.py`) - The technical implementation that connects to Mathem.se's API
2. **An agent workspace** (`.claude/skills/`) - Pre-built workflows for Claude Code agents to handle grocery shopping and recipe management

If you're using Claude Desktop or another MCP client, you want the server. If you're using Claude Code (the CLI), the skills are already set up for you - just ask Claude to order groceries or manage recipes. Note that the skills include references to the dietary preferences of my household and might need tweaking for yours.

## What you'll need

- Python 3.12+ and [uv](https://github.com/astral-sh/uv) (for running the MCP server)
- A Mathem.se account (for adding items to basket - search works without it)
- Notion (optional, if you want recipe management)

## Setup

### Install dependencies

```bash
# Install uv if you don't have it
brew install uv

# Clone and install
git clone https://github.com/kimdebie/mathem-mcp-server
cd mathem-mcp-server
uv sync
```

### Mathem.se authentication (required for adding to basket)

The server uses your browser's session cookies to talk to Mathem's API. Without this, you can search but not add items to your basket.

```bash
cp cookie.txt.example cookie.txt
```

Then grab your session cookies from your browser:
1. Go to [mathem.se](https://www.mathem.se) and log in
2. Open DevTools (F12) → Network tab
3. Refresh the page
4. Click any request to mathem.se and copy the `Cookie` header
5. Paste the whole thing into `cookie.txt`

It should look something like:
```
sessionid=abc123...; csrftoken=xyz789...; other_stuff=values
```

### Notion setup (optional, for recipe management)

If you keep recipes in Notion and want Claude to read them:

1. Create an integration at [notion.so/profile/integrations](https://www.notion.so/profile/integrations)
2. Copy the token and add it to `.env`:
   ```bash
   cp .env.example .env
   # Edit .env and set NOTION_API_KEY=ntn_your_token_here
   ```
3. Share your recipe database with the integration (click the "..." menu → Connections in Notion)

## Using with Claude Code

If you're using Claude Code (the CLI), you need to set up the `.mcp.json` file:

```bash
cp .mcp.json.example .mcp.json
```

Then edit `.mcp.json` and replace `YOUR_TOKEN_HERE` with your actual Notion token (if you're using Notion). The file configures both the Mathem and Notion MCP servers. Claude Code will automatically pick up the MCP servers when working in this directory.

The skills in `.claude/skills/` are ready to use - just ask Claude to order groceries or manage recipes.

## Using with Claude Desktop

Edit your Claude Desktop config:

```bash
# macOS
open ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Linux
open ~/.config/claude/claude_desktop_config.json
```

Add the server (replace the path with your actual project directory):

```json
{
  "mcpServers": {
    "mathem": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mathem-mcp-server",
        "run",
        "mathem.py"
      ]
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "ntn_your_notion_token_here"
      }
    }
  }
}
```

Restart Claude Desktop and you're good to go.

## How to use it

Just talk to Claude normally:

- "Find organic tomatoes on Mathem"
- "Add 2 packages of pasta to my basket"
- "What recipes do I have in Notion?"
- "Order all the ingredients for pasta carbonara"

The server exposes three tools to Claude:

- `search_mathem_ingredients(query)` - Search Mathem.se (queries need to be in Swedish: "kaffe", "mjölk", etc.)
- `add_to_mathem_basket(product_id, quantity)` - Add items to your cart
- `get_mathem_basket()` - See what's currently in your basket

When you combine this with the Notion MCP server, Claude can read your recipes and figure out what you need to buy.

## Development

Run tests:
```bash
uv run pytest
# or
uv run test.py
```

The tests call the MCP tools directly via `.fn()` to bypass the protocol layer.

## How it works

The server uses Mathem's tienda-web-api endpoints:
- Search: `GET /tienda-web-api/v1/search/?q={query}`
- Add to cart: `POST /tienda-web-api/v1/cart/items/`
- View cart: `GET /tienda-web-api/v1/cart/`

Authentication is cookie-based - the server reads your browser cookies from `cookie.txt` and includes them in API requests.

## Notes

This is a personal project I'm sharing as-is. It works for my household but might need tweaking for yours. Feel free to fork and modify.

Mathem doesn't have an official public API, so this uses their internal endpoints. Be reasonable with your usage and respect their terms of service.
