from django.shortcuts import render_to_response

def test(request, poll_id):
    return render_to_response('show.html', {'poll_id': poll_id})
