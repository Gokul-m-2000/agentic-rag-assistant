class SourceDocumentNotFoundError(Exception):
    """Exception raised when a source document is not found."""
    pass


class IndexBuildError(Exception):
    """Exception raised when there is an error building the index."""
    pass