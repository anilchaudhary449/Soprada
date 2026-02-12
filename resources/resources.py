import os
import random
from datetime import datetime, timedelta
import pytz
from faker import Faker

f = Faker()

map_link = "https://maps.google.com"

URL= "https://soprada.com/login/"
RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
IMAGES_DIR = os.path.join(RESOURCES_DIR, "images")

# Gmail API Configuration (OAuth 2.0)
GMAIL_API_CREDENTIALS = os.path.join(RESOURCES_DIR, "credentials.json")
GMAIL_API_TOKEN = os.path.join(RESOURCES_DIR, "token.json")
GMAIL_OTP_QUERY = "subject:\"Verify your account\""
GMAIL_OTP_REGEX = r"\b\d{6}\b"
GMAIL_FETCH_TIMEOUT = 60
GMAIL_POLL_INTERVAL = 7

# Login Email (Must match the account used for token.json)
GMAIL_USER = "cpln.2346@gmail.com"
# Encrypted password (Legacy/IMAP only - ignored for OAuth)
GMAIL_APP_PASSWORD_ENCRYPTED = b'gAAAAABpeZ3Ab0N60Q7HS9HkPtaDByKqwtXKCxNMe0qxWNAm6eRK6IfaOsnW9GeHNmoaXFIqjSS_fubrmxOb6_Kk8PcSoe-_5a6INuNRHBqJE3JNX9F5VdY='

try:
    from utils.security import decrypt_message
    try:
        GMAIL_APP_PASSWORD = decrypt_message(GMAIL_APP_PASSWORD_ENCRYPTED)
    except Exception as e:
        print(f"Warning: Could not decrypt password: {e}")
        GMAIL_APP_PASSWORD = ""
except ImportError:
    # Fallback if utils not available (e.g. in some isolated tests)
    GMAIL_APP_PASSWORD = ""

GMAIL_SENDER_FILTER = "noreply@saauzi.com" 

custom_domain = f.domain_name(levels=2)
updated_domain = f.domain_name(levels=2)

def store_name():
    shop = ["Kathmandu", "Lalitpur",
          "Bhaktapur", "Pokhara", "Biratnagar",
          "Mahendranagar", "Dhangadhi",
          "Dipayal", "Nepalgunj",
          "Birendranagar", "Butwal"]
    return random.choice(shop) + " " + "Store"

def store_contact():
    return f.numerify("##########")

def get_nepal_time_str():
    try:
        nepal_tz = pytz.timezone('Asia/Kathmandu')
        nepal_time = datetime.now(nepal_tz)
        return nepal_time.strftime("%Y%m%d_%H%M%S")
    except Exception as e:
        print(f"Error in get_nepal_time_str: {e}")
        return datetime.now().strftime("%Y%m%d_%H%M%S")

def category_title():
    titles = [
        "Electronics",
        "Fashion",
        "Home & Garden",
        "Sports & Outdoors",
        "Toys & Games",
        "Health & Beauty",
        "Automotive",
        "Books & Audible",
        "Pet Supplies",
        "Office Products"
    ]

    return random.choice(titles)

google_taxonomy_map = {
    "Electronics": "Electronics",
    "Fashion": "Apparel & Accessories",
    "Home & Garden": "Home & Garden",
    "Sports & Outdoors": "Sporting Goods",
    "Toys & Games": "Toys & Games",
    "Health & Beauty": "Health & Beauty",
    "Automotive": "Vehicles & Parts",
    "Books & Audible": "Media > Books",
    "Pet Supplies": "Animals & Pet Supplies",
    "Office Products": "Office Supplies"
}

meta_description_map = {
    "Electronics": "Discover the latest gadgets and electronics including phones, laptops, and accessories.",
    "Fashion": "Shop the newest trends in fashion for men, women, and children. Clothing, shoes, and more.",
    "Home & Garden": "Upgrade your living space with our wide range of home and garden products.",
    "Sports & Outdoors": "Gear up for your next adventure with top-quality sports and outdoor equipment.",
    "Toys & Games": "Find the perfect toys and games for kids of all ages. Fun and educational.",
    "Health & Beauty": "Explore our collection of health and beauty products for your daily care routine.",
    "Automotive": "Get the best parts and accessories for your vehicle. Quality automotive supplies.",
    "Books & Audible": "Dive into a world of stories with our vast selection of books and audio books.",
    "Pet Supplies": "Everything you need for your furry friends. Food, toys, and pet care essentials.",
    "Office Products": "Equip your office with essential supplies and furniture for maximum productivity."
}

product_description_map = {
    # Electronics
    "Smartphone": "Latest model smartphone with high-resolution camera and fast processor.",
    "Laptop": "High-performance laptop suitable for gaming and professional work.",
    "Headphone": "Noise-cancelling over-ear headphones for immersive audio experience.",
    "Wireless Earbuds": "True wireless earbuds with crystal clear sound and long battery life.",
    "Smart Watch": "Feature-rich smartwatch with health tracking and notification capability.",
    "Tablet": "Portable tablet with vibrant display, perfect for entertainment and reading.",
    "Gaming Console": "Next-gen gaming console for the ultimate home entertainment system.",
    "Bluetooth Speaker": "Portable Bluetooth speaker with powerful bass and waterproof design.",
    "Power Bank": "High-capacity power bank to keep your devices charged on the go.",
    "USB-C Cable": "Durable and fast-charging USB-C cable for all compatible devices.",

    # Fashion
    "T-Shirt": "Comfortable cotton t-shirt available in various colors and sizes.",
    "Jeans": "Classic denim jeans with a perfect fit and durable fabric.",
    "Sneakers": "Stylish and comfortable sneakers for daily wear and sports activities.",
    "Leather Jacket": "Premium quality leather jacket that adds style to any outfit.",
    "Sunglasses": "Trendy sunglasses offering UV protection and a chic look.",
    "Backpack": "Spacious and ergonomic backpack, ideal for school, travel, or work.",
    "Wristwatch": "Elegant wristwatch with precision movement and water resistance.",
    "Baseball Cap": "Adjustable baseball cap made from breathable material.",

    # Home & Garden
    "Coffee Maker": "Automatic coffee maker for brewing fresh and delicious coffee every morning.",
    "Vacuum Cleaner": "Powerful vacuum cleaner to keep your floors dust-free and clean.",
    "Air Purifier": "HEPA air purifier to remove allergens and improve indoor air quality.",
    "LED Desk Lamp": "Adjustable LED desk lamp with multiple brightness levels and eye protection.",
    "Garden Hose": "Flexible and durable garden hose for all your watering needs.",
    "Plant Pot": "Decorative plant pot suitable for indoor and outdoor plants.",
    
    # Sports & Outdoors
    "Bicycle": "Mountain bicycle with robust frame and gears for all terrains.",
    "Water Bottle": "Insulated water bottle to keep drinks cold or hot for hours.",
    "Fitness Tracker": "Wearable fitness tracker to monitor steps, heart rate, and sleep.",

    # Toys & Games
    "LEGO Set": "Creative LEGO building set for hours of fun and imagination.",
    "Board Game": "Classic board game for family fun night and social gatherings.",
    "Action Figure": "Collectible action figure with detailed features and accessories.",
    
    # Health & Beauty
    "Face Cream": "Hydrating face cream to rejuvenate skin and reduce wrinkles.",
    "Shampoo": "Nourishing shampoo for healthy, shiny, and strong hair.",
    "Electric Toothbrush": "Rechargeable electric toothbrush for superior dental hygiene.",
    
    # Automotive
    "Car Phone Holder": "Secure car phone holder for hands-free navigation and calls.",
    "Dash Cam": "High-definition dash cam to record your driving for safety and security.",
    "Car Vacuum": "Portable car vacuum cleaner to keep your vehicle interior spotless.",
    
    # Books & Audible
    "Fiction Novel": "Bestselling fiction novel that will keep you turning the pages.",
    "Self-Help Book": "Inspirational self-help book to guide you towards personal growth.",
    "Cookbook": "Delicious recipes and cooking tips in a comprehensive cookbook.",
    
    # Pet Supplies
    "Dog Food": "Nutritious and delicious dog food for puppies and adult dogs.",
    "Cat Litter": "Odor-control cat litter for a clean and fresh home environment.",
    "Pet Bed": "Cozy pet bed providing a comfortable sleeping spot for your pet.",
    
    # Office Products
    "Wireless Mouse": "Ergonomic wireless mouse for smooth navigation and productivity.",
    "Mechanical Keyboard": "Tactile mechanical keyboard for typing comfort and speed.",
    "Office Chair": "Ergonomic office chair with lumbar support for long working hours."
}

def product_name():
    return random.choice(list(product_description_map.keys()))

def get_product_description(name):
    return product_description_map.get(name, "Description not found.")

color_map = {
    "Red Test": "FF0000",
    "Green Test": "008000",
    "Blue Test": "0000FF",
    "Yellow Test": "FFFF00",
    "Black Test": "000000",
    "White Test": "FFFFFF",
    "Orange Test": "FFA500",
    "Purple Test": "800080",
    "Pink Test": "FFC0CB",
    "Gray Test": "808080",
    "Cyan Test": "00FFFF",
    "Brown Test": "A52A2A",
    "Silver Test": "C0C0C0",
    "Magenta Test": "FF00FF",

    # Additional unique colors
    "Lime Test": "00FF00",
    "Navy Blue Test": "000080",
    "Teal Test": "008080",
    "Olive Test": "808000",
    "Maroon Test": "800000",
    "Aqua Test": "7FDBFF",
    "Coral Test": "FF7F50",
    "Gold Test": "FFD700",
    "Indigo Test": "4B0082",
    "Violet Test": "EE82EE",
    "Turquoise Test": "40E0D0",
    "Mint Test": "98FF98",
    "Lavender Test": "E6E6FA",
    "Beige Test": "F5F5DC",
    "Khaki Test": "F0E68C",
    "Crimson Test": "DC143C",
    "Salmon Test": "FA8072",
    "Chocolate Test": "D2691E",
    "Plum Test": "DDA0DD",
    "Slate Gray Test": "708090",
    "Fuchsia Test": "FF00FF"
}


def get_random_color():
    color_name = random.choice(list(color_map.keys()))
    color_hex = color_map[color_name]
    return color_name, color_hex


size_map = {
    "Int": ["XXS", "XS", "S", "M", "L", "XL", "XXL", "XXXL", "XXXXL", "XXXXXL", "XXXXXXL"],
    "EU": ["36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", \
        "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64",\
             "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", \
                "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", \
                    "93", "94", "95", "96", "97", "98", "99", "100"]
}


def get_random_size(size_type="Int"):
    """
    Returns a random size value based on the size type ('Int' or 'EU').
    Defaults to 'Int' if type is invalid.
    """
    if size_type not in size_map:
        size_type = "Int"
    return random.choice(size_map[size_type])


def get_random_size_and_type():
    size_type = random.choice(list(size_map.keys()))
    size_value = random.choice(size_map[size_type])
    return size_type, (f"{size_value}" + "_" + get_nepal_time_str())


def marked_price():
    return random.randint(100, 100000)

def selling_price():
    return random.randint(50, 100000)

def available_quantity():
    return random.randint(100, 10000)

def discount():
    return random.randint(0, 100)

def logistic_charge():
    return random.randint(10, 500)

def confirm_quantity():
    return random.randint(1, 100)

customer_name_map = {
    "Ram Bahadur Thapa": "Ram Bahadur Thapa",
    "Sita Kumari Sherpa": "Sita Kumari Sherpa",
    "Hari Prasad Sharma": "Hari Prasad Sharma",
    "Gita Devi Gurung": "Gita Devi Gurung",
    "Krishna Gopal Shrestha": "Krishna Gopal Shrestha",
    "Laxmi Maya Tamang": "Laxmi Maya Tamang",
    "Bishnu Prasad Adhikari": "Bishnu Prasad Adhikari",
    "Saraswati Devi Rai": "Saraswati Devi Rai",
    "Shiva Kumar Yadav": "Shiva Kumar Yadav",
    "Durga Devi Magar": "Durga Devi Magar",
    "Ramesh Kumar Newar": "Ramesh Kumar Newar",
    "Anita Kumari Chettri": "Anita Kumari Chettri",
    "Suresh Thapa": "Suresh Thapa",
    "Rita Sharma": "Rita Sharma",
    "Rajendra Prasad Koirala": "Rajendra Prasad Koirala",
    "Maya Devi": "Maya Devi",
    "Rajesh Hamal": "Rajesh Hamal",
    "Manisha Koirala": "Manisha Koirala",
    "Sunil Thapa": "Sunil Thapa",
    "Rekha Thapa": "Rekha Thapa",
    "Dayahang Rai": "Dayahang Rai",
    "Saugat Malla": "Saugat Malla",
    "Aryan Sigdel": "Aryan Sigdel",
    "Anmol KC": "Anmol KC",
    "Namrata Shrestha": "Namrata Shrestha",
    "Priyanka Karki": "Priyanka Karki",
    "Bipin Karki": "Bipin Karki",
    "Keki Adhikari": "Keki Adhikari",
    "Swastima Khadka": "Swastima Khadka",
    "Nischal Basnet": "Nischal Basnet",
    "Deepak Raj Giri": "Deepak Raj Giri",
    "Paul Shah": "Paul Shah",
    "Barsha Raut": "Barsha Raut",
    "Samragyee RL Shah": "Samragyee RL Shah",
    "Pradeep Khadka": "Pradeep Khadka",
    "Aanchal Sharma": "Aanchal Sharma",
    "Buddhi Tamang": "Buddhi Tamang",
    "Wilson Bikram Rai": "Wilson Bikram Rai",
    "Sandip Chhetri": "Sandip Chhetri",
    "Malvika Subba": "Malvika Subba",
    "Anju Panta": "Anju Panta",
    "Pramod Kharel": "Pramod Kharel",
    "Sugam Pokharel": "Sugam Pokharel",
    "Indira Joshi": "Indira Joshi",
    "Raju Lama": "Raju Lama",
    "Nima Rumba": "Nima Rumba",
    "Adrian Pradhan": "Adrian Pradhan",
    "Amrit Gurung": "Amrit Gurung",
    "Yabesh Thapa": "Yabesh Thapa",
    "Sajjan Raj Vaidya": "Sajjan Raj Vaidya",
    "Bartika Eam Rai": "Bartika Eam Rai",
    "Bipul Chettri": "Bipul Chettri",
    "Sushant KC": "Sushant KC",
    "Neetesh Jung Kunwar": "Neetesh Jung Kunwar",
    "Swoopna Suman": "Swoopna Suman",
    "Samir Ghimire": "Samir Ghimire",
    "Girish Khatiwada": "Girish Khatiwada",
    "Yama Buddha": "Yama Buddha",
    "Laure": "Laure",
    "Vten": "Vten",
    "Balen Shah": "Balen Shah",
    "Harka Sampang": "Harka Sampang",
    "Gagan Thapa": "Gagan Thapa",
    "Rabi Lamichhane": "Rabi Lamichhane",
    "Baburam Bhattarai": "Baburam Bhattarai",
    "Pushpa Kamal Dahal": "Pushpa Kamal Dahal",
    "KP Sharma Oli": "KP Sharma Oli",
    "Sher Bahadur Deuba": "Sher Bahadur Deuba",
    "Madhav Kumar Nepal": "Madhav Kumar Nepal",
    "Jhalanath Khanal": "Jhalanath Khanal",
    "Ram Baran Yadav": "Ram Baran Yadav",
    "Bidya Devi Bhandari": "Bidya Devi Bhandari",
    "Paras Shah": "Paras Shah",
    "Gyanendra Shah": "Gyanendra Shah",
    "Komal Shah": "Komal Shah",
    "Himani Shah": "Himani Shah",
    "Hridayendra Shah": "Hridayendra Shah",
    "Purnima Shrestha": "Purnima Shrestha",
    "Melina Rai": "Melina Rai",
    "Asmita Adhikari": "Asmita Adhikari",
    "Rachana Rimal": "Rachana Rimal",
    "Eleena Chauhan": "Eleena Chauhan",
    "Samikshya Adhikari": "Samikshya Adhikari",
    "Pratap Das": "Pratap Das",
    "Nishan Bhattarai": "Nishan Bhattarai",
    "Ravi Oad": "Ravi Oad",
    "Buddha Lama": "Buddha Lama",
    "Snehashree Thapa": "Snehashree Thapa",
    "Menuka Poudel": "Menuka Poudel",
    "Tara Devi": "Tara Devi"
}

customer_email_map = {
    "ram.thapa@example.com": "ram.thapa@example.com",
    "sita.sherpa@example.com": "sita.sherpa@example.com",
    "hari.sharma@example.com": "hari.sharma@example.com",
    "gita.gurung@example.com": "gita.gurung@example.com",
    "krishna.shrestha@example.com": "krishna.shrestha@example.com",
    "laxmi.tamang@example.com": "laxmi.tamang@example.com",
    "bishnu.adhikari@example.com": "bishnu.adhikari@example.com",
    "saraswati.rai@example.com": "saraswati.rai@example.com",
    "shiva.yadav@example.com": "shiva.yadav@example.com",
    "durga.magar@example.com": "durga.magar@example.com",
    "maya.devi@example.com": "maya.devi@example.com",
    "rajesh.hamal@example.com": "rajesh.hamal@example.com",
    "manisha.koirala@example.com": "manisha.koirala@example.com",
    "sunil.thapa@example.com": "sunil.thapa@example.com",
    "rekha.thapa@example.com": "rekha.thapa@example.com",
    "dayahang.rai@example.com": "dayahang.rai@example.com",
    "saugat.malla@example.com": "saugat.malla@example.com",
    "aryan.sigdel@example.com": "aryan.sigdel@example.com",
    "anmol.kc@example.com": "anmol.kc@example.com",
    "namrata.shrestha@example.com": "namrata.shrestha@example.com",
    "deepak.giri@example.com": "deepak.giri@example.com",
    "paul.shah@example.com": "paul.shah@example.com",
    "barsha.raut@example.com": "barsha.raut@example.com",
    "samragyee.shah@example.com": "samragyee.shah@example.com",
    "pradeep.khadka@example.com": "pradeep.khadka@example.com",
    "aanchal.sharma@example.com": "aanchal.sharma@example.com",
    "buddhi.tamang@example.com": "buddhi.tamang@example.com",
    "wilson.rai@example.com": "wilson.rai@example.com",
    "sandip.chhetri@example.com": "sandip.chhetri@example.com",
    "malvika.subba@example.com": "malvika.subba@example.com",
    "anju.panta@example.com": "anju.panta@example.com",
    "pramod.kharel@example.com": "pramod.kharel@example.com",
    "sugam.pokharel@example.com": "sugam.pokharel@example.com",
    "indira.joshi@example.com": "indira.joshi@example.com",
    "raju.lama@example.com": "raju.lama@example.com",
    "nima.rumba@example.com": "nima.rumba@example.com",
    "adrian.pradhan@example.com": "adrian.pradhan@example.com",
    "amrit.gurung@example.com": "amrit.gurung@example.com",
    "yabesh.thapa@example.com": "yabesh.thapa@example.com",
    "sajjan.vaidya@example.com": "sajjan.vaidya@example.com",
    "bartika.rai@example.com": "bartika.rai@example.com",
    "bipul.chettri@example.com": "bipul.chettri@example.com",
    "sushant.kc@example.com": "sushant.kc@example.com",
    "neetesh.kunwar@example.com": "neetesh.kunwar@example.com",
    "swoopna.suman@example.com": "swoopna.suman@example.com",
    "samir.ghimire@example.com": "samir.ghimire@example.com",
    "girish.khatiwada@example.com": "girish.khatiwada@example.com",
    "yama.buddha@example.com": "yama.buddha@example.com",
    "laure@example.com": "laure@example.com",
    "vten@example.com": "vten@example.com",
    "balen.shah@example.com": "balen.shah@example.com",
    "harka.sampang@example.com": "harka.sampang@example.com",
    "gagan.thapa@example.com": "gagan.thapa@example.com",
    "rabi.lamichhane@example.com": "rabi.lamichhane@example.com",
    "baburam.bhattarai@example.com": "baburam.bhattarai@example.com",
    "pushpa.dahal@example.com": "pushpa.dahal@example.com",
    "kp.oli@example.com": "kp.oli@example.com",
    "sher.deuba@example.com": "sher.deuba@example.com",
    "madhav.nepal@example.com": "madhav.nepal@example.com",
    "jhalanath.khanal@example.com": "jhalanath.khanal@example.com",
    "ram.yadav@example.com": "ram.yadav@example.com",
    "bidya.bhandari@example.com": "bidya.bhandari@example.com",
    "paras.shah@example.com": "paras.shah@example.com",
    "gyanendra.shah@example.com": "gyanendra.shah@example.com",
    "komal.shah@example.com": "komal.shah@example.com",
    "himani.shah@example.com": "himani.shah@example.com",
    "hridayendra.shah@example.com": "hridayendra.shah@example.com",
    "purnima.shrestha@example.com": "purnima.shrestha@example.com",
    "melina.rai@example.com": "melina.rai@example.com",
    "asmita.adhikari@example.com": "asmita.adhikari@example.com",
    "rachana.rimal@example.com": "rachana.rimal@example.com",
    "eleena.chauhan@example.com": "eleena.chauhan@example.com",
    "samikshya.adhikari@example.com": "samikshya.adhikari@example.com",
    "pratap.das@example.com": "pratap.das@example.com",
    "nishan.bhattarai@example.com": "nishan.bhattarai@example.com",
    "ravi.oad@example.com": "ravi.oad@example.com",
    "buddha.lama@example.com": "buddha.lama@example.com",
    "snehashree.thapa@example.com": "snehashree.thapa@example.com",
    "menuka.poudel@example.com": "menuka.poudel@example.com",
    "tara.devi@example.com": "tara.devi@example.com"
}

customer_phone_map = {
    "9841234567": "9841234567",
    "9851234567": "9851234567",
    "9861234567": "9861234567",
    "9801234567": "9801234567",
    "9811234567": "9811234567",
    "9808123456": "9808123456",
    "9849123456": "9849123456",
    "9818123456": "9818123456",
    "9851123456": "9851123456",
    "9861123456": "9861123456",
    "9741234567": "9741234567",
    "9751234567": "9751234567",
    "9761234567": "9761234567",
    "9771234567": "9771234567",
    "9781234567": "9781234567",
    "9791234567": "9791234567",
    "9801234567": "9801234567",
    "9811234567": "9811234567",
    "9821234567": "9821234567",
    "9831234567": "9831234567",
    "9841234567": "9841234567",
    "9851234567": "9851234567",
    "9861234567": "9861234567",
    "9871234567": "9871234567",
    "9881234567": "9881234567",
    "9891234567": "9891234567",
    "9901234567": "9901234567",
    "9911234567": "9911234567",
    "9921234567": "9921234567",
    "9931234567": "9931234567",
    "9941234567": "9941234567",
    "9951234567": "9951234567",
    "9961234567": "9961234567",
    "9971234567": "9971234567",
    "9981234567": "9981234567",
    "9991234567": "9991234567",
    "9999999999": "9999999999"
}

customer_street_map = {
    "New Road": "New Road",
    "Durbar Marg": "Durbar Marg",
    "Lazimpat": "Lazimpat",
    "Thamel": "Thamel",
    "Baneshwor": "Baneshwor",
    "Koteshwor": "Koteshwor",
    "Kalanki": "Kalanki",
    "Chabahil": "Chabahil",
    "Balkhu": "Balkhu",
    "Satdobato": "Satdobato",
    "Boudha": "Boudha",
    "Patan": "Patan",
    "Jawalakhel": "Jawalakhel",
    "Gwarko": "Gwarko",
    "Suryabinayak": "Suryabinayak",
    "Tinkune": "Tinkune",
    "Sinamangal": "Sinamangal",
    "Gaushala": "Gaushala",
    "Maitidevi": "Maitidevi",
    "Dillibazar": "Dillibazar",
    "Tripureshwor": "Tripureshwor",
    "Teku": "Teku",
    "Kalimati": "Kalimati",
    "Soalteemode": "Soalteemode",
    "Tahachal": "Tahachal",
    "Dallu": "Dallu",
    "Swayambhu": "Swayambhu",
    "Balaju": "Balaju",
    "Gongabu": "Gongabu",
    "Samakhusi": "Samakhusi",
    "Maharajgunj": "Maharajgunj",
    "Basundhara": "Basundhara",
    "Sukedhara": "Sukedhara",
    "Jorpati": "Jorpati",
    "Gokarna": "Gokarna",
    "Sankhu": "Sankhu",
    "Kapan": "Kapan",
    "Mandikhatar": "Mandikhatar",
    "Dhumbarahi": "Dhumbarahi",
    "Handigaun": "Handigaun",
    "Naxal": "Naxal",
    "Baluwatar": "Baluwatar",
    "Bhatbhateni": "Bhatbhateni",
    "Tangal": "Tangal",
    "Kamal Pokhari": "Kamal Pokhari",
    "Gyaneshwor": "Gyaneshwor",
    "Ratopul": "Ratopul",
    "Kalopul": "Kalopul",
    "Siphal": "Siphal",
    "Battisputali": "Battisputali",
    "Old Baneshwor": "Old Baneshwor",
    "Buddhanagar": "Buddhanagar",
    "Shankhamul": "Shankhamul",
    "Thapathali": "Thapathali",
    "Kupondole": "Kupondole",
    "Sanepa": "Sanepa",
    "Jhamsikhel": "Jhamsikhel",
    "Pulchowk": "Pulchowk",
    "Manbhawan": "Manbhawan",
    "Kumaripati": "Kumaripati",
    "Lagankhel": "Lagankhel",
    "Mangalbazar": "Mangalbazar",
    "Imadol": "Imadol",
    "Balkumari": "Balkumari",
    "Jadibuti": "Jadibuti",
    "Pepsicola": "Pepsicola",
    "Sanothimi": "Sanothimi",
    "Gatthaghar": "Gatthaghar",
    "Kaushaltar": "Kaushaltar",
    "Lokanthali": "Lokanthali",
    "Airport": "Airport",
    "Tilganga": "Tilganga",
    "Pingalasthan": "Pingalasthan",
    "Mitrapark": "Mitrapark",
    "Maijubahal": "Maijubahal",
    "Guheshwori": "Guheshwori",
    "Kamalbinayak": "Kamalbinayak",
    "Chyamasingh": "Chyamasingh",
    "Jagati": "Jagati",
    "Sallaghari": "Sallaghari",
    "Katunje": "Katunje",
    "Balkot": "Balkot",
    "Sirutar": "Sirutar",
    "Lubhu": "Lubhu",
    "Lamatar": "Lamatar",
    "Godawari": "Godawari",
    "Thaiba": "Thaiba",
    "Badikhel": "Badikhel",
    "Chapagaun": "Chapagaun",
    "Thecho": "Thecho",
    "Bungamati": "Bungamati",
    "Khokana": "Khokana",
    "Chobhar": "Chobhar",
    "Dakshinkali": "Dakshinkali",
    "Pharping": "Pharping",
    "Nayabazar": "Nayabazar",
    "Khusibu": "Khusibu",
    "Sorhakhutte": "Sorhakhutte",
    "Paknajol": "Paknajol",
    "Jyatha": "Jyatha",
    "Kantipath": "Kantipath",
    "Jamal": "Jamal",
    "Asan": "Asan",
    "Indrachowk": "Indrachowk",
    "Basantapur": "Basantapur",
    "Sundhara": "Sundhara",
    "Bhadrakali": "Bhadrakali",
    "Singha Durbar": "Singha Durbar",
    "Anamnagar": "Anamnagar",
    "Ghattekulo": "Ghattekulo",
    "Putalisadak": "Putalisadak",
    "Bagbazar": "Bagbazar",
    "Exhibition Road": "Exhibition Road"
}

customer_city_map = {
    "Kathmandu": "Kathmandu",
    "Lalitpur": "Lalitpur",
    "Bhaktapur": "Bhaktapur",
    "Pokhara": "Pokhara",
    "Biratnagar": "Biratnagar",
    "Dharan": "Dharan",
    "Butwal": "Butwal",
    "Nepalgunj": "Nepalgunj",
    "Hetauda": "Hetauda",
    "Janakpur": "Janakpur",
    "Itahari": "Itahari",
    "Bhairahawa": "Bhairahawa",
    "Mahendranagar": "Mahendranagar",
    "Dhangadhi": "Dhangadhi",
    "Kirtipur": "Kirtipur",
    "Bhaktapur": "Bhaktapur",
    "Patan": "Patan",
    "Jawalakhel": "Jawalakhel",
    "Gwarko": "Gwarko",
    "Suryabinayak": "Suryabinayak",
    "Tinkune": "Tinkune",
    "Sinamangal": "Sinamangal",
    "Gaushala": "Gaushala",
    "Maitidevi": "Maitidevi",
    "Dillibazar": "Dillibazar",
    "Damak": "Damak",
    "Birtamod": "Birtamod",
    "Bhadrapur": "Bhadrapur",
    "Ilam": "Ilam",
    "Dhankuta": "Dhankuta",
    "Inaruwa": "Inaruwa",
    "Rajbiraj": "Rajbiraj",
    "Lahan": "Lahan",
    "Siraha": "Siraha",
    "Jaleshwor": "Jaleshwor",
    "Malangwa": "Malangwa",
    "Gaur": "Gaur",
    "Kalaiya": "Kalaiya",
    "Birgunj": "Birgunj",
    "Bharatpur": "Bharatpur",
    "Narayangarh": "Narayangarh",
    "Ratnanagar": "Ratnanagar",
    "Tandi": "Tandi",
    "Gorkha": "Gorkha",
    "Besisahar": "Besisahar",
    "Damauli": "Damauli",
    "Lekhnath": "Lekhnath",
    "Baglung": "Baglung",
    "Beni": "Beni",
    "Kusma": "Kusma",
    "Syangja": "Syangja",
    "Waling": "Waling",
    "Palpa": "Palpa",
    "Tansen": "Tansen",
    "Kapilvastu": "Kapilvastu",
    "Taulihawa": "Taulihawa",
    "Dang": "Dang",
    "Ghorahi": "Ghorahi",
    "Tulsipur": "Tulsipur",
    "Lamahi": "Lamahi",
    "Pyuthan": "Pyuthan",
    "Rolpa": "Rolpa",
    "Rukum": "Rukum",
    "Salyan": "Salyan",
    "Kohalpur": "Kohalpur",
    "Bardiya": "Bardiya",
    "Gulariya": "Gulariya",
    "Surkhet": "Surkhet",
    "Birendranagar": "Birendranagar",
    "Dailekh": "Dailekh",
    "Jajarkot": "Jajarkot",
    "Jumla": "Jumla",
    "Kalikot": "Kalikot",
    "Mugu": "Mugu",
    "Dolpa": "Dolpa",
    "Humla": "Humla",
    "Attariya": "Attariya",
    "Tikapur": "Tikapur",
    "Dadeldhura": "Dadeldhura",
    "Dipayal": "Dipayal",
    "Silgadhi": "Silgadhi",
    "Baitadi": "Baitadi",
    "Darchula": "Darchula",
    "Panauti": "Panauti",
    "Banepa": "Banepa",
    "Dhulikhel": "Dhulikhel",
    "Panchkhal": "Panchkhal",
    "Melamchi": "Melamchi",
    "Chautara": "Chautara",
    "Bidur": "Bidur",
    "Trishuli": "Trishuli",
    "Dhunibesi": "Dhunibesi",
    "Gajuri": "Gajuri",
    "Malekhu": "Malekhu",
    "Mugling": "Mugling"
}

customer_image_map = {
    "customer_image.png": "customer_image.png"
}


def customer_name():
    return random.choice(list(customer_name_map.keys()))

def get_customer_name(name):
    return customer_name_map.get(name, "Description not found.")

def customer_email():
    return random.choice(list(customer_email_map.keys()))

def get_customer_email(name):
    return customer_email_map.get(name, "Description not found.")

def customer_phone():
    return random.choice(list(customer_phone_map.keys()))

def get_customer_phone(name):
    return customer_phone_map.get(name, "Description not found.")

def customer_street():
    return random.choice(list(customer_street_map.keys()))

def get_customer_street(name):
    return customer_street_map.get(name, "Description not found.")

def customer_city():
    return random.choice(list(customer_city_map.keys()))

def get_customer_city(name):
    return customer_city_map.get(name, "Description not found.")

def customer_image():
    return random.choice(list(customer_image_map.keys()))

def get_customer_image(name):
    return customer_image_map.get(name, "Description not found.")
def random_status():
    return random.choice(["Unsolved Issues", "Solved Issues"])

def get_random_blog_data():
    """
    Returns (title, content, author, image_path, meta_description)
    - title: random product name
    - content: product description
    - author: random customer name
    - image_path: path to product image
    - meta_description: cohesive description based on title and content
    """
    title = product_name()
    content = get_product_description(title)
    author = customer_name()
    
    # Try to find an image for the product
    image_path = None
    for ext in IMAGE_EXTENSIONS:
        temp_path = os.path.join(IMAGES_DIR, f"{title}{ext}")
        if os.path.exists(temp_path):
            image_path = temp_path
            break
            
    # If no specific image, find any fallback image but try to keep it consistent
    if not image_path and os.path.exists(IMAGES_DIR):
        for filename in os.listdir(IMAGES_DIR):
            if any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                image_path = os.path.join(IMAGES_DIR, filename)
                break

    meta_description = None
    if content:
        meta_description = f"Description of {title}: {content[:100]}..."
            
    return title, image_path, content, author, meta_description
    
    
def get_random_start_date():
    nepal_tz = pytz.timezone('Asia/Kathmandu')
    today = datetime.now(nepal_tz)
    # Randomly choose a date between today and 5 days from now
    random_days = random.randint(0, 5)
    start_date = today + timedelta(days=random_days)
    return start_date.strftime("%Y-%m-%d")

def get_random_end_date(start_date_str):
    # Parse the start date string back to a date object
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    # Randomly add 1 to 10 days to the start date
    random_days = random.randint(1, 10)
    end_date = start_date + timedelta(days=random_days)
    return end_date.strftime("%Y-%m-%d")

def get_random_slider_data():
    """
    Returns (title, subtitle, description, image_path, action_link_name, action_link_url)
    """
    title = product_name()
    subtitle = f"Amazing {title} Deals!"
    description = get_product_description(title)
    
    # Try to find an image for the product
    image_path = None
    for ext in IMAGE_EXTENSIONS:
        temp_path = os.path.join(IMAGES_DIR, f"{title}{ext}")
        if os.path.exists(temp_path):
            image_path = temp_path
            break
            
    if not image_path:
        # Fallback to a known image if product image not found
        image_path = os.path.join(IMAGES_DIR, "Electronics.webp")
    
    action_link_name = "Shop Now"
    action_link_url = "https://www.saauzi.com/products"
    
    return title, subtitle, description, image_path, action_link_name, action_link_url

def get_qr_image():
    """Returns the absolute path to the fake_qr.jpg image."""
    return os.path.join(IMAGES_DIR, "fake_qr.jpg")

def organization():
    return store_name()

def get_profile():
    return os.path.join(IMAGES_DIR, "profile.jpg")

def get_logo():
    return os.path.join(IMAGES_DIR, "logo.webp")

def get_favicon():
    return os.path.join(IMAGES_DIR, "favicon.png")


def slogan():
    slogans = [
        "Quality You Can Trust.",
        "Your One-Stop Shop.",
        "New Trends, New You.",
        "Best Deals, Every Day.",
        "Shop the Best, Forget the Rest.",
        "Elegance in Every Purchase.",
        "Experience Better Shopping.",
        "Where Quality Meets Affordability.",
        "Unbox Happiness.",
        "Style Delivered to Your Door.",
        "Smart Shopping for Smart People.",
        "Discover Your Style.",
        "Fast Delivery, Best Quality.",
        "Beyond Your Expectations.",
        "Elevate Your Lifestyle.",
        "Your Satisfaction, Our Passion.",
        "The Future of Shopping is Here.",
        "Big Savings on Big Brands.",
        "Curated Just for You.",
        "Make Every Day Special."
    ]
    return random.choice(slogans)


def vat_number():
    return f.numerify("##########")

def vat_percentage():
    return f.numerify("##")

def address():
    address_input = [
        "Lazimpat, Kathmandu, Nepal",
        "Baneshwor, Kathmandu, Nepal",
        "Thamel, Kathmandu, Nepal",
        "Kalanki, Kathmandu, Nepal",
        "Koteshwor, Kathmandu, Nepal",
        "Boudha, Kathmandu, Nepal",
        "Patan Dhoka, Lalitpur, Nepal",
        "Jawalakhel, Lalitpur, Nepal",
        "Gwarko, Lalitpur, Nepal",
        "Bhaktapur Durbar Square, Bhaktapur, Nepal",
        "Suryabinayak, Bhaktapur, Nepal",
        "Biratnagar Main Road, Morang, Nepal",
        "Itahari Chowk, Sunsari, Nepal",
        "Dharan Bazar, Sunsari, Nepal",
        "Pokhara Lakeside, Kaski, Nepal",
        "Bagar, Pokhara, Kaski, Nepal",
        "Butwal Traffic Chowk, Rupandehi, Nepal",
        "Bhairahawa, Rupandehi, Nepal",
        "Tansen Bazaar, Palpa, Nepal",
        "Janakpur Dham, Dhanusha, Nepal",
        "Hetauda, Makwanpur, Nepal",
        "Narayangarh, Chitwan, Nepal",
        "Bharatpur, Chitwan, Nepal",
        "Damauli, Tanahun, Nepal",
        "Gorkha Bazar, Gorkha, Nepal",
        "Besisahar, Lamjung, Nepal",
        "Baglung Bazar, Baglung, Nepal",
        "Beni, Myagdi, Nepal",
        "Kusma, Parbat, Nepal",
        "Waling, Syangja, Nepal",
        "Nepalgunj, Banke, Nepal",
        "Kohalpur, Banke, Nepal",
        "Ghorahi, Dang, Nepal",
        "Tulsipur, Dang, Nepal",
        "Birendranagar, Surkhet, Nepal",
        "Dhangadhi, Kailali, Nepal",
        "Mahendranagar, Kanchanpur, Nepal",
        "Ilam Bazar, Ilam, Nepal",
        "Birtamod, Jhapa, Nepal",
        "Damak, Jhapa, Nepal",
        "Bhadrapur, Jhapa, Nepal",
        "Lahan, Siraha, Nepal",
        "Rajbiraj, Saptari, Nepal",
        "Kalaiya, Bara, Nepal",
        "Birgunj, Parsa, Nepal",
        "Gaur, Rautahat, Nepal",
        "Malangwa, Sarlahi, Nepal",
        "Jaleshwor, Mahottari, Nepal",
        "Dhulikhel, Kavre, Nepal",
        "Banepa, Kavre, Nepal",
        "Panauti, Kavre, Nepal",
        "Bidur, Nuwakot, Nepal",
        "Dhunibesi, Dhading, Nepal",
        "Malekhu, Dhading, Nepal",
        "Mugling, Chitwan, Nepal",
        "Tikapur, Kailali, Nepal",
        "Attariya, Kailali, Nepal",
        "Dadeldhura Bazar, Dadeldhura, Nepal",
        "Dipayal Silgadhi, Doti, Nepal",
        "Jumla Khalanga, Jumla, Nepal"
    ]
    return random.choice(address_input)

def about_us():
    about_us_list = [
        "We deliver innovative solutions that help businesses grow.",
        "Committed to quality, reliability, and customer success.",
        "Building smart technology for modern businesses.",
        "Your trusted partner for digital transformation.",
        "Driven by innovation, powered by expertise.",
        "Creating simple solutions for complex problems.",
        "We focus on results, efficiency, and excellence.",
        "Empowering businesses through technology.",
        "Reliable solutions designed for real-world needs.",
        "Turning ideas into impactful digital products."
    ]
    return random.choice(about_us_list)

def contact_number():
    return f.numerify("##########")
def alternate_contact_number():
    return f.numerify("##########")
def email():
    return GMAIL_USER
def alternate_email():
    return GMAIL_USER
def whatsapp():
    return f.numerify("##########")
def viber():
    return f.numerify("##########")

def facebook_link():
    return "https://www.facebook.com/"+get_nepal_time_str()
def instagram_link():
    return "https://www.instagram.com/"+get_nepal_time_str()
def twitter_link():
    return "https://twitter.com/"+get_nepal_time_str()
def linkedin_link():
    return "https://www.linkedin.com/"+get_nepal_time_str()
def youtube_link():
    return "https://www.youtube.com/"+get_nepal_time_str()
def tiktok_link():
    return "https://www.tiktok.com/"+get_nepal_time_str()

def return_policy():
    return "https://www.saauzi.com/return-policy"+get_nepal_time_str()
def privacy_policy():
    return "https://www.saauzi.com/privacy-policy"+get_nepal_time_str()
def terms_and_conditions():
    return "https://www.saauzi.com/terms-and-conditions"+get_nepal_time_str()

def full_name_staff():
    return random.choice(list(customer_name_map.keys()))
def email_staff():
    return random.choice(list(customer_email_map.keys()))
def phone_staff():
    return f.numerify("##########")
def address_staff():
    return random.choice(list(customer_street_map.keys()))

promo_heading_list = [
    "Summer Sale",
    "Winter Clearance",
    "Limited Time Offer",
    "Exclusive Discount",
    "New Year Bash",
    "Festival Special",
    "Weekend Deal",
    "Flash Sale",
    "Member Only Discount",
    "BOGO Offer",
    "Grand Opening Sale",
    "Mid-Season Sale",
    "Holiday Specials",
    "Flash Discount",
    "Early Bird Offer",
    "Black Friday Sale",
    "Cyber Monday Deal",
    "Dashain Dhamaka",
    "Tihar Special",
    "Chhath Puja Offer",
    "Valentine's Day Special",
    "Mother's Day Gift",
    "Father's Day Deal",
    "Back to School",
    "End of Season Sale",
    "Monsoon Madness",
    "Spring Collection Launch",
    "Autumn Sale",
    "Anniversary Sale",
    "Clearance Sale",
    "Mega Deal",
    "Super Saver",
    "Hot Deal",
    "Best Price Guarantee",
    "Loyalty Reward",
    "Referral Bonus",
    "First Order Discount",
    "App Exclusive",
    "Midnight Sale",
    "24 Hour Sale",
    "Weekly Bonanza",
    "Monthly Special",
    "Year End Sale",
    "New Arrival Discount",
    "Pre-Order Special",
    "Nepali New Year Offer",
    "Maghe Sankranti Deal",
    "Holi Special Sale",
    "Teej Festival Offer",
    "Raksha Bandhan Special",
    "Constitution Day Discount",
    "Saturday Market Deal",
    "Haat Bazaar Special",
    "Jatra Festival Offer",
    "Wedding Season Sale",
    "Pasni Ceremony Gift",
    "Bratabandha Special",
    "Winter Warmth Sale",
    "Summer Cool Deal",
    "Monsoon Essentials",
    "11.11 Mega Sale",
    "12.12 Year End Sale",
    "Ghode Jatra Special",
    "Indra Jatra Offer",
    "Lhosar Celebration",
    "Udhauli Ubhauli Special",
    "Shree Panchami Deal",
    "Maha Shivaratri Offer",
    "Chaite Dashain Sale",
    "Buddha Jayanti Special",
    "Janai Purnima Offer",
    "Krishna Janmashtami Deal",
    "Rishi Panchami Special",
    "Saraswati Puja Offer",
    "Local Product Fair",
    "Made in Nepal Sale",
    "Himalayan Special",
    "Pahadi Product Deal",
    "Terai Market Offer"
]

def promo_heading():
    return random.choice(promo_heading_list)

def get_random_blog_category_data():
    blog_category_data = {
        "Technology": "Technology is the application of scientific knowledge for practical purposes.",
        "Fashion": "Fashion is a popular style or practice, especially in clothing, footwear, accessories, makeup, hairstyle, and body modification.",
        "Food": "Food is any nutritious substance that people or animals eat or drink or that plants absorb in order to maintain life and growth.",
        "Travel": "Travel is the movement of people from one place to another.",
        "Health": "Health is the state of being free from illness or injury.",
        "Education": "Education is the process of receiving or giving systematic instruction, especially at a school or university.",
        "Entertainment": "Entertainment is the action of providing or being provided with amusement or enjoyment.",
        "Sports": "Sports is an activity involving physical exertion and skill in which an individual or team competes against another or others for entertainment.",
        "Business": "Business is a commercial activity or enterprise.",
        "Lifestyle": "Lifestyle is the way in which a person or group lives."
    }
    title = random.choice(list(blog_category_data.keys()))
    return title, blog_category_data[title]

alphabet = [
    "a","b","c","d","e","f","g","h",
    "i","j","k","l","m","n","o","p",
    "r","s","t","u","v","w"
    ]
def get_random_alphabet():
    return random.choice(alphabet)