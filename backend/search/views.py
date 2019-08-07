from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import *


@csrf_exempt
def search(request):
    keyword = request.POST.get('keyword')
    rule = request.POST.get('rule')

    entryList = []
    if rule == '中 -> 英':
        # field - SimplifiedName
        result_1 = Entry.objects.filter(SimplifiedName__contains=keyword)
        # field - TraditionalName
        result_2 = Entry.objects.filter(TraditionalName__contains=keyword)
        # field - PinyinName
        result_3 = Entry.objects.filter(PinyinName__contains=keyword)
    elif rule == '英 -> 中':
        # field - EnglishName_1
        result_1 = Entry.objects.filter(EnglishName_1__contains=keyword)
        # field - EnglishName_2
        result_2 = Entry.objects.filter(EnglishName_2__contains=keyword)
        # field - EnglishName_3
        result_3 = Entry.objects.filter(EnglishName_3__contains=keyword)
    
    # union and distinct
    result = result_1 | result_2 | result_3
    result.distinct()
    # get its sort info
    for entry in result:
        entryList.append({
            'id': entry.id,
            'SimplifiedName': entry.SimplifiedName,
            'PinyinName': entry.PinyinName,
            'EnglishName_1': entry.EnglishName_1
        })

    return JsonResponse({ 'info': entryList })



@csrf_exempt
def submitEntry(request):
    simplifiedName = request.POST.get('simplifiedName')
    traditionalName = request.POST.get('traditionalName')
    pinyin = request.POST.get('pinyin')
    englishName_1 = request.POST.get('englishName_1')
    englishName_2 = request.POST.get('englishName_2')
    englishName_3 = request.POST.get('englishName_3')
    englishInterpretation = request.POST.get('englishInterpretation')
    sortName = request.POST.get('sortName')
    sortCode = request.POST.get('sortCode')

    pass



@csrf_exempt
def reportEntry(request):
    item = request.POST.get('item')
    feedback = request.POST.get('feedback')

    pass



@csrf_exempt
def detail(request):
    SimplifiedName = request.POST.get('SimplifiedName')
    try:
        entry = Entry.objects.get(SimplifiedName=SimplifiedName)
        return JsonResponse({
            'id': entry.id,
            'SimplifiedName': entry.SimplifiedName,
            'TraditionalName': entry.TraditionalName,
            'PinyinName': entry.PinyinName,
            'EnglishName_1': entry.EnglishName_1,
            'EnglishName_2': entry.EnglishName_2,
            'EnglishName_3': entry.EnglishName_3,
            'EnglishInterpretation': entry.EnglishInterpretation,
            'sortCode': entry.sort.code,
            'sortName': entry.sort.name
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def autoComplete(request):
    keyword = request.POST.get('keyword')
    rule = request.POST.get('rule')

    entryList = []
    if rule == "中 -> 英":
        # field - SimplifiedName
        result_1 = Entry.objects.filter(SimplifiedName__contains=keyword)
        # field - TraditionalName
        result_2 = Entry.objects.filter(TraditionalName__contains=keyword)
        # field - PinyinName
        result_3 = Entry.objects.filter(PinyinName__contains=keyword)

        # union and distinct
        result = result_1 | result_2 | result_3
        result = result.order_by('id').distinct()[:10]
        # get its sort info
        for entry in result:
            entryList.append(entry.SimplifiedName)
    elif rule == "英 -> 中":
        # field - EnglishName_1
        result_1 = Entry.objects.filter(EnglishName_1__contains=keyword)
        # field - EnglishName_2
        result_2 = Entry.objects.filter(EnglishName_2__contains=keyword)
        # field - EnglishName_3
        result_3 = Entry.objects.filter(EnglishName_3__contains=keyword)

        # union and distinct
        result = result_1 | result_2 | result_3
        result = result.order_by('id').distinct()[:10]
        # get its sort info
        for entry in result:
            entryList.append(entry.EnglishName_1)

    return JsonResponse({ 'info': entryList })
