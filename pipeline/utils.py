# utils.py
from config import CITIES

def get_user_selection():
    """Displays the menu and returns the list of chosen cities"""
    print("\n=== CITY MENU ===")
    for key, info in CITIES.items():
        print(f"[{key}] {info['name']}")
    print("[0] All cities")
    
    choice = input("\nEnter city codes (comma separated) or 0 for all: ")
    
    selected_cities = []
    
    if choice.strip() == '0':
        return list(CITIES.values()) # Return all
    
    codes = choice.split(',')
    for code in codes:
        code = code.strip()
        if code in CITIES:
            selected_cities.append(CITIES[code])
        else:
            print(f"⚠️ Invalid code '{code}' ignored.")
            
    return selected_cities