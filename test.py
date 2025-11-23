import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mathem


def test_search_ingredients():
    """Test searching for ingredients on Mathem.se."""
    results = mathem.search_mathem_ingredients.fn("gul lök")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    assert isinstance(results, list)
    assert len(results) > 0

    product = results[0]
    assert "name" in product
    assert "price" in product
    assert "id" in product
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


def test_add_to_basket():
    print("\n🛒 Testing Add to Basket functionality")

    ingredient_products = mathem.search_mathem_ingredients.fn("gul lök")
    assert len(ingredient_products) > 0

    test_product = ingredient_products[0]
    product_id = test_product["id"]
    print(f"Testing with product: {test_product['name']} (ID: {product_id})")

    result = mathem.add_to_mathem_basket.fn(product_id, 1)
    print(f"Add to basket result: {result}")

    assert isinstance(result, bool)

    if result:
        print("✅ Successfully added item to basket")
    else:
        print("⚠️ Failed to add to basket (expected if no cookie)")

    print("✅ Add to basket function works correctly")


def test_get_basket():
    print("\n🛒 Testing Get Basket functionality")

    result = mathem.get_mathem_basket.fn()
    print(f"Basket result: {json.dumps(result, indent=2, ensure_ascii=False)}")

    assert isinstance(result, dict)
    assert "success" in result

    if result["success"]:
        assert "summary" in result
        assert "items" in result

        summary = result["summary"]
        print(f"\n📊 Basket Summary:")
        print(f"  Total items: {summary['total_items']}")
        print(f"  Subtotal: {summary['subtotal']}")
        print(f"  Total amount: {summary['total_amount']}")

        items = result["items"]
        print(f"\n📦 Items in basket ({len(items)}):")
        for item in items:
            print(f"  - {item['quantity']}x {item['full_name']}")
            print(f"    Price: {item['price']} | Total: {item['total_price']}")
            if "discount" in item:
                print(f"    Discount: {item['discount']['description']}")
            if "labels" in item:
                print(f"    Labels: {', '.join(item['labels'])}")

        print("✅ Successfully retrieved basket contents")
    else:
        print(f"⚠️ Failed to get basket: {result.get('error', 'Unknown error')}")
        print("⚠️ (expected if no cookie.txt or invalid authentication)")

    print("✅ Get basket function works correctly")


if __name__ == "__main__":
    print("🧪 Running MatMCP tests...\n")

    test_search_ingredients()
    test_search_variations()
    test_add_to_basket()
    test_get_basket()

    print("\n🎉 All tests passed!")
