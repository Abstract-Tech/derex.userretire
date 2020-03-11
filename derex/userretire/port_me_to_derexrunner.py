from contextlib import contextmanager


@contextmanager
def exit_cm():
    # Context manager to monkey patch sys.exit calls
    import sys

    def myexit(result_code):
        if result_code != 0:
            raise RuntimeError

    orig = sys.exit
    sys.exit = myexit

    try:
        yield
    finally:
        sys.exit = orig
