from fastmcp import FastMCP
import httpx
import json
import os
import re
import csv
from typing import Any, Dict, List
from urllib.parse import quote
import scrape_schema_recipe  # type: ignore

mcp = FastMCP("MatMCP 🛒")


def load_recipes_from_csv() -> List[Dict[str, str]]:
    recipes = []
    csv_file = "recipes.csv"
    try:
        if os.path.exists(csv_file):
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    recipes.append({
                        "id": row["id"],
                        "title": row["title"],
                        "url": row["url"]
                    })
    except Exception:
        pass
    return recipes


RECIPES: List[Dict[str, str]] = load_recipes_from_csv()


def fetch_and_parse_recipe(url: str) -> Dict[str, Any]:
    headers = {"User-Agent": "MatMCP/0.1"}
    with httpx.Client(
        follow_redirects=True,
        timeout=30.0,
        headers=headers,
    ) as client:
        response = client.get(url)
        response.raise_for_status()
        html = response.text
    recipes = scrape_schema_recipe.loads(
        html,
        python_objects=False,
    )
    if recipes and isinstance(recipes, list):
        recipe = recipes[0]
        if isinstance(recipe, dict):
            return recipe
    return {}


def search_ingredients(query: str) -> List[Dict[str, Any]]:
    encoded_query = quote(query)
    search_url = f"https://www.mathem.se/se/search/products/?q={encoded_query}"

    headers = {"User-Agent": "MatMCP/0.1"}
    with httpx.Client(
        follow_redirects=True,
        timeout=30.0,
        headers=headers,
    ) as client:
        response = client.get(search_url)
        response.raise_for_status()
        html = response.text

    json_match = re.search(
        r'<script id="__NEXT_DATA__"[^>]*>(.+?)</script>', html, re.DOTALL
    )
    if not json_match:
        return []

    try:
        next_data = json.loads(json_match.group(1))
        search_data = (
            next_data.get("props", {})
            .get("pageProps", {})
            .get("dehydratedState", {})
        )

        queries = search_data.get("queries", [])
        product_query = None
        for query_item in queries:
            if "searchpageresponse" in str(query_item.get("queryKey", [])):
                product_query = query_item
                break

        if not product_query:
            return []

        items = product_query.get("state", {}).get("data", {}).get("items", [])
        products = []

        for item in items:
            if item.get("type") != "product":
                continue

            attrs = item.get("attributes", {})
            product = {
                "id": attrs.get("id"),
                "name": attrs.get("name", ""),
                "description": attrs.get("nameExtra", ""),
                "brand": attrs.get("brand", ""),
                "price": (
                    f"{attrs.get('grossPrice', '')} "
                    f"{attrs.get('currency', 'SEK')}"
                ),
                "unit_price": (
                    f"{attrs.get('grossUnitPrice', '')} "
                    f"{attrs.get('currency', 'SEK')} /"
                    f"{attrs.get('unitPriceQuantityAbbreviation', '')}"
                ),
            }

            classifiers = attrs.get("clientClassifiers", [])
            if classifiers:
                labels = [
                    c.get("name", "") for c in classifiers if c.get("name")
                ]
                if labels:
                    product["labels"] = labels

            promotions = attrs.get("promotions", [])
            if promotions:
                offers = [
                    p.get("title", "") for p in promotions if p.get("title")
                ]
                if offers:
                    product["offer"] = ", ".join(offers)

            if product["name"]:
                products.append(product)

        return products[:7]

    except (json.JSONDecodeError, KeyError, AttributeError):
        return []


def read_cookie_from_file() -> str:
    cookie_file = "cookie.txt"
    try:
        if os.path.exists(cookie_file):
            with open(cookie_file, "r", encoding="utf-8") as f:
                return f.read().strip()
    except Exception:
        pass
    return ""


def add_to_basket(product_id: int, quantity: int = 1) -> Dict[str, Any]:
    url = (
        "https://www.mathem.se/tienda-web-api/v1/cart/items/"
        "?group_by=recipes"
    )

    payload = {"items": [{"product_id": product_id, "quantity": quantity}]}

    cookie = read_cookie_from_file()
    headers = {
        "User-Agent": "MatMCP/0.1",
        "Content-Type": "application/json",
    }

    if cookie:
        headers["Cookie"] = cookie

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.json() if response.content else {},
                "product_id": product_id,
                "quantity": quantity,
            }
    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "error": f"HTTP {e.response.status_code}",
            "message": e.response.text if e.response else "Unknown error",
            "product_id": product_id,
            "quantity": quantity,
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Request failed",
            "message": str(e),
            "product_id": product_id,
            "quantity": quantity,
        }


@mcp.tool
def list_recipes() -> List[Dict[str, str]]:
    """List available recipes"""
    return RECIPES


@mcp.tool
def get_recipe_by_index(index: int) -> Dict[str, Any]:
    """Get a recipe by index from the list"""
    if index < 0 or index >= len(RECIPES):
        return {}
    url = RECIPES[index]["url"]
    return fetch_and_parse_recipe(url)


@mcp.tool
def search_mathem_ingredients(query: str) -> List[Dict[str, Any]]:
    """Search for ingredients on Mathem.se grocery store"""
    return search_ingredients(query)


@mcp.tool
def add_to_mathem_basket(product_id: int, quantity: int = 1) -> bool:
    """Add a product to the Mathem.se shopping basket"""
    result = add_to_basket(product_id, quantity)
    return result.get("success", False)


if __name__ == "__main__":
    mcp.run()
