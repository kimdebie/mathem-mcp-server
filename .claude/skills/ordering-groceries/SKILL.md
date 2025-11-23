---
name: Ordering Groceries
description: Orchestrates grocery shopping workflows using Notion recipes and Mathem.se. Use when the user wants to order groceries, shop for recipes, or add ingredients to their basket. Follows household preferences for organic, vegetarian, and seasonal products.
---

# Ordering Groceries

This skill guides you through ordering groceries from Mathem.se using recipes stored in Notion, following the household's dietary preferences and shopping rules.

## When to use this skill

- User wants to order groceries for one or more recipes
- User asks to "shop for" or "get ingredients for" a recipe
- User wants to browse recipes and add ingredients to basket
- Any grocery shopping task involving Mathem.se and Notion recipes

## Workflow

### 1. Retrieve recipe from Notion

Use Notion MCP tools to find and retrieve the recipe:

```
1. Search for the recipe in the "Recepten" database
2. Retrieve the full recipe page content
3. Locate the "Ingrediënten" section (bulleted list)
4. Extract all ingredients from the list
```

### 2. Filter pantry staples

The household keeps these basics stocked at home - **DO NOT search for these by default:**

**Oils & Fats & Sauces:**
- Oils (olijfolie, plantaardige olie), butter (boter), balsamics, vinegar
- Sauces (soy sauce, ketchup, mayonnaise)

**Aromatics:**
- Onion (ui)
- Garlic (knoflook)

**Seasonings:**
- Salt (zout)
- Pepper (peper)
- All common spices (oregano, basil, cumin, paprika, etc.)

**When you encounter pantry staples in a recipe:**
1. Skip searching for them
2. Add them to a separate "Pantry items (not searched)" list
3. In your presentation, list these separately and ask if any need to be ordered

### 3. Check standard ingredients database

**Before searching Mathem**, check the "Mathem standaard ingrediënten" Notion database for commonly used items with pre-selected products.

**Database location:** Search Notion for "Mathem standaard ingrediënten" page, which contains an inline database.

**Database structure:**
- **Ingrediënt** (title) - Ingredient name (e.g., "coffee", "tomaten")
- **Volledige naam** (rich_text) - Full product name from Mathem (e.g., "Kaffe Mellanrost Löfberg")
- **product ID** (number) - Mathem product ID (e.g., 62265)

**Workflow for each ingredient:**

```
1. Query the "Mathem standaard ingrediënten" database using the ingredient name
2. If found in database:
   a. Search Mathem using the exact "Volledige naam" value
   b. Check if the returned product ID matches the stored "product ID"
   c. If MATCH: Present this as the ⭐ Recommended option (skip normal search)
   d. If NO MATCH: Flag with ⚠️ warning that the product has changed, then proceed with normal search
3. If NOT found in database:
   a. Proceed with normal search workflow (step 4)
```

**Presentation format for standard ingredients:**

When a standard ingredient matches:
```markdown
1. [Ingredient name] (need: [quantity]) - FROM STANDARD LIST
    - [Product name] - [price] ([description], [brand]) [ID: [id]] ⭐ Recommended (saved preference)
```

When a standard ingredient ID has changed:
```markdown
1. [Ingredient name] (need: [quantity]) - ⚠️ STANDARD ITEM CHANGED
    - Previous: [old product name] [ID: [old_id]] (no longer available)
    - [New product name] - [price] ([description], [brand]) [ID: [new_id]] ⭐ Recommended
```

### 4. Translate and search ingredients

For each ingredient in the recipe (excluding pantry staples):

```
1. Identify the core ingredient (e.g., "2 tomaten" → "tomaten")
2. Search using MatMCP: search_mathem_ingredients(swedish_term)
3. Review the results (up to 10 products returned by default)
4. Select the best product following household rules
```

**Language requirement:** All searches must use Swedish terms. Common translations:
- tomaten → tomater
- ui → lök
- knoflook → vitlök
- kaas → ost
- melk → mjölk
- eieren → ägg
- boter → smör
- olie → olja

### 5. Apply household rules

When selecting products from search results, follow these rules:

**1. Strictly vegetarian**
- NEVER select meat, fish, or poultry products
- Check product names and descriptions carefully
- Skip ingredients that aren't available in vegetarian form

**2. Prefer organic (with price exception)**
- Choose organic products when available
- EXCEPTION: If organic is >20% more expensive, choose conventional
- Look for "Ekologisk" label in product names or labels field

**3. Household size: 2 adults**
- Often cooking double portions (4 servings total)
- Avoid excessively large packages (e.g., 5kg bags, bulk sizes)
- Standard package sizes are preferred (e.g., 500g pasta, 1L milk)

**4. Seasonal preferences**
- Prioritize seasonal products when available
- Look for seasonal indicators in product descriptions

### 6. Present selections to user

Use this compact format to present products:

```markdown
## Selected products for [Recipe Name]

### Products found:

1. [Ingredient name] (need: [quantity/description])
    - [Product name] - [price] ([description], [brand]) [ID: [id]] ⭐ Recommended
    - [Alternative option if relevant] - [price] ([description], [brand]) [ID: [id]]

2. [Next ingredient] (need: [quantity/description])
    - [Product name] - [price] ([description], [brand]) [ID: [id]] ⭐ Recommended

Total estimated: [sum of prices] SEK

### Pantry items (not searched):
- [Pantry item 1, e.g., "Olive oil"]
- [Pantry item 2, e.g., "Salt"]
- [Pantry item 3, e.g., "Pepper"]

These are assumed to be available at home. Do you need any of these items as well?

---

Would you like me to add the recommended products to your basket?
```

**Format rules:**
- Mark the recommended product with ⭐ Recommended
- Show 1-2 alternatives only if they're meaningfully different (e.g., different colors/varieties)
- Include "need: X" to show the recipe requirement (e.g., "need: 400g", "need: 1 can")
- Use compact single-line format: Name - Price (description, brand) [ID: X]

### 7. Check existing basket contents

**Before adding items to the basket**, check what's already there to prevent unnecessary duplicates:

```
1. Ask user if there are items already in the basket from earlier in the session or previous recipes
2. For each item to be added, check if similar items are already in basket:
   - Same or similar product (e.g., milk, tomatoes, pasta)
   - Sufficient quantity to cover the new recipe's needs
3. If item is already in basket:
   a. Calculate if existing quantity covers the new recipe's requirement
   b. If YES: Ask user if they want to add more or use what's already there
   c. If NO: Explain how much more is needed and suggest appropriate quantity
4. EXCEPTION: If the agent added the item earlier in the same session and knows it's insufficient,
   skip the check and add the additional quantity needed
```

**Example scenarios:**

- Recipe A needed 500ml milk, added 1L carton → Recipe B needs 100ml → Ask: "You already have 1L milk in the basket from Recipe A. That should cover this recipe too. Skip adding more milk?"
- Recipe A needed 400g tomatoes, added 500g pack → Recipe B needs 500g → Ask: "You have 500g tomatoes from Recipe A. Do you want to add another 500g pack for Recipe B, or adjust the portions?"
- Agent added 200g pasta for Recipe A → Recipe B needs 400g → Automatically add another 400g pack (agent knows existing quantity is insufficient)

**How to present the check:**

```markdown
---

Checking existing basket contents...

Items already in basket that appear in this recipe:
- Milk (1L) - already covers this recipe's 100ml requirement
- Tomatoes (500g) - this recipe needs 500g more

Should I:
1. Skip the milk (you have enough)
2. Add another 500g tomatoes for this recipe
```

### 8. Add to basket

After user confirmation and basket check:

```
1. For each selected product, call: add_to_mathem_basket(product_id, quantity)
2. Report success/failure for each item
3. Summarize what was added
```

**Authentication requirement:** Adding to basket requires valid cookie.txt file with Mathem.se session cookies.

### 9. Update standard ingredients (end of session)

After successfully adding items to the basket, ask the user which products should be saved to the "Mathem standaard ingrediënten" database for future use.

**How to ask:**
```markdown
---

Would you like to save any of these products as standard ingredients for next time?

Items you can save:
- [Product name] ([ingredient name]) [ID: [id]]
- [Product name] ([ingredient name]) [ID: [id]]

This will make future shopping faster by remembering your preferred brands.
```

**If user confirms items to save:**

For each item, add a new entry to the database using `mcp__notion__API-post-page`:

```
Parent: The "Mathem standaard ingrediënten" database ID (query the page first to get the database ID)
Properties:
  - Ingrediënt (title): The ingredient name (e.g., "coffee", "milk")
  - Volledige naam (rich_text): The full product name from Mathem (e.g., "Kaffe Mellanrost Löfberg")
  - product ID (number): The Mathem product ID (e.g., 62265)
```

**Database ID:** Query "Mathem standaard ingrediënten" page, then retrieve the child database block to get the database ID.
## Handling edge cases

### Ingredient not found
- Try variations (plural/singular, alternate terms)
- Ask user for suggestions if still not found
- Offer to skip that ingredient

### Multiple good options
- Present 2-3 options to user with pros/cons
- Let user choose based on their preference

### Product unavailable
- Search for alternatives
- Inform user about substitution

### Authentication failure
- Inform user that cookie.txt needs to be updated
- Can still search and present products, just can't add to basket

### Standard ingredient product ID mismatch
- Search returned different product ID than what's stored in database
- Flag clearly with ⚠️ in presentation
- Present the new product as recommendation
- After successful order, offer to update the database entry with the new product ID
- User can choose to keep old preference or update to new product

## Example interaction

**User:** "I want to make Voorjaarssalade"

**You should:**
1. Query Notion "Recepten" database for "Voorjaarssalade"
2. Retrieve the recipe page
3. Extract ingredients from "Ingrediënten" section
4. Separate pantry staples (oil, salt, spices, onion, garlic) from fresh ingredients
5. Check "Mathem standaard ingrediënten" database for each ingredient
6. For standard ingredients: search using saved product name and verify ID match
7. For non-standard ingredients: search Mathem.se (in Swedish) and select following household rules
8. Present selections in compact format with ⭐ Recommended marker + list pantry items separately
9. Flag any standard ingredients where product ID has changed with ⚠️
10. Ask if pantry items also need to be ordered
11. After confirmation, check existing basket contents for duplicates
12. Ask user about any overlapping items before adding
13. Add recommended products to basket (skipping duplicates as confirmed)
14. Report results
15. Ask which new items should be saved to standard ingredients database

## Product selection priority

When choosing between multiple products:

1. **Vegetarian requirement** (non-negotiable)
2. **Organic preference** (unless >20% more expensive)
3. **Appropriate package size** (for 2-4 servings)
4. **Seasonal options** (when applicable)
5. **Special offers** (if product has "offer" field and meets above criteria)
6. **Price** (lower is better, all else equal)

## Tips

- **ALWAYS check standard ingredients database first** before searching Mathem - this saves time and ensures consistency
- **ALWAYS check existing basket contents** before adding items - prevents duplicates and saves money
- When standard ingredient product ID doesn't match, flag it clearly with ⚠️ so user knows to update the database
- Always translate ingredient names to Swedish before searching
- Read product descriptions carefully for vegetarian verification
- Calculate price differences for organic options (check unit_price for fair comparison)
- When in doubt about package size, choose standard/medium sizes
- Use product offers to save money when they align with household rules
- Don't search for pantry staples by default - but always list them and ask if they're needed
- At end of session, proactively ask about saving new items to standard ingredients (don't wait for user to ask)
- Only suggest saving items the user might buy repeatedly (milk, coffee, specific brand preferences)
- If shopping for multiple recipes in one session, keep track of what's been added and check for overlaps
