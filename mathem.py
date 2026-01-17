from fastmcp import FastMCP
import httpx
import json
import os
from typing import Any, Dict, List
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("MatMCP 🛒", version="0.2.0")

# Configuration from environment variables
MATHEM_COUNTRY = os.getenv("MATHEM_COUNTRY", "se")
MATHEM_LANGUAGE = os.getenv("MATHEM_LANGUAGE", "sv")
MATHEM_USER_AGENT = os.getenv("MATHEM_USER_AGENT", "MatMCP/0.2.0")


def search_ingredients(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search for products using Mathem's search API.

    Uses the direct tienda-web-api endpoint instead of scraping Next.js data,
    making it more reliable and less fragile to website changes.

    Args:
        query: Search term in Swedish
        limit: Maximum number of products to return (default: 10)
    """
    encoded_query = quote(query)
    api_url = f"https://www.mathem.se/tienda-web-api/v1/search/?q={encoded_query}"

    headers = {"User-Agent": "MatMCP/0.2.0"}

    try:
        with httpx.Client(
            follow_redirects=True,
            timeout=30.0,
            headers=headers,
        ) as client:
            response = client.get(api_url)
            response.raise_for_status()
            data = response.json()

        products = []
        for item in data.get("products", [])[:limit]:
            product = {
                "id": item.get("id"),
                "name": item.get("name", ""),
                "description": item.get("name_extra", ""),
                "brand": item.get("brand", ""),
                "price": f"{item.get('gross_price', '')} {item.get('currency', 'SEK')}",
                "unit_price": (
                    f"{item.get('gross_unit_price', '')} "
                    f"{item.get('currency', 'SEK')} /"
                    f"{item.get('unit_price_quantity_abbreviation', '')}"
                ),
            }

            # Add labels/classifiers if available
            classifiers = item.get("client_classifiers", [])
            if classifiers:
                labels = [c.get("name", "") for c in classifiers if c.get("name")]
                if labels:
                    product["labels"] = labels

            # Add promotions if available
            promotions = item.get("promotions", [])
            if promotions:
                offers = [p.get("title", "") for p in promotions if p.get("title")]
                if offers:
                    product["offer"] = ", ".join(offers)

            if product["name"]:
                products.append(product)

        return products

    except (httpx.HTTPError, json.JSONDecodeError, KeyError, AttributeError):
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


def get_basket() -> Dict[str, Any]:
    url = "https://www.mathem.se/tienda-web-api/v1/cart/"

    cookie = read_cookie_from_file()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Origin": "https://www.mathem.se",
        "Referer": "https://www.mathem.se/",
    }

    if cookie:
        headers["Cookie"] = cookie

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            cart_data = response.json()

            # Extract summary information
            summary = {
                "total_items": cart_data.get("product_quantity_count", 0),
                "total_amount": f"{cart_data.get('total_gross_amount', '0')} {cart_data.get('currency', 'SEK')}",
                "subtotal": f"{cart_data.get('display_price', '0')} {cart_data.get('currency', 'SEK')}",
            }

            # Extract items from groups
            items = []
            for group in cart_data.get("groups", []):
                category = group.get("title", "Unknown")

                for item in group.get("items", []):
                    product = item.get("product", {})
                    quantity = item.get("quantity", 0)

                    product_info = {
                        "id": product.get("id"),
                        "name": product.get("name", ""),
                        "full_name": product.get("full_name", ""),
                        "brand": product.get("brand", ""),
                        "description": product.get("name_extra", ""),
                        "category": category,
                        "quantity": quantity,
                        "price": f"{product.get('gross_price', '')} {product.get('currency', 'SEK')}",
                        "unit_price": f"{product.get('gross_unit_price', '')} {product.get('currency', 'SEK')} /{product.get('unit_price_quantity_abbreviation', '')}",
                        "total_price": f"{item.get('display_price_total', '')} {product.get('currency', 'SEK')}",
                        "availability": product.get("availability", {}).get("code", "unknown"),
                    }

                    # Add discount information if available
                    discount = product.get("discount")
                    if discount and discount.get("is_discounted"):
                        product_info["discount"] = {
                            "original_price": f"{discount.get('undiscounted_gross_price', '')} {product.get('currency', 'SEK')}",
                            "description": discount.get("description_short", ""),
                        }

                    # Add labels/certifications if available
                    classifiers = product.get("client_classifiers", [])
                    if classifiers:
                        labels = [c.get("name", "") for c in classifiers if c.get("name")]
                        if labels:
                            product_info["labels"] = labels

                    items.append(product_info)

            return {
                "success": True,
                "summary": summary,
                "items": items,
            }

    except httpx.HTTPStatusError as e:
        return {
            "success": False,
            "error": f"HTTP {e.response.status_code}",
            "message": e.response.text if e.response else "Unknown error",
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Request failed",
            "message": str(e),
        }


def add_to_basket(product_id: int, quantity: int = 1) -> Dict[str, Any]:
    url = (
        "https://www.mathem.se/tienda-web-api/v1/cart/items/"
        "?group_by=recipes"
    )

    payload = {"items": [{"product_id": product_id, "quantity": quantity}]}

    cookie = read_cookie_from_file()
    headers = {
        "User-Agent": MATHEM_USER_AGENT,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Origin": "https://www.mathem.se",
        "Referer": "https://www.mathem.se/se/",
        "x-client-app": "tienda-web",
        "x-country": MATHEM_COUNTRY,
        "x-language": MATHEM_LANGUAGE,
    }

    if cookie:
        headers["Cookie"] = cookie
        # Extract CSRF token from cookie and add as header
        for part in cookie.split(";"):
            part = part.strip()
            if part.startswith("csrftoken="):
                csrf_token = part.split("=", 1)[1]
                headers["X-CSRFToken"] = csrf_token
                break

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
def search_mathem_ingredients(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search for ingredients on Mathem.se grocery store.

    Args:
        query: Search term in Swedish (e.g., "kaffe", "mjölk", "ägg")
        limit: Maximum number of products to return (default: 10, max: 40)

    Returns:
        List of products (up to limit), each containing:
        - id (int): Product ID (required for add_to_mathem_basket)
        - name (str): Product name
        - description (str): Package size and any restrictions (e.g., "450 g", "Max 2 per kund")
        - brand (str): Manufacturer/brand name
        - price (str): Full price with currency (e.g., "49.00 SEK")
        - unit_price (str): Comparative price per unit (e.g., "108.89 SEK /kg")
        - labels (list[str], optional): Certifications/labels (e.g., "Rainforest Alliance", "FSC")
        - offer (str, optional): Special offers (e.g., "Extrapris", "2 för 150 kr")

    Example:
        results = search_mathem_ingredients("kaffe")  # Returns up to 10 coffee products
        results = search_mathem_ingredients("kaffe", limit=5)  # Returns up to 5 products
    """
    return search_ingredients(query, limit)


@mcp.tool
def add_to_mathem_basket(product_id: int, quantity: int = 1) -> bool:
    """Add a product to the Mathem.se shopping basket.

    IMPORTANT: Requires authentication via cookie.txt file containing valid
    Mathem.se session cookies. Without authentication, this operation will fail.

    Args:
        product_id: Product ID from search_mathem_ingredients results
        quantity: Number of items to add (default: 1)

    Returns:
        bool: True if successfully added to basket, False otherwise

    Workflow:
        1. Search for products: search_mathem_ingredients("kaffe")
        2. Choose a product and get its id field
        3. Add to basket: add_to_mathem_basket(product_id=62265, quantity=2)

    Authentication Setup:
        Create cookie.txt in the project root with your Mathem.se session cookies.
        See cookie.txt.example for format.
    """
    result = add_to_basket(product_id, quantity)
    return result.get("success", False)


@mcp.tool
def get_mathem_basket() -> Dict[str, Any]:
    """Get the current contents of the Mathem.se shopping basket.

    IMPORTANT: Requires authentication via cookie.txt file containing valid
    Mathem.se session cookies. Without authentication, this operation will fail.

    Returns:
        Dictionary containing:
        - success (bool): Whether the request succeeded
        - summary (dict): Cart summary with total_items, total_amount, subtotal
        - items (list): List of items in the basket, each containing:
            - id (int): Product ID
            - name (str): Product name
            - full_name (str): Full product name including brand
            - brand (str): Brand name
            - description (str): Package size and restrictions
            - category (str): Product category
            - quantity (int): Quantity in basket
            - price (str): Unit price
            - unit_price (str): Comparative price per unit
            - total_price (str): Total price for this item (price × quantity)
            - availability (str): Availability status
            - discount (dict, optional): Discount information if applicable
            - labels (list[str], optional): Certifications/labels

    Example:
        basket = get_mathem_basket()
        if basket["success"]:
            print(f"You have {basket['summary']['total_items']} items")
            for item in basket["items"]:
                print(f"- {item['quantity']}x {item['full_name']}")

    Authentication Setup:
        Create cookie.txt in the project root with your Mathem.se session cookies.
        See cookie.txt.example for format.
    """
    return get_basket()


if __name__ == "__main__":
    mcp.run()
