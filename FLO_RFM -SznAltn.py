
###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

###############################################################
# İş Problemi (Business Problem)
###############################################################
# FLO müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor.
# Buna yönelik olarak müşterilerin davranışları tanımlanacak ve bu davranış öbeklenmelerine göre gruplar oluşturulacak..

###############################################################
# Veri Seti Hikayesi
###############################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından
# elde edilen bilgilerden oluşmaktadır.

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi

###############################################################
# GÖREVLER
###############################################################

# GÖREV 1: Veriyi Anlama (Data Understanding) ve Hazırlama
# 1. flo_data_20K.csv verisini okuyunuz.
######################################################################################
import datetime as dt
import pandas as pd
pd.set_option("display.max_columns", None) # max kolon(sütun) sayısı olmasın.
# tüm sütunlar görünsün
# pd.set_option("display.max_rows", None) # max satır sayısı olmasın
# çıktı kalabalık olmasın diye yorum satırı yaptık
pd.set_option("display.width", 500)
pd.set_option("display.float_format", lambda x: "%.3f" % x)
# sayısal değişkenlerin virgülden sonra kaç basamağını göstersin,
# 3 yazdık o yüzden virgülden sonra 3 basamak görünür.
df_ = pd.read_csv("Datasets/flo_data_20k.csv")
df = df_.copy()
########################################################################################
# 2. Veri setinde
# a. İlk 10 gözlem,
########################################################################################

df.head(10)
df["interested_in_categories_12"]
########################################################################################
# b. Değişken isimleri,
########################################################################################

df.columns # değişkenlerin isimleri
df.info() # değişkenlerin isimleri detaylı bilgi

#########################################################################################
# c. Betimsel istatistik,
#########################################################################################

df.describe().T

#########################################################################################
# d. Boş değer,
#########################################################################################

df.isnull().sum() # boş değerlerin toplamı
df.isnull().values.any() # boş değer var mı hiç

#########################################################################################
 # e. Değişken tipleri, incelemesi yapınız.
#########################################################################################

df.info()

#########################################################################################
# 3. Omnichannel müşterilerin hem online'dan hemde offline
# platformlardan alışveriş yaptığını ifade etmektedir.
# Herbir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
##########################################################################################
# her bir müşterinin yaptığı toplam alışveriş sayısı
df["order_num_total_ever"] = df["order_num_total_ever_offline"] + df["order_num_total_ever_online"]

# her bir müşterin yaptığı toplam alışveriş harcaması
df["customer_value_total_ever"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

############################################################################################
# 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
#############################################################################################
df.info() # veri setindeki değişken tipleri

# tip değiştirme 1. yol:
for i in df.columns:
        if "date" in i:
            df[i] = df[i].apply(pd.to_datetime)

# tip değiştirme 2. yol: list comprehension
[df[i].apply(pd.to_datetime) for i in df.columns if "date" in i]

# tip değiştirme 3. yol:
df["last_order_date"] = df["last_order_date"].apply(pd.to_datetime)
df["first_order_date"] = df["last_order_date"].apply(pd.to_datetime)
df["last_order_date_offline"] = df["last_order_date"].apply(pd.to_datetime)
df["last_order_date_online"] = df["last_order_date"].apply(pd.to_datetime)
df.info()

##########################################################################################
# 5. Alışveriş kanallarındaki müşteri sayısının,
# ortalama alınan ürün sayısının ve ortalama harcamaların dağılımına bakınız.
##########################################################################################
# groupby ile:

df.groupby("order_channel").agg({"order_num_total_ever": ["sum", "mean"],
                                 "customer_value_total_ever":["sum", "mean"]})

# pivot_table ile:
df.pivot_table(["order_num_total_ever", "customer_value_total_ever"],
               "order_channel",  aggfunc=["sum", "mean"])

############################################################################################
# 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
############################################################################################

# en fazla kazancı getiren ilk 10 müşterinin tüm bilgileri:
df.sort_values(by="customer_value_total_ever", ascending=False).head(10)

# daha sade görmek istersek:
df["customer_value_total_ever"].sort_values(ascending=False).head(10)

###############################################################################################
# 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
###############################################################################################

# en fazla sipariş veren ilk 10 müşterinin tüm bilgileri:
df.sort_values(by="order_num_total_ever", ascending=False).head(10)

# daha sade görmek istersek:
df["order_num_total_ever"].sort_values(ascending=False).head(10)

#################################################################################################
# 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.
#################################################################################################
df.shape # boyut bilgisi
df.isnull().sum() # eksik değer sayıları
df.dropna(inplace=True) # eksik değerleri silmek için
df.shape # tekrar verimizi inceledik
df.describe().T # özet istatistikleri, betimsel istatistikleri

df["order_num_total_ever"].sort_values(ascending=True).head(10)
# buna baktım çünkü ödeme tutarı en düşükleri görmek için



#################################################################################################
# GÖREV 2: RFM Metriklerinin Hesaplanması
#################################################################################################

# en son yapılan alışveriş tarihi
df["last_order_date"].max()

# Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi
today_date = dt.datetime(2021, 6, 1 )


# customer_id, recency, frequnecy ve monetary değerlerinin yer aldığı yeni bir rfm dataframe

rfm = df.groupby("master_id").agg({"last_order_date": lambda last_order_date: (today_date - last_order_date.max()).days,
                                     "order_num_total_ever": lambda order_num_total_ever: order_num_total_ever,
                                     "customer_value_total_ever": lambda customer_value_total_ever: customer_value_total_ever.sum()})

rfm.head()

# değişkenlerin isimlerini kendi istediğimiz gibi yapalım:
rfm.columns = ["recency", "frequency", "monetary"]

rfm.head() # gözlemleyelim

rfm.describe().T # betimsel istatistikleri

rfm["frequency"].sort_values(ascending=False) # sıklığı
rfm["monetary"].sort_values(ascending=False) # parasal getirisi
rfm["recency"].sort_values(ascending=False) # yeniliği

rfm["monetary"].sort_values(ascending=True) # parasal değeri en az kaç diye baktım

######################################################################################################
# GÖREV 3: RF ve RFM Skorlarının Hesaplanması (Calculating RF and RFM Scores)
######################################################################################################

#  Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çevrilmesi ve
# Bu skorları recency_score, frequency_score ve monetary_score olarak kaydedilmesi

# recency değişkenini küçükten büyüğe sırala 5 parçaya böl küçük olana 5 , büyük olana 1 ismini ver
rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])

# monetary değişkenini küçükten büyüğe sırala 5 parçaya böl küçük olana 1 , büyük olana 5 ismini ver
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])

# monetary değişkenini küçükten büyüğe sırala 5 parçaya böl küçük olana 1 , büyük olana 5 ismini ver
# rfm["frequency_score"] = pd.qcut(rfm["frequency"], 5, labels=[1, 2, 3, 4, 5])

# hata aldık çünkü aralıklarda unique değerler yer almıyor hatası verdi
# çünkü daha fazla sayıda aralığa hep aynı değerler denk gelmiş
# bunu çözmek için rank methodunu kullanıyoruz.

# doğrusu:
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])



# recency_score ve frequency_score’u tek bir değişken olarak ifade edilmesi ve RF_SCORE olarak kaydedilmesi

rfm["RF_SCORE"] = (rfm["recency_score"].astype(str) +
                    rfm["frequency_score"].astype(str))

rfm.describe().T

# bonus

# şampiyonları görmek için:
rfm[rfm["RF_SCORE"] == "55"]

# sıkıntılı müşteriler
rfm[rfm["RF_SCORE"] == "11"]


#########################################################################################################
# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması
#########################################################################################################

# Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlama ve
# tanımlanan seg_map yardımı ile RF_SCORE'u segmentlere çevirme

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

rfm["segment"] = rfm["RF_SCORE"].replace(seg_map, regex=True)

###############################################################
# GÖREV 5: Aksiyon zamanı!
###############################################################

# 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.

# rfm nin içinden metrikleri bulup, ortalamalarını ve toplamını görelim:
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])


# 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv ye kaydediniz.
# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor.
# Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde.
# Bu nedenle markanın tanıtımı ve ürün satışları için ilgilenecek profildeki
# müşterilerle özel olarak iletişime geçeilmek isteniliyor.
# Sadık müşterilerinden(champions,loyal_customers),
# ortalama 250 TL üzeri ve kadın kategorisinden alışveriş yapan kişiler özel olarak iletişim kuralacak müşteriler.
# Bu müşterilerin id numaralarını csv dosyasına
# yeni_marka_hedef_müşteri_id.cvs olarak kaydediniz.





# b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşterilerden olan ama uzun süredir
# alışveriş yapmayan ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
# olarak kaydediniz.


# GÖREV 6: Tüm süreci fonksiyonlaştırınız.