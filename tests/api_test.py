import requests
import xml.dom.minidom
import sys
import os
import argparse
from colorama import init, Fore, Style

# Colorama'yı başlat
init()

# API URL'lerini tanımla
BASE_URL = "http://localhost:5000"
API_V1_URL = f"{BASE_URL}/api/v1"
API_V2_URL = f"{BASE_URL}/api/v2"
TRANSFORM_URL = f"{API_V1_URL}/transform"

# XML header'ı tanımla
XML_CONTENT_TYPE = {"Content-Type": "application/xml", "Accept": "application/xml"}

# Token'ı sakla
auth_token = None

def print_formatted_xml(xml_string):
    """XML'i güzel bir şekilde format et ve renklendir"""
    try:
        dom = xml.dom.minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml()
        
        # XML yapısını renklendir
        lines = pretty_xml.split('\n')
        for line in lines:
            if '<?' in line:
                print(Fore.CYAN + line + Style.RESET_ALL)
            elif '</' in line:
                print(Fore.YELLOW + line + Style.RESET_ALL)
            elif '<' in line:
                print(Fore.GREEN + line + Style.RESET_ALL)
            else:
                print(line)
    except Exception as e:
        print(f"XML format hatası: {e}")
        print(xml_string)

def print_response(response, test_name):
    """API yanıtını güzel bir şekilde göster"""
    if response is None:
        print(f"{Fore.RED}Response object is None for {test_name}{Style.RESET_ALL}")
        return
        
    print(f"\n{Fore.GREEN}=== {test_name} - Status Code: {response.status_code} ==={Style.RESET_ALL}")
    
    if 'Content-Type' in response.headers:
        print(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.headers.get('Content-Type') == 'application/xml':
        print("Response XML:")
        print_formatted_xml(response.text)
    else:
        print("Response Body:")
        print(response.text[:500] + "..." if len(response.text) > 500 else response.text)

def get_token_from_response(login_response):
    """Login yanıtından token'ı çıkarır"""
    try:
        dom = xml.dom.minidom.parseString(login_response.text)
        token_elements = dom.getElementsByTagName('token')
        
        if token_elements and token_elements[0].childNodes:
            return token_elements[0].childNodes[0].nodeValue
        else:
            print(f"{Fore.RED}Token bulunamadı!{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}Token çıkarma hatası: {e}{Style.RESET_ALL}")
        return None

def test_login(username="admin", password="admin123"):
    """API v1: Login test et, başarılıysa token döndür"""
    print(f"\n{Fore.BLUE}========= API v1: Login ========={Style.RESET_ALL}")
    
    login_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<login>
    <username>{username}</username>
    <password>{password}</password>
</login>"""
    
    print(f"\nGönderilen istek: POST {API_V1_URL}/login")
    print(f"İstek XML:\n{login_xml}\n")
    
    try:
        response = requests.post(
            f"{API_V1_URL}/login", 
            data=login_xml, 
            headers=XML_CONTENT_TYPE
        )
        
        print(f"Durum Kodu: {response.status_code}")
        print("Yanıt XML:")
        print_formatted_xml(response.text)
        
        # Başarı durumunda token çıkar
        global auth_token
        if response.status_code == 200:
            try:
                dom = xml.dom.minidom.parseString(response.text)
                token_element = dom.getElementsByTagName("token")
                if token_element and token_element[0].childNodes:
                    auth_token = token_element[0].childNodes[0].nodeValue
                    print(f"\n{Fore.GREEN}Token alındı: {auth_token[:20]}...{Style.RESET_ALL}")
                    return auth_token
            except Exception as e:
                print(f"{Fore.RED}Token çıkarma hatası: {e}{Style.RESET_ALL}")
        
        return None
    
    except Exception as e:
        print(f"{Fore.RED}İstek hatası: {e}{Style.RESET_ALL}")
        return None

def test_books_list():
    """API v1: Kitap listesini test et"""
    print(f"\n{Fore.BLUE}========= API v1: Kitapları Listele ========={Style.RESET_ALL}")
    
    if not auth_token:
        print(f"{Fore.RED}Token yok. Önce login işlemi gerçekleştirin.{Style.RESET_ALL}")
        return
    
    headers = {
        "Accept": "application/xml",
        "Authorization": f"Bearer {auth_token}"
    }
    
    print(f"\nGönderilen istek: GET {API_V1_URL}/books")
    print(f"Headers: Authorization: Bearer {auth_token[:20]}...")
    
    try:
        response = requests.get(f"{API_V1_URL}/books", headers=headers)
        
        print(f"Durum Kodu: {response.status_code}")
        print("Yanıt XML:")
        print_formatted_xml(response.text)
    
    except Exception as e:
        print(f"{Fore.RED}İstek hatası: {e}{Style.RESET_ALL}")

def test_endpoints():
    """API v1: Endpoints'leri test et"""
    print(f"\n{Fore.BLUE}========= API v1: Endpoints ========={Style.RESET_ALL}")
    
    print(f"\nGönderilen istek: GET {API_V1_URL}/endpoints")
    
    try:
        response = requests.get(f"{API_V1_URL}/endpoints", headers={"Accept": "application/xml"})
        
        print(f"Durum Kodu: {response.status_code}")
        print("Yanıt XML:")
        print_formatted_xml(response.text)
    
    except Exception as e:
        print(f"{Fore.RED}İstek hatası: {e}{Style.RESET_ALL}")

def test_api_v2_info():
    """API v2: Info endpoint'ini test et"""
    print(f"\n{Fore.BLUE}========= API v2: Info ========={Style.RESET_ALL}")
    
    print(f"\nGönderilen istek: GET {API_V2_URL}/info")
    
    try:
        response = requests.get(f"{API_V2_URL}/info", headers={"Accept": "application/xml"})
        
        print(f"Durum Kodu: {response.status_code}")
        print("Yanıt XML:")
        print_formatted_xml(response.text)
    
    except Exception as e:
        print(f"{Fore.RED}İstek hatası: {e}{Style.RESET_ALL}")

def test_add_book():
    """API v1: Kitap eklemeyi test et (Admin yetkisi gerektirir)"""
    print(f"\n{Fore.BLUE}========= API v1: Kitap Ekle ========={Style.RESET_ALL}")
    
    if not auth_token:
        print(f"{Fore.RED}Token yok. Önce login işlemi gerçekleştirin.{Style.RESET_ALL}")
        return
    
    add_book_xml = """<?xml version="1.0" encoding="UTF-8"?>
<book>
    <title>Test Kitabı</title>
    <author>Test Yazarı</author>
    <year>2025</year>
    <isbn>123-456-7890</isbn>
    <publisher>Test Yayınevi</publisher>
    <category>Test</category>
    <description>Bu bir test kitabıdır.</description>
</book>"""
    
    headers = {
        "Content-Type": "application/xml",
        "Accept": "application/xml",
        "Authorization": f"Bearer {auth_token}"
    }
    
    print(f"\nGönderilen istek: POST {API_V1_URL}/books")
    print(f"Headers: Authorization: Bearer {auth_token[:20]}...")
    print(f"İstek XML:\n{add_book_xml}\n")
    
    try:
        response = requests.post(
            f"{API_V1_URL}/books", 
            data=add_book_xml, 
            headers=headers
        )
        
        print(f"Durum Kodu: {response.status_code}")
        print("Yanıt XML:")
        print_formatted_xml(response.text)
    
    except Exception as e:
        print(f"{Fore.RED}İstek hatası: {e}{Style.RESET_ALL}")

def test_weather():
    """API v1: Hava durumunu test et (Öğrenci veya Admin yetkisi gerektirir)"""
    print(f"\n{Fore.BLUE}========= API v1: Hava Durumu ========={Style.RESET_ALL}")
    
    if not auth_token:
        print(f"{Fore.RED}Token yok. Önce login işlemi gerçekleştirin.{Style.RESET_ALL}")
        return
    
    headers = {
        "Accept": "application/xml",
        "Authorization": f"Bearer {auth_token}"
    }
    
    print(f"\nGönderilen istek: GET {API_V1_URL}/weather")
    print(f"Headers: Authorization: Bearer {auth_token[:20]}...")
    
    try:
        response = requests.get(f"{API_V1_URL}/weather", headers=headers)
        
        print(f"Durum Kodu: {response.status_code}")
        print("Yanıt XML:")
        print_formatted_xml(response.text)
    
    except Exception as e:
        print(f"{Fore.RED}İstek hatası: {e}{Style.RESET_ALL}")

def test_xpath_transform():
    """API v1: XML XPath dönüşümünü test et"""
    print(f"\n{Fore.BLUE}========= API v1: XPath Transformation ========={Style.RESET_ALL}")
    
    # Önce login yaparak token al
    global auth_token
    token = auth_token
    
    # Eğer token yoksa login yap
    if not token:
        token = test_login()
        
    if not token:
        print(f"{Fore.RED}Login failed, cannot continue with XPath test{Style.RESET_ALL}")
        return
    
    headers = {
        "Content-Type": "application/xml",
        "Accept": "application/xml",
        "Authorization": f"Bearer {token}"
    }
    
    # XPath test verisi
    xpath_xml = """<?xml version="1.0" encoding="UTF-8"?>
<request>
    <xpath>//book/title/text()</xpath>
    <content>
        <library>
            <books>
                <book id="1">
                    <title>To Kill a Mockingbird</title>
                    <author>Harper Lee</author>
                    <year>1960</year>
                </book>
                <book id="2">
                    <title>1984</title>
                    <author>George Orwell</author>
                    <year>1949</year>
                </book>
            </books>
        </library>
    </content>
</request>"""
    
    try:
        response = requests.post(
            f"{TRANSFORM_URL}/xpath",
            data=xpath_xml,
            headers=headers
        )
        
        print_response(response, "XPath Transformation Test")
        return response
    except Exception as e:
        print(f"{Fore.RED}XPath transformation error: {e}{Style.RESET_ALL}")
        return None

def test_xslt_transform():
    """API v1: XML XSLT dönüşümünü test et"""
    print(f"\n{Fore.BLUE}========= API v1: XSLT Transformation ========={Style.RESET_ALL}")
    
    # Önce login yaparak token al
    global auth_token
    token = auth_token
    
    # Eğer token yoksa login yap
    if not token:
        token = test_login()
        
    if not token:
        print(f"{Fore.RED}Login failed, cannot continue with XSLT test{Style.RESET_ALL}")
        return
    
    headers = {
        "Content-Type": "application/xml",
        "Accept": "application/xml, text/html",
        "Authorization": f"Bearer {token}"
    }
    
    # XSLT test verisi
    xslt_xml = """<?xml version="1.0" encoding="UTF-8"?>
<request>
    <stylesheet-type>html</stylesheet-type>
    <content>
        <library>
            <books>
                <book id="1">
                    <title>To Kill a Mockingbird</title>
                    <author>Harper Lee</author>
                    <year>1960</year>
                    <isbn>978-0446310789</isbn>
                    <publisher>Grand Central Publishing</publisher>
                    <category>Fiction</category>
                    <description>A novel about racial inequality.</description>
                </book>
                <book id="2">
                    <title>1984</title>
                    <author>George Orwell</author>
                    <year>1949</year>
                    <isbn>978-0451524935</isbn>
                    <publisher>Signet Classic</publisher>
                    <category>Dystopian</category>
                    <description>A dystopian novel.</description>
                </book>
            </books>
        </library>
    </content>
</request>"""
    
    try:
        response = requests.post(
            f"{TRANSFORM_URL}/xslt",
            data=xslt_xml,
            headers=headers
        )
        
        if response.headers.get('Content-Type') == 'text/html':
            # HTML yanıtını düzgün göstermek için
            print(f"\n{Fore.GREEN}XSLT HTML Transformation - Success (Content-Type: {response.headers.get('Content-Type')}){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Response contains HTML content (first 300 chars):{Style.RESET_ALL}")
            print(response.text[:300] + "...")
        else:
            print_response(response, "XSLT Transformation Test")
        return response
    except Exception as e:
        print(f"{Fore.RED}XSLT transformation error: {e}{Style.RESET_ALL}")
        return None

def test_transform_examples():
    """API v1: XML dönüşüm örneklerini listele"""
    print(f"\n{Fore.BLUE}========= API v1: Transformation Examples ========={Style.RESET_ALL}")
    
    try:
        response = requests.get(f"{TRANSFORM_URL}/examples")
        print_response(response, "Transformation Examples Test")
        return response
    except Exception as e:
        print(f"{Fore.RED}Transformation examples error: {e}{Style.RESET_ALL}")
        return None

def run_all_tests():
    """Tüm testleri sırayla çalıştır."""
    print(f"\n{Fore.BLUE}========= Tüm Testler Çalıştırılıyor ========={Style.RESET_ALL}")
    
    # 1. Login testi
    login_response = test_login()
    if login_response is None:
        print(f"{Fore.RED}Login testi başarısız. Testler durduruldu.{Style.RESET_ALL}")
        return
    
    # 2. Endpoints listesini test et
    test_endpoints()
    
    # 3. Kitapları listele
    test_books_list()
    
    # 4. Kitap ekle (Admin yetkisi gerektirir)
    test_add_book()
    
    # 5. Hava durumunu test et
    test_weather()
    
    # 6. API v2 info endpoint'ini test et
    test_api_v2_info()
    
    # 7. XML Dönüşüm testleri
    print(f"\n{Fore.BLUE}========= XML Dönüşüm Testleri ========={Style.RESET_ALL}")
    
    # 7.1. XPath dönüşüm testi
    test_xpath_transform()
    
    # 7.2. XSLT dönüşüm testi
    test_xslt_transform()
    
    # 7.3. Dönüşüm örnekleri
    test_transform_examples()
    
    print(f"\n{Fore.GREEN}Tüm testler tamamlandı.{Style.RESET_ALL}")

def main():
    # Komut satırı argümanlarını parse et
    parser = argparse.ArgumentParser(description="API Test Aracı")
    
    parser.add_argument("--test", choices=[
        "all", "login", "books", "endpoints", 
        "add-book", "weather", "api-v2-info",
        "xpath", "xslt", "transform-examples"
    ],
                        help="Çalıştırılacak test", default="all")
    parser.add_argument("--username", help="Giriş için kullanıcı adı", default="admin")
    parser.add_argument("--password", help="Giriş için şifre", default="admin123")
    
    args = parser.parse_args()
    
    # Sunucu çalışıyor mu kontrol et
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print(f"{Fore.RED}Sunucu çalışıyor ancak health endpoint'i 200 dönmüyor.{Style.RESET_ALL}")
            return
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}Sunucuya bağlanılamıyor. Backend'in çalıştığından emin olun.{Style.RESET_ALL}")
        print(f"URL: {BASE_URL}")
        return
    
    print(f"{Fore.GREEN}Sunucu çalışıyor. Testler başlatılıyor...{Style.RESET_ALL}")
    
    # Seçilen testi çalıştır
    if args.test == "all":
        run_all_tests()
    elif args.test == "login":
        test_login(args.username, args.password)
    elif args.test == "books":
        if test_login(args.username, args.password):
            test_books_list()
    elif args.test == "endpoints":
        test_endpoints()
    elif args.test == "add-book":
        if test_login(args.username, args.password):
            test_add_book()
    elif args.test == "weather":
        if test_login(args.username, args.password):
            test_weather()
    elif args.test == "api-v2-info":
        test_api_v2_info()
    elif args.test == "xpath":
        test_xpath_transform()
    elif args.test == "xslt":
        test_xslt_transform()
    elif args.test == "transform-examples":
        test_transform_examples()

if __name__ == "__main__":
    main()
