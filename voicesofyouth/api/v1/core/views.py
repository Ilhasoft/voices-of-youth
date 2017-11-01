from rest_framework import viewsets
from rest_framework.response import Response


class VoYViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = None
    queryset = []

    def list(self, request, *args, **kwargs):
        limit = int(request.GET.get('limit', 0))
        serializer = self.serializer_class(self.queryset, context={'request': request}, many=True)
        if limit:
            serializer = self.serializer_class(self.queryset[:limit], context={'request': request}, many=True)
        return Response(serializer.data)
