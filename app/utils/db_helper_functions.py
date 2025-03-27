

def to_dict(obj):
    if hasattr(obj, "__table__"):
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    else:
        return dict(obj)