import requests
from flask import Flask, jsonify, request  # type: ignore[import-not-found]

flask_app = Flask(__name__)

# Core Database Array
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar, sea salt",
        "quantity": 50
    }
]

# --- REST FULL CRUD ACTIONS ROUTES ---

@flask_app.route('/api/inventory', methods=['GET'], strict_slashes=False)
def get_all_inventory():
    return jsonify(inventory), 200

@flask_app.route('/api/inventory/<int:item_id>', methods=['GET'], strict_slashes=False)
def get_single_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item missing"}), 404
    return jsonify(item), 200

@flask_app.route('/api/inventory', methods=['POST'], strict_slashes=False)
def create_inventory_item():
    if not request.json or 'product_name' not in request.json:
        return jsonify({"error": "Bad Request: 'product_name' is missing"}), 400
    
    next_id = max([i['id'] for i in inventory], default=0) + 1
    new_item = {
        "id": next_id,
        "product_name": request.json['product_name'],
        "brands": request.json.get('brands', 'N/A'),
        "ingredients_text": request.json.get('ingredients_text', 'N/A'),
        "quantity": request.json.get('quantity', 0)
    }
    inventory.append(new_item)
    return jsonify(new_item), 201

@flask_app.route('/api/inventory/<int:item_id>', methods=['PATCH'], strict_slashes=False)
def patch_inventory_item(item_id):
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Target resource ID invalid"}), 404
    
    if not request.json:
        return jsonify({"error": "Missing payload"}), 400

    item['product_name'] = request.json.get('product_name', item['product_name'])
    item['brands'] = request.json.get('brands', item['brands'])
    item['ingredients_text'] = request.json.get('ingredients_text', item['ingredients_text'])
    item['quantity'] = request.json.get('quantity', item['quantity'])
    return jsonify(item), 200

@flask_app.route('/api/inventory/<int:item_id>', methods=['DELETE'], strict_slashes=False)
def delete_inventory_item(item_id):
    global inventory
    item = next((i for i in inventory if i["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    inventory = [i for i in inventory if i["id"] != item_id]
    return jsonify({"message": f"Successfully deleted item ID {item_id}"}), 200

# --- LIVE OPENFOODFACTS INTERFACE ROUTE ---
@flask_app.route('/api/external/<string:barcode>', methods=['GET'], strict_slashes=False)
def fetch_external_product(barcode):
    headers = {
        'User-Agent': 'InventoryManagementAdminPortal/1.0 (admin@retailcompany.com)'
    }
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                return jsonify({
                    "status": 1,
                    "product": {
                        "product_name": data["product"].get("product_name", "Unknown Item"),
                        "brands": data["product"].get("brands", "Unknown Brand"),
                        "ingredients_text": data["product"].get("ingredients_text", "No listed ingredients")
                    }
                }), 200
            else:
                return jsonify({"status": 0, "error": "Product barcode not found"}), 404
        return jsonify({"status": 0, "error": "External registry unavailable"}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"status": 0, "error": str(e)}), 503

@flask_app.route('/')
def home_page():
    return """
    <html>
        <head><title>Inventory System</title></head>
        <body style="font-family: Arial; margin: 40px;">
            <h1>Inventory Dashboard</h1>
            <button onclick="loadInventory()">View Current Inventory</button>
            <pre id="display" style="background: #f4f4f4; padding: 15px; margin-top: 20px;"></pre>

            <script>
                async function loadInventory() {
                    let response = await fetch('/api/inventory');
                    let data = await response.json();
                    document.getElementById('display').textContent = JSON.stringify(data, null, 2);
                }
            </script>
        </body>
    </html>
    """


if __name__ == '__main__':
    flask_app.run(debug=True, port=5000)