document.write('{{ poll_form|escapejs }}');

var pollForm = document.getElementById('poll{{ poll.id }}form');
var pollVoteButton = document.getElementById('poll{{ poll.id }}votebutton');
var pollVoteSubmission = new XMLHttpRequest();

function pollVote() {
    pollVoteSubmission.onreadystatechange = pollStateChange;
    pollVoteSubmission.open(pollForm.method, pollForm.action);
    var postText = '';
    var responses = pollForm.elements['poll{{ poll.id }}response'];
    for (var i = 0; i < responses.length; i++) {
        if (responses[i].checked) postText = responses[i].value
    }
    pollVoteSubmission.setRequestHeader('Content-type', 'text/plain');
    pollVoteSubmission.send(postText);
}

function pollStateChange() {
    if (pollVoteSubmission.readyState == 4) {
        if (pollVoteSubmission.status == 200) {
            document.getElementById('poll{{ poll.id }}display').innerHTML = pollVoteSubmission.responseText;
        }
    }
}

pollVoteButton.onclick = pollVote;
