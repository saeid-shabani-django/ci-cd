from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page"
    max_page_size = 10
