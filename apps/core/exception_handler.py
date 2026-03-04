from http import HTTPStatus

from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return {
            "status_code": HTTPStatus.INTERNAL_SERVER_ERROR.value,
            "error": HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
            "messages": ["An unexpected error occurred"],
        }

    status_code = response.status_code
    phrase = HTTPStatus(status_code).phrase

    response.data = {
        "status_code": status_code,
        "error": phrase,
        "messages": _extract_messages(response.data),
    }

    return response


def _extract_messages(detail):
    if isinstance(detail, list):
        return [str(item) for item in detail]
    if isinstance(detail, dict):
        messages = []
        for value in detail.values():
            messages.extend(_extract_messages(value))
        return messages
    return [str(detail)]
