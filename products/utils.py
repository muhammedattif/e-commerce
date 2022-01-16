from .models import Product
import src.utils as general_utils

def get_product(id, prefetch_related=None, select_related=None):
    try:
        query = Product.objects
        if prefetch_related:
            query =  query.prefetch_related(*prefetch_related)
        if select_related:
            query =  query.select_related(*select_related)
        return query.get(id=id), True, None
    except Product.DoesNotExist:
        return None, False, general_utils.error('product_not_found')
