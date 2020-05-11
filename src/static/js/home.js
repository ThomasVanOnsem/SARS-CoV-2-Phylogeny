function addPlacementForm() {
    let div = document.getElementById("add-data");
    if(div.style.display === ''){
        div.style['display'] = 'none';
        document.getElementById('submit-btn').innerText = 'View';
    }
    else{
        div.style.display = '';
        document.getElementById('submit-btn').innerText = 'Add Data';
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

function sendData() {
	let div = document.getElementById("add-data");
	if(div.style.display !== ''){
		return;
	}

	let proteinName = $('select#proteinChoice option:checked').val();
	let gen_options = document.getElementsByName('gen-option');
	let gen_option;
	for(let i = 0; i < gen_options.length; i++) {
		if(gen_options[i].checked)
			gen_option = gen_options[i].value;
	}

	let id;
	let origin;
	let sequence;
	if(document.getElementById("choose-nuc").classList.contains('is-selected')){
		id = document.getElementById("nucleo-id").value;
		origin = document.getElementById("nucleo-origin").value;
		sequence = document.getElementById("nucleo-seq").value;
	}
	else{
		id = document.getElementById("amino-id").value;
		origin = document.getElementById("amino-origin").value;
		sequence = document.getElementById("amino-seq").value;
	}

	$.ajax({
		type: 'POST',
        url: '/submit-data',
		data: {
			'protein': proteinName,
			'file': 0,
			'gen-option': gen_option,
			'id': id,
			'origin': origin,
			'sequence': sequence
		},
    })
}
