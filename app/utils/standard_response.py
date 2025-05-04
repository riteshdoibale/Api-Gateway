
def responseModel(trackingId, data=None, errors=None):
    if not data:
        data = {}
    if not errors:
        errors = []
    response = {
        'trackingId' : trackingId,
        'errors' : errors,
        'data' : data
    }
    return response