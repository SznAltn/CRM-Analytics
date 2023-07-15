###########################################################################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###########################################################################################################

# 1. İş Problemi (Business Problem)
# 2. Veriyi Anlama (Data Understanding)
# 3. Veri Hazırlama (Data Preparation)
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
# 7. Tüm Sürecin Fonksiyonlaştırılması


# 1. İş Problemi (Business Problem)


# Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre
# pazarlama stratejileri belirlemek istiyor.

# Veri Seti Hikayesi
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

# Değişkenler
#
# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi, açıklaması
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.



# 2. Veriyi Anlama (Data Understanding)

import datetime as dt
import pandas as pd
pd.set_option("display.max_columns", None) # max kolon(sütun) sayısı olmasın. tüm sütunlar görünsün
# pd.set_option("display.max_rows", None) # max satır sayısı olmasın
# çıktı kalabalık olmasın diye yorum satırı yaptık
pd.set_option("display.float_format", lambda x: "%.3f" % x)
# sayısal değişkenlerin virgülden sonra kaç basamağını göstersin,
# 3 yazdık o yüzden virgülden sonra 3 basamak görünür.
df_= pd.read_excel("/Users/PARS/PycharmProjects/pythonProject1/12.Data Scientist Bootcamp/Datasets/online_retail_II.xlsx", sheet_name="Year 2009-2010")
df = df_.copy()
df.head()
df.shape
df.isnull().sum()

# essiz urun sayisi nedir?
df["Description"].nunique()

# hangi üründen kaçar tane var?
df["Description"].value_counts().head()

# en çok sipariş edilen ürünü bulmak için:
# Description a göre veriyi kır quantity ye göre sum yap yani hangi üründen kaçar tane sipariş verilmiş
df.groupby("Description").agg({"Quantity": "sum"}).head()
# problem oldu veri ön işleme bölümünde bakılacak.

# Description a göre veriyi kır quantity ye göre sum alınca sort values ile quantity e göre azalan sıralayınca :
df.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity", ascending=False)

# toplam kaçar tane eşsiz fatura kesilmiş:
df["Invoice"].nunique()

# ürünlerin toplam kazancı:
df["TotalPrice"] = df["Quantity"] * df["Price"]

# Fatura başına toplam kaç para kazanılmış:
df.groupby("Invoice").agg({"TotalPrice": "sum"}).head()

##############################################################################################################
# 3. Veri Hazırlama (Data Preparation)
##############################################################################################################

df.shape # boyut bilgisi
df.isnull().sum() # eksik değer sayıları
df.dropna(inplace=True) # eksik değerleri silmek için
df.shape # tekrar verimizi inceledik
df.describe().T # özet istatistikleri, betimsel istatistikleri

# iade edilen faturaları veri setinden çıkaralım:
df[~df["Invoice"].str.contains("C", na = False)]

# atamasını yapalım:
df = df[~df["Invoice"].str.contains("C", na = False)]

# ürün adedi 0 dan büyük olanlar
df[(df["Quantity"]) > 0]

##############################################################################################################
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
##############################################################################################################

# Recency, Frequency, Monetary
# Yenilik, Sıklık(Toplam satın alma), Müşterinin bıraktığı parasal değer

df.head()

# ilgili hesaplamaların yapılması için analizin yapıldığı günü tanımlamalıyız
# çünkü veri seti eski

df["InvoiceDate"].max()
# gelen cevaba 2 gün ekleyip yapabiliriz yapmazsak sonuçlar çok büyük çıkar.

today_date = dt.datetime(2010, 12, 11)
type(today_date)

# tüm müşterilere göre groupby a alıp recency yi frequency ve monetary yi hesaplıcaz
# today_date ten groupby a aldıktan sonra her bir müşterinin max tarihini bulcaz
# today_date ten çıkardıktan sonra recency i bulmuş oluruz
# customer_id ye göre groupby a aldıktan sonra herbir müşterinin eşsiz fatura sayısına gidersek
# müşterinin kaç işlem yaptığını yani frequency i buluruz
# customer_id ye göre groupby a aldıktan sonra total_price nın sum ını alırsak
# herbir müşterinin toplam kaç para bıraktığını buluruz yani monetary i

rfm = df.groupby("Customer ID").agg({"InvoiceDate": lambda InvoiceDate: (today_date - InvoiceDate.max()).days,
                                     "Invoice": lambda Invoice: Invoice.nunique(),
                                     "TotalPrice": lambda TotalPrice: TotalPrice.sum()})

rfm.head()
rfm.columns = ["recency", "frequency", "monetary"] # değişkenlerin isimlerini kendi istediğimiz gibi yaptık

rfm.describe().T # betimsel istatistikleri

# monetary nin 0 olması işimize gelmedi silelim o kısmı
# yani monetary değeri 0 dan büyük olanları alalım

rfm = rfm[rfm["monetary"] > 0]

rfm.head()
rfm.shape

##############################################################################################################
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
##############################################################################################################

# qcut fonksiyonu quantile yani çeyrek değerlere göre bölme işlemi yapar,
# değişken ver, kaç parçaya böleceğini söyle, böldüğün parçalara vereceğin isimleri ver
# küçükten büyüğe sıralar 5 parçaya böler
# örneğin : önce 0-100 e sıralar, 0-20, 20-40, 40-60, 60-80, 80-100 dilimlerine ayırır.
rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])

# monetary değişkenini küçükten büyüğe sırala 5 parçaya böl küçük olana 1 , büyük olana 5 ismini ver
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

# monetary değişkenini küçükten büyüğe sırala 5 parçaya böl küçük olana 1 , büyük olana 5 ismini ver
rfm["frequency_score"] = pd.qcut(rfm["frequency"], 5, labels=[1, 2, 3, 4, 5])
# hata aldık çünkü aralıklarda unique değerler yer almıyor hatası verdi
# çünkü daha fazla sayıda aralığa hep aynı değerler denk gelmiş
# bunu çözmek için rank methodunu kullanıyoruz.

# doğrusu:
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

# score değişkeni oluşturalım
rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str) +
                    rfm["frequency_score"].astype(str))
rfm.describe().T

# şampiyonları görmek için:
rfm[rfm["RFM_SCORE"] == "55"]

# sıkıntılı müşteriler
rfm[rfm["RFM_SCORE"] == "11"]


################################################################################################
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
################################################################################################
# regex: düzenli ifadeler
# reguler expression

# RFM isimlendirmesi

seg_map = {
    r"[1-2][1-2]": "hibernating",
    r"[1-2][3-4]": "at_Risk",
    r"[1-2]5": "cant_loose",
    r"3[1-2]": "about_to_sleep",
    r"33": "need_attention",
    r"[3-4][4-5]": "loyal_customers",
    r"41": "promossing",
    r"51": "new_customers",
    r"[4-5][2-3]": "potential_loyalists",
    r"5[4-5]": "champions",
}

# birleştirme scorları, replace ile değiştir diyoruz,
rfm["segment"] = rfm["RFM_SCORE"].replace(seg_map, regex=True)

# rfm nin içinden metrikleri bulup, ortalamalarını ve toplamını görelim:
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

# segment in içinden cant_loose olanların ilk5ini getir:
rfm[rfm["segment"] == "cant_loose"].head()

# bu kişilerin id lerine ulaşmak istersek
rfm[rfm["segment"] == "cant_loose"].index

# yeni dataframe oluşturalım:
new_df = pd.DataFrame()

# içine yeni müşterilerin id sini atalım:
new_df["new_customers_id"] = rfm[rfm["segment"] == "new_customers"].index

# id deki ondalıklardan kurtulmak için:
new_df["new_customers_id"] = new_df["new_customers_id"].astype(int)

# başka birine vermek istersek csv dosyasına dönüştürelim:
new_df.to_csv("new_customers.csv")

# rfm i de çıkarmak istersek:
rfm.to_csv("rfm.csv")


#####################################################################################
# 7. Tüm Sürecin Fonksiyonlaştırılması(Functionalization)
#####################################################################################
def create_rfm(dataframe, csv=False):
    # VERIYI HAZIRLAMA
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]

    #RFM METRIKLERININ HAZIRLANMASI
    today_date = dt.datetime(2011, 12, 11)
    rfm = dataframe.groupby("Customer ID").agg({"InvoiceDate": lambda date:(today_date - date.max()).days,
                                                "Invoice": lambda num:num.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
    rfm.columns = ["recency", "frequency", "monetary"]
    rfm = rfm[(rfm["monetary"] > 0)]

    # RFM SKORLARININ HESAPLANMASI
    rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

    # cltv_df skorları kategorik değere dönüştürülüp df e eklendi
    rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str) +
                        rfm["frequency_score"].astype(str))

    # SEGMENTLERIN ISIMLENDIRILMESI
    seg_map = {
        r"[1-2][1-2]": "hibernating",
        r"[1-2][3-4]": "at_Risk",
        r"[1-2]5": "cant_loose",
        r"3[1-2]": "about_to_sleep",
        r"33": "need_attention",
        r"[3-4][4-5]": "loyal_customers",
        r"41": "promossing",
        r"51": "new_customers",
        r"[4-5][2-3]": "potential_loyalists",
        r"5[4-5]": "champions",
    }

    rfm["segment"] = rfm["RFM_SCORE"].replace(seg_map, regex=True)
    rfm = rfm[["segment", "recency", "frequency", "monetary"]]
    rfm.index = rfm.index.astype(int)

    if csv:
        rfm.to_csv("rfm.csv")

    return rfm

# verisetini en baştaki haline geri getirelim: df ilk hali oldu
df = df_.copy()

rfm_new = create_rfm(df)

# csv nin gelmesini istersek:
rfm_new = create_rfm(df, csv=True)


####################################################################################################################
# CUSTOMER LIFETIME VALUE (Müşteri Yaşam Boyu Değeri)
####################################################################################################################

# 1. Veri Hazırlama
# 2. Average Order Value (average_order_value = total_price / total_transaction)
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
# 4. Repeat Rate & Churn Rate (birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler)
# 5. Profit Margin (profit_margin =  total_price * 0.10)
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
# 8. Segmentlerin Oluşturulması
# 9. BONUS: Tüm İşlemlerin Fonksiyonlaştırılması

#####################################################################################################################
# 1. Veri Hazırlama (Data Preparation)
#####################################################################################################################

# Veri Seti Hikayesi
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

# Değişkenler
# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
pd.set_option("display.max_columns", None) # tüm sütunları göster
# pd.set_option("display.max_rows", None) # tüm satırları göster
pd.set_option("display.float_format", lambda x: "%.5f" % x) # virgülden sonra 5 basamak göster

df_ = pd.read_excel("/Users/PARS/PycharmProjects/pythonProject1/12.Data Scientist Bootcamp/Datasets/online_retail_II.xlsx", sheet_name="Year 2009-2010")

df = df_.copy() # okunması uzun sürüyor işler ters giderse df_ ile copyasını oluşturuyorum.
df.head()
df.isnull().sum()

# iade olan ürünleri verisetinden çıkarıyoruz
df = df[~df["Invoice"].str.contains("C", na=False)]
df.describe().T # betimsel istatistikler

# Quantity si 0 dan büyük olanlar
df = df[(df["Quantity"] > 0)]
df.describe().T # betimsel istatistikler

# eksikdeğerleri silelim
df.dropna(inplace=True)
df.describe().T # betimsel istatistikler

# Toplam ödeme = ürün adedi * ödeme
df["TotalPrice"] = df["Quantity"] * df["Price"]

# müşteri yaşam boyu değeri =
# customer ıd ye göre groupby a al
# invoice değerinin eşsiz değer sayısı total_transaction ı verir
# quantity nin toplamı total_unit değerini verir
# total_price ın toplamı total_price ı verir
cltv_c = df.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                        'Quantity': lambda x: x.sum(),
                                        'TotalPrice': lambda x: x.sum()})

cltv_c.columns = ['total_transaction', 'total_unit', 'total_price']

######################################################################################################
# 2. Average Order Value (average_order_value = total_price / total_transaction)
######################################################################################################

cltv_c.head()

cltv_c["average_order_value"] = cltv_c["total_price"] / cltv_c["total_transaction"]

########################################################################################
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
########################################################################################

cltv_c.head()
cltv_c["total_transaction"]

cltv_c.shape

# bu dataframe nin satırları eşsiz müşterileri temsil ediyor
# shape in sıfırıncı elemanını alırsam total_number_of_customers a ulaşırız:

cltv_c.shape[0]

cltv_c["purchase_frequency"] = cltv_c["total_transaction"] / cltv_c.shape[0]


######################################################################################################################
# 4. Repeat Rate & Churn Rate (birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler)
######################################################################################################################

# birden fazla alışveriş yapan müşteri sayısı
cltv_c[cltv_c["total_transaction"] > 1].shape[0]

# Repeat Rate değeri
repeat_rate = cltv_c[cltv_c["total_transaction"] > 1].shape[0] / cltv_c.shape[0]

# churn_rate: bizi terkedecek müşteri oranı
churn_rate = 1 - repeat_rate


#################################################################################################
# 5. Profit Margin (profit_margin =  total_price * 0.10)
#################################################################################################

# 0.10 : şirketten şirkete değişen kar oranı

# herbir müşterinin kendi içinde total_price nı 0.10 ile çarpıyoruz
cltv_c["profit_margin"] = cltv_c["total_price"] * 0.10


#################################################################################################
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
#################################################################################################

# customer_value:
cltv_c["customer_value"] = cltv_c["average_order_value"] * cltv_c["purchase_frequency"]



#################################################################################################
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
#################################################################################################

# Customer Lifetime Value: cltv
cltv_c["cltv"] = (cltv_c["customer_value"] / churn_rate) * cltv_c["profit_margin"]

# cltv ye göre azalan olarak skorları sırala
cltv_c.sort_values(by="cltv", ascending=False).head()



################################################################################################
# 8. Segmentlerin Oluşturulması (Creating Segments)
################################################################################################

# cltv ye göre sıralayım en yüksekten düşüğe doğru çıkan sonucun da ilk 5 gözlemini çekelim
cltv_c.sort_values(by="cltv", ascending=False).head()

# # cltv ye göre sıralayım en yüksekten düşüğe doğru çıkan sonucun da son 5 gözlemini çekelim
cltv_c.sort_values(by="cltv", ascending=False).tail()

# segment adında bir değişken oluştur, qcut ile cltv yi küçükten büyüğe sırala
# 4 gruba ayır , isimlendirmeyi küçük gördüğüne d, büyüğe a de
cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])

# bunun ilk 5 terimi
cltv_c.sort_values(by="cltv", ascending=False).head()

# cltv yi segmentlere göre groupby a alıp
# segmentlerin her biri için bütün değişkenler bazında count, mean ve sum gibi betimsel istatistiklerinii bul
cltv_c.groupby("segment").agg({"count", "mean", "sum"})

# csv dosyasına dönüştürmek istersek:
cltv_c.to_csv("cltc_c.csv")

# 18102.00000       A
# 14646.00000       A
# 14156.00000       A
# 14911.00000       A
# 13694.00000       A

# Customer ID
# 18102.00000       A
# 14646.00000       A
# 14156.00000       A
# 14911.00000       A
# 13694.00000       A

################################################################################################
# 9. BONUS: Tüm İşlemlerin Fonksiyonlaştırılması (Functionalization)
################################################################################################

def create_cltv_c(dataframe, profit=0.10):
    # VERIYI HAZIRLAMA
    dataframe =dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[(dataframe["Quantity"] > 0)]
    dataframe.dropna(inplace=True)
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    cltv_c = dataframe.groupby("Customer ID").agg({"Invoice": lambda x: x.nunique(),
                                                   "Quantity": lambda x: x.sum(),
                                                   "TotalPrice": lambda x: x.sum()})
    cltv_c.columns = ["total_transaction", "total_unit", "total_price"]

    # avg_order_value
    cltv_c["avg_order_value"] = cltv_c["total_price"] / cltv_c["total_transaction"]

    # purchase_frequency
    cltv_c["purchase_frequency"] = cltv_c["total_transaction"] / cltv_c.shape[0]

    # repeat rate & churn rate
    repeat_rate = cltv_c[cltv_c.total_transaction > 1].shape[0] / cltv_c.shape[0]
    churn_rate = 1 - repeat_rate


    # profit_margin
    cltv_c["profit_margin"] = cltv_c["total_price"] * profit

    # Customer Value
    cltv_c["customer_value"] = (cltv_c["avg_order_value"] * cltv_c["purchase_frequency"])

    # Customer Lifetime Value
    cltv_c["cltv"] = (cltv_c["customer_value"] / churn_rate) * cltv_c["profit_margin"]


    # Segment
    cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])


    return cltv_c



df = df_.copy()

clv = create_cltv_c(df)

#########################################################################################
# MÜŞTERİ YAŞAM BOYU DEĞERİ TAHMİNİ (CUSTOMER LIFETIME VALUE PREDICTION)
#########################################################################################


#########################################################################################
# BG-NBD ve Gamma-Gamma ile CLTV Prediction
#########################################################################################
# BG: Beta Geometric
# NBD: Negative Binomial Distribution

# 1. Verinin Hazırlanması (Data Preperation)
# 2. BG-NBD Modeli ile Expected Number of Transaction
# 3. Gamma-Gamma Modeli ile Expected Average Profit
# 4. BG-NBD ve Gamma-Gamma Modeli ile CLTV'nin Hesaplanması
# 5. CLTV'ye Göre Segmentlerin Oluşturulması
# 6. Çalışmanın fonksiyonlaştırılması


##############################################################
# 1. Verinin Hazırlanması (Data Preperation)
##############################################################

# Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre
# pazarlama stratejileri belirlemek istiyor.

# Veri Seti Hikayesi

# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

# Değişkenler

# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.


##########################
# Gerekli Kütüphane ve Fonksiyonlar
##########################

# !pip install lifetimes console den yapılmalı
# Aşağıdaki kütüphaneleri kullanabilmek için gerekli
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions

pd.set_option("display.max_columns", None) # max kolon sayısı olmasın, tüm sütunları göster
pd.set_option("display.width", 500) # sütunları aşağıya inmeden yanyana göster 500 adet olana kadar yanyana göster
pd.set_option("display.float_format", lambda x: "%.4f" % x) # virgülden sonra 4 basamak göster
# from sklearn.preprocessing import MinMaxScaler # lifetime value değeri hesaplandıktan sonra bunu 0-1 ya da 0-100 gibi değerler arasına çekmek için yapılır

# istatistiksel modeller kullanılacak, boxplot yöntemi kullanarak;
# aykırı değerleri belirli bir eşik değeri ile değiştiricez (aykırı değerleri baskılama)
# 2 fonksiyon kullancaz biri outlier_thresholds diğeri de replace_with_thresholds
# 1.sinin görevi: kendisine girilen değer için eşik değeri belirlemektir.
# aykırı değer: bir değişkenin genel dağılımı dışında olan değerdir.
# örneğin yaşta 80 olur ama 240 olmaz. 240 ın kaldırılması gerekir
# genel dağılımın dışındakileri baskılamak istiyoruz silmek değil
# bunun için: eşik değer belirlenir.
# çeyrek değerler ve çeyrek değerlerin farkı hesaplanır.
# 3. çeyrek değerin 1.5 iquier üstü ve 1.çeyreğin 1.5 iquier altındaki değerler
# üst ve alt eşik değerler olarak belirlenir.
def outlier_thresholds(dataframe, veriable):
    quartile1 = dataframe[veriable].quantile(0.01) # normalde burda 0.25 yazar
    quartile3 = dataframe[veriable].quantile(0.99) # normalde burada 0.75 yazar
    # biz bu sayıları kullandık çünkü:
    # bu projeyi bildiğimiz için bu projedeki değerler genelde aynı çerçevede eğer
    # olması gerekeni yaparsak çok sağlıklı olmaz biz şuan ufak traşlama yapıyoruz
    # şuan sadece veri setindeki aşırı problemli olan aykırı değerlerden kurtuluyoruz
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range

    return low_limit, up_limit



# 2.fonksiyon ise: yukarıdakini çağırıp aykırıları öğrenip üst ve altı öğrenip bu fonk üzt ve altı verecek
# bu üst ve altı ilgili değişkenlerdeki değerlerden üst sınırda olanlar varsa bunlara üst belirlenen değeri ata
# aynısını alt için de yap

def replace_with_thresholds(dataframe, veriable):
    low_limit, up_limit = outlier_thresholds(dataframe, veriable)
    # dataframe.loc[(dataframe[veriable] < low_limit), veriable] = low_limit
    # üstteki kodu kapattık şuan ayarlama yaptığımız için eksi değerler olmayacak
    # dolayısıyla kapattığımız kodu açık bırakabiliriz ama önlem amaçlı kapattık
    dataframe.loc[(dataframe[veriable] > up_limit), veriable] = up_limit


####################################################################################
# Verinin Okunması (Data Reading)
####################################################################################

df_ = pd.read_excel("/Users/PARS/PycharmProjects/pythonProject1/12.Data Scientist Bootcamp/Datasets/online_retail_II.xlsx",sheet_name="Year 2010-2011")
df = df_.copy()
df.describe().T
df.head()
df.isnull().sum()


# Veri Ön İşleme

df.dropna(inplace=True) # eksik değerleri kaldırma
df = df[~df["Invoice"].str.contains("C", na=False)] # iade edilen ürünleri çıkaralım
df = df[df["Quantity"] > 0] #  miktarı 0 dan büyük olanlar
df = df[df["Price"] > 0] # fiyatı 0 dan büyük olanlar

df.describe().T # betimsel istatistiklerine bakalım

replace_with_thresholds(df, "Quantity")
# verilen dataframe ve değişkende eşik değerleri hesaplar ve onun üzerinde kalanları değiştirir
replace_with_thresholds(df, "Price")

df.describe().T

df["TotalPrice"] = df["Quantity"] * df["Price"]

today_date = dt.datetime(2011, 12, 11)



################################################################################
# Lifetime Veri Yapısının Hazırlanması (Preparation of Lifetime Data Structures)
################################################################################

# recency: Son satın alma üzerinden geçen zaman. Haftalık. (kullanıcı özelinde)
# diğerlerindeki recency analiz tarihine göre son satın almadan beri geçen zaman
# buradaki recency müşterinin kendisinin ilk satın alma ile son satın almasının arasındaki zamandır.
# T: Müşterinin yaşı. Haftalık. (analiz tarihinden ne kadar süre önce ilk satın alma yapılmış)
# frequency: tekrar eden toplam satın alma sayısı (frequency>1)
# monetary: satın alma başına ortalama kazanç


# Customer ID ye göre groupby a al Invo.ceDate, Invoice, TotalPrice a aşağıdakileri uygula

cltv_df = df.groupby("Customer ID").agg({"InvoiceDate": [lambda Invoicedate: (Invoicedate.max() - Invoicedate.min()).days,
                                                         lambda Invoicedate: (today_date - Invoicedate.min()).days],
                                         "Invoice": lambda Invoice: Invoice.nunique(),
                                         "TotalPrice": lambda TotalPrice: TotalPrice.sum()})

# En üstte InvoiceDate yazan kısmı görmek istemiyorum silmek için:
cltv_df.columns = cltv_df.columns.droplevel(0)

cltv_df.columns = ["recency", "T", "frequency", "monetary"]

# monetary değeri ortalama
# recency değeri ve müşteri yaşı haftalık bunu yapalım yukarıda günlük
cltv_df["monetary"] = cltv_df["monetary"] / cltv_df["frequency"]

cltv_df.describe().T

# frequency değerinde 1 den büyük olanları alalım.
cltv_df = cltv_df[(cltv_df["frequency"] > 1)]

# müşteri yaşını haftalık yapmak için:
cltv_df["recency"] = cltv_df["recency"] / 7

# T yi de haftalık yapalım:
cltv_df["T"] = cltv_df["T"] / 7

cltv_df.describe().T
# yorum:
# recency değeri haftalık müşterilerin kaç haftadır kendi içinde alışveriş yapmadıklarını
# T değeri haftalık cinsten kendi içlerinde kaç haftadır müşterimiz olduğunu ifade etmektedir
# monetary değeri average order value yani sipariş başına bıraktıkları ortalama gelirdir.
# frequency değeri satın alma sıklığı

##################################################################################################################
# 2. BG-NBD Modelinin Kurulması (Establishment of BG-NBD Model)
#################################################################################################################

bgf = BetaGeoFitter(penalizer_coef=0.001)
# parantez içindeki ceza katsayısı: makine öğrenmesinde detaylı anlatılacak
bgf.fit(cltv_df["frequency"],
        cltv_df["recency"],
        cltv_df["T"])

# 1 hafta içerisinde en fazla satın alma gerçekleştirecek 10 müşterimiz kim?:

bgf.conditional_expected_number_of_purchases_up_to_time(1,
                                                        cltv_df["frequency"],
                                                        cltv_df["recency"],
                                                        cltv_df["T"]).sort_values(ascending=False).head(10)

# daha kısa yapmak için: burada kullanılabilir ama gamma gamma da kısayol yok
bgf.predict(1,
            cltv_df["frequency"],
            cltv_df["recency"],
            cltv_df["T"]).sort_values(ascending=False).head(10)

# tüm müşterilerin 1 hafta içinde nekadar alışveriş yapacaktır bu tahmine göre yapar ve verisetine değişken olarak eklemek istersek:
cltv_df["expected_purch_1_week"] = bgf.predict(1,
                                               cltv_df["frequency"],
                                               cltv_df["recency"],
                                               cltv_df["T"])

# büyükten küçüğe göre sıralamak istersek:
cltv_df["expected_purch_1_week"] = bgf.predict(1,
                                               cltv_df["frequency"],
                                               cltv_df["recency"],
                                               cltv_df["T"]).sort_values(ascending=False)

################################################################
# 1 ay içinde en çok satın alma beklediğimiz 10 müşteri kimdir?
################################################################

bgf.predict(4,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sort_values(ascending=False).head(10)

# verisetine değişken olarak eklemek istersek:
cltv_df["expected_purc_1_month"] = bgf.predict(4,
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T'])
# şirket adına 1 ay içinde nekadar satın alma gerçekleşecek:
bgf.predict(4,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sum()

################################################################
# 3 Ayda Tüm Şirketin Beklenen Satış Sayısı Nedir?
################################################################

bgf.predict(4 * 3,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sum()

cltv_df["expected_purc_3_month"] = bgf.predict(4 * 3,
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T'])

cltv_df["expected_purch_3_month"] = bgf.predict(4 * 3,
                                                cltv_df['frequency'],
                                                cltv_df['recency'],
                                                cltv_df['T'])
################################################################
# Tahmin Sonuçlarının Değerlendirilmesi
################################################################
# tahminlerin başarısı
plot_period_transactions(bgf)
plt.show(block=True)

####################################################################################################
# 3. GAMMA-GAMMA Modelinin Kurulması(Establishing the Gamma Gamma Model)
####################################################################################################
# BG/NBD satın alama sayısını modelliyordu
# Gamma Gamma ise average profit i  modelliyor
# model nesnesini kullanarak ggf yi fit et
ggf = GammaGammaFitter(penalizer_coef=0.01)

ggf.fit(cltv_df["frequency"], cltv_df["monetary"])

ggf.conditional_expected_average_profit(cltv_df["frequency"],
                                        cltv_df["monetary"]).head(10)

# azalan şekilde sıralamak istersek: tüm müşterilerin içinde beklenen karı azalan şekilde ilk 10u verdi
ggf.conditional_expected_average_profit(cltv_df["frequency"],
                                        cltv_df["monetary"]).sort_values(ascending=False).head(10)

# verisetine eklemek istersek:
cltv_df["expected_average_profit"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                             cltv_df['monetary'])
#azalan şekilde sıralamak istersek tüm dataframe i görmek istersek beklenen değere göre sıralamak istersek
cltv_df.sort_values("expected_average_profit", ascending=False).head(10)


######################################################################################
# 4. BG-NBD ve GG modeli ile CLTV'nin hesaplanması(Calculation of CLTV with BG-NBD and GG Model)
######################################################################################

# bg-nbd modeli ve gamma modelini daha önce kurmuştuk
# ccltv (customer life time metodu) derki:
# gamma gamma ve bg-nbd modellerini, frequency, recency, T, monetary ve bana bir zaman ver (aylık olarak)
# T ve recency için zamanın hangi frekansta olduğunu ver bu da w (week), haftalık
# discount_rate ise zaman içerisinde satılan ürünlerde ürün oranı olabilir bunu göz ardı etme
cltv = ggf.customer_lifetime_value(bgf,
                                    cltv_df["frequency"],
                                    cltv_df["recency"],
                                    cltv_df["T"],
                                    cltv_df["monetary"],
                                    time=3, # 3aylık
                                    freq="W",# Tnin frekans bilgisi
                                    discount_rate=0.01 )
cltv.head()

cltv = cltv.reset_index() # index leri değişkene çeviyoruz
# çünkü index lerde olan customer id değişkene dönüştü
# index lerde 1,2, 3 gibi sayılar değil customer id ler var bunu düzelttik

# tüm veriyi bir araya getirelim
# daha önce cltv_df ve cltv leri birleştirelim ki sağlıklı bir çıktı elde edelim
cltv_final = cltv_df.merge(cltv, on="Customer ID", how= "left")
# how=left birlestirmeyi soldan yap yani cltv_df in üzerine ekle
# customer Id  yi değişkenini baz alarak birleştir

# clv ye göre azalan şekilde sırala
cltv_final.sort_values(by="clv", ascending=False).head(10)

# YORUMLAR
# 3 aylık müşteri yaşam boyu değerine ulaştık
# recency değeri yüksek olan müşteriler en büyük değeri vadediyor
# bg-nbd modelinde buy till you die prensibi der ki
# düzenli bir müşterin churn olmadıysa (dropout olmadıysa)
# müşterinin recency si arttıkça satın alma olasılığı artar der.
# potansiyeli yüksek müşteriyi de yakalar
# yeni müşteriyi de yakalar
# eski müşteriyi de yakalar

###############################################################################################
# 5. CLTV'ye Göre Segmentlerin Oluşturulması (Creating thr Customer Segment)
###############################################################################################

# önce son oluşan verisetimizi görelim:
cltv_final

# segmentlere ayıralım 4 gruba ayıralım ve clv değerine göre küçükten büyüğe sıralasın
# 0-25 e d , 25-50 ye c, 50-75 e b, 75-100e a desin
cltv_final["segment"] = pd.qcut(cltv_final["clv"], 4, labels=["D", "C", "B", "A"])

# clv ye göre sıralayalım en büyükten küçüğe doğru sıralansın
# ilk 50 değeri görelim
cltv_final.sort_values(by="clv", ascending=False).head(50)

# segment e göre groupby a alıp betimsel istatistikleri görelim:
cltv_final.groupby("segment").agg(
    {"count", "mean", "sum"})



###############################################################################################
# 6. Çalışmanın Fonksiyonlaştırılması (Functionalization)
###############################################################################################

def create_cltv_p(dataframe, month=3):
    # 1. Veri Ön İşleme
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    today_date = dt.datetime(2011, 12, 11)

    cltv_df = dataframe.groupby('Customer ID').agg(
        {'InvoiceDate': [lambda InvoiceDate: (InvoiceDate.max() - InvoiceDate.min()).days,
                         lambda InvoiceDate: (today_date - InvoiceDate.min()).days],
         'Invoice': lambda Invoice: Invoice.nunique(),
         'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

    cltv_df.columns = cltv_df.columns.droplevel(0)
    cltv_df.columns = ['recency', 'T', 'frequency', 'monetary']
    cltv_df["monetary"] = cltv_df["monetary"] / cltv_df["frequency"]
    cltv_df = cltv_df[(cltv_df['frequency'] > 1)]
    cltv_df["recency"] = cltv_df["recency"] / 7
    cltv_df["T"] = cltv_df["T"] / 7

    # 2. BG-NBD Modelinin Kurulması
    bgf = BetaGeoFitter(penalizer_coef=0.001)
    bgf.fit(cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T'])

    cltv_df["expected_purc_1_week"] = bgf.predict(1,
                                                  cltv_df['frequency'],
                                                  cltv_df['recency'],
                                                  cltv_df['T'])

    cltv_df["expected_purc_1_month"] = bgf.predict(4,
                                                   cltv_df['frequency'],
                                                   cltv_df['recency'],
                                                   cltv_df['T'])

    cltv_df["expected_purc_3_month"] = bgf.predict(12,
                                                   cltv_df['frequency'],
                                                   cltv_df['recency'],
                                                   cltv_df['T'])


    # 3. GAMMA-GAMMA Modelinin Kurulması
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(cltv_df['frequency'], cltv_df['monetary'])
    cltv_df["expected_average_profit"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                                 cltv_df['monetary'])

    # 4. BG-NBD ve GG modeli ile CLTV'nin hesaplanması.
    cltv = ggf.customer_lifetime_value(bgf,
                                       cltv_df['frequency'],
                                       cltv_df['recency'],
                                       cltv_df['T'],
                                       cltv_df['monetary'],
                                       time=month,  # 3 aylık
                                       freq="W",  # T'nin frekans bilgisi.
                                       discount_rate=0.01)

    cltv = cltv.reset_index()
    cltv_final = cltv_df.merge(cltv, on="Customer ID", how="left")
    cltv_final["segment"] = pd.qcut(cltv_final["clv"], 4, labels=["D", "C", "B", "A"])

    return cltv_final


df = df_.copy()
# son yaptığımız fonk saklamak istersek:
cltv_final2 = create_cltv_p(df)

cltv_final2.to_csv("cltv_prediction.csv")











