import sys

import requests

BASE_URL = "http://127.0.0.1:5000/api/inventory"
EXTERNAL_URL = "http://127.0.0.1:5000/api/external"
def display_dashboard():
    print("\n" + "="*50)
    print(" RETAIL INVENTORY MANAGEMENT CONSOLE PORTAL")
    print("="*50)
    print("1. Read All Local Inventory Items")
    print("2. Read Specific Item Details by ID")
    print("3. Create New Item Manually (POST)")
    print("4. Fetch & Save Live Item from OpenFoodFacts (External API UX)")
    print("5. Modify Existing Stock/Information (PATCH)")
    print("6. Delete Item from Database (DELETE)")
    print("7. Exit System")
    print("="*50)

def handle_view_all():
    try:
        res = requests.get(BASE_URL)
        if res.status_code == 200:
            print(f"\n{'ID':<5} | {'PRODUCT NAME':<25} | {'BRAND':<15} | {'QTY':<5}")
            print("-"*58)
            for item in res.json():
                print(f"{item['id']:<5} | {item['product_name'][:25]:<25} | {item['brands'][:15]:<15} | {item['quantity']:<5}")
    except requests.exceptions.ConnectionError:
        print("Runtime Connection Error: Check if Flask server app.py is alive.")

def handle_view_one():
    target_id = input("Enter Inventory Item ID: ")
    res = requests.get(f"{BASE_URL}/{target_id}")
    if res.status_code == 200:
        print("\nRecord Retreived:", res.json())
    else:
        print("Record lookup error:", res.json().get('error'))

def handle_create_manual():
    name = input("Enter Product Name: ")
    brand = input("Enter Brand Label: ")
    ing = input("Enter Structural Ingredients Text: ")
    try: qty = int(input("Enter Stock Quantity: "))
    except ValueError: qty = 0

    res = requests.post(BASE_URL, json={
        "product_name": name, "brands": brand, "ingredients_text": ing, "quantity": qty
    })
    if res.status_code == 201:
        print("Success: Record safely appended.")
    else:
        print("Failed to execute creation:", res.text)

def handle_external_import():
    print("\n--- Live OpenFoodFacts Barcode Lookup ---")
    print("Example Barcodes: '3017620422003' (Nutella), '737628064502' (Rice)")
    barcode = input("Scan or Input Product Barcode: ").strip()
    
    print("Pinging global OpenFoodFacts API registries...")
    res = requests.get(f"{EXTERNAL_URL}/{barcode}")
    
    if res.status_code == 200:
        data = res.json()
        prod = data["product"]
        print("\n[LIVE PRODUCT DISCOVERED]")
        print(f"Name:  {prod['product_name']}")
        print(f"Brand: {prod['brands']}")
        
        choice = input("\nWould you like to import this record into local store systems? (y/n): ")
        if choice.lower() == 'y':
            try: qty = int(input("Set Initial Store Stock Volume: "))
            except ValueError: qty = 1
            
            save_res = requests.post(BASE_URL, json={
                "product_name": prod['product_name'],
                "brands": prod['brands'],
                "ingredients_text": prod['ingredients_text'],
                "quantity": qty
            })
            if save_res.status_code == 201:
                print("Success: Registry entries initialized locally.")
            else:
                print("Error completing ingestion.")
    else:
        print("Product Barcode reference not located globally.")

def handle_patch():
    target_id = input("Enter structural record ID to modify: ")
    print("(Press enter to keep existing attributes unaltered)")
    name = input("Modify Product Name: ")
    brand = input("Modify Brand String: ")
    qty = input("Modify Stock Volume: ")

    payload = {}
    if name: payload["product_name"] = name
    if brand: payload["brands"] = brand
    if qty: payload["quantity"] = int(qty)

    res = requests.patch(f"{BASE_URL}/{target_id}", json=payload)
    if res.status_code == 200:
        print("Mutation execution complete.")
    else:
        print("Modification failed:", res.json().get('error'))


def handle_delete():
    target_id = input("Enter Inventory Item ID to delete: ")
    res = requests.delete(f"{BASE_URL}/{target_id}")
    if res.status_code == 200:
        print("Deletion performed successfully.")
    else:
        print("Deletion failed:", res.json().get('error'))


def main():
    while True:
        display_dashboard()
        opt = input("Choose Operation Route (1-7): ")
        if opt == '1': handle_view_all()
        elif opt == '2': handle_view_one()
        elif opt == '3': handle_create_manual()
        elif opt == '4': handle_external_import()
        elif opt == '5': handle_patch()
        elif opt == '6': handle_delete()
        elif opt == '7':
            print("Terminating Management Session.")
            sys.exit()
        else:
            print("Invalid input selection identifier.")

if __name__ == '__main__':
    main()