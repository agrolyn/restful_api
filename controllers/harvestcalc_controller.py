from flask import *
from datetime import datetime, timedelta

def harvest_corn(tanggal_tanam, luas_sawah, harga_per_kg=None):
    try:
        # Konversi tanggal tanam
        tanggal_tanam = datetime.strptime(tanggal_tanam, '%Y-%m-%d')
        tanggal_panen = tanggal_tanam + timedelta(days=100)
        sisa_hari = (tanggal_panen - datetime.now()).days
        
        # Perhitungan hasil panen dan harga
        hasil_per_meter = 0.57  # hasil dalam kg/m²
        harga_per_kg = harga_per_kg if harga_per_kg is not None else 5160  # harga jagung nasional tingkat produsen
        
        total_hasil = (luas_sawah * 10000) * hasil_per_meter  # total hasil dalam kilogram
        total_harga = int(total_hasil * harga_per_kg)  # total harga langsung dihitung
        
        return jsonify({
            "tanggal_panen": tanggal_panen.strftime('%Y-%m-%d'),
            "sisa_hari": int(abs(sisa_hari)),
            "total_hasil_ton": float(total_hasil) / 1000,  # konversi ke ton jika diperlukan
            "total_hasil_kilogram": float(total_hasil),  # total hasil dalam kg
            "harga_per_kg": harga_per_kg,
            "total_harga_rupiah": total_harga
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Fungsi untuk perhitungan panen padi
def harvest_rice(tanggal_tanam, luas_sawah, harga_per_kg=None):
    try:
        # Konversi tanggal tanam
        tanggal_tanam = datetime.strptime(tanggal_tanam, '%Y-%m-%d')
        tanggal_panen = tanggal_tanam + timedelta(days=120)  # Masa tanam padi rata-rata 120 hari
        sisa_hari = (tanggal_panen - datetime.now()).days
        
        # Perhitungan hasil panen dan harga
        hasil_per_meter = 0.511  # Hasil dalam kg/m²
        harga_per_kg = harga_per_kg if harga_per_kg is not None else 5624  # Harga gabah nasional tingkat produsen
        
        total_hasil = (luas_sawah * 10000) * hasil_per_meter  # Total hasil dalam kilogram
        total_harga = int(total_hasil * harga_per_kg)  # Total harga langsung dihitung
        
        return jsonify({
            "tanggal_panen": tanggal_panen.strftime('%Y-%m-%d'),
            "sisa_hari": int(abs(sisa_hari)),
            "total_hasil_ton": float(total_hasil) / 1000,  # Konversi ke ton jika diperlukan
            "total_hasil_kilogram": float(total_hasil),  # Total hasil dalam kilogram
            "harga_per_kg": harga_per_kg,
            "total_harga_rupiah": total_harga
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def harvestcalc(plant):
    data = request.get_json()
    tanggal_tanam = data.get('tanggal_tanam')
    luas_sawah = data.get('luas_sawah')
    harga_per_kg = data.get('harga_per_kg')
    
    if plant == 'corn':
        return harvest_corn(tanggal_tanam, luas_sawah, harga_per_kg)
    elif plant == 'rice':
        return harvest_rice(tanggal_tanam, luas_sawah, harga_per_kg)
    else:
        return jsonify({
            "message": "Failed calculation, not valid name of plant"
        }), 404
