from .api import specification


class CQiException(Exception):
    """
    A base class from which all other exceptions inherit.
    If you want to catch all errors that the CQi package might raise,
    catch this base exception.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = None
        self.name = None
        self.description = None


class Error(CQiException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.ERROR


class ErrorGeneralError(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.ERROR_GENERAL_ERROR
        self.name = specification.lookup[self.code]


class ErrorConnectRefused(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.ERROR_CONNECT_REFUSED
        self.name = specification.lookup[self.code]


class ErrorUserAbort(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.ERROR_USER_ABORT
        self.name = specification.lookup[self.code]


class ErrorSyntaxError(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.ERROR_SYNTAX_ERROR
        self.name = specification.lookup[self.code]


class CLError(CQiException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR


class CLErrorNoSuchAttribute(CLError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR_NO_SUCH_ATTRIBUTE
        self.name = specification.lookup[self.code]
        self.description = "CQi server couldn't open attribute"


class CLErrorWrongAttributeType(CLError):
    # CDA_EATTTYPE
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR_WRONG_ATTRIBUTE_TYPE
        self.name = specification.lookup[self.code]


class CLErrorOutOfRange(CLError):
    # CDA_EIDORNG, CDA_EIDXORNG, CDA_EPOSORNG
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR_OUT_OF_RANGE
        self.name = specification.lookup[self.code]


class CLErrorRegex(CLError):
    # CDA_EPATTERN (not used), CDA_EBADREGEX
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR_REGEX
        self.name = specification.lookup[self.code]


class CLErrorCorpusAccess(CLError):
    # CDA_ENODATA
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR_CORPUS_ACCESS
        self.name = specification.lookup[self.code]


class CLErrorOutOfMemory(CLError):
    # CDA_ENOMEM
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR_OUT_OF_MEMORY
        self.name = specification.lookup[self.code]
        self.description = ('CQi server has run out of memory; try discarding '
                            'some other corpora and/or subcorpora')


class CLErrorInternal(CLError):
    # CDA_EOTHER, CDA_ENYI
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR_INTERNAL
        self.name = specification.lookup[self.code]
        self.description = "Classical 'please contact technical support' error"


class CQPError(CQiException):
    # CQP error messages yet to be defined
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CQP_ERROR


class CQPErrorGeneral(CQPError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CQP_ERROR_GENERAL
        self.name = specification.lookup[self.code]


class CQPErrorNoSuchCorpus(CQPError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CQP_ERROR_NO_SUCH_CORPUS
        self.name = specification.lookup[self.code]


class CQPErrorInvalidField(CQPError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CQP_ERROR_INVALID_FIELD
        self.name = specification.lookup[self.code]


class CQPErrorOutOfRange(CQPError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CQP_ERROR_OUT_OF_RANGE
        self.name = specification.lookup[self.code]
        self.description = 'A number is out of range'


error_lookup = {
    specification.ERROR: Error,
    specification.ERROR_GENERAL_ERROR: ErrorGeneralError,
    specification.ERROR_CONNECT_REFUSED: ErrorConnectRefused,
    specification.ERROR_USER_ABORT: ErrorUserAbort,
    specification.ERROR_SYNTAX_ERROR: ErrorSyntaxError
}


cl_error_lookup = {
    specification.CL_ERROR: CLError,
    specification.CL_ERROR_NO_SUCH_ATTRIBUTE: CLErrorNoSuchAttribute,
    specification.CL_ERROR_WRONG_ATTRIBUTE_TYPE: CLErrorWrongAttributeType,
    specification.CL_ERROR_OUT_OF_RANGE: CLErrorOutOfRange,
    specification.CL_ERROR_REGEX: CLErrorRegex,
    specification.CL_ERROR_CORPUS_ACCESS: CLErrorCorpusAccess,
    specification.CL_ERROR_OUT_OF_MEMORY: CLErrorOutOfMemory,
    specification.CL_ERROR_INTERNAL: CLErrorInternal
}


cqp_error_lookup = {
    specification.CQP_ERROR: CQPError,
    specification.CQP_ERROR_GENERAL: CQPErrorGeneral,
    specification.CQP_ERROR_NO_SUCH_CORPUS: CQPErrorNoSuchCorpus,
    specification.CQP_ERROR_INVALID_FIELD: CQPErrorInvalidField,
    specification.CQP_ERROR_OUT_OF_RANGE: CQPErrorOutOfRange
}
