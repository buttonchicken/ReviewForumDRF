from itertools import product
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .serializers import *
from ReviewForum.custom_permissions import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist

class ViewProducts(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        try:
            products = Product.objects.all()
            product_data = ProductSerializer(products,many=True).data
        except ObjectDoesNotExist:
            product_data={}
        return Response({'data':product_data},status=status.HTTP_200_OK)

class ViewProductbyID(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        product_id = request.data['product_id']
        try:
            product = Product.objects.get(product_id=product_id)
            if product.created_by == request.user:
                product_data = ProductSerializer(product).data
                return Response({'success':True,'data':product_data},status=status.HTTP_200_OK)
            return Response({'success':False,'message':"Cannot View Product by ID which you did not create!"},status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response({'success':False,'message':"Invalid Product ID"},status=status.HTTP_400_BAD_REQUEST)

class CreateProduct(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [seller]
    def post(self,request):
        try:
            body = request.data['body']
            image_file = request.FILES['file']
            product = Product.objects.create(created_by=request.user,image=image_file,body=body)
            return Response({'Success':True,'Product_ID':product.product_id},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Success':False,'message':'Please enter all the data!'},status=status.HTTP_400_BAD_REQUEST)

class EditProduct(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [seller]
    def put(self, request):
        product_id = request.data['product_id']
        try:
            product = Product.objects.get(product_id=product_id)
            if product.created_by==request.user:
                serializer = EditProductSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                product.body = serializer.validated_data.get('body')
                product.image = serializer.validated_data.get('file')
                product.save()
                return Response({"success": True, "message": "Product Updated"}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "message": "Cannot edit products you did not create!"}, status=status.HTTP_403_FORBIDDEN)    
        except:
            return Response({"success": False, "message": "Invalid Product ID"}, status=status.HTTP_400_BAD_REQUEST)

class DeleteProduct(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [seller]
    def put(self, request):
        product_id = request.data['product_id']
        try:
            product = Product.objects.get(product_id=product_id)
            if product.created_by==request.user:
                product.body = "Deleted"
                product.image = "Deleted"
                product.save()
                return Response({"success": True, "message": "Product Deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "message": "Cannot delete products you did not create!"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"success": False, "message": "Invalid product ID"}, status=status.HTTP_400_BAD_REQUEST)

class AddReview(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[customer]
    def post(self,request):
        product_id = request.data['product_id']
        try:
            product = Product.objects.get(product_id=product_id)
            rating = request.data['rating']
            comment = request.data['comment']
            review = Review.objects.create(written_by=request.user,rating=rating,comment=comment)
            product.save()
            product.reviews.add(review)
            return Response({"success": True,"review_id": review.review_id,"message": "Review posted"}, status=status.HTTP_200_OK)
        except ValidationError:
            return Response({"success": False, "message": "Rating needs to be between 0 and 5"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"success": False, "message": "Invalid product ID"}, status=status.HTTP_200_OK)

class EditReview(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[customer]
    def put(self, request):
        review_id = request.data['review_id']
        try:
            review = Review.objects.get(review_id=review_id)
            if review.written_by==request.user:
                review.comment = request.data['comment']
                review.rating = request.data['rating']
                review.save()
                return Response({"success": True, "message": "Review updated"}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "message": "Cannot edit review you did not write!"}, status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response({"success": False, "message": "Invalid product/review ID"}, status=status.HTTP_400_BAD_REQUEST)

class DeleteReview(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[customer]
    def put(self, request):
        review_id = request.data['review_id']
        try:
            review = Review.objects.get(review_id=review_id)
            if review.written_by==request.user:
                review.comment = "Deleted"
                review.rating = 0
                review.save()
                return Response({"success": True, "message": "Review Deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "message": "Cannot delete review you did not write!"}, status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response({"success": False, "message": "Invalid product/review ID"}, status=status.HTTP_400_BAD_REQUEST)

class AddReply(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[seller]
    def put(self, request):
        review_id = request.data['review_id']
        product_id = request.data['product_id']
        reply = request.data['reply']
        try:
            product = Product.objects.get(product_id=product_id)
            review = Review.objects.get(review_id=review_id)
            if product.created_by==request.user and review in product.reviews.all():
                review.reply = reply
                review.save()
                return Response({"success": True, "message": "Successfully replied"}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "message": "Cannot reply for product you did not create!"}, status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response({"success": False, "message": "Invalid review ID"}, status=status.HTTP_400_BAD_REQUEST)    
        


