# Project: Web Scraper for Phone Data Extraction

## Introduction
This project is a Python-based web scraper designed to extract phone-related data from a target website using the `requests` library for HTTP requests and `BeautifulSoup` for HTML parsing. The extracted data is systematically stored in an SQLite database for further use and analysis. The scraper efficiently handles multiple data points such as mobile numbers, names, email addresses, CNICs, addresses, and operators. 

This scraper is designed to process a large dataset efficiently by dividing the number range into 20 different parts, ensuring smooth execution and avoiding excessive server requests that might lead to blocking.

---

## Features
### ✅ Automated Scraping
- Extracts mobile-related data from a specific website.
- Processes a wide range of numbers efficiently by splitting them into manageable parts.
- Avoids redundant requests by checking the database before querying a new number.

### ✅ Cloudflare Email Decoding
- Extracts and decodes Cloudflare-protected email addresses using XOR-based decryption.
- Ensures that email addresses are stored in a human-readable format.

### ✅ SQLite Database Storage
- Stores extracted data in an SQLite database (`scraped_data.db`).
- Prevents duplicate entries and allows easy querying for later analysis.

### ✅ Error Handling & Logging
- Skips numbers that have already been processed.
- Logs errors when a request fails or when unexpected data formatting is encountered.
- Implements retry mechanisms for better reliability.

### ✅ Rate Limiting
- Introduces a `time.sleep(2)` delay between requests to avoid triggering website defenses against automated scraping.

---

## Installation
### Prerequisites
To run this scraper, you need to have Python installed on your system. You can install the required dependencies using:

```sh
pip install requests beautifulsoup4 sqlite3
```

Ensure you have an appropriate Python version (3.6 or newer recommended) installed before proceeding.

### Downloading the Script
You can download or clone this project using:
```sh
git clone https://github.com/example/scraper-project.git
cd scraper-project
```

---

## Usage
### Configuring the Script
Before running the script, you need to specify which part of the dataset to process. The script divides the total number range into 20 parts. Modify the following variable inside the script:

```python
CURRENT_PART = 1  # Set this to process a different part (1-20)
```

### Running the Scraper
After configuring the script, run it using the following command:

```sh
python scraper.py
```

The script will begin processing numbers from the specified range and storing results in the database.

### Viewing Extracted Data
After running the script, you can inspect the extracted data using SQLite commands:
```sh
sqlite3 scraped_data.db
SELECT * FROM phone_data LIMIT 10;
```

---

## Database Schema
The extracted data is stored in an SQLite database (`scraped_data.db`) within a table called `phone_data`. Below is the schema for the database:

| Column         | Type    | Description                                    |
|---------------|--------|------------------------------------------------|
| id            | INTEGER | Auto-incremented primary key                  |
| search_number | TEXT    | The searched phone number                     |
| result_number | INTEGER | Result index if multiple results are found    |
| mobile        | TEXT    | Extracted mobile number                       |
| name          | TEXT    | Extracted name                                |
| email         | TEXT    | Extracted or decoded email address            |
| cnic          | TEXT    | Extracted CNIC number                         |
| address       | TEXT    | Extracted address                             |
| operator      | TEXT    | Extracted mobile operator                     |

The `search_number` column ensures that we can track which numbers have been processed, while the `result_number` helps distinguish multiple results for a single search.

---

## How the Scraper Works
### Step 1: Generate Number Range
The script starts by defining the range of numbers to be processed. The total possible numbers are divided into 20 parts, and the `CURRENT_PART` variable determines which segment is processed during execution.

### Step 2: Sending HTTP Requests
For each number, the script sends a `POST` request to the target website’s search endpoint using predefined headers. The headers mimic a real web browser to avoid detection.

### Step 3: Parsing the Response
Upon receiving the response, the script uses `BeautifulSoup` to parse the HTML content and extract relevant data fields. If an email address is protected by Cloudflare obfuscation, it is decrypted using an XOR-based decoding method.

### Step 4: Storing Data in the Database
The extracted data is then inserted into an SQLite database. Before inserting, the script checks whether the number has already been processed to prevent duplicate entries.

### Step 5: Rate Limiting
To prevent server detection and blocking, the script introduces a 2-second delay between each request using `time.sleep(2)`. This reduces the risk of being flagged as an automated bot.

---

## Handling Errors and Debugging
The script includes multiple error-handling mechanisms to ensure smooth execution:

### ✅ Connection Errors
If the target website is unavailable or the connection fails, the script logs an error and moves to the next number.

### ✅ Data Extraction Issues
If an expected data field is missing, the script logs a warning and continues processing other data.

### ✅ Cloudflare Email Decoding Errors
If the Cloudflare-protected email cannot be decoded, the script logs an error message and stores `N/A` instead of the email.

---

## Legal & Ethical Considerations
### ⚠️ Important Disclaimer
**This project is strictly for educational and research purposes only.**

1. **Respect the Target Website's Terms of Service**
   - Unauthorized web scraping may violate the website’s terms of use. Ensure you have permission before scraping data.

2. **Compliance with Data Protection Laws**
   - If scraping personal data, you must comply with applicable laws such as the **GDPR (General Data Protection Regulation)** or **CCPA (California Consumer Privacy Act)**.
   - Collecting personal data without consent is illegal in many jurisdictions.

3. **Usage Responsibility**
   - The author of this project does not condone unethical data scraping practices.
   - If you choose to use this script, you are responsible for ensuring compliance with local laws and regulations.

4. **Avoid Overloading the Server**
   - Sending too many requests in a short period can overload the server and potentially get your IP blocked. Always use appropriate rate-limiting techniques.

By using this script, you acknowledge that you are solely responsible for any consequences resulting from its use.

---

## License
This project is distributed under the **MIT License**. You are free to use, modify, and distribute the code under this license. However, please ensure that you use it responsibly and ethically.

For more information, refer to the `LICENSE` file included in the repository.

---

## Final Notes
This web scraper is designed to efficiently extract structured data while maintaining ethical web scraping practices. If you plan to modify this script, ensure that you follow proper guidelines and respect the rights of the data owners. If you have any questions or need further enhancements, feel free to contribute to the project.

