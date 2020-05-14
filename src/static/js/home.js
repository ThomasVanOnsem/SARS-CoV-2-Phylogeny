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
	$('#selectedNodeContent').empty();
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
        document.getElementById("submit-btn").classList.add("is-loading")
        let formData = new FormData(this);
        if ($("#choose-pplacer").hasClass("is-selected")) {
            formData.append("algorithm", "pplacer");
        } else {
            formData.append("algorithm", "fasttree");
        }

        $.ajax({
            url: '/submit-data',
            type: 'POST',
            data: formData,
            cache: false,
            contentType: false,
            processData: false
        }).done(function (data) {
            document.getElementById("submit-btn").classList.remove("is-loading");
            if(!data["success"]){
                let error_div = document.getElementById("error-field");
                error_div.innerHTML = data['error'];
                error_div.style.display = '';
                return;
            }
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
        content: 'Run a fast placement algorithm.'
    });
    tippy('#choose-fasttree',{
        content: 'Completely rebuild the phylo tree with FastTree.'
    });
    tippy('#newick-info',{
        content: 'Interactive Newick representation of chosen protein.'
    });
}
