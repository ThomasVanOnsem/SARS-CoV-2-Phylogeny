function recursiveDraw(draw, node, heightBegin, heightEnd, lengthHorLine, depth) {
    var denominatorSize;
    if (node["name"]) {
        denominaterSize = Object.keys(node['children']).length+1;
    } else {
        denominaterSize = Object.keys(node['children']).length;
        if (denominatorSize === 0){
            //there is nothing to draw
            return;
        }
    }

    var sizeOneBox = (heightEnd-heightBegin)/denominaterSize;

    var beginLine = heightBegin+(sizeOneBox/2);
    var endLine = heightEnd-(sizeOneBox/2);
    var xPointsVer = lengthHorLine*depth+10;
    var connectionEndX = xPointsVer+lengthHorLine;


    var line1 = draw.line(xPointsVer, beginLine, xPointsVer, endLine);
    line1.stroke({width: 2, color: '#000000'});

    if (node["name"]) {
        var name = draw.text(node["name"]);

        var xName = 0;
        if (Object.keys(node['children']).length != 0) {
            //we draw a line to for this variant (not an offspring)
            var line2 = draw.line(xPointsVer, endLine, connectionEndX, endLine);
            line2.stroke({width: 2, color: '#000000'});
            xName = connectionEndX+10;
        }else{
            xName = xPointsVer+10;
        }
        name.move(xName, endLine-10);
    }

    var iter = 0;
    for (var key in node['children']) {
        connectionLineY = (iter+0.5)*sizeOneBox+heightBegin;
        var line3 = draw.line(xPointsVer, connectionLineY, connectionEndX, connectionLineY);
        line3.stroke({width: 2, color: '#000000'});
        console.log(key);
        var beginNextHeight = iter*sizeOneBox+heightBegin;
        var endNextHeight = (iter+1)*sizeOneBox+heightBegin;
        recursiveDraw(draw, node['children'][key], beginNextHeight, endNextHeight, lengthHorLine,depth+1);
        iter++;
    }
    return
};

function getNewick() {
    $('#newick-graph').empty();
    var draw = SVG().addTo('#newick-graph').size('5000', '1000')

    var proteinName = $("select#proteinChoice option:checked").val();
    var callUrl = "/data/newick/" + String(proteinName);

    $.ajax({
        url: callUrl,
    }).done(function( data ) {
        var totalWidth = $("#newick-graph").attr('width');
        console.log(data["depth"]);
        lengthHorizontalLine = (0.95*totalWidth)/data['depth'];
        var totalHeight = $("#newick-graph").attr('height');
        //we give depth specifically as a parameter as it only appears in the top level of data
        recursiveDraw(draw, data, 0, totalHeight, lengthHorizontalLine, 0);
    });

    $('#hidden-section').attr('style', "");
}