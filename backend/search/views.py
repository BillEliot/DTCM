from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import *


@csrf_exempt
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    # _cEtCm_s
    if username == 'CETCMS' and password == '88c8f87eadd78d87eafabfe0f529fbe8':
        return HttpResponse(0)
    else:
        return HttpResponse(1)



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
def searchEntry(request):
    simplifiedName = request.POST.get('simplifiedName')

    entryList = []
    for entry in Entry.objects.filter(SimplifiedName__contains=simplifiedName):
        entryList.append({
            'key': entry.id,
            'simplifiedName': entry.SimplifiedName,
            'pinyin': entry.PinyinName,
            'sortName': entry.sort.name,
            'sortCode': entry.sort.code
        })
    
    return JsonResponse({ 'info': entryList })



@csrf_exempt
def reportEntry(request):
    _id = request.POST.get('id')
    item = request.POST.get('item')
    feedback = request.POST.get('feedback')

    try:
        Review.objects.create(
            entry=Entry.objects.get(id=_id),
            item=item,
            feedback=feedback
        )
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def getAllEntries(request):
    entryList = []
    for entry in Entry.objects.all():
        entryList.append({
            'key': entry.id,
            'simplifiedName': entry.SimplifiedName,
            'pinyin': entry.PinyinName,
            'sortName': entry.sort.name,
            'sortCode': entry.sort.code
        })
    
    return JsonResponse({ 'info': entryList })



@csrf_exempt
def getAllReviews(request):
    reviewList = []
    for review in Review.objects.all():
        reviewList.append({
            'reviewID': review.id,
            'key': review.entry.id,
            'item': review.item,
            'feedback': review.feedback,
            'date': review.date
        })
    
    return JsonResponse({ 'info': reviewList })



@csrf_exempt
def detail(request):
    SimplifiedName = request.POST.get('SimplifiedName')
    try:
        entry = Entry.objects.get(SimplifiedName=SimplifiedName)
        return JsonResponse({
            'id': entry.id,
            'simplifiedName': entry.SimplifiedName,
            'traditionalName': entry.TraditionalName,
            'pinyinName': entry.PinyinName,
            'englishName_1': entry.EnglishName_1,
            'englishName_2': entry.EnglishName_2,
            'englishName_3': entry.EnglishName_3,
            'englishInterpretation': entry.EnglishInterpretation,
            'sortCode': entry.sort.code,
            'sortName': entry.sort.name
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def getEntry(request):
    _id = request.POST.get('id')
    try:
        entry = Entry.objects.get(id=_id)
        return JsonResponse({
            'id': entry.id,
            'simplifiedName': entry.SimplifiedName,
            'traditionalName': entry.TraditionalName,
            'pinyinName': entry.PinyinName,
            'englishName_1': entry.EnglishName_1,
            'englishName_2': entry.EnglishName_2,
            'englishName_3': entry.EnglishName_3,
            'englishInterpretation': entry.EnglishInterpretation,
            'sortCode': entry.sort.code,
            'sortName': entry.sort.name
        })
    except:
        return HttpResponse(1)



@csrf_exempt
def deleteEntry(request):
    _id = request.POST.get('id')
    try:
        entry = Entry.objects.get(id=_id)
        entry.delete()
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def updateEntry(request):
    _id = request.POST.get('id')
    simplifiedName = request.POST.get('simplifiedName')
    traditionalName = request.POST.get('traditionalName')
    pinyinName = request.POST.get('pinyinName')
    englishName_1 = request.POST.get('englishName_1')
    englishName_2 = request.POST.get('englishName_2')
    englishName_3 = request.POST.get('englishName_3')
    englishInterpretation = request.POST.get('englishInterpretation')
    sortName = request.POST.get('sortName')
    sortCode = request.POST.get('sortCode')

    try:
        entry = Entry.objects.get(id = _id)
        entry.SimplifiedName = simplifiedName
        entry.TraditionalName = traditionalName
        entry.PinyinName = pinyinName
        entry.EnglishName_1 = englishName_1
        entry.EnglishName_2 = englishName_2
        entry.EnglishName_3 = englishName_3
        entry.EnglishInterpretation = englishInterpretation
        entry.sort.name = sortName
        entry.sort.code = sortCode
        entry.save()
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def denyReview(request):
    reviewID = request.POST.get('reviewID')
    try:
        review = Review.objects.get(id=reviewID)
        review.delete()
        return HttpResponse(0)
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
