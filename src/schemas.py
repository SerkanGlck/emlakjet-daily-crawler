from marshmallow import Schema, fields

class IlanSchema(Schema):
    url = fields.String(required=True)
    baslik = fields.String(required=True)
    fiyat = fields.String(required=True)
    konum = fields.String(required=True)
    Ilan_Numarasi = fields.String(required=True)
    İlan_Numarası = fields.String(required=True)
    İlan_Güncelleme_Tarihi = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    Kategorisi = fields.String()
    Net_Metrekare = fields.String()
    Oda_Sayısı = fields.String()
    Bulunduğu_Kat = fields.String()
    Isıtma_Tipi = fields.String()
    Kullanım_Durumu = fields.String()
    Site_İçerisinde = fields.String()
    Fiyat_Durumu = fields.String()
    İlan_Oluşturma_Tarihi = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    Türü = fields.String()
    Tipi = fields.String()
    Brüt_Metrekare = fields.String()
    Binanın_Yaşı = fields.String()
    Binanın_Kat_Sayısı = fields.String()
    İzin_Belge_No = fields.String()
    Eşya_Durumu = fields.String()
    Banyo_Sayısı = fields.String()