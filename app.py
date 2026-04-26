from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

#  KNOWLEDGE BASE — Penyakit Tanaman Cabai

PENYAKIT = {
    "C001": {
        "nama": "Antraknosa / Patek",
        "patogen": "Colletotrichum capsici",
        "jenis": "Jamur",
        "deskripsi": "Penyakit paling merusak pada cabai, terutama menyerang buah. Kerugian bisa mencapai 100% jika tidak ditangani.",
        "gejala_utama": [
            "Bercak hitam cekung pada buah cabai (muda maupun tua)",
            "Bercak melebar cepat dan buah mengkerut / membusuk",
            "Permukaan bercak terdapat spora jamur berwarna merah muda / oranye",
            "Buah gugur sebelum masak",
        ],
        "penanganan": [
            "Semprot fungisida berbahan aktif Mankozeb atau Propineb setiap 5-7 hari",
            "Petik dan musnahkan buah yang terinfeksi (jangan dibuang di kebun)",
            "Hindari luka mekanis pada buah saat panen",
            "Atur jarak tanam agar sirkulasi udara baik (60×70 cm)",
        ],
        "pencegahan": "Gunakan benih bersertifikat, rendam benih dalam fungisida sebelum semai.",
        "tingkat_bahaya": "Sangat Tinggi",
        "warna": "#dc2626",
    },
    "C002": {
        "nama": "Layu Fusarium",
        "patogen": "Fusarium oxysporum",
        "jenis": "Jamur",
        "deskripsi": "Penyakit tular tanah yang menyerang sistem pembuluh akar, menyebabkan tanaman layu mendadak meski cukup air.",
        "gejala_utama": [
            "Tanaman layu mendadak meski tanah lembab / cukup air",
            "Daun menguning dimulai dari bagian bawah tanaman",
            "Batang bagian dalam berwarna coklat jika dipotong melintang",
            "Akar membusuk berwarna coklat kehitaman",
        ],
        "penanganan": [
            "Cabut dan bakar tanaman yang terinfeksi beserta tanahnya",
            "Siram fungisida sistemik Benomil atau Karbendazim ke lubang tanam",
            "Rotasi tanaman dengan non-solanaceae minimal 2 musim",
            "Perbaiki drainase lahan, hindari genangan air",
        ],
        "pencegahan": "Sterilisasi media tanam, gunakan pupuk organik matang, hindari bekas lahan terinfeksi.",
        "tingkat_bahaya": "Sangat Tinggi",
        "warna": "#b45309",
    },
    "C003": {
        "nama": "Virus Kuning / Gemini Virus",
        "patogen": "Begomovirus (ditularkan kutu kebul)",
        "jenis": "Virus",
        "deskripsi": "Penyakit virus yang ditularkan oleh kutu kebul (Bemisia tabaci). Menyebabkan tanaman kerdil dan gagal berbuah.",
        "gejala_utama": [
            "Daun menguning cerah (kuning emas), terutama daun muda",
            "Daun menggulung ke atas atau mengeriting",
            "Pertumbuhan tanaman sangat terhambat / kerdil",
            "Ditemukan kutu kebul (serangga putih kecil) di balik daun",
        ],
        "penanganan": [
            "Cabut dan bakar tanaman yang terinfeksi virus",
            "Kendalikan kutu kebul dengan insektisida Imidakloprid atau Abamektin",
            "Pasang perangkap kuning (yellow sticky trap) di sekitar lahan",
            "Semprot insektisida sistemik sejak awal tanam sebagai proteksi",
        ],
        "pencegahan": "Gunakan mulsa plastik perak untuk mengusir kutu kebul, tanam tanaman refugia di pematang.",
        "tingkat_bahaya": "Sangat Tinggi",
        "warna": "#ca8a04",
    },
    "C004": {
        "nama": "Busuk Phytophthora",
        "patogen": "Phytophthora capsici",
        "jenis": "Oomisetes",
        "deskripsi": "Penyakit yang menyerang akar, batang, dan buah cabai. Berkembang cepat pada kondisi tanah basah dan curah hujan tinggi.",
        "gejala_utama": [
            "Pangkal batang membusuk berwarna coklat kehitaman",
            "Tanaman layu dan mati mendadak dalam 2-3 hari",
            "Buah dan daun tertutup miselium putih seperti kapas",
            "Akar membusuk total, mudah dicabut dari tanah",
        ],
        "penanganan": [
            "Aplikasi fungisida Metalaksil atau Fosetil-Al ke tanah sekitar batang",
            "Perbaiki sistem drainase, buat bedengan lebih tinggi",
            "Kurangi frekuensi penyiraman pada musim hujan",
            "Cabut tanaman mati dan ganti tanah di lubang tanam",
        ],
        "pencegahan": "Buat bedengan tinggi minimal 30 cm, aplikasi kapur pertanian sebelum tanam.",
        "tingkat_bahaya": "Tinggi",
        "warna": "#0369a1",
    },
    "C005": {
        "nama": "Bercak Daun Cercospora",
        "patogen": "Cercospora capsici",
        "jenis": "Jamur",
        "deskripsi": "Penyakit jamur yang menyerang daun dan menyebabkan daun gugur massal, melemahkan tanaman secara bertahap.",
        "gejala_utama": [
            "Bercak bulat / tidak beraturan berwarna coklat muda di tengah, coklat tua di tepi",
            "Bercak dikelilingi zona kuning (halo)",
            "Daun gugur massal dari bagian bawah ke atas",
            "Menyerang terutama saat musim hujan atau kelembaban tinggi",
        ],
        "penanganan": [
            "Semprot fungisida Klorotalonil atau Mankozeb setiap 7 hari",
            "Buang daun yang sudah terinfeksi parah",
            "Kurangi kelembaban dengan mengatur jarak tanam",
            "Hindari penyiraman di malam hari",
        ],
        "pencegahan": "Rotasi tanaman, sanitasi sisa tanaman setelah panen.",
        "tingkat_bahaya": "Sedang",
        "warna": "#16a34a",
    },
    "C006": {
        "nama": "Layu Bakteri",
        "patogen": "Ralstonia solanacearum",
        "jenis": "Bakteri",
        "deskripsi": "Penyakit bakteri tular tanah yang sangat agresif. Dapat membunuh tanaman dalam 3-5 hari setelah gejala muncul.",
        "gejala_utama": [
            "Tanaman layu mendadak namun daun masih hijau (layu hijau)",
            "Layu terjadi di siang hari dan sedikit pulih di malam hari (awalnya)",
            "Lendir bakteri keluar saat batang dipotong dan dimasukkan ke air",
            "Tidak ada perubahan warna akar (berbeda dari Fusarium)",
        ],
        "penanganan": [
            "Tidak ada obat efektif — cabut dan bakar tanaman terinfeksi",
            "Siram bakterisida Tembaga hidroksida ke lubang bekas tanaman",
            "Jangan tanam solanaceae di lokasi sama minimal 3 musim",
            "Sterilisasi alat pertanian dengan alkohol atau larutan klorin",
        ],
        "pencegahan": "Hindari lahan bekas terinfeksi, gunakan bibit sehat, aplikasi agen hayati Bacillus subtilis.",
        "tingkat_bahaya": "Sangat Tinggi",
        "warna": "#7c3aed",
    },
    "C007": {
        "nama": "Embun Tepung",
        "patogen": "Leveillula taurica",
        "jenis": "Jamur",
        "deskripsi": "Penyakit jamur yang membentuk lapisan tepung putih pada daun. Berkembang pada kondisi kering dengan kelembaban rendah.",
        "gejala_utama": [
            "Lapisan serbuk / tepung putih pada permukaan daun bagian bawah",
            "Bercak kuning tidak beraturan pada sisi atas daun",
            "Daun mengering dan gugur jika infeksi berat",
            "Menyerang saat musim kemarau dengan suhu tinggi",
        ],
        "penanganan": [
            "Semprot fungisida belerang (sulfur) atau Trifloksistrobin",
            "Hindari penyiraman berlebih pada musim kemarau",
            "Pangkas bagian tanaman yang terinfeksi berat",
            "Atur sirkulasi udara di sekitar tanaman",
        ],
        "pencegahan": "Hindari penanaman terlalu rapat, aplikasi belerang preventif saat musim kemarau.",
        "tingkat_bahaya": "Sedang",
        "warna": "#64748b",
    },
}

#  GEJALA — 25 Parameter Gejala Tanaman Cabai
SEMUA_GEJALA = {
    # Gejala Buah
    "G01": {"label": "Bercak hitam cekung pada buah cabai",                    "kategori": "Buah"},
    "G02": {"label": "Buah mengkerut / membusuk dan gugur",                    "kategori": "Buah"},
    "G03": {"label": "Spora merah muda / oranye pada permukaan bercak buah",   "kategori": "Buah"},
    "G04": {"label": "Buah tertutup miselium / lapisan seperti kapas",         "kategori": "Buah"},
    # Gejala Daun
    "G05": {"label": "Daun menguning dari bagian bawah tanaman",               "kategori": "Daun"},
    "G06": {"label": "Daun menguning cerah (kuning emas) terutama daun muda",  "kategori": "Daun"},
    "G07": {"label": "Daun menggulung ke atas atau mengeriting",               "kategori": "Daun"},
    "G08": {"label": "Bercak bulat coklat muda di tengah, coklat tua di tepi", "kategori": "Daun"},
    "G09": {"label": "Bercak dikelilingi zona / halo berwarna kuning",         "kategori": "Daun"},
    "G10": {"label": "Daun gugur massal dari bawah ke atas",                   "kategori": "Daun"},
    "G11": {"label": "Lapisan serbuk / tepung putih di bawah daun",            "kategori": "Daun"},
    "G12": {"label": "Bercak kuning tidak beraturan di sisi atas daun",        "kategori": "Daun"},
    # Gejala Batang & Akar
    "G13": {"label": "Pangkal batang membusuk berwarna coklat kehitaman",      "kategori": "Batang & Akar"},
    "G14": {"label": "Batang dalam berwarna coklat saat dipotong melintang",   "kategori": "Batang & Akar"},
    "G15": {"label": "Akar membusuk berwarna coklat / hitam",                  "kategori": "Batang & Akar"},
    "G16": {"label": "Lendir keluar dari batang saat direndam air",            "kategori": "Batang & Akar"},
    # Gejala Tanaman Keseluruhan
    "G17": {"label": "Tanaman layu mendadak meski tanah cukup lembab",         "kategori": "Tanaman"},
    "G18": {"label": "Tanaman layu di siang hari, sedikit pulih di malam hari","kategori": "Tanaman"},
    "G19": {"label": "Pertumbuhan tanaman sangat terhambat / kerdil",          "kategori": "Tanaman"},
    "G20": {"label": "Tanaman mati dalam 2–5 hari setelah gejala muncul",      "kategori": "Tanaman"},
    # Kondisi Lingkungan
    "G21": {"label": "Ditemukan kutu kebul (serangga putih kecil) di daun",    "kategori": "Lingkungan"},
    "G22": {"label": "Cuaca hujan terus / kelembaban sangat tinggi",            "kategori": "Lingkungan"},
    "G23": {"label": "Musim kemarau, cuaca kering dan panas",                  "kategori": "Lingkungan"},
    "G24": {"label": "Lahan bekas tanaman solanaceae (tomat, terong, dll)",    "kategori": "Lingkungan"},
    "G25": {"label": "Tanah tergenang / drainase buruk",                       "kategori": "Lingkungan"},
}

#  RULES — Forward Chaining
RULES = [
    {
        "penyakit": "C001",  # Antraknosa
        "gejala_kuat":       ["G01", "G02"],
        "gejala_pendukung":  ["G03", "G22"],
        "min_kuat": 1,
        "min_total": 2,
    },
    {
        "penyakit": "C002",  # Layu Fusarium
        "gejala_kuat":       ["G14", "G15", "G17"],
        "gejala_pendukung":  ["G05", "G24"],
        "min_kuat": 2,
        "min_total": 3,
    },
    {
        "penyakit": "C003",  # Virus Kuning
        "gejala_kuat":       ["G06", "G21"],
        "gejala_pendukung":  ["G07", "G19"],
        "min_kuat": 1,
        "min_total": 2,
    },
    {
        "penyakit": "C004",  # Busuk Phytophthora
        "gejala_kuat":       ["G13", "G20"],
        "gejala_pendukung":  ["G04", "G15", "G22", "G25"],
        "min_kuat": 1,
        "min_total": 2,
    },
    {
        "penyakit": "C005",  # Bercak Cercospora
        "gejala_kuat":       ["G08", "G09"],
        "gejala_pendukung":  ["G10", "G22"],
        "min_kuat": 1,
        "min_total": 2,
    },
    {
        "penyakit": "C006",  # Layu Bakteri
        "gejala_kuat":       ["G16", "G17", "G18"],
        "gejala_pendukung":  ["G24"],
        "min_kuat": 2,
        "min_total": 2,
    },
    {
        "penyakit": "C007",  # Embun Tepung
        "gejala_kuat":       ["G11"],
        "gejala_pendukung":  ["G12", "G23"],
        "min_kuat": 1,
        "min_total": 2,
    },
]

#  FORWARD CHAINING ENGINE

def diagnosa(gejala_user: list):
    hasil = []
    for rule in RULES:
        kuat_cocok   = [g for g in rule["gejala_kuat"]      if g in gejala_user]
        dukung_cocok = [g for g in rule["gejala_pendukung"] if g in gejala_user]

        if len(kuat_cocok) < rule["min_kuat"]:
            continue
        if len(kuat_cocok) + len(dukung_cocok) < rule["min_total"]:
            continue

        bobot_cocok = len(kuat_cocok) * 2 + len(dukung_cocok)
        bobot_total = len(rule["gejala_kuat"]) * 2 + len(rule["gejala_pendukung"])
        confidence  = round((bobot_cocok / bobot_total) * 100, 1)

        p = PENYAKIT[rule["penyakit"]]
        hasil.append({
            "id": rule["penyakit"],
            "nama": p["nama"],
            "patogen": p["patogen"],
            "jenis": p["jenis"],
            "deskripsi": p["deskripsi"],
            "gejala_utama": p["gejala_utama"],
            "penanganan": p["penanganan"],
            "pencegahan": p["pencegahan"],
            "tingkat_bahaya": p["tingkat_bahaya"],
            "warna": p["warna"],
            "confidence": confidence,
            "gejala_kuat_cocok": kuat_cocok,
            "gejala_semua_cocok": kuat_cocok + dukung_cocok,
        })

    hasil.sort(key=lambda x: x["confidence"], reverse=True)
    return hasil

#  ROUTES

@app.route("/")
def index():
    kategori_map = {}
    for gid, gdata in SEMUA_GEJALA.items():
        kat = gdata["kategori"]
        if kat not in kategori_map:
            kategori_map[kat] = []
        kategori_map[kat].append({"id": gid, "label": gdata["label"]})
    return render_template("index.html", kategori_map=kategori_map)

@app.route("/diagnosa", methods=["POST"])
def route_diagnosa():
    data        = request.get_json()
    gejala_user = data.get("gejala", [])
    if not gejala_user:
        return jsonify({"error": "Pilih minimal 1 gejala"}), 400
    hasil = diagnosa(gejala_user)
    gejala_labels = {gid: SEMUA_GEJALA[gid]["label"] for gid in gejala_user if gid in SEMUA_GEJALA}
    return jsonify({
        "hasil":        hasil,
        "total_gejala": len(gejala_user),
        "gejala_labels": gejala_labels,
        "ditemukan":    len(hasil),
    })

if __name__ == "__main__":
    app.run(debug=True, port=3000)
