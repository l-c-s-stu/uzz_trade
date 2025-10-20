from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        goods_id = self.kwargs['goods_id']
        return Comment.objects.filter(goods_id=goods_id).order_by('-created_at')

    def perform_create(self, serializer):
        goods_id = self.kwargs['goods_id']
        serializer.save(user=self.request.user, goods_id=goods_id)
