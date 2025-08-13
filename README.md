# MatMCP 🛒

An MCP (Model Context Protocol) server that provides AI assistants with tools to interact with Mathem.se, a Swedish online grocery store. Search for ingredients, add items to your basket, and manage recipes directly through your AI assistant.

## Features

- **Search Ingredients**: Find products on Mathem.se by name or description
- **Add to Basket**: Add products directly to your Mathem.se shopping cart
- **Recipe Management**: List and fetch detailed recipe information
- **Structured Data**: Get clean, structured product and recipe data

## Prerequisites

- **macOS/Linux**: This guide assumes macOS, but Linux instructions are similar
- **Python 3.12+**: Required for the project
- **uv**: Fast Python package manager
- **Mathem.se Account**: For adding items to basket functionality

## Installation

### 1. Install uv (Python package manager)

```bash
brew install uv
```

### 2. Clone and setup the project

```bash
git clone <your-repo-url>
cd matmcp
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Configure Mathem.se authentication (optional)

For basket functionality, you need to provide your Mathem.se session cookies:

1. Copy the example cookie file:
   ```bash
   cp cookie.txt.example cookie.txt
   ```

2. Get your session cookies from Mathem.se:
   - Open your browser and go to [mathem.se](https://www.mathem.se)
   - Log in to your account
   - Open Developer Tools (F12)
   - Go to the Network tab
   - Refresh the page
   - Find a request to mathem.se and copy the Cookie header value
   - Paste it into `cookie.txt`

   The format should look like:
   ```
   sessionid=your_session_id_here; csrftoken=your_csrf_token_here; other_cookies=value
   ```

**Note**: Without cookies, you can still search for ingredients, but adding to basket will not work.

## Claude Desktop Integration

Add this MCP server to your Claude Desktop configuration:

### 1. Open Claude Desktop config

```bash
# macOS
open ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Linux
open ~/.config/claude/claude_desktop_config.json
```

### 2. Add the server configuration

Replace `/YOUR/PATH/TO/matmcp` with your actual project directory:

```json
{
  "mcpServers": {
    "mathem": {
      "command": "uv",
      "args": [
        "--directory",
        "/YOUR/PATH/TO/matmcp",
        "run",
        "mathem.py"
      ]
    }
  }
}
```

### 3. Restart Claude Desktop

Close and reopen Claude Desktop to load the new MCP server.

## Usage

Once configured, you can ask Claude to:

- **Search for ingredients**: "Find organic tomatoes on Mathem"
- **Add items to basket**: "Add 2 packages of pasta to my Mathem basket"
- **Get recipes**: "Show me the available recipes"
- **Recipe details**: "Get the details for recipe number 1"

## Available Tools

### `search_mathem_ingredients(query: str)`
Search for products on Mathem.se

**Example**: Search for "organic milk"

### `add_to_mathem_basket(product_id: int, quantity: int = 1)`
Add a product to your Mathem.se shopping basket

**Requirements**: Valid session cookies in `cookie.txt`

### `list_recipes()`
List all available recipes from `recipes.csv`

### `get_recipe_by_index(index: int)`
Get detailed recipe information by index

## Development

### Running tests
```bash
uv run pytest
```

### Running the server directly
```bash
uv run mathem.py
```

### Adding recipes
Edit `recipes.csv` to add new recipes with columns: `id`, `title`, `url`

## License

This project is for educational and personal use. Please respect Mathem.se's terms of service when using this tool.
