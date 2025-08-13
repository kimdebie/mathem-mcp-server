import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mathem


def test_list_recipes():
    """Test listing available recipes."""
    recipes = mathem.list_recipes.fn()
    assert isinstance(recipes, list)
    assert len(recipes) > 0
    assert "title" in recipes[0]
    assert "url" in recipes[0]
    print(f"✅ Found {len(recipes)} recipes")


def test_get_recipe():
    """Test fetching recipe data by index."""
    recipe_data = mathem.get_recipe_by_index.fn(0)
    print(json.dumps(recipe_data, indent=2, ensure_ascii=False))
    assert recipe_data is not None
    assert "name" in recipe_data
    assert "recipeIngredient" in recipe_data
    assert "recipeInstructions" in recipe_data
    print("✅ Recipe data fetched successfully")


def test_search_ingredients():
    """Test searching for ingredients on Mathem.se."""
    results = mathem.search_mathem_ingredients.fn("gul lök")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    assert isinstance(results, list)
    assert len(results) > 0

    product = results[0]
    assert "name" in product
    assert "price" in product
    assert "search_url" in product
    print(f"✅ Found {len(results)} products for 'gul lök'")


def test_search_variations():
    """Test different search queries."""
    searches = ["gul lök", "lök", "EKO"]

    for query in searches:
        print(f"\n=== Search: '{query}' ===")
        results = mathem.search_mathem_ingredients.fn(query)
        assert isinstance(results, list)
        print(f"Found {len(results)} products")

        for product in results[:3]:
            print(
                f"- {product['name']} | {product['price']} | {product.get('origin', 'N/A')}"
            )

        if query == "EKO":
            assert len(results) >= 1
            assert "EKO" in results[0]["name"]
        elif query == "gul lök":
            assert len(results) >= 5

    print("✅ Search variations work correctly")


def test_invalid_recipe_index():
    """Test handling of invalid recipe indices."""
    result = mathem.get_recipe_by_index.fn(-1)
    assert result == {}

    result = mathem.get_recipe_by_index.fn(999)
    assert result == {}

    print("✅ Invalid indices handled correctly")


def test_complete_workflow():
    """Test a complete grocery shopping workflow."""
    print("\n🛒 Complete Grocery Shopping Workflow Test")

    recipes = mathem.list_recipes.fn()
    print(f"1. Available recipes: {len(recipes)}")

    recipe = mathem.get_recipe_by_index.fn(0)
    print(f"2. Recipe: {recipe.get('name', 'Unknown')}")

    if "recipeIngredient" in recipe and recipe["recipeIngredient"]:
        first_ingredient = recipe["recipeIngredient"][0]

        search_term = "lök" if "lök" in first_ingredient.lower() else "gul lök"

        products = mathem.search_mathem_ingredients.fn(search_term)
        print(f"3. Found {len(products)} products for ingredient: {first_ingredient}")

        if products:
            cheapest = min(
                products, key=lambda p: float(p["price"].replace(",", ".").split()[0])
            )
            print(f"4. Cheapest option: {cheapest['name']} - {cheapest['price']}")

    print("✅ Complete workflow successful")


def test_add_to_basket():
    print("\n🛒 Testing Add to Basket functionality")

    ingredient_products = mathem.search_mathem_ingredients.fn("gul lök")
    assert len(ingredient_products) > 0

    test_product = ingredient_products[0]
    product_id = test_product["id"]
    print(f"Testing with product: {test_product['name']} (ID: {product_id})")

    result = mathem.add_to_mathem_basket.fn(product_id, 1)
    print(f"Add to basket result: {json.dumps(result, indent=2, ensure_ascii=False)}")

    assert isinstance(result, dict)
    assert "success" in result
    assert "product_id" in result
    assert result["product_id"] == product_id

    if result["success"]:
        print("✅ Successfully added item to basket")
    else:
        print(
            f"⚠️ Failed to add to basket (expected if no cookie): {result.get('error', 'Unknown error')}"
        )

    print("✅ Add to basket function works correctly")


if __name__ == "__main__":
    print("🧪 Running comprehensive MatMCP tests...\n")

    test_list_recipes()
    test_get_recipe()
    test_search_ingredients()
    test_search_variations()
    test_invalid_recipe_index()
    test_complete_workflow()
    test_add_to_basket()

    print("\n🎉 All tests passed!")
