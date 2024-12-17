import requests
from bs4 import BeautifulSoup
from termcolor import colored
import platform
import time
import os

# Konsol renk ayarları
def print_colored(text, color="white"):
    print(colored(text, color))

def clear_screen():
    # İşletim sistemini kontrol et
    current_os = platform.system()

    if current_os == "Windows":
        os.system("cls")  # Windows için ekranı temizler
    else:
        os.system("clear")  # Linux/MacOS için ekranı temizler

# Dosyadan dorkları yükleme
def load_dorks_from_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print_colored(f"[-] File not found: {filename}", "red")
        return []

# Google üzerinden dork tarama
def search_dork(dork, page=0):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    start = page * 10
    base_url = f"https://www.google.com/search?q={dork}&start={start}"
    try:
        response = requests.get(base_url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True) if "http" in a['href']]
            return list(set(links))  # Yinelenen linkleri filtrele
        else:
            print_colored(f"[-] Failed to fetch results for: {dork}", "red")
            return []
    except Exception as e:
        print_colored(f"[-] Error fetching results for: {dork}, Error: {e}", "red")
        return []

# Sonuçları dosyaya kaydetme
def save_links(links, filename="results.txt"):
    existing_links = set()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            existing_links = set(file.readlines())
    except FileNotFoundError:
        pass
    
    with open(filename, "a", encoding="utf-8") as file:
        for link in links:
            if link + "\n" not in existing_links:  # Benzersizse ekle
                file.write(link + "\n")
                existing_links.add(link + "\n")

# Banner
def show_banner():
    clear_screen()
    banner = """
    -----------------------------------------
            Advanced Google Dork Scanner
             Developer By Furkan Dinçer
    -----------------------------------------
    """
    print_colored(banner, "cyan")

# Ana menü
def main():
    show_banner()
    print_colored("""
    [1] Dork Taraması
    [0] Çıkış
    """, "yellow")
    
    choice = input(colored("Seçiminizi yapın: ", "blue")).strip()

    if choice == "1":
        print_colored("""
        [1] Örnek Dork Kategorisinden Seç
        [2] Kendi Dorkunu Gir
        [3] Kendi Dork Listenizi Yükleyin
        """, "yellow")
        
        dork_choice = input(colored("Dork seçimini yapın: ", "blue")).strip()

        if dork_choice == "1":
            print_colored("""
            [1] SQL Injection Dorkları
            [2] Admin Panel Dorkları
            [3] Open Directory Dorkları
            [4] File Inclusion Dorkları
            [5] Error Based Dorkları
            """, "yellow")
            
            category_choice = input(colored("Kategori seçiminizi yapın: ", "blue")).strip()
            category_files = {
                "1": "example_dorks/sql_injection_dorks.txt",
                "2": "example_dorks/admin_panel_dorks.txt",
                "3": "example_dorks/open_directory_dorks.txt",
                "4": "example_dorks/file_inclusion_dorks.txt",
                "5": "example_dorks/error_based_dorks.txt"
            }

            if category_choice in category_files:
                dorks = load_dorks_from_file(category_files[category_choice])
            else:
                print_colored("[-] Geçersiz kategori seçimi!", "red")
                return

        elif dork_choice == "2":
            dork = input(colored("Lütfen tek bir dork girin: ", "blue")).strip()
            if "," in dork or " " in dork:
                print_colored("[-] Sadece tek bir dork girmelisiniz!", "red")
                return
            dorks = [dork]

        elif dork_choice == "3":
            file_path = input(colored("Dork listesinin dosya yolunu girin: ", "blue")).strip()
            dorks = load_dorks_from_file(file_path)

        else:
            print_colored("[-] Geçersiz seçim!", "red")
            return

        num_pages = int(input(colored("Kaç sayfa taramak istiyorsunuz? (Örn: 3): ", "blue")).strip())
        all_results = []
        print_colored("[*] Starting dork scan...\n", "cyan")

        for dork in dorks:
            print_colored(f"[+] Searching for: {dork}", "blue")
            for page in range(num_pages):
                print_colored(f"[*] Searching page {page + 1} for: {dork}\n", "yellow")
                links = search_dork(dork, page)
                if links:
                    print_colored(f"[+] {len(links)} links found on page {page + 1}\n", "green")
                    save_links(links)
                    all_results.extend(links)
                else:
                    print_colored(f"[-] No results found on page {page + 1}\n", "red")

        unique_results = list(set(all_results))
        print_colored("\n--- Tarama İstatistikleri ---", "cyan")
        print_colored(f"Toplam Dork Sayısı: {len(dorks)}", "green")
        print_colored(f"Toplam Bulunan Bağlantılar (Yinelenenler Kaldırıldı): {len(unique_results)}", "green")

    elif choice == "0":
        print_colored("[*] Çıkış yapılıyor...", "cyan")
    else:
        print_colored("[-] Geçersiz seçim!", "red")

if __name__ == "__main__":
    main()
