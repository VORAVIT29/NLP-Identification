import ast
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, session, Markup
from flask_session import Session
# from flaskext.markdown import Markdown
import tempfile
import shutil
import os
import NLP.gen as nlp
import NLP.Spacy as sp
import NLP.fackeNew as fn
import NLP.sentiment as sent


app = Flask(__name__)
# Markdown(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
    if 'dict' in session:
        if os.path.isdir(session['dict']):
            shutil.rmtree(session['dict'])
            session.pop('dict', None)

    return render_template('page.html')


@app.route('/', methods=['POST'])
def process():
    if 'dict' in session:
        if os.path.isdir(session['dict']):
            print("rm", session['dict'])
            shutil.rmtree(session['dict'])  # ลบ dictionary จำลอง
            session.pop('dict', None)

    filenames = []
    # สร้าง dictionary จำลองมาเพื่อเปิดไฟล์
    tempdir = tempfile.mkdtemp(prefix="Tempdir")
    form = request.files.getlist('fileName[]')

    for file in form:
        # เปลี่ยนชื่อไฟล์ ให้คล้องจอง เช่น ชื่อไฟล์ hello world.txt ก็จะเป็น hello_world.txt
        filename = secure_filename(file.filename)
        # รวมไฟล์ให้เป็น patch ที่บันทึก
        patch_save = os.path.join(tempdir, filename)
        # save file
        file.save(patch_save)
        filenames.append(patch_save)

    session['dict'] = tempdir
    session['filename'] = filenames
    text_nlp = nlp.NLP(filenames)
    text = text_nlp.createToken()

    return render_template("page.html", text=text, bagOfWords=text_nlp.bag_of_words(), tf_idf=text_nlp.TfIdf())


@app.route('/search-text', methods=['POST'])
def search_text():
    search = str(request.form.get('search')).lower()
    # search = str(search).lower()
    filenames = session['filename']
    list_nlp = nlp.NLP(filenames)
    text = list_nlp.createToken()

    return list_nlp.searchText(search)


@app.route('/search-text')
def search():
    return redirect('/')


@app.route('/pocess-spacy', methods=['POST'])
def pocess_spacy():
    if request.method == 'POST':
        input_text = request.form.get('text')
        check_list = request.form.getlist('chEn')[0]
        # convert Json string to list
        check_list = ast.literal_eval(check_list)

        convert_html = sp.pocess_spacy(input_text, check_list)
        return convert_html


@app.route('/pocess-spacy')
def re_spacy():
    return redirect('/')


@app.route('/flask-new', methods=['POST'])
def process_flask_new():
    if request.method == 'POST':
        text = request.form.get('text_predict')
        fack_new = fn.get_prediction(text, True)
    return fack_new


@app.route('/flask-new')
def flask_new_re():
    return redirect('/')


@app.route('/sentiment', methods=['POST'])
def process_sentiment():
    if request.method == 'POST':
        text = request.form.get('text_sentiment')
        sentiment = sent.sentiment(text)
    return sentiment


@app.route('/sentiment')
def sentiment_re():
    return redirect('/')


if __name__ == '__main__':
    # app.run(debug=True, host="ipAddr", port=80)
    app.run(debug=True)
