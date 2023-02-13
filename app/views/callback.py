from django.http import HttpResponse, JsonResponse
from app.serializers import ChequeSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics
from bot.services import notification_service

# http://143f-185-139-139-218.ngrok.io/cheque-info?id=%id%&street=%street%&house=%house%&phonenum=%phonenum%&name=%name%&remaining=%remaining%&status_code=%status_code%&code=%code%&car_phone=%car_phone%&car_firstname=%car_firstname%&car_photo=%car_photo%&brand=%brand%&model=%model%&color=%color%&autonum=%autonum%&amount=%amount%&uuid=%uuid%&bonus=%bonus%&discount=%discount%

@api_view(['GET', 'POST'])
def cheque_info(request):
    print(request.method)
    if request.method == 'GET':
        # print(request.GET['phonenum'])
        if request.GET['phonenum'] == '+998901385003':
            print(request.GET)

        return Response(status=status.HTTP_200_OK)
        
        serializer = ChequeSerializer(data=request.GET)
        
        if serializer.is_valid():
            data = serializer.initial_data
            # check status
            if data['status_code'] == '101':
                serializer.save()
                # send notification
                notification_service.send_cheque(
                    data['phonenum'], data['car_phone'], data['car_firstname'], 
                    data['brand'] or '', data['model'] or '', data['color'] or '', 
                    data['autonum'] or '', data['amount'], 
                )
                return Response(status=status.HTTP_200_OK)

            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    return JsonResponse({})


# <QueryDict: {'id': ['1008881'], 'street': [''], 'house': [''], 'phonenum': ['+998919800555'], 'name': [''], 'remaining': ['10'], 'status_code': ['100'], 'code': ['054'], 'car_phone': ['+998900065196'], 'car_firstname': ['Асадбек'], 'car_photo': [''], 'brand': ['Chevrolet'], 'model': ['Cobalt'], 'color': ['Белый'], 'autonum': ['054'], 'amount': ['10000.0000'], 'uuid': [''], 'bonus': [''], 'discount': ['']}>
# {'code': 80, 'name': 'На модерации'}} , operator qabul qilishi kk
# {'code': 95, 'name': 'Клиент отказался'}
# {'code': 10, 'name': 'Сообщили время подъезда'}  ///  'remaining': ['5']
# {'code': 11, 'name': 'Сообщили о подъезде машины'}} mashina yetib keldi
# 'code': 4, 'name': 'В исполнении'}}, start, yulda
# {'code': 100, 'name': 'Заказ выполнен'}}
