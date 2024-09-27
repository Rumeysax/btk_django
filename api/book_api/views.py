from django.shortcuts import render
from django.http import JsonResponse
from book_api.models import Books
from book_api.serializer import BookSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# @api_view(['GET'])
# def book_list (request):
#     books = Books.objects.all()
#     serializer = BookSerializer(books, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def book (request, id):
#     try:
#         book = Books.objects.get(pk=id)
#         serializer = BookSerializer(book)
#         return Response(serializer.data)
#     except:
#         return Response({"error":"eşleşen bir kayıt bulunamadı"}, status=status.HTTP_404_NOT_FOUND)
    
# @api_view(['PUT'])
# def book_update(request, id):
#     book = Books.objects.get(pk=id)
#     serializer = BookSerializer(book, data = request.data)    
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
    
#     return Response(serializer.errors)

# @api_view(["DELETE"])
# def book_delete(request, id):
#     book = Books.objects.get(pk=id)
#     book.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['POST'])
# def book_create (request):
#     serializer = BookSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(serializer.errors)



@api_view(['GET', 'POST'])
def books (request):
    if request.method == "GET":
        books = Books.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
# bu fonksiyon ile ekleme ve döndürme işlemleri birleştirilmiş oldu. böylece daha yalın az kod elde edildi 
    

@api_view(['GET', 'PUT', 'DELETE'])
def book (request, id):
    try:
        book = Books.objects.get(pk=id)
    except:
        return Response({"error":"eşleşen bir kayıt bulunamadı"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = BookSerializer(book, data = request.data)    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
        return Response(serializer.errors)

    elif request.method == "DELETE":
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


