function callView(e) {
    e.preventDefault();
    var proteinName = $("select#proteinChoice option:checked").val();
    var url = "/data/view/" + String(proteinName);

    $(location).attr('href', url);

}