import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# Define number generation parameters
START_NUMBER = 3000000000  # First possible number
TOTAL_NUMBERS = 1000000000  # Total possible numbers
PARTS = 20  # Divide into 20 parts

# Change this number to process a different part (1-20)
CURRENT_PART = 1  

NUMBERS_PER_PART = TOTAL_NUMBERS // PARTS  # Numbers per part (50,000,000 per part)

# Calculate start and end numbers for this part
part_start = START_NUMBER + ((CURRENT_PART - 1) * NUMBERS_PER_PART)
part_end = part_start + NUMBERS_PER_PART - 1  # End number for this part

print(f"[INFO] Running Part {CURRENT_PART}/20")
print(f"[INFO] Processing numbers from {part_start} to {part_end}")

# Headers (anonymized for security reasons)
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://dummywebsite.com",  # Dummy URL
    "Referer": "https://dummywebsite.com/search",  # Dummy URL
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("scraped_data.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS phone_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        search_number TEXT,
        result_number INTEGER,
        mobile TEXT,
        name TEXT,
        email TEXT,  -- Column for email
        cnic TEXT,
        address TEXT,
        operator TEXT
    )
""")
conn.commit()

# Function to decode obfuscated email addresses (if applicable)
def decode_email(obfuscated_email):
    """Decodes obfuscated email addresses if found."""
    try:
        r = int(obfuscated_email[:2], 16)  # Extract XOR key from first 2 chars
        decoded_email = "".join(
            chr(int(obfuscated_email[i:i+2], 16) ^ r) for i in range(2, len(obfuscated_email), 2)
        )
        return decoded_email
    except Exception as e:
        print(f"[ERROR] Failed to decode email: {e}")
        return "N/A"

# Process each number in sequence
for search_number in range(part_start, part_end + 1):
    search_number = str(search_number)
    print(f"[INFO] Searching for number: {search_number}")

    # Check if the number is already processed
    cursor.execute("SELECT COUNT(*) FROM phone_data WHERE search_number = ?", (search_number,))
    if cursor.fetchone()[0] > 0:
        print(f"[INFO] Number {search_number} already processed, skipping...")
        continue  # Skip already processed numbers

    # Form request payload
    data = {"cnnum": search_number}

    # Send POST request (Dummy URL used)
    response = requests.post("https://dummywebsite.com/result", data=data, headers=headers)

    # Check response status
    if response.status_code != 200:
        print(f"[ERROR] Failed to retrieve data for {search_number}. Status Code: {response.status_code}")
        continue  # Move to next number

    # Parse HTML response
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract number of records found
    records_found_text = soup.find("h6", class_="text-success text-center")
    num_records = int(records_found_text.text.split("(")[-1].split(")")[0]) if records_found_text else 0
    print(f"[INFO] {num_records} record(s) found for {search_number}")

    if num_records == 0:
        print(f"[WARNING] No data found for {search_number}, moving to next number.")
        continue  # Skip processing and move to next number

    # Extract all records
    result_blocks = soup.find_all("div", class_="container bg-light w-75 my-5 border border-dark")

    for index, result in enumerate(result_blocks[:num_records], start=1):
        data = {"search_number": search_number, "result_number": index}
        print(f"[DEBUG] Processing Result #{index} for {search_number}...")

        # Extract key-value pairs
        labels = result.find_all("div", class_="col-3")
        values = result.find_all("div", class_="col-9")

        if len(labels) != len(values):
            print(f"[WARNING] Mismatch in label-value pairs for {search_number}!")

        for label, value in zip(labels, values):
            field_name = label.text.strip().replace(":", "").lower()
            field_value = value.text.strip()

            if "mobile" in field_name:
                data["mobile"] = field_value
            elif "name" in field_name:
                data["name"] = field_value
            elif "cnic" in field_name:
                data["cnic"] = field_value
            elif "address" in field_name:
                data["address"] = field_value
            elif "operator" in field_name:
                data["operator"] = field_value

            print(f"[DEBUG] Extracted {field_name.capitalize()}: {field_value}")

        # Extract & Decode Email (if exists)
        email_element = result.find(attrs={"data-cfemail": True})
        if email_element:
            obfuscated_email = email_element["data-cfemail"]
            decoded_email = decode_email(obfuscated_email)
            data["email"] = decoded_email
            print(f"[INFO] Decoded Email: {decoded_email}")
        else:
            data["email"] = "N/A"

        # Ensure all fields exist, if not add N/A
        data.setdefault("mobile", "N/A")
        data.setdefault("name", "N/A")
        data.setdefault("cnic", "N/A")
        data.setdefault("address", "N/A")
        data.setdefault("operator", "N/A")
        data.setdefault("email", "N/A")  # Ensure consistency in the database

        # Insert data into SQLite database
        cursor.execute("""
            INSERT INTO phone_data (search_number, result_number, mobile, name, email, cnic, address, operator)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["search_number"], data["result_number"], data["mobile"], 
            data["name"], data["email"], data["cnic"], data["address"], data["operator"]
        ))
        conn.commit()

        print(f"[DEBUG] Final Extracted Data for {search_number} - Result #{index}: {data}")

    # Wait before next request to avoid rate limits
    time.sleep(2)

print(f"[INFO] Data saved in SQLite database: 'scraped_data.db'")

# Close database connection
conn.close()
