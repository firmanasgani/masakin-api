from flask import url_for
from http import HTTPStatus

def build_paginated_response(pagination, page, per_page, endpoint, schema, **filters):
    """
    Builds a paginated response for any model.
    
    Parameters:
    - pagination: SQLAlchemy pagination object.
    - page: Current page number.
    - per_page: Number of items per page.
    - endpoint: The endpoint for generating URL links.
    - schema: Marshmallow schema for serializing items.
    - filters: Additional filters as query parameters.
    """
    items = schema.dump(pagination.items)
    links = {
        "self": url_for(endpoint, page=page, per_page=per_page, _external=True, **filters),
        "first": url_for(endpoint, page=1, per_page=per_page, _external=True, **filters),
        "last": url_for(endpoint, page=pagination.pages, per_page=per_page, _external=True, **filters),
    }

    if pagination.has_next:
        links["next"] = url_for(endpoint, page=page + 1, per_page=per_page, _external=True, **filters)
    if pagination.has_prev:
        links["prev"] = url_for(endpoint, page=page - 1, per_page=per_page, _external=True, **filters)

    return {
        "status": "success",
        "data": {
            "items": items,
            "metadata": {
                "total_items": pagination.total,
                "total_pages": pagination.pages,
                "current_page": page,
                "per_page": per_page,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
            },
            "links": links,
        },
    }, HTTPStatus.OK


from flask import url_for
from http import HTTPStatus

def build_non_paginated_response(items, endpoint, schema, **filters):
    """
    Builds a non-paginated response for any model.

    Parameters:
    - items: List of model instances.
    - endpoint: The endpoint for generating URL links.
    - schema: Marshmallow schema for serializing items.
    - filters: Additional filters as query parameters.
    """
    serialized_items = schema.dump(items)
    links = {
        "self": url_for(endpoint, _external=True, **filters)
    }

    return {
        "status": "success",
        "data": {
            "items": serialized_items, 
            "links": links,
        },
    }, HTTPStatus.OK


def build_single_item_response(item, endpoint, schema, **params):
    """
    Builds a response for a single item.
    
    Parameters:
    - item: The model instance.
    - endpoint: The endpoint for generating self URL.
    - schema: Marshmallow schema for serializing the item.
    - params: Additional query parameters for URL generation.
    """
    return {
        "status": "success",
        "data": {
            "item": schema.dump(item),
            "links": {
                "self": url_for(endpoint, _external=True, **params),
            },
        },
    }, HTTPStatus.OK
