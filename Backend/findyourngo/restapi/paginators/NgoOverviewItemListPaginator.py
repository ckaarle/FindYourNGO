from django.http import JsonResponse
from rest_framework import pagination


class NgoOverviewItemListPaginator(pagination.PageNumberPagination):

    def get_paginated_response(self, data) -> JsonResponse:
        response = super(NgoOverviewItemListPaginator, self).get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        response.data['current_page'] = self.page.number
        return response
