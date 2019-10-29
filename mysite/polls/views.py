from django.http import  HttpResponse

def index(request):
    return HttpResponse("hello world!")

def detail(request, question_id):
    return HttpResponse("You are looking at question %s." % question_id)

def results(request, question_id):
    response="You'are looing at the result of question %s."
    return HttpResponse(response % question_id)
def vote(request, question_id):
    return HttpResponse("You are voting on question %s." % question_id)