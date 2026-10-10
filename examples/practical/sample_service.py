"""Small, dependency-free service used only for AICP documentation examples."""


def retry(operation, attempts=3):
    """Retry transient ValueError failures, returning the first success."""
    if attempts < 1:
        raise ValueError("attempts must be positive")
    for index in range(attempts):
        try:
            return operation()
        except ValueError:
            if index == attempts - 1:
                raise


def health():
    """Return a simple response body and status code."""
    return 200, {"status": "ok"}
