from django.http import HttpResponse, JsonResponse
from app.serializers import ChequeSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics
from app.services.order_service import *
from bot.services import notification_service

# http://143f-185-139-139-218.ngrok.io/cheque-info?id=%id%&street=%street%&house=%house%&phonenum=%phonenum%&name=%name%&remaining=%remaining%&status_code=%status_code%&code=%code%&car_phone=%car_phone%&car_firstname=%car_firstname%&car_photo=%car_photo%&brand=%brand%&model=%model%&color=%color%&autonum=%autonum%&amount=%amount%&uuid=%uuid%&bonus=%bonus%&discount=%discount%

@api_view(['GET', 'POST'])
def cheque_info(request):
    if request.method == 'GET':
        if request.GET['phonenum'] == '+998901385003':
            print(request.GET)
        
        serializer = ChequeSerializer(data=request.GET)
        
        if serializer.is_valid():
            data = serializer.initial_data
            phone = data['phonenum']
            uuid = data['uuid']
            # check status and send message
            if data['status_code'] in ['80', '95', '10', '11', '4']:
                # send notification
                notification_service.send_order_status(phone, data)
                change_order_status_by_uuid(uuid, data['status_code'])

            elif data['status_code'] == '100':
                serializer.save()
                # send notification
                notification_service.send_cheque(
                    phone, data['car_phone'], data['car_firstname'], 
                    data['brand'] or '', data['model'] or '', data['color'] or '', 
                    data['autonum'] or '', data['amount'], 
                )
                change_order_status_by_uuid(uuid, data['status_code'])
                return Response(status=status.HTTP_200_OK)

            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    return JsonResponse({})


# <QueryDict: {'id': ['1008881'], 'street': [''], 'house': [''], 'phonenum': ['+998919800555'], 'name': [''], 'remaining': ['10'], 'status_code': ['100'], 'code': ['054'], 'car_phone': ['+998900065196'], 'car_firstname': ['??????????????'], 'car_photo': [''], 'brand': ['Chevrolet'], 'model': ['Cobalt'], 'color': ['??????????'], 'autonum': ['054'], 'amount': ['10000.0000'], 'uuid': [''], 'bonus': [''], 'discount': ['']}>
# {'code': 80, 'name': '???? ??????????????????'}} , operator qabul qilishi kk
# {'code': 95, 'name': '???????????? ??????????????????'}
# {'code': 10, 'name': '???????????????? ?????????? ????????????????'}  ///  'remaining': ['5']
# {'code': 11, 'name': '???????????????? ?? ???????????????? ????????????'}} mashina yetib keldi
# 'code': 4, 'name': '?? ????????????????????'}}, start, yulda
# {'code': 100, 'name': '?????????? ????????????????'}}

# {'code': 9, 'name': '??????????????????'}}