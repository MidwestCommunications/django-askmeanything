from django.shortcuts import render_to_response

def polldone(request):
    return render_to_response('polldone.html', {'current_user': request.user})
