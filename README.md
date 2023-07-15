# CRM-Analytics
RFM, CLTV , BG-NBD, Gamma Gamma Models

Eğitim sonunda aşağıdaki konular hakkında bilgi sahibi olacağız:

- CRM Analitiği
- RFM Analizi
- Müşteri Yaşam Boyu Değeri
- Müşteri Yaşam Boyu Değeri Tahmini

# CRM Analitiğine Giriş

## Introduction to CRM Analytics

**CRM:** Customer Relationship Management (Müşteri İlişkileri Yönetimi)

**Customer Lifecycle / Journey / Funnel:** Müşteri Yaşam Döngüsü Optimizasyonları

**KPI:** Temel performans gösterileri

**Cross-sell:** çapraz satış örneğin müşteri hamburger aldıysa patates ve kola da satalım. Tamamlayıcı ürün satma

**Up-sell:** Üst satış. Küçük kola aldıysa büyük kola satalım

**CRM Analitiği:** Tüm müşteri ilişkileri sürecini veriye dayalı bir şekilde daha verimli hale getirmektir.

## KPI:Key Performance Indicators(Temel Performans Göstergeleri)

**KPI:** Şirket , departman ya da çalışanların performanslarını değerlendirmek için kullanılan matematiksel göstergelerdir.

**Customer Acquisition Rate:** Müşteri Kazanma Oranı

**Customer Retention Rate:** Müşteri Elde Tutma Oranı

**Customer Churn Rate:** Müşteri Terk Oranı

**Conversion Rate:** Dönüşüm Oranı

**Örnek:** yayınlanan bir ilanı bin kişi gördü 10 kişi tıkladıysa dönüşüm oranı 10 / 1000 dir. 10 kişi satın aldıysa dönüşüm oranı 1 / 10 dur.

**Growth Rate:** Büyüme Oranı

## **Analysis of Cohort (Kohort Analizi):**

**Cohort:** ortak özelliklere sahip bir grup insan

**Cohort Analizi:** ortak özelliğe sahip bir grup  insan davranışının analizi

# RFM Analizi

## RFM ile Müşteri Segmentasyonu(Customer Segmentation with RFM )

- **RFM:** Recency(yenilik), Frequency(sıklık), Monetary(parasal)
- RFM müşteri segmentasyonu için kullanılan bir tekniktir.
- Müşterilerin satın alma alışkanlıkları üzerinden gruplara ayrılması ve bu gruplar özelinde stratejiler geliştirilebilmesini sağlar.
- CRM çalışmaları için bir çok başlıkta veriye dayalı aksiyon alma imkanı sağlar.

**RFM Metrikleri:**

- **Recency(Yenilik):** Bizden en son nezaman alışveriş yaptı sorusuna cevap verir. Bu değer 1 veya 10 ise 1 olan 1 gün önce, 10 olan 10 gün önce alışveriş yaptı demektir. (Günlük konuşuluyorsa)
- **Frequency(sıklık):** Bizden ne sıklıkta alışveriş yaptığını söyler. işlem sıklığıörneğin 40 ise 40 alışveriş yapmış.
- **Monetary(parasal):** Müşterilerin bize bıraktığı parasal değerdir.

**RFM Skorları:** RFM metriklerin skorlarla temsil halidir. 1 ile 5 arasında değerlendirme gibi.

**NOT:**

- F ve M değerinin yüksek olması iyi ama R değerinin düşük olması iyidir. Dolayısıyla skorlanırken F ve M değerleri skorlanırken yüksek değere yüksek skor verilirken R değerinde yüksek değere düşük skor, düşük değere yüksek skor verilir.
- RFM skoru 145 olan ile 454 olan kıyaslanırsa 454 olan daha iyidir.

**Skorlar Üzerinden Metrik Oluşturmak:** x ekseninde R, y ekseninde F olur. M olmaz, çünkü etkileşim halindeki müşteri daha önemlidir.

# Müşteri Yaşam Boyu Değeri

## Müşteri Yaşam Boyu Değeri(Customer Lifetime Value)

Bir müşterinin bir şirketle kurduğu ilişki-iletişim süresince bu şirkete kazandıracağı parasal değerdir.

Değerin Hesaplanması: satın alma başına ortalama kazanç * satın alma sayısı

**CLTV =** (Customer Value / Churn Rate) *Profit Margin

**Customer Value =** Average Order Value * Purchase Frequency

**Average Order Value =** Total Price / Total Transaction 

**Purchase Frequency =** Total Transaction / Total Number of Customers

**Churn Rate =** 1- Repeat Rate

**Repeat Rate** = ****Birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler

**Profit Margin =** Total Price * 0.10 (Buradaki 0.10 şirketten şirkete değişebilirsabit sayısıdır, şirketin kar oranıdır.)

**CLTV:** Customer Lifetime Value (Müşteri yaşam boyu değeri)

**Customer Value:** Müşteri değeri (Ana odak)

**Churn Rate**: Müşteri terk oranı

**Profit Margin:** Kar marjı ( miktarı )

**Average Order Value:** Satın alma başına ortalama kazanç

**Purchase Frequency:** Satın alma frekansı

**Total Price:** Toplam fiyat

**Total Transaction:** Toplam işlem sayısı

**Total Number of Customers:** Toplam müşteri sayısı

**Repeat Rate:** Elde tutma oranı

NOT: Sonuç olarak her bir müşteri için hesaplanacak olan CLTV değerlerine göre bir sıralama yapıldığında ve CLTV değerlerine göre belirli noktalardan bölme işlemi yapılarak gruplar oluşturulduğunda müşterilerimiz segmentlere ayrılmış olacaktır.

# Müşteri Yaşam Boyu Değeri Tahmini (Customer Lifetime Value Prediction)

Zaman projeksiyonlu olasılıksal lifetime value tahmini

**CLTV =** (Customer Value / Churn Rate) * Profit Margin    olduğu incelenmişti.

**Customer Value =** Purchase Frequency * Average Order Value olduğu incelenmişti.

**CLTV =** Expected Number of Transaction * Expected Average Profit üstekinin aynısı sadece olasılıksal değeri

**CLTV =** BG/NBD Model * Gamma Gamma Submodel

**Expected:**  beklenen

**Conditional:**  koşullu

**Beklenen Değer:** Raasal değişkenin ortalaması

**Rassal:** Değerlerini bir deneyin sonuçlarından almak 

**Expected:** Bir rassal değişkenin beklenen değeridir.

NOT: Purchase Frequency yi BG/NBD modeli ile

Average Order Value yu Gamma Gamma Submodel ile yapacağız.

BG/NBD MODELİ TEK BAŞINA SATIŞ TAHMİN MODELİDİR. Namı diğer: Buy Till You Die

BG/NBD  modeli expected number of transaction için iki süreci olasılıksal olarak modeller:

- Transaction Process (Buy): satın alma süreci - işlem süreci
- Dropout Process(Till you die): bırakma-düşme-inaktif olma-markayı terk etme süreci

**Transaction Process(Buy):**  

Alive olduğu sürece belirli bir zaman periyodunda,bir müşteri tarafından gerçekleştirilecek işlem sayısı transaction rate parametresi ile poisson dağılır.

Bir müşteri alive olduğu sürece kendi transaction rate i etrafında rastgele satın alma yapmaya devam edecektir.

Transaction rate ler her bir müşteriye göre değişir ve tüm kitle için gamma dağılır.(r, a)

**Dropout Process(Till you die):**

Her bir müşterinin p olasılığı ile dropout rate (dropout probability) i vardır.

Bir müşteri alışveriş yaptıktan sonra belirli bir olasılıkla drop olur.

Dropout rate ler her bir müşteriye  göre değişir ve tüm kitle için beta dağılır.(a, b)

**BG/NBD Modeli**

CLTV = BG/NBD Model * Gamma Gamma Submodel

## Gamma Gamma Submodel

Gamma Gamma Submodel: Bir müşterinin işlem başına ortalama nekadar kar getirebileceğini tahmin etme modelidir.

- Bir müşterinin işlemlerinin parasal değeri (monetary) transaction value larının ortalaması etrafında rastgele dağılır.
- Ortalama transaction value, zaman içinde kullanılan arasında değişebilir fakat tek bir kullanıcı için değişmez.
- Ortalama transaction value tüm müşteriler arasında gamma dağılır.
