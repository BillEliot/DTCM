from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import check_password
from django.db.models.functions import Length
from .models import *
from utils.utils import *


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
    captcha = request.POST.get('captcha')
    encryCaptcha = request.POST.get('encryCaptcha')

    # Multiple consecutive searches are not allowed
    request.session['searchNum'] = request.session.get('searchNum', default=0) + 1
    request.session.set_expiry(0)
    if request.session.get('searchNum', default=0) > 2 and captcha == '':
        encryCaptcha = genCaptcha()
        return JsonResponse({ 'encryCaptcha': encryCaptcha })
    elif request.session.get('searchNum', default=0) > 2 and captcha != '':
        # check captcha
        if not check_password(captcha, encryCaptcha):
            return HttpResponse(1)

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
    # get its sort info
    for entry in result.distinct().order_by(Length('SimplifiedName').asc(), 'PinyinName')[:10]:
        entryList.append({
            'id': entry.id,
            'SimplifiedName': entry.SimplifiedName,
            'TraditionalName': entry.TraditionalName,
            'PinyinName': entry.PinyinName,
            'EnglishName_1': entry.EnglishName_1
        })

    return JsonResponse({ 'info': entryList })



@csrf_exempt
def searchEntry(request):
    simplifiedName = request.POST.get('simplifiedName')

    entryList = []
    try:
        for entry in Entry.objects.filter(SimplifiedName__contains=simplifiedName):
            entryList.append({
                'key': entry.id,
                'simplifiedName': entry.SimplifiedName,
                'pinyin': entry.PinyinName,
                'sortName': entry.sort.name,
                'sortCode': entry.sort.code
            })
    except:
        print('Error')
    return JsonResponse({ 'info': entryList })



@csrf_exempt
def reportEntry(request):
    _id = request.POST.get('id')
    item = request.POST.get('item')
    feedback = request.POST.get('feedback')
    captcha = request.POST.get('captcha')
    encryCaptcha = request.POST.get('encryCaptcha')

    # Multiple consecutive reports are not allowed
    request.session['reportNum'] = request.session.get('reportNum', default=0) + 1
    request.session.set_expiry(0)
    if request.session.get('reportNum', default=0) > 2 and captcha == '':
        encryCaptcha = genCaptcha()
        return JsonResponse({ 'encryCaptcha': encryCaptcha })
    elif request.session.get('reportNum', default=0) > 2 and captcha != '':
        # check captcha
        if not check_password(captcha, encryCaptcha):
            return HttpResponse(1)

    try:
        Review.objects.create(
            entry=Entry.objects.get(id=_id),
            item=item,
            feedback=feedback
        )
        return HttpResponse(0)
    except:
        return HttpResponse(2)



@csrf_exempt
def getAllEntries(request):
    index = int(request.POST.get('index'))

    entryList = []
    for entry in Entry.objects.all()[index*10+1:index*10+11]:
        try:
            entryList.append({
                'key': entry.id,
                'simplifiedName': entry.SimplifiedName,
                'pinyin': entry.PinyinName,
                'sortName': entry.sort.name,
                'sortCode': entry.sort.code
            })
        except:
            print("Error")
    
    return JsonResponse({ 'list': entryList, 'total': Entry.objects.all().count() / 10 })



@csrf_exempt
def getAllReviews(request):
    reviewList = []
    for review in Review.objects.all():
        reviewList.append({
            'key': review.id,
            'id': review.entry.id,
            'item': review.item,
            'feedback': review.feedback,
            'date': review.date
        })
    
    return JsonResponse({ 'info': reviewList })



@csrf_exempt
def detail(request):
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
    key = request.POST.get('key')
    try:
        review = Review.objects.get(id=key)
        review.delete()
        return HttpResponse(0)
    except:
        return HttpResponse(1)



@csrf_exempt
def autoComplete(request):
    keyword = request.POST.get('keyword')
    rule = request.POST.get('rule')

    if keyword:
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
            return JsonResponse({ 'info': entryList })
        elif rule == "英 -> 中":
            # field - EnglishName_1
            result_1 = Entry.objects.filter(EnglishName_1__contains=keyword)
            if result_1.count() != 0:
                for entry in result_1.order_by('id').distinct()[:10]:
                    entryList.append(entry.EnglishName_1)
                return JsonResponse({ 'info': entryList })
            # field - EnglishName_2
            result_2 = Entry.objects.filter(EnglishName_2__contains=keyword)
            if result_2.count() != 0:
                for entry in result_2.order_by('id').distinct()[:10]:
                    entryList.append(entry.EnglishName_2)
                return JsonResponse({ 'info': entryList })
            # field - EnglishName_3
            result_3 = Entry.objects.filter(EnglishName_3__contains=keyword)
            if result_3.count() != 0:
                for entry in result_3.order_by('id').distinct()[:10]:
                    entryList.append(entry.EnglishName_3)
                return JsonResponse({ 'info': entryList })

    return JsonResponse({ 'info': ['NULL'] })
