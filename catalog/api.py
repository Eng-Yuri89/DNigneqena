##### get data from model ---------> json
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def category_list_api(request):
    all_category = Category.objects.all()
    data = CategorySerializer(all_category , many=True).data
    return Response({'data':data})

@api_view(['GET'])
def category_details_api(request,id):
    category_detail = Category.objects.get(id=id)
    data = CategorySerializer(category_detail ).data
    return Response({'data':data})

#####Clas based
class CategoryListAPi(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    model = Category
    queryset = Category.objects.all()

    serializer_class = CategorySerializer

class CategoryListAPi(generics.ListCreateAPIView):
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class CategoryAPi(generics.RetrieveUpdateDestroyAPIView):
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class ProductListAPi(generics.ListAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class ProductAPi(generics.RetrieveUpdateDestroyAPIView):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class CatList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'admin/pages/category.html'

    def get(self, request):
        queryset = Category.objects.all()
        return Response({'categories': queryset})