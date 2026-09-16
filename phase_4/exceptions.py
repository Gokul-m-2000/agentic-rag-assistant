class SourceDocumentNotFoundError(Exception):
    """Exception raised when a source document is not found."""
    pass


class IndexBuildError(Exception):
    """Exception raised when there is an error building the index."""
    pass

class DocumentSplitError(Exception):
    """Exception raised when there is an error splitting documents."""
    pass

class DocumentEmbeddingError(Exception):
    """Exception raised when there is an error embedding documents."""
    pass