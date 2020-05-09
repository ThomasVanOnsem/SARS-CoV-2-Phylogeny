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
				$('#nucleotide-adding-title').attr('style', '');
				$('#nucleotide-adding').attr('style', '');
				$('#amino-acid-adding-title').attr('style', 'display:none;');
				$('#amino-acid-adding').attr('style', 'display:none;');
			} else {
				$('#nucleotide-adding-title').attr('style', 'display:none;');
				$('#nucleotide-adding').attr('style', 'display:none;');
				$('#amino-acid-adding-title').attr('style', '');
				$('#amino-acid-adding').attr('style', '');
			}
		}
	})
}

const fileInput = $('#upload-zone input[type=file]').eq(0);
fileInput.onchange = () => {
if (fileInput.files.length > 0) {
  const fileName = $('#upload-zone .file-name').eq(0);
  fileName.textContent = fileInput.files[0].name;
}
}