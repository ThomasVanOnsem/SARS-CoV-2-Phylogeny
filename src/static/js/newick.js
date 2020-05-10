
function getNewick() {
    $('#newick-graph').empty();
    $('#title-protein').empty();

    var height = $('#result-box').height();
    var width = $('#result-box').width();

    var draw = SVG().addTo('#newick-graph').size(width.toString(), height.toString());

    var proteinName = $('select#proteinChoice option:checked').val();
    var callUrl = '/data/newick/' + String(proteinName);

    $.ajax({
        url: callUrl,
    }).done(function( data ) {
        // var totalWidth = draw.attr('width');
        var totalWidth = 20*data['depth'];
        //-10 because we want to write text
        lengthHorizontalLine = ((0.95*totalWidth)/data['depth'])-10;
        // var totalHeight = draw.attr('height');
        var totalHeight = 10*(Math.pow(data['depth'],2));
        var maxWidthHeight = Math.max(totalWidth, totalHeight);
        var viewBoxStr =  '0 0 ' + maxWidthHeight.toString() + ' ' + maxWidthHeight.toString();
        draw.attr('viewBox', viewBoxStr);
        //we give depth specifically as a parameter as it only appears in the top level of data
        recursiveDraw(draw, data, 0, totalHeight, lengthHorizontalLine, 0);
    });
    var spaceSeperatedProteinName = String(proteinName).replace(/_/g, ' ');
    $('#title-protein').append(spaceSeperatedProteinName);
}


function startHoveringNode(node){
    if (!$(node).hasClass('data-selected')){
        $(node).attr({
            fill: '#00D1B2',
            r: '7.5'
        });
    }
}

function stopHoveringNode(node){
    if (!$(node).hasClass('data-selected')){
        $(node).attr({
            fill: '#000000',
            r: '5'
        });
    }
}


function showInfoVariant(node){
    $('#selectedNodeContent').empty();
    $('.data-selected').removeClass('data-selected').attr({fill: '#000000'});
    $(node).addClass('data-selected');
    $(node).attr({
        fill: '#00D1B2',
        r: '5'
    });
    $.ajax({
        url: '/data/info/protein/' + $(node).attr('id')
    }).done(function (data){
        var nameString = '<p><span class="has-text-primary">Name:</span> ' + data['name'] + '</p>';
        $('#selectedNodeContent').append(nameString);
    });
}

function recursiveDraw(draw, node, heightBegin, heightEnd, lengthHorLine, depth) {
    var denominaterSize;
    if (jQuery.isEmptyObject(node['children'])){
        denominaterSize = 1;
    } else {
        denominaterSize = Object.keys(node['children']).length;
     }

    var sizeOneBox = (heightEnd-heightBegin)/denominaterSize;

    var beginLine = heightBegin+(sizeOneBox/2);
    var endLine = heightEnd-(sizeOneBox/2);
    var xPointsVer = lengthHorLine*depth+10;
    var connectionEndX = xPointsVer+lengthHorLine;


    var line1 = draw.line(xPointsVer, beginLine, xPointsVer, endLine);
    line1.stroke({width: 2, color: '#000000'});

    //only leaves have names
    if (node['name']) {
        var endDot = draw.circle(10);
        endDot.move(xPointsVer-5, endLine-5);
        endDot.attr('id', node['name'])
        endDot.attr('onmouseover', 'startHoveringNode(this)')
        endDot.attr('onmouseout', 'stopHoveringNode(this)')
        endDot.attr('onclick', 'showInfoVariant(this)')
    }

    var iter = 0;
    for (var key in node['children']) {
        connectionLineY = (iter+0.5)*sizeOneBox+heightBegin;
        var line3 = draw.line(xPointsVer-1, connectionLineY, connectionEndX, connectionLineY);
        line3.stroke({width: 2, color: '#000000'});
        var beginNextHeight = iter*sizeOneBox+heightBegin;
        var endNextHeight = (iter+1)*sizeOneBox+heightBegin;
        recursiveDraw(draw, node['children'][key], beginNextHeight, endNextHeight, lengthHorLine, depth+1);
        iter++;
    }
}

function initializeMoveNewick() {
    pos1X = 0;
    pos2X = 0;
    pos1Y = 0;
    pos2Y = 0;
    var newickDiv = $('#newick-graph');

    $(newickDiv).on('mousedown', moveNewick)


    function moveNewick(e) {
        e.preventDefault();

        var xInsideDiv = e.pageX - $('#result-box').offset().left;
        var yInsideDiv = e.pageY - $('#result-box').offset().top;

        pos2X = xInsideDiv;
        pos2Y = yInsideDiv;

        $(document).on('mouseup', stopDrag);

        function stopDrag(e) {
            $(document).off('mousemove', moveDrag);
            $(document).off('mouseup', stopDrag);
        }

        $(document).on('mousemove', moveDrag);

    }
}

function moveDrag(e) {
    var xInsideDiv = e.pageX - $('#result-box').offset().left;
    var yInsideDiv = e.pageY - $('#result-box').offset().top;

    pos1X = pos2X - xInsideDiv;
    pos1Y = pos2Y - yInsideDiv;

    draw = $('#newick-graph').children()[0];
    var box = $(draw).attr('viewBox');
    var viewList = box.split(/\s+|,/);
    var current1X = parseInt(viewList[0]);
    var current1Y = parseInt(viewList[1]);
    var current2X = parseInt(viewList[2]);
    var current2Y = parseInt(viewList[3]);

    var new1X = current1X + pos1X;
    var new1Y =  current1Y + pos1Y;
    var new2X = current2X + pos1X;
    var new2Y = current2Y + pos1Y;
    if (new1X < 10){
        new1X = 10;
    }
    if (new1Y < 10){
        new1Y = 10;
    }
    if (new2X < 10) {
        new2X = 10;
    }
    if (new2Y < 10) {
        new2Y = 10;
    }

    var viewBoxStr = new1X.toString() + ' ' + new1Y.toString()+
        ' ' + new2X.toString() + ' ' + new2Y.toString();
    $(draw).attr('viewBox', viewBoxStr);

    pos2X = xInsideDiv;
    pos2Y = yInsideDiv;

}


function initializeScaleNewick() {
    $('#newick-graph').on('wheel', function(event){
        event.preventDefault();
        scaleNewick(event);
    });
}

function scaleNewick(e) {
    var draw = $('#newick-graph').children()[0];
    var box = $(draw).attr('viewBox');
    var viewList = box.split(/\s+|,/);
    var current1X = parseInt(viewList[0]);
    var current1Y = parseInt(viewList[1]);
    var current2X = parseInt(viewList[2]);
    var current2Y = parseInt(viewList[3]);

    if (e.originalEvent.deltaY > 0) {
        var new1X = current1X + 8;
        var new1Y = current1Y + 8;
        var new2X = current2X - 8;
        var new2Y = current2Y - 8;

        if (new2X < 10){
            new2X = 10;
        }
        if (new2Y < 10){
            new2Y = 10;
        }
        var viewBoxStr = new1X.toString() + ' ' + new1Y.toString() + ' ' + new2X.toString() + ' ' + new2Y.toString();
        $(draw).attr('viewBox', viewBoxStr);
    } else {
        var new1X = current1X - 8;
        var new1Y = current1Y - 8;
        var new2X = current2X + 8;
        var new2Y = current2Y + 8;

        if (new1X < 10){
            new1X = 10;
        }
        if (new1Y < 10){
            new1Y = 10;
        }
        var viewBoxStr = new1X.toString() + ' ' + new1Y.toString() + ' ' + new2X.toString() + ' ' + new2Y.toString();
        $(draw).attr('viewBox', viewBoxStr);
    }
}