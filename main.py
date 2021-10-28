import mysql.connector
import pandas as pd
import os
import matplotlib.pyplot as plt
import pyodbc

#connect to mysql server
db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="STOK_BUAH"
)

#for create table if "STOK_BUAH" doesn't exist
cursor =db.cursor()
sql = '''CREATE TABLE IF NOT EXISTS STOK_BUAH (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    asal VARCHAR(255),
    stok INT,
    harga_satuan INT
);'''
cursor.execute(sql)

#function for insert new data
def insert_data(db):
    #inisiasi variabel
    name = input('Masukan nama buah: ')
    asal = input('Masukan asal buah (Impor/Lokal): ')
    stok = input('Masukan stok: ')
    harga_satuan =input('Masukan harga satuan: ')
    val = (name, asal, stok, harga_satuan)
    
    cursor = db.cursor()
    sql = '''INSERT INTO STOK_BUAH 
    (name, asal, stok, harga_satuan)
    VALUES (%s, %s, %s, %s)'''
    
    cursor.execute(sql, val)
    db.commit()
    print("{} data berhasil disimpan".format(cursor.rowcount))

#function for showing table that we have
def show_data(db):
    cursor = db.cursor()
    sql = 'SELECT * FROM STOK_BUAH'
    cursor.execute(sql)
    results = cursor.fetchall()

    if cursor.rowcount < 0:
        print("Tidak ada data")
    else:
        for data in results:
            print(data)

#function for updating stock
def update_data(db):
    cursor = db.cursor()
    show_data(db)
    id_buah = input('Pilih ID buah> ')
    stok = int(input('Masukan stok yang baru: '))
    
    sql = ('UPDATE STOK_BUAH SET stok=%s WHERE ID=%s')
    val = (stok, id_buah)
    cursor.execute(sql, val)
    db.commit()
    print("{} data berhasil diubah".format(cursor.rowcount))

#function untuk menampilkan laporan stok buah berdasarkan asal
def show_stock(db):
    cursor = db.cursor()
    
    sql = '''SELECT SUM(stok) AS StokBuah, asal 
    FROM STOK_BUAH
    GROUP BY asal
    ORDER BY StokBuah ASC;'''
    cursor.execute(sql)
    results = cursor.fetchall()

    if cursor.rowcount < 0:
        print("Tidak ada data")
    else:
        for data in results:
            print(data)

    #db.commit()
    print("{} data berhasil ditampilkan".format(cursor.rowcount))

#function for show graph
def show_graph(db):
    cursor = db.cursor()
    sql = "SELECT name, stok, harga_satuan FROM STOK_BUAH"
    cursor.execute(sql)
    results = cursor.fetchall()

    name = []
    stok = []
    harga_satuan = []
    for i in results:
        print(i)
        name.append(i[0])
        stok.append(i[1])
        harga_satuan.append(i[2])

    plt.figure(figsize=(9,3))
    plt.subplot(121)
    plt.title('Grafik Nama Buah dan Stok')
    plt.plot(name, stok)
    plt.xticks(fontsize=7)
    plt.xlabel('Nama Buah')
    plt.ylabel('Stok Buah')

    plt.subplot(122)
    plt.title('Grafik Nama Buah dan Harga Satuan')
    plt.bar(name, harga_satuan)
    plt.xticks(fontsize=7)
    plt.xlabel('Nama Buah')
    plt.ylabel('Harga Satuan')

    plt.show()

#convert sql database to File csv
def export_sql(db):
    result_dataFrame = pd.read_sql("SELECT * FROM STOK_BUAH", db)
    result_dataFrame.to_csv('Stok Buah.csv')
    print('--Berhasil membuat file csv--')

#function for show menu
def show_menu(db):
    print('====APLIKASI DATABASE STOK BUAH DENGAN PYTHON====')
    print('a. Insert Data')
    print('b. Tampilkan Data')
    print('c. Update Stok Buah')
    print('d. Lihat Stok Buah')
    print('e. Analisis Grafik')
    print('f. Eksport Database ke CSV')
    print('g. Keluar')
    print("------------------")
    menu = input("Pilih menu> ")


    if menu == 'a':
        insert_data(db)
    elif menu == 'b':
        show_data(db)
    elif menu == 'c':
        update_data(db)
    elif menu == 'd':
        show_stock(db)
    elif menu == 'e':
        show_graph(db)
    elif menu == 'f':
        export_sql(db)
    elif menu == 'g':
        exit()
    else :
        print('Pilihan Menu Tidak Ada!')

#to hold menu
if __name__ == "__main__":
    while(True):
        show_menu(db)
    

