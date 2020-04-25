function recursiveDraw(draw, node, heightBegin, heightEnd, lengthHorLine, depth) {
    var denominaterSize;
    if (jQuery.isEmptyObject(node['children'])){
        denominaterSize = 1;
    } else {
        denominaterSize = Object.keys(node['children']).length;
        lastYText = 0;
    }

    var sizeOneBox = (heightEnd-heightBegin)/denominaterSize;

    var beginLine = heightBegin+(sizeOneBox/2);
    var endLine = heightEnd-(sizeOneBox/2);
    var xPointsVer = lengthHorLine*depth+10;
    var connectionEndX = xPointsVer+lengthHorLine;


    var line1 = draw.line(xPointsVer, beginLine, xPointsVer, endLine);
    line1.stroke({width: 2, color: '#000000'});

    //only leaves have names
    if (node["name"]) {
        var name = draw.text(node["name"]);

        var xName = xPointsVer+10;
        var yName = endLine-10;
        if (lastYText < yName && lastYText > yName-20){
            yName = lastYText+15;
        }
        name.move(xName, yName);
        lastYText = yName;
    }

    var iter = 0;
    for (var key in node['children']) {
        connectionLineY = (iter+0.5)*sizeOneBox+heightBegin;
        var line3 = draw.line(xPointsVer, connectionLineY, connectionEndX, connectionLineY);
        line3.stroke({width: 2, color: '#000000'});
        console.log(key);
        var beginNextHeight = iter*sizeOneBox+heightBegin;
        var endNextHeight = (iter+1)*sizeOneBox+heightBegin;
        recursiveDraw(draw, node['children'][key], beginNextHeight, endNextHeight, lengthHorLine, depth+1);
        iter++;
    }
    return
};

function getNewick() {
    $('#newick-graph').empty();

    var draw = SVG().addTo('#newick-graph').size('1500', '2000')

    var proteinName = $("select#proteinChoice option:checked").val();
    var callUrl = "/data/newick/" + String(proteinName);

    $.ajax({
        url: callUrl,
    }).done(function( data ) {
        var totalWidth = draw.attr('width');
        console.log(data["depth"]);
        //-10 because we want to write text
        lengthHorizontalLine = ((0.95*totalWidth)/data['depth'])-10;
        var totalHeight = draw.attr('height');
        lastYText = 0;
        //we give depth specifically as a parameter as it only appears in the top level of data
        recursiveDraw(draw, data, 0, totalHeight, lengthHorizontalLine, 0);
    });

    $('#hidden-section').attr('style', "");
}