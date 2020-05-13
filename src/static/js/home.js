$(window).ready(function(){
    getNewick();
});

function addPlacementForm() {
    let div = document.getElementById("add-data");
    if(div.style.display === ''){
        div.style['display'] = 'none';
        document.getElementById('submit-btn').disabled = true;
    }
    else{
        div.style.display = '';
        document.getElementById('submit-btn').disabled = false;
    }
}

function triggerToggleAdd(event){
	event.preventDefault();
	var options = $('#type-sequence-input').children();
	options.each(function () {
		$(this).blur()
		if ($(this).hasClass('is-selected')) {
			$(this).removeClass('is-selected');
			$(this).removeClass('is-primary');
		} else {
			$(this).addClass('is-selected');
			$(this).addClass('is-primary');

			//now we change the page
			if($(this).attr('id') === 'choose-nuc'){
				$('#nucleotide-adding').attr('style', '');
				$('#amino-acid-adding').attr('style', 'display:none;');
			} else {
				$('#nucleotide-adding').attr('style', 'display:none;');
				$('#amino-acid-adding').attr('style', '');
			}
		}
	})
}
