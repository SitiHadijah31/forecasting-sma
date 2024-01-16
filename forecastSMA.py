from database import db, data_train, data_test, resultSMA
import pandas as pd
import numpy as np

def distance():
    return 7

def forecast():
    data = data_test.query.all()

    # Menyiapkan data ke dalam DataFrame Pandas
    df = pd.DataFrame([(d.Date, d.Close) for d in data], columns=['date', 'close'])

    # Menghitung Simple Moving Average (SMA)
    window_size = distance()
    df['SMA'] = df['close'].rolling(window=window_size).mean()
    for index, row in df.iterrows():
        if row['close'] == 0:
            if index > 0:
                df.at[index, 'close'] = df.at[index - 1, 'SMA']
        start_index = max(0, index - window_size + 1)
        subset = df.loc[start_index:index, 'close']
        df.at[index, 'SMA'] = subset.mean()

    for index, row in df.iterrows():
        # set arrow close to 0 at last 7 data
        if index >= len(df) - window_size:
            row['close'] = 0
        hasil = (resultSMA(Date=row['date'], Close=row['close'], Result=row['SMA']))
        db.session.add(hasil)

    db.session.commit()


    # # hasil = df['close'].rolling(window=window_size).mean()
    # # df['SMA'] = df['close'].rolling(window=window_size).mean()
    # print(df['SMA'])
    # print(df['close'])

    # for index, row in df.iterrows():
    #     if row['close'] == 0:
    #         row['close'] = df.loc[index-1, 'SMA']
    #     sma_value = row['SMA']
    #     if pd.isnull(sma_value):  # Periksa apakah nilai SMA NaN
    #         sma_value = 0  # Ganti dengan nilai default atau nilai lain yang sesuai
    #     hasil = resultSMA(Date=row['date'], Close=row['close'], Result=sma_value)
    #     db.session.add(hasil)
    #
    # db.session.commit()

# def forecast():
#     data = data_test.query.all()
#
#     # Menyiapkan data ke dalam DataFrame Pandas
#     df = pd.DataFrame([(d.Date, d.Close) for d in data], columns=['date', 'close'])
#
#     # Menghitung Simple Moving Average (SMA)
#     window_size = distance()
#     df['SMA'] = df['close'].rolling(window=window_size).mean()
#
#     for index, row in df.iterrows():
#         sma_value = row['SMA']
#         if pd.isnull(sma_value):  # Periksa apakah nilai SMA NaN
#             sma_value = 0  # Ganti dengan nilai default atau nilai lain yang sesuai
#         hasil = resultSMA(Date=row['date'], Close=row['close'], Result=sma_value)
#         db.session.add(hasil)
#
#     db.session.commit()

# Hitung MAPE
def calculate_mape():
    data = resultSMA.query.order_by(resultSMA.Date.desc()).limit(50).all()
    data.reverse()

    if len(data) == 0:
        return "-"

    df = pd.DataFrame([(d.Date, d.Close, d.Result) for d in data], columns=['Date', 'Close', 'Result'])
    df.set_index('Date', inplace=True)
    data2 = df.head(43)
    series = data2['Result']
    series2 = data2['Close']
    mape = np.mean(np.abs((series2 - series) / series2)) * 100
    mape = round(mape, 2)

    return mape


