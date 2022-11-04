// -------------------------------------- Spacy --------------------------------------
function call_spacy() {
    var check = []
    text = document.getElementsByName('nerText')[0].value
    for (var iterator of document.getElementById('check').options) {
        if (iterator.selected) {
            check.push(iterator.value)
        }
    }

    $.ajax({
        type: "POST",
        url: "/pocess-spacy",
        data: {
            'text': text,
            'chEn': JSON.stringify(check), // convert list to Json string
        },
        success: function (data) {
            document.getElementById('showSpacy').innerHTML = data
        }
    })
}

function check_text_input() {
    nerText = document.getElementsByName('nerText')[0].value
    document.getElementById('search-ner').disabled = nerText == '' || nerText == null
}

// -------------------------------------- search-text --------------------------------------
function search_text() {
    text_search = document.getElementsByName('search')[0].value
    chang_btn_disabled("spinner-border spinner-border-sm", "spinner", true, 'btn_search')

    setTimeout(function () {
        $.ajax({
            type: 'POST',
            url: '/search-text',
            data: { 'search': text_search },
            success: function (data) {
                document.getElementById('show-search').innerHTML = data
                chang_btn_disabled("", "spinner", false, 'btn_search')
            }
        })

    }, 3000)
}

function chang_btn_disabled(class_anima, id_anima, dis_bool, html_id) {
    const spinner = document.getElementById(id_anima)
    spinner.className = class_anima
    document.getElementById(html_id).disabled = dis_bool
}

// -------------------------------------- fake-new --------------------------------------
var hidden;
function predict_fake() {
    let text_predict = document.getElementsByName('text_predict')[0].value
    chang_btn_disabled("spinner-border spinner-border-sm", "spinner_predict", true, 'btn_predict')

    setTimeout(() => {
        $.ajax({
            type: 'POST',
            url: '/flask-new',
            data: { 'text_predict': text_predict },
            success: function (data) {
                if (data == 'fake') {
                    document.getElementById('news').hidden = true
                    document.getElementById('fake-new').removeAttribute('hidden')
                } else {
                    document.getElementById('fake-new').hidden = true
                    document.getElementById('news').removeAttribute('hidden')
                }
                document.getElementById('resulte-predict').innerHTML = data.toUpperCase()
                chang_btn_disabled("", "spinner_predict", false, 'btn_predict')
            }
        })
    }, 1000);
}
// -------------------------------------- Sentiment --------------------------------------
var keepClassName = ''
function predict_sentiment() {
    let value = document.getElementsByName('sentiment_name')[0].value;
    chang_btn_disabled("spinner-border spinner-border-sm", "spinner_predict_sentiment", true, 'btn_predict_sentiment')

    setTimeout(() => {
        $.ajax({
            type: 'POST',
            url: '/sentiment',
            data: { 'text_sentiment': value },
            success: (data) => {
                if (keepClassName) document.getElementById('box-result').classList.remove(keepClassName)

                // Edit title result
                let title_result_container = document.querySelector('#title-result')
                // Edit title icon
                let icon_result = ''
                // Get name sentiment
                let className = data.split(' ')[0].toLowerCase();
                if (className == 'negative') {
                    document.getElementById('box-result').classList.add('alert-danger')
                    keepClassName = 'alert-danger'
                    icon_result = `<i class='bi bi-emoji-frown-fill'></i>&nbsp;${data.split(' ')[0]} ${(data.split(' ')[1] * 100)} %<hr>`
                }
                else if (className == 'positive') {
                    document.getElementById('box-result').classList.add('alert-success')
                    keepClassName = 'alert-success'
                    // icon_result.setAttribute('class', 'bi bi-emoji-smile-fill')
                    icon_result = `<i class='bi bi-emoji-smile-fill'></i>&nbsp;${data.split(' ')[0]} ${(data.split(' ')[1] * 100)} %<hr>`
                }
                else {
                    document.getElementById('box-result').classList.add('alert-warning')
                    keepClassName = 'alert-warning'
                    // icon_result.setAttribute('class', 'bi bi-emoji-neutral-fill')
                    icon_result = `<i class='bi bi-emoji-neutral-fill'></i>&nbsp;${data.split(' ')[0]} ${(data.split(' ')[1] * 100)} %<hr>`
                }
                // show Title Result
                title_result_container.innerHTML = icon_result
                document.getElementById('sent_result').innerHTML = value
                chang_btn_disabled("", "spinner_predict_sentiment", false, "btn_predict_sentiment")
            }
        })
    }, 1000);
}