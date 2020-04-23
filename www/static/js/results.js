function callView() {
    var proteinName = $("select#proteinChoice option:checked").val();
    var callUrl = "/data/view/" + String(proteinName);

    $.ajax({
        url: callUrl,
    }).done(function( data ) {
        $('#result-img').attr('src', data['image'])
    });

}