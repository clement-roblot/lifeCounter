from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# def index(request):
#     return HttpResponse("Hello, world. You're at the counter index.")



def index(request):

    if not request.user.is_authenticated():
        template = loader.get_template('index.html')

        #testList = Test.objects.filter(user=request.user.id).order_by('title')

        # context = RequestContext(request, {
        # #   'testList'  : testList,
        # })

        return HttpResponse(template.render())

    else:
        template = loader.get_template('index.html')

        #testList = Test.objects.filter(user=request.user.id).order_by('title')

        # context = RequestContext(request, {
        # #    'testList'  : testList,
        # })

        return HttpResponse(template.render())

