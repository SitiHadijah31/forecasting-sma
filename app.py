from flask import Flask, render_template, request, url_for, redirect, make_response
from database import db, data_train, data_test, resultSMA
from datetime import datetime
from forms import uploadForm
import pandas as pd
from forecastSMA import forecast, calculate_mape, distance
from scrape import saveScrape
from xhtml2pdf import pisa
from addDate import add

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/db_antm'
db.init_app(app)
app.config['SECRET_KEY'] = 'kunci_rahasia'

@app.route('/')
def dashboard():  # put application's code here
    segment = 'dashboard'
    hitung1 = data_train.query.count()
    hitung2 = data_test.query.count()
    return render_template("/home/index.html", hitung1=hitung1, hitung2=hitung2, segment=segment)

@app.route('/train/', methods=['GET', 'POST'])
def train():  # put application's code here
    segment = 'train'
    if request.method == 'POST':
        # Mendapatkan data dari tabel Train
        dataTrainRecords = data_train.query.all()

        # Mengambil hanya field Date dan Close
        dataTestRecords = [(record.Date, record.Close) for record in dataTrainRecords]

        # Memasukkan data ke tabel Test
        for date, close in dataTestRecords:
            formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
            newDataTest = data_test(Date=formatted_date, Close=close)
            db.session.add(newDataTest)

        db.session.commit()
        add()
        return redirect(url_for("test"))
    data = data_train.query.all()
    return render_template("/home/tablesTrain.html", value=data, segment=segment)

@app.route('/deleteAllTrain/', methods=['POST'])
def deleteAllTrain():
    if request.method == 'POST':
        data_train.query.delete()
        db.session.commit()
        return redirect(url_for('train'))

@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    form = uploadForm()

    if form.validate_on_submit():
        csv_file = form.csv_file.data
        df = pd.read_csv(csv_file)

        for index, row in df.iterrows():
            train_data = data_train(
                Date=row['Date'],
                Open=row['Open'],
                High=row['High'],
                Low=row['Low'],
                Close=row['Close'],
                Adj=row['Adj Close'],
                Volume=row['Volume']
            )
            db.session.add(train_data)

        db.session.commit()
        return redirect(url_for('train'))

    return render_template('/home/upload.html', title='Upload', form=form)

@app.route('/test/', methods=['GET', 'POST'])
def test():  # put application's code here
    data = data_test.query.all()
    segment = 'test'
    if request.method == 'POST':
        forecast()  # Memanggil fungsi forecast saat tombol proses ditekan
        return redirect(url_for('result'))  # Arahkan ke halaman result setelah perhitungan

    return render_template("/home/tablesTest.html", value=data, segment=segment)

@app.route('/deleteAllTest/', methods=['POST'])
def deleteAllTest():
    if request.method == 'POST':
        data_test.query.delete()
        db.session.commit()
        return redirect(url_for('test'))

@app.route('/result/')
def result():  # put application's code here
    # get resultsma only 20 data last
    data = resultSMA.query.order_by(resultSMA.Date.desc()).limit(50).all()
    data.reverse()
    segment = 'result'
    limit = 7
    dates = [result.Date.strftime('%Y-%m-%d') for result in data]
    close = [result.Close for result in data[:-limit]]
    result = [result.Result for result in data]
    mape = calculate_mape()
    return render_template("home/result.html", value=data, dates=dates, close=close, result=result, mape=mape, segment=segment)

@app.route('/deleteAllResult/', methods=['POST'])
def deleteAllResult():
    if request.method == 'POST':
        resultSMA.query.delete()
        db.session.commit()
        return redirect(url_for('result'))

@app.route('/crawling/', methods=['POST', 'GET'])
def scraping():
    if request.method == 'POST':
        symbol = request.form['symbol']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        saveScrape(symbol=symbol, startDate=start_date, endDate=end_date)

        return redirect(url_for('train'))

    return render_template('/home/scraping.html')

@app.route('/cetak-result')
def cetakResult():  # put application's code here
    data = resultSMA.query.all()
    dates = [result.Date.strftime('%Y-%m-%d') for result in data]
    close = [result.Close for result in data]
    result = [result.Result for result in data]
    # Render template HTML menggunakan Flask
    rendered = render_template("home/printResult.html", value=data, dates=dates, close=close, result=result)  # Ganti 'nama_template.html' dengan nama template Anda

    pdf = pisa.CreatePDF(rendered)

    if not pdf.err:
        response = make_response(pdf.dest.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=laporan.pdf'
        return response

@app.route('/about/')
def about():  # put application's code here
    segment = 'about'
    return render_template("/home/about.html/", segment=segment)

if __name__ == '__main__':
    app.run()
