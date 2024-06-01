#PENELITIAN
#FAHRI DESRIZAL


#Import library yang diperlukan
import cv2
import schedule
import time
import datetime
import numpy as np
import csv

# Fungsi untuk melakukan pengambilan gambar dan pemrosesan
def Jumlah_Bibit():
    # Inisiasi kamera
    cam1 = cv2.VideoCapture(0)

    # Pengaturan kamera (contoh: kecerahan dan kontras)
    cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Lebar frame (resolusi)
    cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Tinggi frame (resolusi)

    # Baca frame dari kamera
    ret1, frame1 = cam1.read()

    # Jika berhasil membaca frame
    if ret1:

        #BGR to HSV 
        hsv = cv2.cvtColor(frame1,cv2.COLOR_BGR2HSV)

        #THRESHOLDING BERDASARKAN RANGE 3 CHANNEL WARNA (HSV)
        lower = np.array([18, 17, 129])
        upper = np.array([55, 96, 255]) 
        mask = cv2.inRange(hsv,lower,upper) #masking
        kernel = np.ones((1, 1), np.uint8) #untuk operasi blur, erosi, dilasi
        erosion = cv2.erode(mask, kernel, iterations=1) #operasierosi
        dilation = cv2.dilate(erosion, kernel, iterations=1) #operasidilasi
        bitwise = cv2.bitwise_and(frame1, frame1, mask=dilation) #bitwise(n)

        # VARIABLE UNTUK MENENTUKAN WAKTU
        now = datetime.datetime.now()
        waktu = now.strftime("(%H;%M WIB)")
        tanggal = now.strftime("%d-%b-%Y")

        # VARIABLE UNTUK MENENTUKAN LOKASI PENYIMPANAN CITRA
        lokasi_file_original = "/home/pi/Documents/Penelitian/Gambar/Kamera1/Ori/"
        lokasi_file_threshold = "/home/pi/Documents/Penelitian/Gambar/Kamera1/Thres/"
        lokasi_file_bitwise = "/home/pi/Documents/Penelitian/Gambar/Kamera1/Mask/"

        # VARIABLE UNTUK MENENTUKAN NAMA FILE CITRA
        img_name_original = lokasi_file_original + str(tanggal) + str(waktu) + ".jpg"
        img_name_threshold = lokasi_file_threshold + str(tanggal) + str(waktu) + ".jpg"
        img_name_bitwise = lokasi_file_bitwise + str(tanggal) + str(waktu) + ".jpg"

        # MENYIMPAN CITRA
        cv2.imwrite(img_name_original,frame1)
        cv2.imwrite(img_name_threshold, dilation)
        cv2.imwrite(img_name_bitwise, bitwise)

        # Cari kontur bibit
        contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Inisialisasi jumlah bibit yang tumbuh
        jumlah_bibit = 0

        # Loop melalui setiap kontur
        for contour in contours:
            # Hitung luas kontur
            area = cv2.contourArea(contour)
    
        # Jika luas kontur lebih besar dari batas tertentu, anggap sebagai bibit yang tumbuh
        if area > 100:
            jumlah_bibit += 1
        
            # Gambar kotak pembatas di sekitar bibit
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        
    # Tutup kamera
    cam1.release()

    return jumlah_bibit

# Fungsi untuk melakukan pengambilan gambar dan pemrosesan
def JumlahDaun_TinggiDaun_DiameterDaun():
    # Inisiasi kamera
    cam2 = cv2.VideoCapture(2)

    # Pengaturan kamera (contoh: kecerahan dan kontras)
    cam2.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Lebar frame (resolusi)
    cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Tinggi frame (resolusi)

    # Baca frame dari kamera
    ret2, frame2 = cam2.read()

    # Jika berhasil membaca frame
    if ret2:

        #BGR to HSV 
        hsv = cv2.cvtColor(frame2,cv2.COLOR_BGR2HSV)

        #THRESHOLDING BERDASARKAN RANGE 3 CHANNEL WARNA (HSV)
        lower = np.array([0, 7, 0])
        upper = np.array([72, 255, 255]) 
        mask = cv2.inRange(hsv,lower,upper) #masking
        kernel = np.ones((1, 1), np.uint8) #untuk operasi blur, erosi, dilasi
        erosion = cv2.erode(mask, kernel, iterations=1) #operasierosi
        dilation = cv2.dilate(erosion, kernel, iterations=1) #operasidilasi
        bitwise = cv2.bitwise_and(frame2, frame2, mask=dilation) #bitwise(n)

        # VARIABLE UNTUK MENENTUKAN WAKTU
        now = datetime.datetime.now()
        waktu = now.strftime("(%H;%M WIB)")
        tanggal = now.strftime("%d-%b-%Y")

        # VARIABLE UNTUK MENENTUKAN LOKASI PENYIMPANAN CITRA
        lokasi_file_original = "/home/pi/Documents/Penelitian/Gambar/Kamera2/Ori/"
        lokasi_file_threshold = "/home/pi/Documents/Penelitian/Gambar/Kamera2/Thres/"
        lokasi_file_bitwise = "/home/pi/Documents/Penelitian/Gambar/Kamera2/Mask/"

        # VARIABLE UNTUK MENENTUKAN NAMA FILE CITRA
        img_name_original = lokasi_file_original + str(tanggal) + str(waktu) + ".jpg"
        img_name_threshold = lokasi_file_threshold + str(tanggal) + str(waktu) + ".jpg"
        img_name_bitwise = lokasi_file_bitwise + str(tanggal) + str(waktu) + ".jpg"

        # MENYIMPAN CITRA
        cv2.imwrite(img_name_original,frame2)
        cv2.imwrite(img_name_threshold, dilation)
        cv2.imwrite(img_name_bitwise, bitwise)

        # Mengukur faktor konversi piksel ke cm (disesuaikan dengan skala pengukuran Anda)
        faktor_konversi = 0.3 # Contoh: 1 cm = 10 piksel

        # Mencari Kontur Objek
        contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Inisialisasi JumlahDaun, TinggiDaun, Dan Diameter Daun
        jumlah_daun = 0
        tinggi_daun_tertinggi = 0
        diameter_daun = 0
        rata_rata_diameter_daun = 0

        # Loop melalui setiap kontur
        for contour in contours:
            # Hitung luas kontur
            area = cv2.contourArea(contour)

        # Jika luas kontur lebih besar dari batas tertentu, anggap sebagai bibit yang tumbuh
        if area > 10:
            jumlah_daun += 1
        
            # Gambar kotak pembatas di sekitar bibit
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Hitung tinggi daun (jarak dari titik terendah ke titik tertinggi)
            tinggi_daun = h

            # Perbarui tinggi_daun_tertinggi_cm jika ditemukan tinggi daun yang lebih tinggi
            if tinggi_daun > tinggi_daun_tertinggi:
                tinggi_daun_tertinggi = tinggi_daun / faktor_konversi

            # Menghitung diameter daun
            (x, y), radius = cv2.minEnclosingCircle(contour)
            diameter = 2 * radius
            diameter_daun += diameter

            # Gambar kotak pembatas di sekitar daun
            #cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Hitung diameter daun (menggunakan sifat proporsional)
            diameter_daun = max(w, h) / faktor_konversi

    
            
    # Tutup kamera
    cam2.release()

    return jumlah_daun, tinggi_daun_tertinggi, rata_rata_diameter_daun


# Fungsi untuk menyimpan data ke dalam file CSV
def Simpan_CSV(jumlah_bibit, jumlah_daun, tinggi_daun_tertinggi, rata_rata_diameter_daun):

    #Nama File yang akan disimpan
    nama_file = 'DataBenih.csv'
    
    # VARIABLE UNTUK MENENTUKAN WAKTU
    now = datetime.datetime.now()
    waktu = now.strftime("(%H;%M WIB)")
    tanggal = now.strftime("%d-%b-%Y")

    # Data yang akan disimpan dalam format list of lists
    data = [
        ['Waktu' , 'Tanggal' , 'Jumlah Bibit', 'Jumlah Daun', 'Tinggi Daun Tertinggi', 'Rata-rata Diameter Daun'],
        [waktu, tanggal, jumlah_bibit, jumlah_daun, tinggi_daun_tertinggi, rata_rata_diameter_daun]
    ]

    # Menyimpan data ke dalam file CSV
    with open(nama_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print("Data berhasil disimpan dalam file CSV.")


# Fungsi untuk menjalankan capture_and_process() pada kedua kamera setiap hari jam 10 pagi
def job():
    # VARIABLE UNTUK MENENTUKAN WAKTU
    now = datetime.datetime.now()
    tanggal = now.strftime("%d-%b-%Y")
    
    print("Mengambil dan Memproses Gambar " + str(tanggal))
    jumlah_bibit = Jumlah_Bibit()  # Kamera pertama dengan indeks 0
    jumlah_daun, tinggi_daun_tertinggi, rata_rata_diameter_daun = JumlahDaun_TinggiDaun_DiameterDaun()  # Kamera kedua dengan indeks 2
    Simpan_CSV(jumlah_bibit, jumlah_daun, tinggi_daun_tertinggi, rata_rata_diameter_daun)

# Atur jadwal pemrosesan gambar setiap hari jam 10 pagi
schedule.every().day.at("10:00").do(job)


# Loop utama untuk menjalankan jadwal
while True:
    schedule.run_pending()
    time.sleep(1)