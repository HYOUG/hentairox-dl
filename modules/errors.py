class Error(Exception):
    """Base class for other exceptions"""
    pass

class InvalidURL(Error):
    """The given URL is invalid, check the validity and the spelling of provided URL """
    pass