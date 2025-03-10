# UYAP UDF Dosya Formatı
## İçindekiler
1. [Genel Bakış](#genel-bakış)
2. [UDF Dosya Yapısı](#udf-dosya-yapısı)
3. [XML Yapısı](#xml-yapısı)
4. [Kök Eleman](#kök-eleman)
5. [Ana Bölümler](#ana-bölümler)
   - [İçerik Bölümü](#i̇çerik-bölümü)
   - [Özellikler Bölümü](#özellikler-bölümü)
   - [Elemanlar Bölümü](#elemanlar-bölümü)
   - [Stiller Bölümü](#stiller-bölümü)
6. [Detaylı Eleman Açıklamaları ve Özellik Örnekleri](#detaylı-eleman-açıklamaları-ve-özellik-örnekleri)

## Genel Bakış
Bu belge, belge şablonlama ve biçimlendirme için kullanılan UDF ve dahili XML formatının yapısını ve elemanlarını açıklar. Bu format, çeşitli biçimlendirme seçenekleri, tablolar, gömülü öğeler, üstbilgiler, altbilgiler ve listeler içeren zengin metin belgelerini temsil etmek için tasarlanmıştır.

## UDF Dosya Yapısı
UDF formatı, esasen belirli bir iç yapıya sahip bir ZIP arşividir:

1. UDF (ZIP) içindeki ana dosya `content.xml` olarak adlandırılır.
2. Bu `content.xml` dosyası, XML formatında gerçek belge içeriğini ve biçimlendirme bilgilerini içerir.
3. ZIP arşivinde diğer kaynaklar (örneğin, resimler veya ek meta veriler) de bulunabilir.

Bir UDF dosyasının içeriğini düzenlemek veya görüntülemek için:
1. Dosya uzantısını `.udf`'den `.zip`'e değiştirin
2. ZIP dosyasının içeriğini çıkarın
3. `content.xml` dosyasını açın ve düzenleyin
4. Düzenlenmiş dosyaları tekrar ZIP arşivine paketleyin
5. ZIP dosyasını tekrar `.udf` olarak yeniden adlandırın

## XML Yapısı
`content.xml` dosyası, aşağıda ayrıntılı olarak açıklayacağımız belirli bir XML yapısını takip eder.

## Kök Eleman
XML belgesinin kök elemanı, aşağıdaki özelliğe sahip `<template>`'dir:
- `format_id`: Formatın sürümü
  - Örnek: `format_id="1.8"`

## Ana Bölümler
`<template>` elemanı dört ana bölüm içerir:

1. `<content>`: Belgenin ham metin içeriği
2. `<properties>`: Belge genelindeki özellikler
3. `<elements>`: Belgenin yapısı ve biçimlendirmesi
4. `<styles>`: Belgede kullanılan metin stilleri

### İçerik Bölümü
`<content>` bölümü bir CDATA bloğu içine sarılmıştır ve belgenin ham metnini içerir. Bu, üstbilgiler, altbilgiler ve ana gövde metni dahil olmak üzere tüm metinsel içeriği içerir.

Örnek:
```xml
<content><![CDATA[
  Bu, belgenin ham içeriğidir.
  Özel karakterler dahil her türlü metni içerebilir.
]]></content>
```

**Önemli Not:** İçerik bölümü, tüm metinsel verileri içeren tek bir havuz olarak çalışır. `<elements>` bölümündeki `startOffset` ve `length` özellikleri, bu içerik havuzundaki belirli metin parçalarını referans alır.

### Özellikler Bölümü
`<properties>` elemanı, sayfa düzenini tanımlayan özelliklerle bir `<pageFormat>` elemanı içerir:

- `mediaSizeName`: Sayfa boyutunu tanımlar
  - Değerler: Standart kağıt boyutlarını temsil eden tamsayı
  - Örnek: `mediaSizeName="1"` (A4 boyutu)

- `leftMargin`, `rightMargin`, `topMargin`, `bottomMargin`: Sayfa kenar boşlukları (punto cinsinden)
  - Değerler: Ondalık sayılar
  - Örnek: `leftMargin="42.51968479156494"` (yaklaşık 1.5 cm)

- `paperOrientation`: Sayfa yönü
  - Değerler: Dikey için "1", yatay için "2"
  - Örnek: `paperOrientation="1"` (dikey)

- `headerFOffset`, `footerFOffset`: Üstbilgi ve altbilgi ofsetleri (punto cinsinden)
  - Değerler: Ondalık sayılar
  - Örnek: `headerFOffset="20.0"` (yaklaşık 0.7 cm)

#### Arka Plan Görüntüsü
`<properties>` bölümünde bir `<bgImage>` elemanı bulunabilir. Bu eleman, belge için arka plan görüntüsünü tanımlar:

- `bgImageSource`: Görüntünün kaynak konumu
  - Örnek: `bgImageSource="/resources/modules/dis/1.jpg"`

- `bgImageData`: Base64 kodlanmış görüntü verisi
  - Örnek: `bgImageData="iVBORw0KGgoAAAANSUhEUgAA..."`

- `bgImageBottomMargin`, `bgImageUpMargin`, `bgImageRigtMargin`, `bgImageLeftMargin`: Arka plan görüntüsünün kenar boşlukları
  - Örnek: `bgImageBottomMargin="28" bgImageUpMargin="28" bgImageRigtMargin="28" bgImageLeftMargin="28"`

Örnek:
```xml
<properties>
  <pageFormat mediaSizeName="1" leftMargin="42.51968479156494" rightMargin="42.51968479156494" topMargin="42.51968479156494" bottomMargin="70.8661413192749" paperOrientation="1" headerFOffset="20.0" footerFOffset="20.0" />
  <bgImage bgImageSource="/resources/modules/dis/1.jpg" bgImageData="iVBORw0KGgoAAAANSUhEUgAA..." bgImageBottomMargin="28" bgImageUpMargin="28" bgImageRigtMargin="28" bgImageLeftMargin="28" />
</properties>
```

### Elemanlar Bölümü
`<elements>` bölümü, belgenin yapısını ve biçimlendirmesini tanımlar. Aşağıdaki elemanları içerebilir:

1. Üstbilgi
2. Altbilgi
3. Paragraf
4. İçerik
5. Tablo
6. Resim
7. Sekme
8. Sayfa Sonu

`<elements>` elemanı bir `resolver` özelliğine sahip olabilir, bu özellik belgenin hangi stil çözümleyiciyi kullanacağını belirtir.
Örnek: `<elements resolver="hvl-default">`

### Stiller Bölümü
`<styles>` bölümü, belgede kullanılan metin stillerini tanımlar:

- `name`: Stilin adı
- `description`: Stilin açıklaması
- `family`: Yazı tipi ailesi
- `size`: Yazı tipi boyutu (punto cinsinden)
- `bold`, `italic`: Metin stili
- `foreground`: Metin rengi (RGB formatında)
- `FONT_ATTRIBUTE_KEY`: Java Swing yazı tipi özelliği

Örnek:
```xml
<styles>
  <style name="default" description="Geçerli" family="Dialog" size="12" bold="false" italic="false" foreground="-13421773" FONT_ATTRIBUTE_KEY="javax.swing.plaf.FontUIResource[family=Dialog,name=Dialog,style=plain,size=12]" />
  <style name="hvl-default" family="Times New Roman" size="12" description="Gövde" />
</styles>
```

## Detaylı Eleman Açıklamaları ve Özellik Örnekleri

### Üstbilgi
`<header>` elemanı ile temsil edilir, üstbilgi içeriği için paragraflar içerir. Arka plan rengi ve metin rengi ayarlanabilir.

Özellikler:
- `background`: Üstbilgi arka plan rengi (RGB formatında)
  - Örnek: `background="-8323073"` (açık mavi)

- `foreground`: Üstbilgi metin rengi (RGB formatında)
  - Örnek: `foreground="-16776961"` (mavi)

Örnek:
```xml
<header background="-8323073" foreground="-16776961">
  <paragraph family="Times New Roman" size="12" description="Gövde">
    <content family="Times New Roman" size="12" description="Gövde" startOffset="0" length="14" />
  </paragraph>
</header>
```

### Altbilgi
`<footer>` elemanı ile temsil edilir ve aşağıdaki özelliklere sahiptir:

- `background`: Altbilgi arka plan rengi (RGB formatında)
  - Örnek: `background="-8339328"` (açık yeşil)

- `foreground`: Altbilgi metin rengi (RGB formatında)
  - Örnek: `foreground="-16776961"` (mavi)

- `pageNumber-spec`: Sayfa numarası özelliği
  - Örnek: `pageNumber-spec="BSP32_40"`

- `pageNumber-color`: Sayfa numarası rengi (RGB formatında)
  - Örnek: `pageNumber-color="-16777216"` (siyah)

- `pageNumber-fontFace`: Sayfa numarası için yazı tipi
  - Örnek: `pageNumber-fontFace="Arial"`

- `pageNumber-fontSize`: Sayfa numarası için yazı tipi boyutu
  - Örnek: `pageNumber-fontSize="11"`

- `pageNumber-foreStr`: Sayfa numarasından önce gelen metin
  - Örnek: `pageNumber-foreStr="sayfa"`

- `pageNumber-pageStartNumStr`: Başlangıç sayfa numarası
  - Örnek: `pageNumber-pageStartNumStr="1"`

Örnek:
```xml
<footer background="-8339328" foreground="-16776961" pageNumber-spec="BSP32_40" pageNumber-color="-16777216" pageNumber-fontFace="Arial" pageNumber-fontSize="11" pageNumber-foreStr="sayfa" pageNumber-pageStartNumStr="1">
  <paragraph FirstLineIndent="2.5" family="Times New Roman" size="12">
    <content FirstLineIndent="2.5" family="Times New Roman" size="12" startOffset="166" length="17" />
  </paragraph>
</footer>
```

### Paragraf
`<paragraph>` elemanı ile temsil edilir ve aşağıdaki özelliklere sahiptir:

- `Alignment`: Metin hizalama
  - Değerler: Sola için "0", ortaya için "1", sağa için "2", iki yana yasla için "3"
  - Örnek: `Alignment="3"` (iki yana yasla)

- `LeftIndent`, `RightIndent`: Girinti değerleri (punto cinsinden)
  - Örnek: `LeftIndent="36.0"` (yaklaşık 1.27 cm)

- `LineSpacing`: Satır aralığı
  - Değerler: Ondalık sayılar (1.0 tek aralık, 2.0 çift aralık)
  - Örnek: `LineSpacing="1.0"` (tek aralık)

- `TabSet`: Sekme durak pozisyonları ve türleri
  - Örnek: `TabSet="36.0:0:0"` (36 puntoda sekme durağı, sola hizalı)

- `Bulleted`: Madde işaretli liste öğeleri için "true"
  - Örnek: `Bulleted="true"`

- `BulletType`: Madde işareti türü
  - Örnek: `BulletType="BULLET_TYPE_ELLIPSE"`

- `Numbered`: Numaralandırılmış liste öğeleri için "true"
  - Örnek: `Numbered="true"`

- `NumberType`: Numaralandırma türü
  - Örnek: `NumberType="NUMBER_TYPE_NUMBER_DOT"`

- `ListLevel`: Liste öğesinin girinti seviyesi
  - Örnek: `ListLevel="1"`

- `ListId`: Liste için tanımlayıcı
  - Örnek: `ListId="1"`

- `FirstLineIndent`: İlk satır girintisi
  - Örnek: `FirstLineIndent="2.5"`

- `family`: Paragraf için yazı tipi ailesi
  - Örnek: `family="Times New Roman"`

- `size`: Paragraf için varsayılan yazı tipi boyutu
  - Örnek: `size="12"`

Örnek:
```xml
<paragraph Alignment="0" LeftIndent="36.0" LineSpacing="1.0" family="Verdana">
  <content family="Verdana" startOffset="77" length="19" />
</paragraph>
```

### Sayfa Sonu
`<page-break>` elemanı bir sayfa sonunu temsil eder ve içinde bir paragraf içerir.

Örnek:
```xml
<page-break>
  <paragraph>
    <content startOffset="147" length="1" />
  </paragraph>
</page-break>
```

### İçerik
`<content>` elemanı, belirli biçimlendirmeye sahip metni temsil eder:

- `size`: Yazı tipi boyutu (punto cinsinden)
  - Örnek: `size="12"`

- `bold`, `italic`, `underline`: Metin stili
  - Örnek: `bold="true"` `italic="false"` `underline="true"`

- `startOffset`, `length`: Ham içerikteki metnin konumu ve uzunluğu
  - Örnek: `startOffset="16" length="39"`

- `resolver`: Kullanılacak stil çözümleyiciyi belirtir
  - Örnek: `resolver="hvl-default"`

- `strikethrough`: Üstü çizili metin için "true"
  - Örnek: `strikethrough="true"`

- `subscript`: Alt simge metni için "true"
  - Örnek: `subscript="true"`

- `superscript`: Üst simge metni için "true"
  - Örnek: `superscript="true"`

- `background`: Arka plan rengi (RGB formatında)
  - Örnek: `background="-8239546"` (açık mavi)

- `foreground`: Metin rengi (RGB formatında)
  - Örnek: `foreground="-196608"` (koyu yeşil)

- `family`: Yazı tipi ailesi
  - Örnek: `family="Verdana"`

Örnek:
```xml
<content bold="true" startOffset="19" length="14" />
<content italic="true" startOffset="33" length="15" />
<content underline="true" startOffset="52" length="23" />
<content family="Verdana" foreground="-196608" startOffset="105" length="9" />
```

### Tablo
Tablolar `<table>` elemanı ile temsil edilir ve aşağıdaki özelliklere sahiptir:

- `tableName`: Tablonun adı
  - Örnek: `tableName="Sabit"`

- `columnCount`: Sütun sayısı
  - Örnek: `columnCount="2"`

- `columnSpans`: Sütun genişlikleri (punto cinsinden)
  - Örnek: `columnSpans="100,100"`

- `border`: Kenarlık stili
  - Değerler: "borderCell" (tüm hücrelere kenarlık), "border" (dış kenarlık), "borderOuter" (sadece dış kenarlık)
  - Örnek: `border="borderCell"`

- `rowSpans`: Satır yükseklikleri (punto cinsinden)
  - Örnek: `rowSpans="428,428"`

Satırlar `<row>` elemanı ile temsil edilir ve aşağıdaki özelliklere sahiptir:

- `rowName`: Satırın adı
  - Örnek: `rowName="row1"`

- `rowType`: Satırın türü
  - Örnek: `rowType="dataRow"`

- `height_min`: Minimum satır yüksekliği
  - Örnek: `height_min="1.5"`

Hücreler `<cell>` elemanı ile temsil edilir ve her biri bir veya daha fazla paragraf içerebilir.

Örnek:
```xml
<table tableName="Sabit" columnCount="2" columnSpans="100,100" border="borderCell" rowSpans="428,428">
  <row rowName="row1" rowType="dataRow" height_min="1.5">
    <cell>
      <paragraph Alignment="0" LeftIndent="3.0" RightIndent="1.0">
        <content Alignment="0" LeftIndent="3.0" RightIndent="1.0" startOffset="157" length="2" />
      </paragraph>
    </cell>
    <cell>
      <paragraph Alignment="0" LeftIndent="3.0" RightIndent="1.0">
        <content Alignment="0" LeftIndent="3.0" RightIndent="1.0" startOffset="159" length="2" />
      </paragraph>
    </cell>
  </row>
</table>
```

### Resim
Resimler `<image>` elemanı ile temsil edilir ve aşağıdaki özelliklere sahiptir:

- `family`: Resim yer tutucu için yazı tipi ailesi
  - Örnek: `family="Times New Roman"`

- `size`: Resim yer tutucu için yazı tipi boyutu
  - Örnek: `size="12"`

- `imageData`: Base64 ile kodlanmış resim verisi
  - Örnek: `imageData="iVBORw0KGgoAAAANSUhEUgAA..."`

Örnek:
```xml
<image family="Times New Roman" size="12" imageData="iVBORw0KGgoAAAANSUhEUgAA..." />
```

### Sekme
`<tab>` elemanı bir sekme karakterini temsil eder ve aşağıdaki özelliklere sahiptir:

- `startOffset`: Ham içerikteki sekmenin konumu
  - Örnek: `startOffset="130"`

- `length`: Tek bir sekme karakteri için her zaman 1'dir
  - Örnek: `length="1"`

Örnek:
```xml
<tab startOffset="130" length="1" />
```

### Boşluk
`<space>` elemanı bir boşluk karakterini temsil eder ve genellikle `<paragraph>` içinde diğer içerik elemanları arasında kullanılır.

Örnek:
```xml
<paragraph>
  <content bold="true" startOffset="19" length="14" />
  <space />
  <content italic="true" startOffset="33" length="15" />
</paragraph>
```