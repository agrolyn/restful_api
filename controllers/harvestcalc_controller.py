from flask import *
from datetime import datetime, timedelta

def harvest_corn(tanggal_tanam, luas_sawah, harga_per_kg=None):
    try:
        # Konversi tanggal tanam
        tanggal_tanam = datetime.strptime(tanggal_tanam, '%Y-%m-%d')
        tanggal_panen = tanggal_tanam + timedelta(days=100)
        sisa_hari = (tanggal_panen - datetime.now()).days
        
        # Perhitungan hasil panen dan harga
        hasil_per_meter = 0.4 
        harga_per_kg = harga_per_kg if harga_per_kg is not None else 5000
        
        total_hasil = luas_sawah * hasil_per_meter
        total_harga = int(total_hasil * 1000 * harga_per_kg)
        
        return jsonify({
            "tanggal_panen": tanggal_panen.strftime('%Y-%m-%d'),
            "sisa_hari": int(abs(sisa_hari)),
            "total_hasil_ton": float(total_hasil),
            "total_hasil_kilogram": float(total_hasil) * 1000,
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
        tanggal_panen = tanggal_tanam + timedelta(days=120)
        sisa_hari = (tanggal_panen - datetime.now()).days
        
        # Perhitungan hasil panen dan harga
        hasil_per_meter = 0.6
        harga_per_kg = harga_per_kg if harga_per_kg is not None else 6000
        
        total_hasil = luas_sawah * hasil_per_meter
        total_harga = int(total_hasil * 1000 * harga_per_kg)
        
        return jsonify({
            "tanggal_panen": tanggal_panen.strftime('%Y-%m-%d'),
            "sisa_hari": int(abs(sisa_hari)),
            "total_hasil_ton": float(total_hasil),
            "total_hasil_kilogram": float(total_hasil) * 1000,
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
