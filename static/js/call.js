function call_spacy() {
    var check = []
    var result = ""
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
            result_text(data)
        }
    })
}

function result_text(result) {
    document.getElementById('showSpacy').innerHTML = result
}