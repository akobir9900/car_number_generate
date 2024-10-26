from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/app.py", methods=["POST"])
def generate():
    region = request.form.get("region")
    uz_auto_number = generate_uz_auto_number(region)
    price = determine_price(uz_auto_number)
    region_name = get_region_name(uz_auto_number)  # Viloyat nomini olish
    return render_template("index.html", uz_auto_number=uz_auto_number, price=price, region=region, region_name=region_name)

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/admin/app.py", methods=["POST"])
def admin_generate():
    number = request.form.get("number")
    if not is_valid_auto_number(number):
        return render_template("admin.html", error="Bunday raqam yo'q.", number=number)

    price = determine_price(number)
    region_name = get_region_name(number)
    return render_template("admin.html", generated_number=number, price=price, region_name=region_name)



# Viloyatga mos avtomobil raqamini yaratish funksiyasi
def generate_uz_auto_number(region):
    regions = {
        "Toshkent": "01",
        "Samarqand": "30",
        "Andijon": "60",
        "Buxoro": "80",
        "Qoraqalpog'iston": "95",
        "Farg‘ona": "40",
        "Namangan": "50",
        "Jizzax": "25",
        "Surxondaryo": "75",
        "Qashqadaryo": "70",
        "Sirdaryo": "20",
        "Navoiy": "85",
        "Xorazm": "90",
    }
    region_code = regions.get(region, "01")
    letter = random.choice(string.ascii_uppercase)
    numbers = ''.join(random.choices(string.digits, k=3))
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    return f"{region_code} {letter} {numbers} {letters}"

# Narxni aniqlash funksiyasi
def determine_price(auto_number):
    parts = auto_number.split()
    numbers = parts[2]  # "777"
    letters = parts[3]  # "AA"

    same_numbers = len(set(numbers)) == 1  # Barcha raqamlar bir xilmi?
    same_letters = len(set(letters)) == 1  # Barcha harflar bir xilmi?

    # Oddiy raqamlar
    if not same_numbers and not same_letters:
        return "500$ (Oddiy raqam)"
    
    # Chiroyli raqamlar
    elif (same_numbers and not same_letters) or (not same_numbers and same_letters):
        return "800$ (Chiroyli raqam)"
    
    # Oltin raqamlar
    elif same_numbers and same_letters:
        return "1000$ (Oltin raqam)"
    
    return "500$ (Oddiy raqam)"  # Qolgan hollarda

# Raqamning to'g'riligini tekshirish funksiyasi
def is_valid_auto_number(auto_number):
    parts = auto_number.split()
    if len(parts) != 4:
        return False

    region_code = parts[0]  # Viloyat kodi
    regions = {
        "01",  # Toshkent
        "30",  # Samarqand
        "60",  # Andijon
        "80",  # Buxoro
        "95",  # Qoraqalpog'iston
        "40",  # Farg‘ona
        "50",  # Namangan
        "25",  # Jizzax
        "75",  # Surxondaryo
        "70",  # Qashqadaryo
        "20",  # Sirdaryo
        "85",  # Navoiy
        "90",  # Xorazm
    }
    return region_code in regions

# Viloyat kodiga mos viloyat nomini olish funksiyasi
def get_region_name(auto_number):
    parts = auto_number.split()
    region_code = parts[0]  # Viloyat kodi

    regions = {
        "01": "Toshkent",
        "30": "Samarqand",
        "60": "Andijon",
        "80": "Buxoro",
        "95": "Qoraqalpog'iston",
        "40": "Farg‘ona",
        "50": "Namangan",
        "25": "Jizzax",
        "75": "Surxondaryo",
        "70": "Qashqadaryo",
        "20": "Sirdaryo",
        "85": "Navoiy",
        "90": "Xorazm",
    }
    
    return regions.get(region_code, "Noma'lum viloyat")

if __name__ == "__main__":
    app.run(debug=True)
