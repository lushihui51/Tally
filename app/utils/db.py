def model_to_dict(obj) -> dict:
    """Convert any SQLAlchemy model to dict."""
    return {
        col.name: getattr(obj, col.name) for col in obj.__table__.columns
    }