
def error(error_key):
    return {
        'status': False,
        'message': 'error',
        'error_description': error_messages[error_key]
    }

def success(success_key):
    return {
        'status': True,
        'message': 'success',
        'success_description': success_messages[success_key]
    }

error_messages = {
    'not_vendor': 'You must be a Vendor to add Products.',
    'product_not_found': 'This Product is not available.',
    'access_denied': 'You don\'t have access to this resourse!, enroll this course to see its content.',
    'required_fields': 'Some fields are required.',
    'quiz_not_found': 'This content does not has any quizzes.',
    'question_not_found': 'This question does not exists.',
    'choice_not_found': 'The answer must be one of the choices.',
    'page_access_denied': 'You don\'t have access to preview this page.',
    'invalid_params': "Invalid Parameters.",
    'out_of_stock': "Out of Stock.",
    'product_not_available': "Product with selected features is not avilable.",
    'empty_cart': 'Cart is empty!'
}

success_messages = {
    'product_available': "Product with selected features is avilable."
}
