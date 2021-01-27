def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': user.username,
        'user_id': user.id
    }


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNum(PageNumberPagination):
    page_size = 5
    page_size_query_description = 'pagesize'

    def get_paginated_response(self, data):
        return Response(
            {
                'count': self.page.paginator.count,
                'lists': data,
                'page': self.page.number,
                'pages': self.page.paginator.num_pages,
                'pagesize': self.page_size,
            }
        )
