from database import db, data_train
import yfinance as yf
# from datetime import datetime

# Fungsi untuk menyimpan data ke dalam tabel dataTest
def saveScrape(symbol, startDate, endDate):
    data = yf.download(symbol, start=startDate, end=endDate)

    for index, row in data.iterrows():
        data_tr = data_train(
            Date=index.date(),
            Open=row['Open'],
            High=row['High'],
            Low=row['Low'],
            Close=row['Close'],
            Adj=row['Adj Close'],
            Volume=row['Volume']
        )
        db.session.add(data_tr)

    db.session.commit()