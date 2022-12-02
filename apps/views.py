from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.filters import ProductFilter
from apps.models import Category, ProductImage, Product
from apps.serializers import CategoryModelSerializer, ProductImageModelSerializer, ProductModelSerializer


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.order_by('-created_at')
    serializer_class = CategoryModelSerializer
    lookup_field = 'slug'


class ProductImageAPIView(GenericAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageModelSerializer
    parser_classes = (MultiPartParser,)

    def get(self, request):
        images = ProductImage.objects.all()
        serializer = ProductImageModelSerializer(images, many=True)
        serializer_dict = {
            'status': 'OK',
            'success': True,
            'data': serializer.data
        }
        return Response(serializer_dict)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.order_by('-created_at')
    serializer_class = ProductModelSerializer
    lookup_url_kwarg = 'id'
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    filterset_fields = {
        'price': ['gte','lte']
    }