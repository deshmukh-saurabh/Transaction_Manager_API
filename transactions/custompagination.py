from rest_framework.pagination import LimitOffsetPagination
class LimitOffsetPaginationWithUpperBound(LimitOffsetPagination):
    # max limit = 5
    max_limit=5