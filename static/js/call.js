function call_spacy() {
    check_entity_label = document.getElementsByName('check[]')[0].value
    text = document.getElementsByName('nerText')[0].value
    // console.log(check_entity_label)

    // let form_data = new FormData($('#process-spacy')[0])
    // alert(form_data)

    $.ajax({
        type: 'POST',
        url: '{{ url_for(pocess-spacy) }}',
        data: form_data,
    })

    document.getElementById('showSpacy').innerHTML = text
}