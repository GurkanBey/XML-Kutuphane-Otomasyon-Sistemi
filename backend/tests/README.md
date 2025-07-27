# API Test Betiği

Bu betik, XML tabanlı API'lerinizi test etmek için kullanılır. API v1 ve API v2 fonksiyonlarını test edebilirsiniz.

## Kurulum

Test betiğini çalıştırmak için gereken bağımlılıkları yükleyin:

```
pip install requests colorama
```

## Kullanım

Backend sunucunuzu çalıştırdıktan sonra test betiğini aşağıdaki şekilde kullanabilirsiniz:

### Tüm Testleri Çalıştırmak İçin

```
python api_test.py
```

veya

```
python api_test.py --test all
```

### Belirli Bir Testi Çalıştırmak İçin

```
python api_test.py --test [test-adı]
```

Mevcut test seçenekleri:
- `login`: API v1 login fonksiyonunu test eder
- `books`: API v1 kitapları listeleme fonksiyonunu test eder
- `endpoints`: API v1 endpoints listeleme fonksiyonunu test eder
- `add-book`: API v1 kitap ekleme fonksiyonunu test eder (Admin yetkisi gerektirir)
- `weather`: API v1 hava durumu fonksiyonunu test eder
- `api-v2-info`: API v2 info fonksiyonunu test eder

### Kullanıcı Adı ve Şifre Belirterek Giriş Yapmak İçin

```
python api_test.py --username [kullanıcı adı] --password [şifre]
```

Örnek:
```
python api_test.py --test books --username student --password student123
```

## Çıktı

Test betiği, gönderilen istekleri ve alınan yanıtları renkli bir şekilde konsola yazdırır. XML yanıtlar da güzelleştirilmiş ve renk kodlu olarak görüntülenir.

## Not

Test ederken backend sunucunuzun çalışıyor olması gerekir. Betik varsayılan olarak `http://localhost:5000` adresine istek gönderir.
