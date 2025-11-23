---
name: Writing Recipes
description: Creates clear, foolproof recipes in Notion from URLs or descriptions. Use when the user wants to add a recipe to their Notion database. Focuses on Dutch language, chronological steps, and simple instructions.
---

# Writing Recipes

This skill guides you through creating recipes in Notion that are clear and chronological.

## When to use this skill

- User provides a recipe URL to add to Notion
- User describes a dish they want to document
- User wants to add, create, or save a recipe
- User wants to ideate or brainstorm recipe ideas (e.g., "help me come up with a seasonal weeknight recipe")
- Any task involving writing recipes to the Notion "Recepten" database

## Recipe philosophy

Every step must be:

1. **Chronological** - Steps happen in the exact order they're written
2. **Self-contained** - Each step has all the info needed to execute it
3. **Simple language** - Short sentences, common words, no complex phrasing
4. **Small actions** - Break complex tasks into tiny steps

**BAD example (NOT chronological):**
```
1. Snijd de groenten
2. Bak de ui
3. Voeg tomaten toe
4. Doe alles in een ovenschaal
5. Bak 30 minuten in de oven op 220 graden
```
❌ Problem: Step 5 assumes the oven is hot, but we never turned it on!

**GOOD example (chronological):**
```
1. Zet de oven aan op 220 graden
2. Snijd de ui in kleine stukjes
3. Snijd de tomaten in blokjes
4. Verwarm een pan met olie
5. Bak de ui 3 minuten
6. Voeg de tomaten toe
7. Bak nog 5 minuten
8. Doe alles in een ovenschaal
9. Zet de schaal in de oven
10. Bak 30 minuten
11. Haal uit de oven
```
✓ Oven is turned on first, steps are tiny, no assumptions about reading ahead

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
   - Use your culinary knowledge to develop the full ingredient list and chronological steps

**Important:** Do NOT create the Notion page until the user explicitly confirms they want to save the recipe. The ideation phase is exploratory and conversational.

### 1. Get the recipe content

**If user provides a URL:**
```
1. Use WebFetch to retrieve the recipe page
2. Extract the title, ingredients list, and cooking steps
3. Note any cooking times, temperatures, and serving sizes
```

**If user provides a description:**
```
1. Ask clarifying questions about:
   - Ingredients needed
   - Cooking method (oven, stovetop, etc.)
   - Approximate cooking time
   - Number of servings
2. Use your knowledge to fill in standard steps for that dish type
```

### 2. Restructure steps chronologically

This is the **most critical step**. Review all instructions and reorder them so:

**Preheating comes first:**
- ✓ "Zet de oven aan op X graden" (step 1)
- ✗ NOT mentioned later as "in een voorverwarmde oven"

**Prep happens before cooking:**
- ✓ "Snijd de ui" before "Bak de ui"
- ✗ NOT "Bak de gesneden ui" (assumes cutting already happened)

**Timer-based tasks are explicit:**
- ✓ "Bak 5 minuten" then "Voeg tomaten toe"
- ✗ NOT "Bak de ui tot zacht en voeg dan tomaten toe" (vague timing)

**Equipment is prepared before use:**
- ✓ "Verwarm een pan met olie" before "Bak de ui"
- ✗ NOT "Bak de ui in olie" (assumes pan is already hot)

### 3. Simplify language

**Use simple, direct sentences:**
- ✓ "Snijd de ui in kleine stukjes"
- ✗ "Snipper de ui fijn" (less common verb)

**Avoid complex clauses:**
- ✓ "Bak 3 minuten. Roer af en toe."
- ✗ "Bak ongeveer 3 minuten terwijl je regelmatig roert"

**Be specific with amounts:**
- ✓ "Voeg 2 eetlepels olie toe"
- ✗ "Voeg wat olie toe"

### 4. Translate to Dutch if needed

If the source recipe is in another language, translate into Dutch.

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
2. Snijd de uien in kleine stukjes
3. Snijd de tomaten in blokjes
[etc.]
```

**Format rules for steps:**
- Numbered list (1, 2, 3...)
- One action per step
- Include timing explicitly
- Include temperature/heat level
- Add safety reminders where needed

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

### Example 1: Oven-based recipe

**INPUT:** User shares link to "Roasted Vegetables Recipe"

**YOUR PROCESS:**
1. Fetch recipe from URL
2. Identify: oven temp (220°C), ingredients (vegetables, oil), timing (30 min)
3. Restructure chronologically:
   - Oven on FIRST
   - Prep vegetables
   - Arrange on tray
   - Into oven
   - Take out (with reminder about oven mitts)

**OUTPUT STEPS:**
```
1. Zet de oven aan op 220 graden
2. Snijd de courgette in plakken
3. Snijd de paprika in stukken
4. Leg bakpapier op een bakplaat
5. Leg de groenten op de bakplaat
6. Besprenkel met 2 eetlepels olijfolie
7. Strooi zout en peper erover
8. Zet de bakplaat in de oven
9. Bak 30 minuten
10. Haal de bakplaat uit de oven
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
6. User confirms, then develop full recipe with chronological steps

**OUTPUT:** Full recipe created in Notion with detailed steps.

### Example 3: Stovetop recipe

**INPUT:** User says "I want to add a simple pasta aglio e olio recipe"

**YOUR PROCESS:**
1. Ask: "How many servings?" (user says 2)
2. Use standard pasta aglio e olio knowledge
3. Structure chronologically:
   - Water on to boil FIRST
   - Prep garlic while water heats
   - Cook pasta
   - Make sauce
   - Combine

**OUTPUT STEPS:**
```
1. Zet een grote pan water op het vuur
2. Voeg 1 eetlepel zout toe aan het water
3. Snijd 4 tenen knoflook in dunne plakjes
4. Als het water kookt: doe de pasta erin
5. Kook de pasta 10 minuten (of volgens de verpakking)
6. Verwarm een pan met 4 eetlepels olijfolie
7. Bak de knoflook 2 minuten (niet te bruin!)
8. Giet de pasta af (bewaar 1 kopje pastwater)
9. Doe de pasta bij de knoflookolie
10. Voeg 3 eetlepels pastwater toe
11. Roer goed
12. Strooi peterselie erover (optioneel)
```

## Handling edge cases

### Recipe has vague timing
- **Problem:** "Bak tot goudbruin"
- **Solution:** Add approximate time: "Bak 5-7 minuten tot goudbruin"

### Recipe has complex multi-tasking
- **Problem:** "While the sauce simmers, prepare the vegetables"
- **Solution:** Break into sequential steps:
  ```
  1. Zet het vuur onder de saus laag
  2. Laat sudderen (10 minuten)
  3. Ondertussen: snijd de groenten
  ```

### Recipe has specialty ingredients
- **Problem:** "balsamic reduction", "saffron threads"
- **Solution:** Use common Dutch names or explain:
  ```
  • Balsamico azijn (of gewone azijn)
  • Saffraan draden (gele specerij)
  ```

### Source recipe is already in Dutch but poorly structured
- **Solution:** Still reorder to be chronological! Don't assume it's good just because it's in Dutch.

## Quality checklist

Before creating the Notion page, verify:

- [ ] Oven/heat is turned on in first relevant step
- [ ] All prep (chopping, measuring) happens before cooking
- [ ] Each step is one simple action
- [ ] Timing is explicit (not "until done")
- [ ] Language is simple Dutch (no fancy cooking terms)
- [ ] Steps are numbered and in execution order
- [ ] Ingredients match what's used in steps

## Tips

- **Start chronologically, not logically** - Logical order groups similar tasks; chronological order is when they actually happen
- **Test with "what if I stop reading here?"** - After each step, would the cook know what to do next?
- **Timing should be countable** - "Bak 5 minuten" not "Bak tot zacht"
- **Equipment prep is a step** - "Verwarm een pan" is step 1, not assumed
