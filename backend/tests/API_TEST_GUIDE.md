# API Test Rehberi

Bu rehber, XML tabanlı API'lerinizi test etmek için oluşturulan araçların nasıl kullanılacağını açıklıyor. Bu araçlarla API fonksiyonlarınızı backend tarafında test edebilirsiniz.

## Test Araçları

Bu klasörde üç farklı test aracı bulunmaktadır:

1. **api_test.py**: Komut satırından hızlı testler yapmak için interaktif script
2. **test_api_unittest.py**: Python unittest çerçevesini kullanan kapsamlı test sınıfları
3. **postman_collection.json**: Postman ile test etmek için hazır koleksiyon

## 1. Hızlı Test Aracı (api_test.py)

Bu betik, tüm API fonksiyonlarını hızlıca test etmek için kullanılabilir. XML istekleri gönderir ve yanıtları renkli bir şekilde konsola yazdırır.

### Kurulum

```bash
pip install requests colorama
```

### Kullanım

Tüm API fonksiyonlarını test etmek için:

```bash
python api_test.py
```

Belirli bir API fonksiyonunu test etmek için:

```bash
python api_test.py --test login
python api_test.py --test books
python api_test.py --test endpoints
python api_test.py --test add-book
python api_test.py --test weather
python api_test.py --test api-v2-info
```

Farklı kullanıcı bilgileriyle test etmek için:

```bash
python api_test.py --username student --password student123
```

## 2. Unittest Test Sınıfları (test_api_unittest.py)

Bu betik, daha kapsamlı ve otomatik testler için unittest çerçevesini kullanır. Ayrıca sonuçları assertion'larla doğrular.

### Kullanım

```bash
python test_api_unittest.py
```

### Test Sınıfları

- **AuthAPITest**: Giriş ve kimlik doğrulama testleri
- **BooksAPITest**: Kitapları listeleme ve ekleme testleri
- **APIV2Test**: API v2 fonksiyonlarını test eder

Yeni test senaryoları eklemek için ilgili sınıfa yeni test metodları ekleyebilirsiniz.

## 3. Postman Koleksiyonu (postman_collection.json)

Bu JSON dosyası, API'lerinizi test etmek için Postman'e içe aktarabileceğiniz bir koleksiyon içerir.

### Kullanım

1. Postman'i açın
2. "Import" butonuna tıklayın
3. `postman_collection.json` dosyasını seçin
4. API v1 ve API v2 isteklerini içeren koleksiyon içe aktarılacaktır
5. Login isteğini gönderin ve dönen tokeni kopyalayın
6. "{{token}}" değişkenini kopyaladığınız token ile güncelleyin veya bir environment değişkeni olarak tanımlayın

## Test Etme İpuçları

1. **Backend'i Çalıştırma**: Testleri çalıştırmadan önce backend'inizin çalıştığından emin olun:
   ```bash
   cd backend
   python run.py
   ```

2. **Token Kullanımı**: API v1 fonksiyonlarının çoğu için JWT token gerekiyor. Test betikleri otomatik olarak login yapıp token alacaktır.

3. **Yetki Kontrolü**: Bazı endpoint'ler (örn. kitap ekleme) admin yetkisi gerektirirken, bazıları (örn. kitapları listeleme) öğrenci yetkisi ile de çalışır.

4. **XML Doğrulama**: Test betikleri, XML yanıtlarını ayrıştırır ve temel doğrulama yapar. Ancak karmaşık XML şemalarını doğrulamak için ek kodlar gerekebilir.

5. **API v2**: API v2 testleri, sadece `/api/v2/info` endpoint'ini test eder. Yeni endpoint'ler eklerseniz, test betiklerini de güncellemeyi unutmayın.

## Sorun Giderme

1. **Bağlantı Hatası**: "Sunucuya bağlanılamıyor" hatası alırsanız, backend'in çalıştığından ve 5000 portunu dinlediğinden emin olun.

2. **Token Hatası**: API isteklerinden 401 Unauthorized yanıtı alıyorsanız, token'in doğru bir şekilde alındığından veya kullanıldığından emin olun.

3. **XML Ayrıştırma Hatası**: XML yanıt ayrıştırılamazsa, backend'den dönen yanıtı kontrol edin ve XML yapısının doğru olduğundan emin olun.
