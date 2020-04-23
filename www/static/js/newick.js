function recursiveDraw(node, height) {
    var sizeOneBox = (height*0.9)/(Object.keys(node['children']).length+1)

    for (var key in node['children']) {

        console.log(key);
        recursiveDraw(node['children'][key]);
    }
}

function getNewick() {
    var proteinName = $("select#proteinChoice option:checked").val();
    var callUrl = "/data/newick/" + String(proteinName);

    $.ajax({
        url: callUrl,
    }).done(function( data ) {
        var totalWidth = $("newick-graph").attr('width');
        lengthHorizontalLine = (0.89*totalWidth)/data['depth'];
        var totalHeight = $("newick-graph").attr('height');
        recursiveDraw(data, totalHeight);

    });
}