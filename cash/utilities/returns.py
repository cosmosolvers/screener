from rest_framework.response import Response
from rest_framework import status


def get_response(status_code, message, data=None):
    return Response(
        {
            'status': status_code,
            'message': message,
            'data': data
        },
        status=status_code
    )


def many(self, request, *args, **kwargs):
    paginator = self.pagination_class()
    page = paginator.paginate_queryset(self.get_queryset(), request)
    serializer = self.get_serializer(page, many=True)
    return get_response(
        status.HTTP_200_OK,
        'all',
        paginator.get_paginated_response(
            serializer.data
        ).data
    )


def one(self, request, *args, **kwargs):
    serializer = self.get_serializer(self.get_object())
    return get_response(
        status.HTTP_200_OK,
        'details',
        serializer.data
    )


def error_manage(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            return func(self, request, *args, **kwargs)
        except Exception as e:
            return get_response(
                status.HTTP_400_BAD_REQUEST if not kwargs.get('status_code')
                else kwargs.get('status_code'),
                str(e)
            )
    return wrapper
