import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# 1. Fungsi untuk membuat file CSV jika belum ada
def create_csv_file(file_name):
    try:
        with open(file_name, mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["date", "currency_pair", "exchange_rate"])
            print(f"File {file_name} berhasil dibuat.")
    except FileExistsError:
        print(f"File {file_name} sudah ada, data akan ditambahkan.")

# 2. Fungsi untuk scrape data exchange rate
def get_exchange_rate_api():
    api_url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(api_url)
    data = response.json()
    if response.status_code == 200 and "IDR" in data["rates"]:
        return data["rates"]["IDR"]
    else:
        raise Exception("Error fetching exchange rate data.")

# 3. Fungsi untuk menyimpan data ke CSV
def save_exchange_rate_to_csv(file_name, currency_pair, exchange_rate):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        current_time = datetime.now()
        writer.writerow([current_time, currency_pair, exchange_rate])

# 4. Main Function
if __name__ == "__main__":
    file_name = "exchange_rates.csv"
    create_csv_file(file_name)

    try:
        currency_pair = "USD/IDR"
        exchange_rate = get_exchange_rate_api()
        print(f"Exchange rate {currency_pair}: {exchange_rate}")

        save_exchange_rate_to_csv(file_name, currency_pair, exchange_rate)
        print(f"Data berhasil disimpan ke {file_name}.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")