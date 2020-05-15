$(window).ready(function() {
	setupFormSubmission();
	setupFileInput();
	setupPopovers();
    fetchTree();
	initializeScaleNewick();
    initializeMoveNewick();
});

function onProteinChange(event) {
	event.preventDefault();
	$('#selectedNodeCard').hide();
	fetchTree();
}

function toggleSubmissionForm() {
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

function triggerToggleAlgorithmType(event) {
	event.preventDefault();
	var options = $('#algorithm-input').children();
	options.each(function () {
		$(this).blur();
		if ($(this).hasClass('is-selected')) {
			$(this).removeClass('is-selected');
			$(this).removeClass('is-primary');
		} else {
			$(this).addClass('is-selected');
			$(this).addClass('is-primary');
		}
	})
}

function setupFormSubmission() {
	$("form#submit-form-data").submit(function(e) {
        let div = document.getElementById("add-data");
        if(div.style.display !== ''){
            return;
        }
        e.preventDefault();
        document.getElementById("submit-btn").classList.add("is-loading");
        let formData = new FormData(this);
        if ($("#choose-pplacer").hasClass("is-selected")) {
            formData.append("algorithm", "pplacer");
        } else {
            formData.append("algorithm", "fasttree");
        }
        formData.append('proteinChoice', $("#proteinChoice").val());

        $.ajax({
            url: '/submit-data',
            type: 'POST',
            data: formData,
            cache: false,
            contentType: false,
            processData: false
        }).done(function (data) {
            document.getElementById("submit-btn").classList.remove("is-loading");
            let errorBar = $("#error-field");
            let successBar = $("#success-field");
            if(!data["success"]){
                successBar.hide();
                errorBar.show();
                errorBar.text(data['error']);
                return;
            }
            errorBar.hide();
            $("#add-data").hide();
            successBar.show().text("Success! Location of your sequences are in red");
            let newickJson = data['newick'];
            setUpNewick(newickJson);
        });
    });
}

function setupFileInput() {
	const fileInput = document.querySelector('#upload-zone input[type=file]');
    fileInput.onchange = () => {
        if (fileInput.files.length > 0) {
            const fileName = document.querySelector('#upload-zone .file-name');
            fileName.textContent = fileInput.files[0].name;
        }
    };
}

function setupPopovers() {
	tippy('#choose-pplacer',{
        content: 'Makes a temporary and quick placement using pplacer, which includes a likelihood.'
    });
    tippy('#choose-fasttree',{
        content: 'Permanently adds your sequences to the tree by using FastTree, takes longer but has more accurate results'
    });
}
