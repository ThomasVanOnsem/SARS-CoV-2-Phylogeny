$(window).ready(function(){
    getStoredSequences();
});


let sequences;


function getStoredSequences() {
    let request = new XMLHttpRequest();
    request.open('GET', '/get-stored-sequences', true);
    request.onload = function() {
        let data = JSON.parse(this.response);
        if (request.status >= 200 && request.status < 400) {
            sequences = data;
            populateSequenceChoices();
        } else {
            console.log('Failed to fetch stored sequences!');
        }
    };
    request.send();
}

function populateSequenceChoices() {
    let select = document.getElementById("sequence-choices");
    for(let i=0; i<sequences.length; i++){
        let option = document.createElement("option");
        option.value = sequences[i]; //TODO correct read
        select.appendChild(option);
    }
    //TODO show in text area
}

function addProgressBar() {
    let div = document.getElementById("progress-bar-div")

}