# <div align="center">Russian Government Procurement Scraper</div>

This project is designed to scrape procurement contract data from the Russian government procurement website [zakupki.gov.ru](https://zakupki.gov.ru). It consists of two main scripts, `Parsing-url.py` and `Parsing-tin.py`, which together extract contract URLs and then gather details like TIN, cost, supplier name, and contract date.

## Project Structure

- **Parsing-url.py** - This script scrapes a list of contract URLs based on specific search criteria and saves them in `result2024.json`.
- **Parsing-tin.py** - This script reads the URLs from `result2024.json`, extracts additional details for each contract (TIN, cost, supplier name, date), and saves the results in `tins2024.json`.

## Requirements

- Python 3.6 or higher
- Required packages:
  - `requests`
  - `beautifulsoup4`
  - `tqdm`

You can install the required packages using:
```bash
pip install requests beautifulsoup4 tqdm
```

## Usage

1. **Set Up Proxy and User-Agent**
   - In both scripts, replace `"yours proxy"` in the `PROXY` dictionary and `"yours user agent"` in `HEADERS` with your actual proxy details and user-agent string.

2. **Run Parsing-url.py**
   - This script collects URLs of procurement contracts and saves them in `result2024.json`.
   ```bash
   python parsing_url.py
   ```

3. **Run Parsing-tin.py**
   - This script reads `result2024.json`, visits each contract URL, scrapes additional contract details (TIN, cost, supplier name, date), and saves the final data in `tins2024.json`.
   ```bash
   python parsing_tin.py
   ```

## Files

- **result2024.json** - Contains a list of contract URLs and contract numbers after running `Parsing-url.py`.
- **tins2024.json** - Contains detailed information for each contract after running `Parsing-tin.py`.

## Functions

### Parsing-url.py

- **get_soup(url, proxy, headers)** - Fetches the webpage content and returns a BeautifulSoup object.
- **url_contracts(soup)** - Extracts contract URLs and numbers from the webpage and returns a list of dictionaries.
- **save_to_file_json(data, file_name)** - Saves a Python dictionary to a JSON file.

### Parsing-tin.py

- **connect_json(file_name)** - Loads JSON data from a file.
- **save_to_file_json(data, file_name)** - Saves a Python dictionary to a JSON file.
- **get_soup(url, proxy, headers)** - Fetches the webpage content and returns a BeautifulSoup object.
- **find_cost(soup)** - Extracts the cost of the contract from the page.
- **find_name(soup)** - Extracts the supplier's name.
- **find_tin(soup)** - Extracts the TIN (taxpayer identification number) of the supplier.
- **find_date(soup)** - Extracts the date of the contract.

## Notes

- The script has a built-in delay (`time.sleep(0.5)`) to avoid overloading the server.
- The progress of data extraction is displayed using `tqdm` for a better experience.