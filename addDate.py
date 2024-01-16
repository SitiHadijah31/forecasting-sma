from datetime import datetime, timedelta
from database import db, data_test

def add():
    # Mendapatkan tanggal terakhir dari dataTest
    last_date_entry = data_test.query.order_by(data_test.Date.desc()).first()
    if last_date_entry:
        last_date = last_date_entry.Date
    else:
        last_date = datetime(2022, 1, 1)  # Atur tanggal awal jika tabel kosong

    # Tambahkan 3 data terakhir dari tanggal terakhir
    for i in range(1, 8):
        new_date = last_date + timedelta(days=i)
        new_data_test = data_test(Date=new_date, Close=0.0)  # Gantilah nilai Close sesuai kebutuhan
        db.session.add(new_data_test)

    db.session.commit()