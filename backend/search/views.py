from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import *


@csrf_exempt
def search(request):
    keyword = request.POST.get('keyword')

    entryList = []
    # field - SimplifiedName
    result_1 = Entry.objects.filter(SimplifiedName__contains=keyword)
    # field - TraditionalName
    result_2 = Entry.objects.filter(TraditionalName__contains=keyword)
    # field - PinyinName
    result_3 = Entry.objects.filter(PinyinName__contains=keyword)
    # field - EnglishName_1
    result_4 = Entry.objects.filter(EnglishName_1__contains=keyword)
    # field - EnglishName_2
    result_5 = Entry.objects.filter(EnglishName_2__contains=keyword)
    # field - EnglishName_3
    result_6 = Entry.objects.filter(EnglishName_3__contains=keyword)
    
    # union and distinct
    result = result_1 | result_2 | result_3 | result_4 | result_5 | result_6
    result.distinct()
    # get its sort info
    for entry in result:
        entryList.append({
            'id': entry.id,
            'SimplifiedName': entry.SimplifiedName,
            'TraditionalName': entry.TraditionalName,
            'PinyinName': entry.PinyinName,
            'EnglishName_1': entry.EnglishName_1,
            'EnglishName_2': entry.EnglishName_2,
            'EnglishName_3': entry.EnglishName_3,
            'EnglishInterpretation': entry.EnglishInterpretation,
            'sortName': entry.sort.name,
            'sortCode': entry.sort.code
        })

    return JsonResponse({ 'info': entryList })
