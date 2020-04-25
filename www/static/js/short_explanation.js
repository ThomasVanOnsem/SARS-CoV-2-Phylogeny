function getShortInfo() {
	$('#protein-explanation').empty();

	var proteinName = $('select#proteinChoice option:checked').val();
    var callUrl = '/data/info/' + String(proteinName);

    $.ajax({
    	url: callUrl,
    }).done(function (data){
    	$('#protein-explanation').append(data['explanation']);
    });
}