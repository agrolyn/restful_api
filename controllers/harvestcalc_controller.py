from flask import *
from datetime import datetime, timedelta

# Fungsi untuk perhitungan panen jagung
def harvest_corn(tanggal_tanam, luas_sawah):
    try:
        # Konversi tanggal tanam
        tanggal_tanam = datetime.strptime(tanggal_tanam, '%Y-%m-%d')
        tanggal_panen = tanggal_tanam + timedelta(days=100)  # Masa panen jagung rata-rata 100 hari
        sisa_hari = (tanggal_panen - datetime.now()).days
        
        # Perhitungan hasil panen dan harga
        hasil_per_meter = 0.4  # Hasil rata-rata jagung dalam ton per m²
        harga_per_kg = 5000    # Harga per kilogram jagung
        
        total_hasil = luas_sawah * hasil_per_meter  # Total hasil dalam ton
        total_harga = int(total_hasil * 1000 * harga_per_kg)  # Konversi ton ke kg dan ke integer
        
        return jsonify({
            "tanggal_panen": tanggal_panen.strftime('%Y-%m-%d'),  # String (format date)
            "sisa_hari": int(abs(sisa_hari)),  # Integer
            "total_hasil_ton": float(total_hasil),  # Float
            "total_hasil_kilogram": float(total_hasil) * 1000,
            "total_harga_rupiah": total_harga  # Integer
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Fungsi untuk perhitungan panen padi
def harvest_rice(tanggal_tanam, luas_sawah):
    try:
        # Konversi tanggal tanam
        tanggal_tanam = datetime.strptime(tanggal_tanam, '%Y-%m-%d')
        tanggal_panen = tanggal_tanam + timedelta(days=120)  # Masa panen padi rata-rata 120 hari
        sisa_hari = (tanggal_panen - datetime.now()).days
        
        # Perhitungan hasil panen dan harga
        hasil_per_meter = 0.6  # Hasil rata-rata padi dalam ton per m²
        harga_per_kg = 6000    # Harga per kilogram padi
        
        total_hasil = luas_sawah * hasil_per_meter  # Total hasil dalam ton
        total_harga = int(total_hasil * 1000 * harga_per_kg)  # Konversi ton ke kg dan ke integer
        
        return jsonify({
            "tanggal_panen": tanggal_panen.strftime('%Y-%m-%d'),  # String (format date)
            "sisa_hari": int(abs(sisa_hari)),  # Integer
            "total_hasil_ton": float(total_hasil),  # Float
            "total_hasil_kilogram": float(total_hasil) * 1000,
            "total_harga_rupiah": total_harga  # Integer
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def harvestcalc(plant):
    data = request.get_json()
    tanggal_tanam =  data.get('tanggal_tanam')
    luas_sawah =  data.get('luas_sawah')
    
    if plant == 'corn':
        return harvest_corn(tanggal_tanam, luas_sawah)
    elif plant == 'rice':
        return harvest_rice(tanggal_tanam, luas_sawah)
    else:
        return jsonify({
            "message": "Failed calculation, not valid name of plant"
        }), 404