from logging import Filter

class CustomLogFilter(Filter):
    def filter(self, record):
        # Add user ID and request path to logs
        request = getattr(record, 'request', None)
        if request:
            record.user = getattr(request, 'user', None)
            record.path = request.path
        else:
            record.user = 'Anonymous'
            record.path = 'N/A'
        return True
