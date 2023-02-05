from django.http import HttpResponse, JsonResponse
from bot.serializers import ChequeSerializer
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
        print(request.GET)
        serializer = ChequeSerializer(data=request.GET)
        if serializer.is_valid():
            data = serializer.data
            
            # check status
            if data['status_code'] == '100':

                # send notification
                notification_service.send_cheque(
                    data['phonenum'], data['car_phone'], data['car_firstname'], 
                    data['brand'] or '', data['model'] or '', data['color'] or '', 
                    data['autonum'] or '', data['amount'], 
                )
                return Response(status=status.HTTP_200_OK)

            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            print()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    return JsonResponse({})


# <QueryDict: {'id': ['1008881'], 'street': [''], 'house': [''], 'phonenum': ['+998919800555'], 'name': [''], 'remaining': ['10'], 'status_code': ['100'], 'code': ['054'], 'car_phone': ['+998900065196'], 'car_firstname': ['Асадбек'], 'car_photo': [''], 'brand': ['Chevrolet'], 'model': ['Cobalt'], 'color': ['Белый'], 'autonum': ['054'], 'amount': ['10000.0000'], 'uuid': [''], 'bonus': [''], 'discount': ['']}>