---
name: Writing Recipes
description: Creates clear, foolproof recipes in Notion from URLs or descriptions. Use when the user wants to add a recipe to their Notion database. Focuses on Dutch language, chronological steps, and simple instructions.
---

# Writing Recipes

This skill guides you through creating recipes in Notion that are clear and easy to follow.

## When to use this skill

- User provides a recipe URL to add to Notion
- User describes a dish they want to document
- User wants to add, create, or save a recipe
- User wants to ideate or brainstorm recipe ideas (e.g., "help me come up with a seasonal weeknight recipe")
- Any task involving writing recipes to the Notion "Recepten" database

## Recipe philosophy

The goal is to **preserve the original recipe's structure** while making it clear and readable in Dutch. Recipes should NOT become significantly longer than the original.

Every recipe must be:

1. **Clear language** - Simple Dutch, short sentences, common words
2. **Preserve structure** - Keep the original recipe's flow; only split steps if genuinely confusing
3. **Fix obvious issues** - Move oven preheating to the start if it's mentioned late, but don't restructure everything
4. **Slight expansion OK** - Recipe can be ~20-30% longer if it genuinely improves clarity

**BAD example (over-fragmented):**
```
1. Zet de oven aan op 220 graden
2. Snijd de ui
3. Snijd de ui in kleine stukjes
4. Snijd de tomaten
5. Snijd de tomaten in blokjes
6. Pak een pan
7. Verwarm de pan
8. Voeg olie toe
9. Bak de ui
10. Bak de ui 3 minuten
... (continues to 20+ steps)
```
❌ Problem: Original recipe had 5 steps, this has 20+! Every action is split unnecessarily.

**GOOD example (preserved structure, clear language):**
```
1. Zet de oven aan op 220 graden
2. Snijd de ui in kleine stukjes en de tomaten in blokjes
3. Verwarm een pan met olie en bak de ui 3 minuten
4. Voeg de tomaten toe en bak nog 5 minuten
5. Doe alles in een ovenschaal en bak 30 minuten in de oven
```
✓ Original flow preserved, clear Dutch, oven preheated first (the one obvious fix needed)

## Workflow

### 0. Recipe Ideation Phase (if applicable)

**When to use:** User wants to brainstorm or come up with recipe ideas rather than documenting an existing recipe.

**Examples:**
- "Help me come up with a seasonal weeknight recipe"
- "What's a good vegetarian dinner for spring?"
- "I need ideas for a quick pasta dish"

**Default assumptions:**
- **Location:** Stockholm, Sweden
- **Seasonality:** Use current date to determine what's in season
- **Diet:** Strictly vegetarian (no meat, poultry, or fish)

**Process:**
1. **Understand constraints:**
   - Determine current season from today's date (e.g., Nov = late autumn/early winter)
   - Ask about time constraints (quick weeknight vs. weekend project)
   - Ask about specific preferences or ingredients to use/avoid
   - Ask about cooking methods if relevant

2. **Propose initial ideas:**
   - Suggest 2-3 recipe concepts using **seasonal Stockholm ingredients**
   - Include brief descriptions with timing (e.g., "Roasted root vegetable pasta - 35 minutes, uses seasonal celeriac and carrots")
   - All suggestions must be **strictly vegetarian**
   - Explain why each fits the season and request

3. **Refine with user feedback:**
   - User picks a favorite or asks for modifications
   - Adjust based on feedback (simpler, more complex, different ingredients, etc.)
   - Continue iterating until user is satisfied with the concept

4. **Transition to recipe creation:**
   - Once user confirms they want to add the recipe: "Shall I create this recipe in your Notion database?"
   - If yes, proceed to step 1 below (Get the recipe content)
   - Use your culinary knowledge to develop the full ingredient list and steps

**Important:** Do NOT create the Notion page until the user explicitly confirms they want to save the recipe. The ideation phase is exploratory and conversational.

### 1. Get the recipe content

**If user provides a URL:**
1. Use WebFetch to retrieve the recipe page
2. Extract the title, ingredients list, and cooking steps
3. Note any cooking times, temperatures, and serving sizes

**If user provides a description:**
1. Ask clarifying questions about:
   - Ingredients needed
   - Cooking method (oven, stovetop, etc.)
   - Approximate cooking time
   - Number of servings
2. Use your knowledge to fill in standard steps for that dish type

### 2. Fix obvious chronology issues

**Only intervene when something is clearly wrong.** Trust the original recipe's flow.

**Fix these issues:**
- Oven preheating mentioned at the end → move to step 1
- Marinating time not accounted for → add early
- "In a preheated oven" but no preheat step → add preheat at start

**Do NOT:**
- Split every step into atomic actions
- Reorganize the entire recipe "to be chronological"
- Separate prep from cooking if they flow naturally together

**Example - when to intervene:**
```
Original: "...bak 30 minuten in een voorverwarmde oven op 220 graden"
Fix: Add "Zet de oven aan op 220 graden" as step 1
```

**Example - when NOT to intervene:**
```
Original: "Snijd de groenten en bak ze in een pan met olie"
Keep as: "Snijd de groenten en bak ze in een pan met olie"
DON'T split into: 4 separate steps for cutting, heating pan, adding oil, cooking
```

### 3. Simplify language

Translate to clear, simple Dutch. This is about **language clarity**, not restructuring.

**Use simple, direct sentences:**
- ✓ "Snijd de ui in kleine stukjes"
- ✗ "Snipper de ui fijn" (less common verb)

**Clarify vague timing:**
- ✓ "Bak ongeveer 5 minuten tot zacht"
- ✗ "Bak tot zacht" (add approximate time)

**Be specific with amounts:**
- ✓ "Voeg 2 eetlepels olie toe"
- ✗ "Voeg wat olie toe"

### 4. Translate to Dutch if needed

If the source recipe is in another language, translate into Dutch while preserving the original step count and structure.

### 5. Structure the Notion page

Create the recipe page with this structure:

**Title:** Recipe name in Dutch (e.g., "Tomatensoep")

**Ingrediënten section (bulleted list):**
```
• 2 uien
• 4 tomaten
• 2 eetlepels olijfolie
• 500 ml groentebouillon
• Zout en peper
```

**Format rules for ingredients:**
- Start with quantity, then ingredient name
- Use consistent units (eetlepels, theelepels, gram, etc.)
- List in order they're used in recipe (roughly)
- Keep pantry staples (oil, salt, pepper) at the end

**Recept section (numbered list):**
```
1. Zet de oven aan op 200 graden
2. Snijd de uien en tomaten in stukjes
3. Verwarm olie in een pan en fruit de uien 5 minuten
[etc.]
```

**Format rules for steps:**
- Numbered list (1, 2, 3...)
- Preserve original recipe structure
- Include timing where helpful
- Include temperature/heat level

**Bron (source) section:**
- Always add the source URL at the end of the recipe when the recipe comes from a URL
- Format: "Bron: " followed by clickable link with domain name as display text
- Example: `Bron: [miljuschka.nl](https://miljuschka.nl/recipe-url/)`
- Skip this section only for recipes created from scratch (ideation) or user descriptions

### 6. Create the Notion page

Use Notion MCP tools:

```
1. Call: mcp__notion__API-post-page with:
   - parent: {page_id: "YOUR_RECEPTEN_DATABASE_ID"}
   - properties: {title: [{text: {content: "Recipe Name"}}], type: "title"}
   - children: [blocks for Ingrediënten and Recept sections]

2. For Ingrediënten section:
   - Heading block: "Ingrediënten"
   - Bulleted list items for each ingredient

3. For Recept section:
   - Heading block: "Recept"
   - Numbered list items for each step
```

## Examples

### Example 1: Oven-based recipe (minimal intervention)

**INPUT:** User shares link to "Roasted Vegetables Recipe" (6 steps in original)

**Original steps:**
1. Chop the vegetables into chunks
2. Toss with olive oil, salt and pepper
3. Spread on a baking sheet
4. Roast at 220°C for 30 minutes
5. Stir halfway through
6. Serve hot

**YOUR PROCESS:**
1. Fetch recipe from URL
2. Identify issue: oven temp mentioned at step 4, should preheat first
3. Keep structure, just add preheat and translate

**OUTPUT (7 steps - only 1 added):**
```
1. Zet de oven aan op 220 graden
2. Snijd de groenten in grove stukken
3. Meng met olijfolie, zout en peper
4. Verdeel over een bakplaat
5. Rooster 30 minuten in de oven
6. Roer halverwege even om
7. Serveer warm
```

### Example 2: Recipe ideation

**INPUT:** User says "help me come up with a seasonal weeknight recipe"

**YOUR PROCESS:**
1. Determine season from date (e.g., November = late autumn)
2. Ask time constraint: "How much time do you have for cooking?"
   - User: "About 30-40 minutes"
3. Propose 2-3 seasonal vegetarian ideas:
   - **Rotsakspasta med rosmarin** - Roasted root vegetables with pasta, garlic, and rosemary (35 min)
   - **Svampsoppa med timjan** - Creamy mushroom soup with fresh thyme and crusty bread (30 min)
   - **Vitkålsgryta med äpplen** - Braised white cabbage stew with apples and potatoes (40 min)
4. User picks: "The pasta sounds great!"
5. Ask: "Shall I create this recipe in your Notion database?"
6. User confirms, then develop full recipe (aim for 6-8 steps)

**OUTPUT:** Full recipe created in Notion with clear, consolidated steps.

### Example 3: Stovetop recipe (preserve structure)

**INPUT:** User says "I want to add a simple pasta aglio e olio recipe"

**YOUR PROCESS:**
1. Ask: "How many servings?" (user says 2)
2. Use standard pasta aglio e olio knowledge
3. Keep it simple - this is a 5-step recipe, not a 15-step one

**OUTPUT (6 steps):**
```
1. Kook de pasta volgens de verpakking in ruim gezouten water
2. Snijd 4 tenen knoflook in dunne plakjes
3. Verwarm 4 eetlepels olijfolie in een pan en bak de knoflook 2 minuten (niet te bruin!)
4. Giet de pasta af en bewaar een kopje kookwater
5. Meng de pasta met de knoflookolie, voeg wat kookwater toe en roer goed
6. Serveer met peterselie en peper
```

## Handling edge cases

### Recipe has vague timing
- **Problem:** "Bak tot goudbruin"
- **Solution:** Add approximate time: "Bak 5-7 minuten tot goudbruin"

### Original recipe has multi-tasking
- **Original:** "While the sauce simmers, prepare the vegetables"
- **Keep as:** "Laat de saus 10 minuten sudderen. Snijd ondertussen de groenten."
- **DON'T split into:** 5 separate steps

### Recipe has specialty ingredients
- **Problem:** "balsamic reduction", "saffron threads"
- **Solution:** Use common Dutch names or add brief clarification:
  ```
  • Balsamico azijn (of gewone azijn)
  • Saffraan draden (gele specerij)
  ```

### Source recipe is already in Dutch but unclear
- Focus on **language clarity**, not restructuring
- Fix vague timing, unclear quantities
- Keep the original step count

## Quality checklist

Before creating the Notion page, verify:

- [ ] Recipe length is within 20-30% of original (no extreme fragmentation!)
- [ ] Only obvious chronology issues fixed (oven preheat, marinating time)
- [ ] Original recipe flow is preserved
- [ ] Language is simple Dutch (no fancy cooking terms)
- [ ] Timing is explicit where it was vague
- [ ] Ingredients match what's used in steps
- [ ] Source URL included at the end (if recipe came from a URL)

## Tips

- **Preserve, don't restructure** - Your job is translation and clarity, not reorganization
- **Count your steps** - If original has 6 steps and yours has 15, something went wrong
- **Trust the source** - Most recipes are already in reasonable order
- **Only fix what's broken** - Oven preheat missing? Fix it. Steps flow naturally? Leave them alone
