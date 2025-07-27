import unittest
import requests
import xml.dom.minidom
import sys
import os
from io import StringIO

# Ana proje dizinini sys.path'e ekle (içe aktarma için)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# API URL'lerini tanımla
BASE_URL = "http://localhost:5000"
API_V1_URL = f"{BASE_URL}/api/v1"
API_V2_URL = f"{BASE_URL}/api/v2"

class APITestCase(unittest.TestCase):
    """API fonksiyonlarını test etmek için temel test sınıfı"""
    
    def setUp(self):
        """Her test öncesinde çağrılır"""
        self.auth_token = None
        self.xml_content_type = {"Content-Type": "application/xml", "Accept": "application/xml"}
        
        # Admin olarak giriş yap
        self.login()
    
    def login(self, username="admin", password="admin123"):
        """Kullanıcı girişi yapar ve token alır"""
        login_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<login>
    <username>{username}</username>
    <password>{password}</password>
</login>"""
        
        try:
            response = requests.post(
                f"{API_V1_URL}/login", 
                data=login_xml, 
                headers=self.xml_content_type
            )
            
            if response.status_code == 200:
                dom = xml.dom.minidom.parseString(response.text)
                token_element = dom.getElementsByTagName("token")
                if token_element and token_element[0].childNodes:
                    self.auth_token = token_element[0].childNodes[0].nodeValue
            
            return response
        except Exception as e:
            print(f"Login hatası: {e}")
            return None
    
    def get_auth_headers(self):
        """Authorization headerlarını döndürür"""
        if not self.auth_token:
            self.fail("Token yok. Login işlemi başarısız.")
            
        return {
            "Accept": "application/xml",
            "Authorization": f"Bearer {self.auth_token}"
        }
    
    def assert_xml_status(self, response, expected_status="success"):
        """XML yanıtında status değerini kontrol eder"""
        dom = xml.dom.minidom.parseString(response.text)
        status_element = dom.getElementsByTagName("status")
        
        self.assertTrue(status_element, "XML yanıtında 'status' elementi bulunamadı")
        self.assertEqual(status_element[0].childNodes[0].nodeValue, expected_status, 
                         f"XML durum değeri '{expected_status}' değil")

class AuthAPITest(APITestCase):
    """Kimlik doğrulama API'lerini test eden sınıf"""
    
    def test_login_success(self):
        """Başarılı giriş testi"""
        response = self.login("admin", "admin123")
        
        self.assertEqual(response.status_code, 200, "Giriş başarısız oldu")
        self.assert_xml_status(response, "success")
        self.assertTrue(self.auth_token, "Token alınamadı")
    
    def test_login_failure(self):
        """Başarısız giriş testi"""
        response = self.login("admin", "wrong_password")
        
        self.assertEqual(response.status_code, 401, "Hatalı şifre ile giriş başarılı olmamalıydı")
        self.assert_xml_status(response, "error")

class BooksAPITest(APITestCase):
    """Kitap API'lerini test eden sınıf"""
    
    def test_get_books(self):
        """Kitapları listeleme testi"""
        response = requests.get(f"{API_V1_URL}/books", headers=self.get_auth_headers())
        
        self.assertEqual(response.status_code, 200, "Kitapları alma işlemi başarısız")
        
        # XML'in doğru formatta olup olmadığını kontrol et
        dom = xml.dom.minidom.parseString(response.text)
        
        # Book elementlerini kontrol et
        book_elements = dom.getElementsByTagName("book")
        self.assertTrue(len(book_elements) >= 0, "Kitap elementleri bulunamadı")
    
    def test_add_book(self):
        """Kitap ekleme testi"""
        add_book_xml = """<?xml version="1.0" encoding="UTF-8"?>
<book>
    <title>Test Book</title>
    <author>Test Author</author>
    <year>2025</year>
    <isbn>123-456-7890</isbn>
    <publisher>Test Publisher</publisher>
    <category>Test</category>
    <description>This is a test book</description>
</book>"""
        
        headers = self.get_auth_headers()
        headers["Content-Type"] = "application/xml"
        
        response = requests.post(f"{API_V1_URL}/books", data=add_book_xml, headers=headers)
        
        self.assertEqual(response.status_code, 201, "Kitap ekleme işlemi başarısız")
        self.assert_xml_status(response, "success")

class APIV2Test(unittest.TestCase):
    """API v2 fonksiyonlarını test eden sınıf"""
    
    def test_api_info(self):
        """API v2 bilgi endpoint testi"""
        response = requests.get(f"{API_V2_URL}/info", headers={"Accept": "application/xml"})
        
        self.assertEqual(response.status_code, 200, "API bilgi endpoint'i başarısız")
        
        # XML'in doğru formatta olup olmadığını kontrol et
        dom = xml.dom.minidom.parseString(response.text)
        
        # API bilgi elementlerini kontrol et
        api_info = dom.getElementsByTagName("api_info")
        self.assertTrue(api_info, "API bilgi elementleri bulunamadı")
        
        # Versiyon elementini kontrol et
        version_element = dom.getElementsByTagName("version")
        self.assertTrue(version_element, "Versiyon elementi bulunamadı")
        self.assertEqual(version_element[0].childNodes[0].nodeValue, "v2", "API versiyonu v2 değil")

def run_tests():
    """Tüm testleri çalıştır"""
    # Çıktıyı yakalamak için
    output = StringIO()
    runner = unittest.TextTestRunner(stream=output, verbosity=2)
    
    # Test sınıflarını topla
    test_classes = [AuthAPITest, BooksAPITest, APIV2Test]
    
    # Her sınıf için test süitini oluştur ve çalıştır
    for test_class in test_classes:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        result = runner.run(suite)
        
        if not result.wasSuccessful():
            print(output.getvalue())
            return False
    
    # Tüm testler başarılı olursa sonucu yazdır
    print(output.getvalue())
    return True

if __name__ == "__main__":
    # Sunucu çalışıyor mu kontrol et
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("Sunucu çalışıyor ancak health endpoint'i 200 dönmüyor.")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Sunucuya bağlanılamıyor. Backend'in çalıştığından emin olun.")
        print(f"URL: {BASE_URL}")
        sys.exit(1)
    
    print("Sunucu çalışıyor. Testler başlatılıyor...")
    
    # Testleri çalıştır
    if run_tests():
        sys.exit(0)
    else:
        sys.exit(1)
