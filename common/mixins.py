from rest_framework.fields import empty
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import status


class CustomFieldsMixin:
    def get_serializer(self, instance=None, data=empty, many=False, partial=False):
        print "mixin"
        if self.request.method == "PUT":
            return self.serializer_class(instance=instance, data=data, many=many, partial=True, fields=None,
                                         context={'request': self.request})

        else:
            fields = self.request.GET.get('fields', None)
            if fields is None:
                return self.serializer_class(instance=instance, data=data, many=many, partial=partial,
                                             fields=None, context={'request': self.request})

            else:
                fields = fields.split(',')
                return self.serializer_class(instance=instance, data=data, many=many, partial=partial, fields=fields,
                                             context={'request': self.request})


class ActiveDesactiveMixin:
    @detail_route(methods=['put'])
    def activate(self, request, pk=None, username=None):
        try:
            if pk:
                instance = self.model.objects.get(pk=pk)
            else:
                instance = self.model.objects.get(username=username)
        except self.model.DoesNotExist:
            instance = None

        if instance is None:
            return Response(data={
                'has_error': True,
                'error_message': 'Resource does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)

        instance.is_active = True
        instance.save()
        return Response(data={
            'success': True,
            'success_message': 'Resource activated',
            'result': self.serializer_class(instance, fields=['is_active']).data
        }, status=status.HTTP_200_OK)

    @detail_route(methods=['put'])
    def deactivate(self, request, pk=None, username=None):
        try:
            if pk:
                instance = self.model.objects.get(pk=pk)
            else:
                instance = self.model.objects.get(username=username)
        except self.model.DoesNotExist:
            instance = None

        if instance is None:
            return Response(data={
                'has_error': True,
                'error_message': 'Resource does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)

        instance.is_active = False
        instance.save()
        return Response(data={
            'success': True,
            'success_message': 'Resource deactivated',
            'result': self.serializer_class(instance, fields=['is_active']).data
        }, status=status.HTTP_200_OK)