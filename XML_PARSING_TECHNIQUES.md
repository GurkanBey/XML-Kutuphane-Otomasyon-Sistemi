# XML Parsing Teknikleri Kılavuzu

Bu belge, XML1 projesinde uygulanan farklı XML ayrıştırma tekniklerini açıklar ve bu tekniklerin kullanımı hakkında bilgi verir.

## İçindekiler

1. [XML Ayrıştırma Teknikleri](#xml-ayrıştırma-teknikleri)
2. [Projedeki Uygulamalar](#projedeki-uygulamalar)
3. [API Kullanımı](#api-kullanımı)
4. [Performans Karşılaştırması](#performans-karşılaştırması)

## XML Ayrıştırma Teknikleri

Projemizde üç farklı XML ayrıştırma tekniği uygulanmıştır:

### 1. DOM-based Parsing (XmlDocument)

DOM (Document Object Model) tabanlı ayrıştırma, tüm XML belgesini belleğe bir ağaç yapısı olarak yükler. Bu yaklaşım, XML'in rastgele erişim gerektiren işlemler için uygundur.

**Avantajlar:**
- Belgenin herhangi bir bölümüne doğrudan erişim
- XML ağacını değiştirme ve güncelleyebilme
- Kolay gezinme

**Dezavantajlar:**
- Büyük belgeler için yüksek bellek kullanımı
- Büyük belgeler için düşük performans

### 2. SAX/Pull Parsing (XmlReader)

SAX (Simple API for XML) veya Pull ayrıştırma, belgeyi olaylar halinde sırayla işler. Belge tam olarak belleğe yüklenmez, bu nedenle bellek kullanımı düşüktür.

**Avantajlar:**
- Düşük bellek kullanımı
- Çok büyük XML belgeleri için uygun
- Streaming işlemler için ideal

**Dezavantajlar:**
- Yalnızca sıralı erişim (ileri doğru)
- Rastgele erişim yok
- Belgeyi değiştirmek zor

### 3. ElementTree (LINQ to XML benzeri)

ElementTree, Python'a özgü bir XML API'sidir. LINQ to XML'in sağladığı bazı sorgu özelliklerine benzer şekilde XML'i işler.

**Avantajlar:**
- Pythonic API, kolay kullanım
- DOM ve SAX arasında dengelenmiş performans
- Verimli bellek kullanımı
- Sorgu benzeri işlemler

**Dezavantajlar:**
- SAX kadar bellek verimli değil
- DOM kadar zengin özellikli değil

## Projedeki Uygulamalar

Aşağıdaki modüller, farklı XML ayrıştırma tekniklerini uygular:

- `backend/app/utils/xml_parsers/dom_parser.py`: DOM-based ayrıştırma
- `backend/app/utils/xml_parsers/sax_parser.py`: SAX/Pull ayrıştırma
- `backend/app/utils/xml_parsers/etree_parser.py`: ElementTree ayrıştırma
- `backend/app/utils/xml_parsers/comparison.py`: Karşılaştırma ve performans analizi

Her modül, ayrıştırma işlevselliğini ve kullanım örneklerini içerir.

## API Kullanımı

API'yi kullanarak XML ayrıştırma tekniklerini test edebilirsiniz:

### Tüm Yöntemlerle Ayrıştırma

**Endpoint:** `/api/v1/parsing/methods`  
**Metot:** POST  
**Yetkilendirme:** Öğrenci veya Admin rolü gerektirir  
**İstek Formatı:** XML  
**İstek Gövdesi:** Ayrıştırılacak herhangi bir XML belgesi

**Örnek İstek:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<library>
    <book id="1">
        <title>To Kill a Mockingbird</title>
        <author>Harper Lee</author>
        <year>1960</year>
        <isbn>978-0446310789</isbn>
    </book>
    <book id="2">
        <title>1984</title>
        <author>George Orwell</author>
        <year>1949</year>
        <isbn>978-0451524935</isbn>
    </book>
</library>
```

**Örnek Yanıt:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<parsing-methods-results>
  <summary>
    <total-time-ms>15.23</total-time-ms>
  </summary>
  <methods>
    <method>
      <name>dom</name>
      <type>DOM-based (XmlDocument equivalent)</type>
      <status>success</status>
      <time-ms>5.12</time-ms>
      <description>Loads entire document into memory as a tree, good for random access</description>
    </method>
    <method>
      <name>sax</name>
      <type>SAX/Pull parsing (XmlReader equivalent)</type>
      <status>success</status>
      <time-ms>4.87</time-ms>
      <description>Event-based, sequential parsing, memory efficient</description>
    </method>
    <method>
      <name>etree</name>
      <type>ElementTree (LINQ to XML equivalent)</type>
      <status>success</status>
      <time-ms>5.24</time-ms>
      <description>Pythonic API, good balance between features and performance</description>
    </method>
  </methods>
  <recommendations>
    <note>DOM: Best for small documents with random access needs</note>
    <note>SAX: Best for large documents with low memory requirements</note>
    <note>ElementTree: Good balance for most general XML processing</note>
  </recommendations>
</parsing-methods-results>
```

### Performans Karşılaştırması

**Endpoint:** `/api/v1/parsing/performance`  
**Metot:** POST  
**Yetkilendirme:** Öğrenci veya Admin rolü gerektirir  
**İstek Formatı:** XML  
**İstek Gövdesi:** Ayrıştırılacak herhangi bir XML belgesi  
**Query Parametreleri:** `repeat` (isteğe bağlı, varsayılan: 50) - Tekrar sayısı

**Örnek İstek URL:** `/api/v1/parsing/performance?repeat=100`

**Örnek Yanıt:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<parsing-performance-results>
  <summary>
    <repeat-count>100</repeat-count>
  </summary>
  <methods>
    <method>
      <name>dom</name>
      <time-ms>0.2345</time-ms>
      <memory-note>Highest memory usage, loads entire document</memory-note>
    </method>
    <method>
      <name>sax</name>
      <time-ms>0.1876</time-ms>
      <memory-note>Low memory usage, sequential access only</memory-note>
    </method>
    <method>
      <name>etree</name>
      <time-ms>0.2153</time-ms>
      <memory-note>Moderate memory usage, good balance</memory-note>
    </method>
    <method>
      <name>sax_callback</name>
      <time-ms>0.1654</time-ms>
      <memory-note>Lowest memory usage, best for very large documents</memory-note>
    </method>
  </methods>
  <fastest-method>sax_callback</fastest-method>
</parsing-performance-results>
```

## Performans Karşılaştırması

Farklı XML ayrıştırma teknikleri arasındaki performans karşılaştırması:

| Yöntem | Bellek Kullanımı | Hız | Erişim Modeli | En İyi Kullanım Alanı |
|--------|-----------------|-----|---------------|----------------------|
| DOM | Yüksek | Orta | Rastgele | Küçük-orta büyüklükteki belgeler, çok sayıda erişim gerektiren işlemler |
| SAX | Çok Düşük | Yüksek | Sıralı | Çok büyük belgeler, düşük bellek gereksinimleri, streaming işlemler |
| ElementTree | Orta | Orta-Yüksek | Yarı-rastgele | Genel amaçlı XML işleme, sorgu benzeri işlemler |

## Komut Satırından Test Etme

Aşağıdaki komutları kullanarak API'yi test edebilirsiniz:

```bash
# XML'i tüm yöntemlerle ayrıştırma
curl -X POST -H "Content-Type: application/xml" -H "Authorization: Bearer YOUR_TOKEN" -d @examples/books.xml http://localhost:5000/api/v1/parsing/methods

# Performans karşılaştırması
curl -X POST -H "Content-Type: application/xml" -H "Authorization: Bearer YOUR_TOKEN" -d @examples/books.xml "http://localhost:5000/api/v1/parsing/performance?repeat=100"
```
