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
    document.getElementById('search').disabled = (nerText == '' || nerText == null) ? true : false
}
// -------------------------------------- search-text --------------------------------------
function search_text() {
    text_search = document.getElementsByName('search')[0].value

    $.ajax({
        type: 'POST',
        url: '/search-text',
        data: { 'search': text_search },
        success: function (data) {
            document.getElementById('show-search').innerHTML = data
        }
    })
}