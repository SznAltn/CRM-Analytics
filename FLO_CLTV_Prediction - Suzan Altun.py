##############################################################
# BG-NBD ve Gamma-Gamma ile CLTV Prediction
##############################################################

###############################################################
# İş Problemi (Business Problem)
###############################################################
# FLO satış ve pazarlama faaliyetleri için roadmap belirlemek istemektedir.
# Şirketin orta uzun vadeli plan yapabilmesi için var olan müşterilerin
# gelecekte şirkete sağlayacakları potansiyel değerin tahmin edilmesi gerekmektedir.


###############################################################
# Veri Seti Hikayesi
###############################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan)
# olarak yapan müşterilerin geçmiş alışveriş davranışlarından
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
# GÖREV 1: Veriyi Hazırlama
           # 1. flo_data_20K.csv verisini okuyunuz.Dataframe’in kopyasını oluşturunuz.
           # 2. Aykırı değerleri baskılamak için gerekli olan outlier_thresholds ve replace_with_thresholds fonksiyonlarını tanımlayınız.
           # Not: cltv hesaplanırken frequency değerleri integer olması gerekmektedir.Bu nedenle alt ve üst limitlerini round() ile yuvarlayınız.
           # 3. "order_num_total_ever_online","order_num_total_ever_offline","customer_value_total_ever_offline","customer_value_total_ever_online" değişkenlerinin
           # aykırı değerleri varsa baskılayanız.
           # 4. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Herbir müşterinin toplam
           # alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
           # 5. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.

# GÖREV 2: CLTV Veri Yapısının Oluşturulması
           # 1.Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi olarak alınız.
           # 2.customer_id, recency_cltv_weekly, T_weekly, frequency ve monetary_cltv_avg değerlerinin yer aldığı yeni bir cltv dataframe'i oluşturunuz.
           # Monetary değeri satın alma başına ortalama değer olarak, recency ve tenure değerleri ise haftalık cinsten ifade edilecek.


# GÖREV 3: BG/NBD, Gamma-Gamma Modellerinin Kurulması, CLTV'nin hesaplanması
           # 1. BG/NBD modelini fit ediniz.
                # a. 3 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_3_month olarak cltv dataframe'ine ekleyiniz.
                # b. 6 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_6_month olarak cltv dataframe'ine ekleyiniz.
           # 2. Gamma-Gamma modelini fit ediniz. Müşterilerin ortalama bırakacakları değeri tahminleyip exp_average_value olarak cltv dataframe'ine ekleyiniz.
           # 3. 6 aylık CLTV hesaplayınız ve cltv ismiyle dataframe'e ekleyiniz.
                # b. Cltv değeri en yüksek 20 kişiyi gözlemleyiniz.

# GÖREV 4: CLTV'ye Göre Segmentlerin Oluşturulması
           # 1. 6 aylık tüm müşterilerinizi 4 gruba (segmente) ayırınız ve grup isimlerini veri setine ekleyiniz. cltv_segment ismi ile dataframe'e ekleyiniz.
           # 2. 4 grup içerisinden seçeceğiniz 2 grup için yönetime kısa kısa 6 aylık aksiyon önerilerinde bulununuz

# BONUS: Tüm süreci fonksiyonlaştırınız.


###############################################################
# GÖREV 1: Veriyi Hazırlama
###############################################################

#######################################################################################################################
# 1. OmniChannel.csv verisini okuyunuz.Dataframe’in kopyasını oluşturunuz.
#######################################################################################################################
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions


pd.set_option("display.max_columns", None) # max kolon(sütun) sayısı olmasın, tüm sütunları göster
# pd.set_option("display.max_rows", None) # max satır sayısı olmasın
# çıktı kalabalık olmasın diye yorum satırı yaptık
pd.set_option("display.width", 500)
# sütunları aşağıya inmeden yanyana göster 500 adet olana kadar yanyana göster
pd.set_option("display.float_format", lambda x: "%.3f" % x)
# sayısal değişkenlerin virgülden sonra kaç basamağını göstersin,
# 3 yazdık o yüzden virgülden sonra 3 basamak görünür.
# from sklearn.preprocessing import MinMaxScaler
# lifetime value değeri hesaplandıktan sonra bunu 0-1 ya da 0-100 gibi değerler arasına çekmek için yapılır

df_ = pd.read_csv("Datasets/flo_data_20k.csv")
df = df_.copy()

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

#######################################################################################################################
# 2. Aykırı değerleri baskılamak için gerekli olan outlier_thresholds ve
# replace_with_thresholds fonksiyonlarını tanımlayınız.
# Not: cltv hesaplanırken frequency değerleri integer olması gerekmektedir.
# Bu nedenle alt ve üst limitlerini round() ile yuvarlayınız.
#######################################################################################################################

def outlier_thresholds(dataframe, veriable):
    quartile1 = dataframe[veriable].quantile(0.01) # normalde burda 0.25 yazar
    quartile3 = dataframe[veriable].quantile(0.99) # normalde burada 0.75 yazar
    # biz bu sayıları kullandık çünkü:
    # bu projeyi bildiğimiz için bu projedeki değerler genelde aynı çerçevede eğer
    # olması gerekeni yaparsak çok sağlıklı olmaz biz şuan ufak traşlama yapıyoruz
    # şuan sadece veri setindeki aşırı problemli olan aykırı değerlerden kurtuluyoruz
    interquantile_range = quartile3 - quartile1
    up_limit = round(quartile3 + 1.5 * interquantile_range)
    low_limit = round(quartile1 - 1.5 * interquantile_range)

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


#############################################################################################################
# 3. "order_num_total_ever_online","order_num_total_ever_offline",
# "customer_value_total_ever_offline","customer_value_total_ever_online" değişkenlerinin
#aykırı değerleri varsa baskılayanız.
#############################################################################################################
df.describe().T # betimsel istatistiklerine bakalım

replace_with_thresholds(df,"order_num_total_ever_online" )
# verilen dataframe ve değişkende eşik değerleri hesaplar ve onun üzerinde kalanları değiştirir
replace_with_thresholds(df, "order_num_total_ever_offline")
replace_with_thresholds(df, "customer_value_total_ever_offline")
replace_with_thresholds(df, "customer_value_total_ever_online")


##################################################################################################
# 4. Omnichannel müşterilerin hem online'dan hemde offline platformlardan
# alışveriş yaptığını ifade etmektedir.
# Herbir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
##################################################################################################
# her bir müşterinin yaptığı toplam alışveriş sayısı
df["order_num_total_ever"] = df["order_num_total_ever_offline"] + df["order_num_total_ever_online"]

# her bir müşterin yaptığı toplam alışveriş harcaması
df["customer_value_total_ever"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]


####################################################################################################
# 5. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
#####################################################################################################

df.info() # değişken tipleri

# tip değiştirme 1. yol:
for i in df.columns:
        if "date" in i:
            df[i] = df[i].apply(pd.to_datetime)

######################################################################################################
# GÖREV 2: CLTV Veri Yapısının Oluşturulması
######################################################################################################

# 1.Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi olarak alınız.
#####################################################################################################

df["last_order_date"].max()

# Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi
today_date = dt.datetime(2021, 6, 1 )

#########################################################################################################
# 2.customer_id, recency_cltv_weekly, T_weekly, frequency ve monetary_cltv_avg değerlerinin
# yer aldığı yeni bir cltv dataframe'i oluşturunuz.
#######################################################################################################

# recency: Son satın alma üzerinden geçen zaman. Haftalık. (kullanıcı özelinde)
# diğerlerindeki recency analiz tarihine göre son satın almadan beri geçen zaman
# buradaki recency müşterinin kendisinin ilk satın alma ile son satın almasının arasındaki zamandır.
# T: Müşterinin yaşı. Haftalık. (analiz tarihinden ne kadar süre önce ilk satın alma yapılmış)
# frequency: tekrar eden toplam satın alma sayısı (frequency>1)
# monetary: satın alma başına ortalama kazanç

# önce tarih farkını gösteren yeni bir değişken oluşturalım:
df["difference_of_date"] = df["last_order_date"] - df["first_order_date"]

cltv_df = df.groupby("master_id").\
    agg({"difference_of_date": lambda difference_of_date: ((difference_of_date)/7),
         "first_order_date":  lambda first_order_date: ((today_date - first_order_date)/7),
         "order_num_total_ever": lambda order_num_total_ever: order_num_total_ever,
         "customer_value_total_ever": lambda customer_value_total_ever: customer_value_total_ever})

cltv_df.columns = ["recency_cltv_weekly", "T_weekly", "frequency", "monetary"]
cltv_df2 = pd.DataFrame()

cltv_df2['master_id'] = df['master_id']
cltv_df2['recency_cltv_weekly'] = (df['last_order_date']- df['first_order_date']).dt.days / 7
cltv_df2['T_weekly'] = (df['first_order_date'].apply(lambda x: (today_date - x))).dt.days / 7
cltv_df2['frequency'] = df['order_num_total_ever']
cltv_df2['monetary'] = df['customer_value_total_ever']


# monetary değeri ortalama
cltv_df2["monetary"] = cltv_df2["monetary"] / cltv_df2["frequency"]

cltv_df2.describe().T

# frequency değerinde 1 den büyük olanları alalım.
cltv_df2 = cltv_df2[(cltv_df2["frequency"] > 1)]

cltv_df2["frequency"].sort_values(ascending=True)
#########################################################################################
# GÖREV 3: BG/NBD, Gamma-Gamma Modellerinin Kurulması, 6 aylık CLTV'nin hesaplanması
##########################################################################################

# 1. BG/NBD modelini kurunuz.

bgf = BetaGeoFitter(penalizer_coef=0.001)
# parantez içindeki ceza katsayısı: makine öğrenmesinde detaylı anlatılacak
bgf.fit(cltv_df2["frequency"],
        cltv_df2["recency_cltv_weekly"],
        cltv_df2["T_weekly"])

# yorum:
# recency değeri haftalık müşterilerin kaç haftadır kendi içinde alışveriş yapmadıklarını
# T değeri haftalık cinsten kendi içlerinde kaç haftadır müşterimiz olduğunu ifade etmektedir
# monetary değeri average order value yani sipariş başına bıraktıkları ortalama gelirdir.
# frequency değeri satın alma sıklığı

##############################################################################################################
# 3 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve
# exp_sales_3_month olarak cltv dataframe'ine ekleyiniz.

cltv_df2.index = cltv_df2["master_id"]
# 1 aylık
cltv_df2["exp_sales_1_month "] = bgf.predict(4,
                                            cltv_df2['frequency'],
                                            cltv_df2['recency_cltv_weekly'],
                                            cltv_df2['T_weekly'])

# 3 aylık
cltv_df2["exp_sales_3_month "] = bgf.predict(4 * 3,
                                            cltv_df2['frequency'],
                                            cltv_df2['recency_cltv_weekly'],
                                            cltv_df2['T_weekly'])

############################################################################################################
# 6 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve
# exp_sales_6_month olarak cltv dataframe'ine ekleyiniz.

cltv_df2["exp_sales_6_month "] = bgf.predict(4 * 6,
                                            cltv_df2['frequency'],
                                            cltv_df2['recency_cltv_weekly'],
                                            cltv_df2['T_weekly'])

###############################################################################################################
# 3. ve 6.aydaki en çok satın alım gerçekleştirecek 10 kişiyi inceleyeniz.

# 3 aydaki en çok satın alım gerçekleştirecek 10 kişi
bgf.predict(4 * 3,
            cltv_df2["frequency"],
            cltv_df2["recency_cltv_weekly"],
            cltv_df2["T_weekly"]).sort_values(ascending=False).head(10)

# 6 aydaki en çok satın alım gerçekleştirecek 10 kişi
bgf.predict(4 * 6,
            cltv_df2["frequency"],
            cltv_df2["recency_cltv_weekly"],
            cltv_df2["T_weekly"]).sort_values(ascending=False).head(10)


# tahminlerin başarısı
plot_period_transactions(bgf)
plt.show(block=True)
#############################################################################################
# 2.  Gamma-Gamma modelini fit ediniz.
# Müşterilerin ortalama bırakacakları değeri tahminleyip
# exp_average_value olarak cltv dataframe'ine ekleyiniz.


# BG/NBD satın alama sayısını modelliyordu
# Gamma Gamma ise average profit i  modelliyor
# model nesnesini kullanarak ggf yi fit et
ggf = GammaGammaFitter(penalizer_coef=0.01)

ggf.fit(cltv_df2["frequency"], cltv_df2["monetary"])

ggf.conditional_expected_average_profit(cltv_df2["frequency"],
                                        cltv_df2["monetary"]).head(10)


# verisetine eklemek istersek:
cltv_df2["exp_average_value"] = ggf.conditional_expected_average_profit(cltv_df2['frequency'],
                                                                             cltv_df2['monetary'])
#################################################################################################################
# 3. 6 aylık CLTV hesaplayınız ve cltv ismiyle dataframe'e ekleyiniz.

cltv = ggf.customer_lifetime_value(bgf,
                                    cltv_df2["frequency"],
                                    cltv_df2["recency_cltv_weekly"],
                                    cltv_df2["T_weekly"],
                                    cltv_df2["monetary"],
                                    time=6, # 6aylık
                                    freq="W",# Tnin frekans bilgisi
                                    discount_rate=0.01 )
cltv = cltv.reset_index() # index leri değişkene çeviyoruz
# çünkü index lerde olan customer id değişkene dönüştü
# index lerde 1,2, 3 gibi sayılar değil customer id ler var bunu düzelttik

cltv_df2 = cltv_df2.drop("master_id", axis=1)

cltv.head()



# tüm veriyi bir araya getirelim
# daha önce cltv_df ve cltv leri birleştirelim ki sağlıklı bir çıktı elde edelim
cltv_final = cltv_df2.merge(cltv, on="master_id", how= "left")

###############################################################################################
# CLTV değeri en yüksek 20 kişiyi gözlemleyiniz.

# clv ye göre azalan şekilde sırala
cltv_final.sort_values(by="clv", ascending=False).head(20)



# YORUMLAR
# 6 aylık müşteri yaşam boyu değerine ulaştık
# recency değeri yüksek olan müşteriler en büyük değeri vadediyor
# bg-nbd modelinde buy till you die prensibi der ki
# düzenli bir müşterin churn olmadıysa (dropout olmadıysa)
# müşterinin recency si arttıkça satın alma olasılığı artar der.
# potansiyeli yüksek müşteriyi de yakalar
# yeni müşteriyi de yakalar
# eski müşteriyi de yakalar

###############################################################
# GÖREV 4: CLTV'ye Göre Segmentlerin Oluşturulması
###############################################################

# 1. 6 aylık CLTV'ye göre tüm müşterilerinizi 4 gruba (segmente) ayırınız ve
# grup isimlerini veri setine ekleyiniz.
# cltv_segment ismi ile atayınız.



cltv_final["cltv_segment"] = pd.qcut(cltv_final["clv"], 4, labels=["D", "C", "B", "A"])


cltv_final.groupby("cltv_segment").agg(
    {"count", "mean", "sum"})

##############################################################################################
# 2. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.

# betimsel istatikleri
cltv_final.groupby("segment").agg(
    {"count", "mean", "sum"})






