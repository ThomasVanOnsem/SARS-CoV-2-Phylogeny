function triggerToggleResult(event){
	event.preventDefault();
	var options = $('#type-view-output').children();
	options.each(function () {
		$(this).blur()
		if ($(this).hasClass('is-selected')) {
			$(this).removeClass('is-selected');
			$(this).removeClass('is-primary');
		} else {
			$(this).addClass('is-selected');
			$(this).addClass('is-primary');

			//now we change the page
			if($(this).attr('id') === 'choose-img'){
				$('#image-view').attr('style', '');
				$('#newick-view').attr('style', 'display:none;');
			} else {
				$('#image-view').attr('style', 'display:none;');
				$('#newick-view').attr('style', '');
			}
		}
	})
}