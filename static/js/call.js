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
    document.getElementById('search').disabled = nerText == '' || nerText == null
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

function predict_fake() {
    let text_predict = document.getElementsByName('text_predict')[0].value
    chang_btn_disabled("spinner-border spinner-border-sm", "spinner_predict", true, 'btn_predict')

    setTimeout(function () {
        $.ajax({
            type: 'POST',
            url: '/flask-new',
            data: { 'text_predict': text_predict },
            success: function (data) {
                document.getElementById('resulte-predict').innerHTML = data
                chang_btn_disabled("", "spinner_predict", false, 'btn_predict')
            }
        })
    }, 3000);
}