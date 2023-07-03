from .api import specification


class CQiException(Exception):
    '''
    A base class from which all other exceptions inherit.
    If you want to catch all errors that the CQi package might raise,
    catch this base exception.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = None
        self.description = None


class Error(CQiException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.ERROR


class ErrorGeneralError(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.ERROR_GENERAL_ERROR


class ErrorConnectRefused(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.ERROR_CONNECT_REFUSED


class ErrorUserAbort(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.ERROR_USER_ABORT


class ErrorSyntaxError(Error):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.ERROR_SYNTAX_ERROR


class CLError(CQiException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR


class CLErrorNoSuchAttribute(CLError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR_NO_SUCH_ATTRIBUTE
        self.description = 'CQi server couldn\'t open attribute'


class CLErrorWrongAttributeType(CLError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR_WRONG_ATTRIBUTE_TYPE


class CLErrorOutOfRange(CLError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR_OUT_OF_RANGE


class CLErrorRegex(CLError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR_REGEX


class CLErrorCorpusAccess(CLError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR_CORPUS_ACCESS
        self.description = ''


class CLErrorOutOfMemory(CLError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR_OUT_OF_MEMORY
        self.description = (
            'CQi server has run out of memory; try discarding some other '
            'corpora and/or subcorpora'
        )


class CLErrorInternal(CLError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CL_ERROR_INTERNAL
        self.description = (
            'The classical \'please contact technical support\' error'
        )


class CQPError(CQiException):
    # CQP error messages yet to be defined
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CQP_ERROR


class CQPErrorGeneral(CQPError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CQP_ERROR_GENERAL


class CQPErrorNoSuchCorpus(CQPError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CQP_ERROR_NO_SUCH_CORPUS


class CQPErrorInvalidField(CQPError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CQP_ERROR_INVALID_FIELD


class CQPErrorOutOfRange(CQPError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = specification.CQP_ERROR_OUT_OF_RANGE
        self.description = 'A number is out of range'


lookup = {
    specification.ERROR: Error,
    specification.ERROR_GENERAL_ERROR: ErrorGeneralError,
    specification.ERROR_CONNECT_REFUSED: ErrorConnectRefused,
    specification.ERROR_USER_ABORT: ErrorUserAbort,
    specification.ERROR_SYNTAX_ERROR: ErrorSyntaxError,
    specification.CL_ERROR: CLError,
    specification.CL_ERROR_NO_SUCH_ATTRIBUTE: CLErrorNoSuchAttribute,
    specification.CL_ERROR_WRONG_ATTRIBUTE_TYPE: CLErrorWrongAttributeType,
    specification.CL_ERROR_OUT_OF_RANGE: CLErrorOutOfRange,
    specification.CL_ERROR_REGEX: CLErrorRegex,
    specification.CL_ERROR_CORPUS_ACCESS: CLErrorCorpusAccess,
    specification.CL_ERROR_OUT_OF_MEMORY: CLErrorOutOfMemory,
    specification.CL_ERROR_INTERNAL: CLErrorInternal,
    specification.CQP_ERROR: CQPError,
    specification.CQP_ERROR_GENERAL: CQPErrorGeneral,
    specification.CQP_ERROR_NO_SUCH_CORPUS: CQPErrorNoSuchCorpus,
    specification.CQP_ERROR_INVALID_FIELD: CQPErrorInvalidField,
    specification.CQP_ERROR_OUT_OF_RANGE: CQPErrorOutOfRange
}
