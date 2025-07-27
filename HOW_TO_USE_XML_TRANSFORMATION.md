# XML Dönüşüm Kılavuzu

Bu belge, XML1 projesi içindeki XML dönüşüm özelliklerinin kullanımını açıklar. Bu özellikler, XML verilerini XPath ifadeleri kullanarak çıkarmak ve XSLT stil tabloları kullanarak farklı formatlara dönüştürmek için API'ler sağlar.

## İçindekiler

1. [XPath Kullanımı](#xpath-kullanımı)
2. [XSLT Dönüşümleri](#xslt-dönüşümleri)
3. [API Referansı](#api-referansı)
4. [Örnekler](#örnekler)

## XPath Kullanımı

XPath, XML belgelerinden veri çıkarmak için kullanılan güçlü bir sorgulama dilidir. Projemizdeki XPath uygulaması, karmaşık XML yapılarından belirli öğeleri seçmenize olanak tanır.

### XPath API Nasıl Kullanılır

XPath API'sini kullanmak için `/api/v1/transform/xpath` endpoint'ine POST isteği gönderin:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<request>
    <xpath>//book/title/text()</xpath>
    <content>
        <!-- XML içeriği buraya -->
        <library>
            <books>
                <book id="1">
                    <title>To Kill a Mockingbird</title>
                    <author>Harper Lee</author>
                </book>
                <book id="2">
                    <title>1984</title>
                    <author>George Orwell</author>
                </book>
            </books>
        </library>
    </content>
</request>
```

### Yaygın XPath İfadeleri

| XPath İfadesi | Açıklama |
|---------------|----------|
| `//book/title` | Tüm kitap başlıklarını seçer |
| `//book[@id='1']` | ID'si 1 olan kitabı seçer |
| `//book[author='George Orwell']` | Yazarı George Orwell olan kitapları seçer |
| `count(//book)` | Kitapların toplam sayısını döndürür |
| `//book[year>2000]` | 2000 yılından sonra yayınlanan kitapları seçer |

## XSLT Dönüşümleri

XSLT (eXtensible Stylesheet Language Transformations), XML belgelerini diğer formatlara dönüştürmek için kullanılan bir dildir. Projemiz, XML verilerini HTML, düz metin veya farklı bir XML yapısına dönüştürmeyi destekler.

### XSLT API Nasıl Kullanılır

XSLT API'sini kullanmak için `/api/v1/transform/xslt` endpoint'ine POST isteği gönderin:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<request>
    <stylesheet-type>html</stylesheet-type>
    <content>
        <!-- XML içeriği buraya -->
        <library>
            <books>
                <book id="1">
                    <title>To Kill a Mockingbird</title>
                    <author>Harper Lee</author>
                    <year>1960</year>
                    <isbn>978-0446310789</isbn>
                </book>
            </books>
        </library>
    </content>
</request>
```

### Kullanılabilir Stil Tabloları

| Stil Tablosu | Açıklama |
|--------------|----------|
| `html` | XML'i biçimlendirilmiş HTML tablosuna dönüştürür |
| `text` | XML'i okunabilir düz metin formatına dönüştürür |
| `simplified` | XML'i daha basit bir XML yapısına dönüştürür |

## API Referansı

### XPath Endpoint

**Endpoint:** `/api/v1/transform/xpath`  
**Metot:** POST  
**Yetkilendirme:** Student veya Admin rolü gerektirir  
**İstek Formatı:** XML  
**İstek Gövdesi:**

```xml
<request>
    <xpath>XPath İfadesi</xpath>
    <content>
        <!-- XML içeriği -->
    </content>
</request>
```

**Yanıt Formatı:** XML
```xml
<xpath-result>
    <expression>Kullanılan XPath ifadesi</expression>
    <results>
        <item>Sonuç 1</item>
        <item>Sonuç 2</item>
        <!-- Diğer sonuçlar -->
    </results>
</xpath-result>
```

### XSLT Endpoint

**Endpoint:** `/api/v1/transform/xslt`  
**Metot:** POST  
**Yetkilendirme:** Student veya Admin rolü gerektirir  
**İstek Formatı:** XML  
**İstek Gövdesi:**

```xml
<request>
    <stylesheet-type>html|text|simplified</stylesheet-type>
    <content>
        <!-- XML içeriği -->
    </content>
</request>
```

**Yanıt Formatı:** HTML, düz metin veya XML (seçilen stil tablosuna bağlı)

### Örnekler Endpoint

**Endpoint:** `/api/v1/transform/examples`  
**Metot:** GET  
**Yetkilendirme:** Gerekli değil  
**Yanıt Formatı:** XML
```xml
<transformation-examples>
    <xpath-examples>
        <example>
            <expression>//book/title/text()</expression>
            <description>Extract all book titles</description>
        </example>
        <!-- Daha fazla örnek -->
    </xpath-examples>
    <xslt-examples>
        <example>
            <stylesheet-type>html</stylesheet-type>
            <description>Transform books to HTML table</description>
        </example>
        <!-- Daha fazla örnek -->
    </xslt-examples>
</transformation-examples>
```

## Örnekler

### XPath Örneği: Tüm Kitap Başlıklarını Alma

İstek:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<request>
    <xpath>//book/title/text()</xpath>
    <content>
        <library>
            <books>
                <book id="1">
                    <title>To Kill a Mockingbird</title>
                    <author>Harper Lee</author>
                </book>
                <book id="2">
                    <title>1984</title>
                    <author>George Orwell</author>
                </book>
            </books>
        </library>
    </content>
</request>
```

Yanıt:
```xml
<xpath-result>
    <expression>//book/title/text()</expression>
    <results>
        <item>To Kill a Mockingbird</item>
        <item>1984</item>
    </results>
</xpath-result>
```

### XSLT Örneği: HTML Dönüşümü

İstek:
```xml
<?xml version="1.0" encoding="UTF-8"?>
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
                </book>
            </books>
        </library>
    </content>
</request>
```

Yanıt:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Library Book Catalog</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        /* ... daha fazla stil ... */
    </style>
</head>
<body>
    <h1>Library Book Catalog</h1>
    <div class="book">
        <h2 class="book-title">To Kill a Mockingbird</h2>
        <p class="book-author">by Harper Lee</p>
        <p class="book-meta"><strong>Year:</strong> 1960 | <strong>ISBN:</strong> 978-0446310789</p>
    </div>
</body>
</html>
```

## Komut Satırından Test Etme

Eklediğimiz API testini çalıştırmak için:

```bash
cd backend
python tests/api_test.py --test xpath
python tests/api_test.py --test xslt
python tests/api_test.py --test transform-examples
```
