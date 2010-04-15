//requires jQuery

var addExtraResponse = function(event) {
    $(this).unbind(event);
    var forms_count = parseInt($('#id_responses-TOTAL_FORMS').val()) + 1;
    var new_response = $(this).parent().parent().clone();
    new_response.find('input:text').attr({
        id: 'id_responses-' + forms_count + '-answer',
        name: 'responses-' + forms_count + '-answer',
        value: ''
    });
    new_response.insertBefore('#pollcreateformsubmitrow');
    $('#id_responses-TOTAL_FORMS').val(forms_count);
    bindLastResponse();
}

var bindLastResponse = function() {
    $('#pollcreateform input[id^="id_responses-"][id$="-answer"]:last').bind('keydown', addExtraResponse);
}

$(document).ready(function() {
    $('#pollcreateformtable tr').not(':lt(2), :last').remove();
    $('#id_responses-TOTAL_FORMS').val(1);
    bindLastResponse();
});