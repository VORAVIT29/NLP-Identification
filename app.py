from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from flaskext.markdown import Markdown
import tempfile
import shutil
import os
import NLP.gen as nlp
import NLP.Spacy as sp


app = Flask(__name__)
Markdown(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
    if os.path.isdir(session['dict']):
        shutil.rmtree(session['dict'])
        session['dict'] = '/clear-patch'

    return render_template('page.html')


@app.route('/', methods=['POST'])
def process():
    if os.path.isdir(session['dict']):
        print("rm", session['dict'])
        shutil.rmtree(session['dict'])  # ลบ dictionary จำลอง
        session['dict'] = '/clear-patch'

    filenames = []
    # สร้าง dictionary จำลองมาเพื่อเปิดไฟล์
    tempdir = tempfile.mkdtemp(prefix="Tempdir")
    # print(os.listdir(tempdir))
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
    # print("after", session['dict'])
    session['filename'] = filenames
    text_nlp = nlp.NLP(filenames)
    text = text_nlp.createToken()

    return render_template("page.html", text=text, bagOfWords=text_nlp.bag_of_words(), tf_idf=text_nlp.TfIdf())


@app.route('/search-text', methods=['POST'])
def search_text():
    search = request.form.get('search')
    filenames = session['filename']
    list_nlp = nlp.NLP(filenames)
    text = list_nlp.createToken()
    return render_template("page.html", text=text, text_search=list_nlp.searchText(search), bagOfWords=list_nlp.bag_of_words(), tf_idf=list_nlp.TfIdf())


@app.route('/search-text')
def search():
    return redirect('/')


@app.route('/pocess-spacy', methods=['POST'])
def pocess_spacy():
    if request.method == 'POST':
        input_text = request.form.get('nerText')
        convert_html = sp.pocess_spacy(input_text)
        # print(convert_html)
    return render_template('page.html', result=convert_html)


@app.route('/pocess-spacy')
def re_spacy():
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
