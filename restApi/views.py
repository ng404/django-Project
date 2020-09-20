from django.shortcuts import render

# Create your views here.
import requests
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Templates
import pymongo
import json
from bson import ObjectId
from django.http import JsonResponse

client=pymongo.MongoClient("mongodb+srv://Password1:Password1@tester.6wke2.mongodb.net/te?retryWrites=true&w=majority")
webhook_url = 'https://hooks.slack.com/services/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'
headers = {
    'Content-type': 'application/json',
}

class TemplateList(APIView):
    
    def get(self,request,customer_id):
        try:
            s=int(customer_id)
            myquery={"customerId":s}
            data=client.te.restApi_templates.find(myquery).sort("id",-1)
            for i in data:
                res = json.dumps(i, cls=JSONEncoder)
                return JsonResponse({"status":status.HTTP_200_OK,"data":res},safe=False)
            data = '{"text":"Customer is not available for which you are accessing i.e customerId:-'+customer_id+'!!"}'
            response = requests.post(webhook_url, headers=headers, data=data)
            return JsonResponse({"status":status.HTTP_200_OK,"data":{"message":"Customer is not available"}},safe=False)
        except ValueError:
            s="Only integers are allowed for Customer_Id"+customer_id
            data = '{"text":"Only integers are allowed for Customer_Id:-  '+customer_id+'"}'
            response = requests.post(webhook_url, headers=headers, data=data)
            return JsonResponse({"status":status.HTTP_404_NOT_FOUND,"data":{"message":"Only integers are allowed"}},safe=False)
    
    
    def post(self,request,customer_id):
        try:
            s=int(customer_id)
            myquery={"customerId":s}
            flag=0
            template=Templates()
            l=[]
            for i in client.te.restApi_templates.find(myquery):
                if(flag==0):
                    template.type=i['type']
                    template.customerId=i['customerId']
                    template.entity=i["entity"]
                    template.law=i["law"]   
                    l=i['fields']
                    flag=1
                else:
                    l=l+i['fields']
            template.fields=l
            if(template.customerId!=None):
                template.save()
            else:
                data = '{"text":"Customer is not available for which you are accessing i.e customerId:-'+customer_id+'!!"}'
                response = requests.post(webhook_url, headers=headers, data=data)
                return JsonResponse({"status":status.HTTP_200_OK,"data":{"message":"Customer is not available"}},safe=False)    
            data=client.te.restApi_templates.find(myquery).sort("id",-1)
            for i in data:
                res = json.dumps(i, cls=JSONEncoder)
                return JsonResponse({"status":status.HTTP_200_OK,"data":res},safe=False)
            data = '{"text":"Connectivity Error for fetching data for CustomerId:- '+customer_id+'"}'
            response = requests.post(webhook_url, headers=headers, data=data)
            return JsonResponse({"status":status.HTTP_500_INTERNAL_SERVER_ERROR,"data":{"message":"Connectivity Error for fetching data"}},safe=False)
        except ValueError:
            data = '{"text":"Only integers are allowed for customerId:-'+customer_id+'"}'
            response = requests.post(webhook_url, headers=headers, data=data)
            return JsonResponse({"status":status.HTTP_404_NOT_FOUND,"data":{"message":"Only integers are allowed"}},safe=False)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)