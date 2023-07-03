from typing import List, Tuple
import socket
import struct
import time
from . import specification
from .. import errors
from .. import status


class APIClient:
    '''
    A low-level client for the IMS Open Corpus Workbench (CWB) corpus query
    interface (CQi) API.

    Example:
    >>> import cqi
    >>> client = cqi.APIClient('127.0.0.1')
    >>> client.ctrl_connect('user', 'password')
    258  # CQI_STATUS_CONNECT_OK
    >>> client.ctrl_ping()
    260  # CQI_STATUS_PING_OK
    >>> client.ctrl_bye()
    259  # CQI_STATUS_BYE_OK

    Attributes:
    host (str): URL to the CQP server. For example,
        ``cqpserver.localhost`` or ``127.0.0.1``.
    port (int): Port the CQP server listens on. Default: ``4877``
    socket (socket.socket): Socket for communicating with a CQP server.
    timeout (int): Default timeout for API calls, in seconds. Default: ``60``
    version (str): The version of the CQi protocol to use. Default: ``0.1``
    '''

    def __init__(
        self,
        host: str,
        port: int = 4877,
        timeout: int = 60,
        version: str = '0.1'
    ):
        self.host: str = host
        self.port: int = port
        self.socket: socket.socket = socket.socket()
        self.timeout: int = timeout
        self.version: str = version

    def ctrl_connect(
        self,
        username: str,
        password: str
    ) -> status.StatusConnectOk:
        self.socket.connect((self.host, self.port))
        self.__send_WORD(specification.CTRL_CONNECT)
        self.__send_STRING(username)
        self.__send_STRING(password)
        return self.__recv_response()

    def ctrl_bye(self) -> status.StatusByeOk:
        self.__send_WORD(specification.CTRL_BYE)
        response = self.__recv_response()
        self.socket.close()
        return response

    def ctrl_user_abort(self):
        self.__send_WORD(specification.CTRL_USER_ABORT)

    def ctrl_ping(self) -> status.StatusPingOk:
        self.__send_WORD(specification.CTRL_PING)
        return self.__recv_response()

    def ctrl_last_general_error(self) -> str:
        ''' 
        Full-text error message for the last general error reported by the CQi
        server
        '''
        self.__send_WORD(specification.CTRL_LAST_GENERAL_ERROR)
        return self.__recv_response()

    def ask_feature_cqi_1_0(self) -> bool:
        self.__send_WORD(specification.ASK_FEATURE_CQI_1_0)
        return self.__recv_response()

    def ask_feature_cl_2_3(self) -> bool:
        self.__send_WORD(specification.ASK_FEATURE_CL_2_3)
        return self.__recv_response()

    def ask_feature_cqp_2_3(self) -> bool:
        self.__send_WORD(specification.ASK_FEATURE_CL_2_3)
        return self.__recv_response()

    def corpus_list_corpora(self) -> List[str]:
        self.__send_WORD(specification.CORPUS_LIST_CORPORA)
        return self.__recv_response()

    def corpus_charset(self, corpus: str) -> str:
        self.__send_WORD(specification.CORPUS_CHARSET)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def corpus_properties(self, corpus: str) -> List[str]:
        self.__send_WORD(specification.CORPUS_PROPERTIES)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def corpus_positional_attributes(self, corpus: str) -> List[str]:
        self.__send_WORD(specification.CORPUS_POSITIONAL_ATTRIBUTES)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def corpus_structural_attributes(self, corpus: str) -> List[str]:
        self.__send_WORD(specification.CORPUS_STRUCTURAL_ATTRIBUTES)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def corpus_structural_attribute_has_values(self, attribute: str) -> bool:
        self.__send_WORD(specification.CORPUS_STRUCTURAL_ATTRIBUTE_HAS_VALUES)
        self.__send_STRING(attribute)
        return self.__recv_response()

    def corpus_alignment_attributes(self, corpus: str) -> List[str]:
        self.__send_WORD(specification.CORPUS_ALIGNMENT_ATTRIBUTES)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def corpus_full_name(self, corpus: str) -> str:
        ''' the full name of <corpus> as specified in its registry entry '''
        self.__send_WORD(specification.CORPUS_FULL_NAME)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def corpus_info(self, corpus: str) -> List[str]:
        ''' 
        returns the contents of the .info file of <corpus> as a list of lines
        '''
        self.__send_WORD(specification.CORPUS_INFO)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def corpus_drop_corpus(self, corpus: str) -> status.StatusOk:
        ''' try to unload a corpus and all its attributes from memory '''
        self.__send_WORD(specification.CORPUS_DROP_CORPUS)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def cl_attribute_size(self, attribute: str) -> int:
        ''' 
        returns the size of <attribute>:
        - number of tokens        (positional)
        - number of regions       (structural)
        - number of alignments    (alignment)
        '''
        self.__send_WORD(specification.CL_ATTRIBUTE_SIZE)
        self.__send_STRING(attribute)
        return self.__recv_response()

    def cl_lexicon_size(self, attribute: str) -> int:
        '''
        returns the number of entries in the lexicon of a positional
        attribute;

        valid lexicon IDs range from 0 .. (lexicon_size - 1)
        '''
        self.__send_WORD(specification.CL_LEXICON_SIZE)
        self.__send_STRING(attribute)
        return self.__recv_response()

    def cl_drop_attribute(self, attribute: str) -> status.StatusOk:
        ''' unload attribute from memory '''
        self.__send_WORD(specification.CL_DROP_ATTRIBUTE)
        self.__send_STRING(attribute)
        return self.__recv_response()

    '''
    ' NOTE: simple (scalar) mappings are applied to lists (the returned list
    '       has exactly the same length as the list passed as an argument)
    '''

    def cl_str2id(self, attribute: str, strings: List[str]) -> List[int]:
        '''
        returns -1 for every string in <strings> that is not found in the
        lexicon
        '''
        self.__send_WORD(specification.CL_STR2ID)
        self.__send_STRING(attribute)
        self.__send_STRING_LIST(strings)
        return self.__recv_response()

    def cl_id2str(self, attribute: str, id: List[int]) -> List[str]:
        ''' returns "" for every ID in <id> that is out of range '''
        self.__send_WORD(specification.CL_ID2STR)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(id)
        return self.__recv_response()

    def cl_id2freq(self, attribute: str, id: List[int]) -> List[int]:
        ''' returns 0 for every ID in <id> that is out of range '''
        self.__send_WORD(specification.CL_ID2FREQ)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(id)
        return self.__recv_response()

    def cl_cpos2id(self, attribute: str, cpos: List[int]) -> List[int]:
        ''' 
        returns -1 for every corpus position in <cpos> that is out of range
        '''
        self.__send_WORD(specification.CL_CPOS2ID)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(cpos)
        return self.__recv_response()

    def cl_cpos2str(self, attribute: str, cpos: List[int]) -> List[str]:
        '''
        returns "" for every corpus position in <cpos> that is out of range
        '''
        self.__send_WORD(specification.CL_CPOS2STR)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(cpos)
        return self.__recv_response()

    def cl_cpos2struc(self, attribute: str, cpos: List[int]) -> List[int]:
        '''
        returns -1 for every corpus position not inside a structure region
        '''
        self.__send_WORD(specification.CL_CPOS2STRUC)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(cpos)
        return self.__recv_response()

    '''
    ' NOTE: temporary addition for the Euralex2000 tutorial, but should
    '       probably be included in CQi specs
    '''

    def cl_cpos2lbound(self, attribute: str, cpos: List[int]) -> List[int]:
        '''
        returns left boundary of s-attribute region enclosing cpos, -1 if not
        in region
        '''
        self.__send_WORD(specification.CL_CPOS2LBOUND)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(cpos)
        return self.__recv_response()

    def cl_cpos2rbound(self, attribute: str, cpos: List[int]) -> List[int]:
        '''
        returns right boundary of s-attribute region enclosing cpos, -1 if not
        in region
        '''
        self.__send_WORD(specification.CL_CPOS2RBOUND)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(cpos)
        return self.__recv_response()

    def cl_cpos2alg(self, attribute: str, cpos: List[int]) -> List[int]:
        ''' returns -1 for every corpus position not inside an alignment '''
        self.__send_WORD(specification.CL_CPOS2ALG)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(cpos)
        return self.__recv_response()

    def cl_struc2str(self, attribute: str, strucs: List[int]) -> List[str]:
        '''
        returns annotated string values of structure regions in <strucs>;
        "" if out of range

        check corpus_structural_attribute_has_values(<attribute>) first
        '''
        self.__send_WORD(specification.CL_STRUC2STR)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(strucs)
        return self.__recv_response()

    '''
    ' NOTE: the following mappings take a single argument and return multiple
    '       values, including lists of arbitrary size
    '''

    def cl_id2cpos(self, attribute: str, id: int) -> List[int]:
        ''' returns all corpus positions where the given token occurs '''
        self.__send_WORD(specification.CL_ID2CPOS)
        self.__send_STRING(attribute)
        self.__send_INT(id)
        return self.__recv_response()

    def cl_idlist2cpos(self, attribute: str, id_list: List[int]) -> List[int]:
        '''
        returns all corpus positions where one of the tokens in <id_list>
        occurs; the returned list is sorted as a whole, not per token id
        '''
        self.__send_WORD(specification.CL_IDLIST2CPOS)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(id_list)
        return self.__recv_response()

    def cl_regex2id(self, attribute: str, regex: str) -> List[int]:
        '''
        returns lexicon IDs of all tokens that match <regex>; the returned
        list may be empty (size 0);
        '''
        self.__send_WORD(specification.CL_REGEX2ID)
        self.__send_STRING(attribute)
        self.__send_STRING(regex)
        return self.__recv_response()

    def cl_struc2cpos(self, attribute: str, struc: int) -> Tuple[int, int]:
        '''
        returns start and end corpus positions of structure region <struc>
        '''
        self.__send_WORD(specification.CL_STRUC2CPOS)
        self.__send_STRING(attribute)
        self.__send_INT(struc)
        return self.__recv_response()

    def cl_alg2cpos(self, attribute: str, alg: int) -> Tuple[int, int, int, int]:
        ''' returns (src_start, src_end, target_start, target_end) '''
        self.__send_WORD(specification.CL_ALG2CPOS)
        self.__send_STRING(attribute)
        self.__send_INT(alg)
        return self.__recv_response()

    def cqp_query(self,
        mother_corpus: str,
        subcorpus_name: str,
        query: str
    ) -> status.StatusOk:
        ''' <query> must include the ';' character terminating the query. '''
        self.__send_WORD(specification.CQP_QUERY)
        self.__send_STRING(mother_corpus)
        self.__send_STRING(subcorpus_name)
        self.__send_STRING(query)
        return self.__recv_response()

    def cqp_list_subcorpora(self, corpus: str) -> List[str]:
        self.__send_WORD(specification.CQP_LIST_SUBCORPORA)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def cqp_subcorpus_size(self, subcorpus: str) -> int:
        self.__send_WORD(specification.CQP_SUBCORPUS_SIZE)
        self.__send_STRING(subcorpus)
        return self.__recv_response()

    def cqp_subcorpus_has_field(self, subcorpus: str, field: int) -> bool:
        self.__send_WORD(specification.CQP_SUBCORPUS_HAS_FIELD)
        self.__send_STRING(subcorpus)
        self.__send_BYTE(field)
        return self.__recv_response()

    def cqp_dump_subcorpus(
        self,
        subcorpus: str,
        field: int,
        first: int,
        last: int
    ) -> List[int]:
        '''
        Dump the values of <field> for match ranges <first> .. <last> in
        <subcorpus>. <field> is one of the CQI_CONST_FIELD_* constants.
        '''
        self.__send_WORD(specification.CQP_DUMP_SUBCORPUS)
        self.__send_STRING(subcorpus)
        self.__send_BYTE(field)
        self.__send_INT(first)
        self.__send_INT(last)
        return self.__recv_response()

    def cqp_drop_subcorpus(self, subcorpus: str) -> status.StatusOk:
        ''' delete a subcorpus from memory '''
        self.__send_WORD(specification.CQP_DROP_SUBCORPUS)
        self.__send_STRING(subcorpus)
        return self.__recv_response()

    '''
    ' NOTE: The following two functions are temporarily included for the
    '       Euralex 2000 tutorial demo
    '''

    def cqp_fdist_1(
        self,
        subcorpus: str,
        cutoff: int,
        field: int,
        attribute: str
    ) -> List[int]:
        '''
        frequency distribution of single tokens

        returns <n> (id, frequency) pairs flattened into a list of size 2*<n>

        field is one of
        - CQI_CONST_FIELD_MATCH
        - CQI_CONST_FIELD_TARGET
        - CQI_CONST_FIELD_KEYWORD

        NB: pairs are sorted by frequency desc.
        '''
        self.__send_WORD(specification.CQP_FDIST_1)
        self.__send_STRING(subcorpus)
        self.__send_INT(cutoff)
        self.__send_BYTE(field)
        self.__send_STRING(attribute)
        return self.__recv_response()

    def cqp_fdist_2(
        self,
        subcorpus: str,
        cutoff: int,
        field1: int,
        attribute1: str,
        field2: int,
        attribute2: str
    ) -> List[int]:
        '''
        frequency distribution of pairs of tokens

        returns <n> (id1, id2, frequency) pairs flattened into a list of size
        3*<n>

        NB: triples are sorted by frequency desc.
        '''
        self.__send_WORD(specification.CQP_FDIST_2)
        self.__send_STRING(subcorpus)
        self.__send_INT(cutoff)
        self.__send_BYTE(field1)
        self.__send_STRING(attribute1)
        self.__send_BYTE(field2)
        self.__send_STRING(attribute2)
        return self.__recv_response()

    def __recv_response(self):
        byte_data = self.__recv_WORD()
        response_type = byte_data >> 8
        if response_type == specification.DATA:
            return self.__recv_DATA(byte_data)
        elif response_type == specification.STATUS:
            return status.lookup[byte_data]()
        else:
            raise errors.lookup.get(byte_data, errors.CQiException)()

    def __recv_DATA(self, data_type):
        if data_type == specification.DATA_BYTE:
            return self.__recv_DATA_BYTE()
        elif data_type == specification.DATA_BOOL:
            return self.__recv_DATA_BOOL()
        elif data_type == specification.DATA_INT:
            return self.__recv_DATA_INT()
        elif data_type == specification.DATA_STRING:
            return self.__recv_DATA_STRING()
        elif data_type == specification.DATA_BYTE_LIST:
            return self.__recv_DATA_BYTE_LIST()
        elif data_type == specification.DATA_BOOL_LIST:
            return self.__recv_DATA_BOOL_LIST()
        elif data_type == specification.DATA_INT_LIST:
            return self.__recv_DATA_INT_LIST()
        elif data_type == specification.DATA_STRING_LIST:
            return self.__recv_DATA_STRING_LIST()
        elif data_type == specification.DATA_INT_INT:
            return self.__recv_DATA_INT_INT()
        elif data_type == specification.DATA_INT_INT_INT_INT:
            return self.__recv_DATA_INT_INT_INT_INT()
        elif data_type == specification.DATA_INT_TABLE:
            return self.__recv_DATA_INT_TABLE()
        else:
            raise errors.CQiException(f'Unknown data type: {data_type}')

    def __recv_wrapper(self, bufsize: int) -> bytes:
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            # Check if the server already sent over the desired number of bytes
            if len(self.socket.recv(bufsize, socket.MSG_PEEK)) == bufsize:
                return self.socket.recv(bufsize)
            time.sleep(0.05)
        else:
            raise errors.CQiException('Timeout: Not enough bytes')

    def __recv_DATA_BYTE(self) -> int:
        byte_data = self.__recv_wrapper(1)
        return struct.unpack('!B', byte_data)[0]

    def __recv_DATA_BOOL(self) -> bool:
        byte_data = self.__recv_wrapper(1)
        return struct.unpack('!?', byte_data)[0]

    def __recv_DATA_INT(self) -> int:
        byte_data = self.__recv_wrapper(4)
        return struct.unpack('!i', byte_data)[0]

    def __recv_DATA_STRING(self) -> str:
        n = self.__recv_WORD()
        byte_data = self.__recv_wrapper(n)
        return struct.unpack(f'!{n}s', byte_data)[0].decode()

    def __recv_DATA_BYTE_LIST(self) -> List[int]:
        data = []
        n = self.__recv_DATA_INT()
        while n > 0:
            data.append(self.__recv_DATA_BYTE())
            n -= 1
        return data

    def __recv_DATA_BOOL_LIST(self) -> List[bool]:
        data = []
        n = self.__recv_DATA_INT()
        while n > 0:
            data.append(self.__recv_DATA_BOOL())
            n -= 1
        return data

    def __recv_DATA_INT_LIST(self) -> List[int]:
        data = []
        n = self.__recv_DATA_INT()
        while n > 0:
            data.append(self.__recv_DATA_INT())
            n -= 1
        return data

    def __recv_DATA_STRING_LIST(self) -> List[str]:
        data = []
        n = self.__recv_DATA_INT()
        while n > 0:
            data.append(self.__recv_DATA_STRING())
            n -= 1
        return data

    def __recv_DATA_INT_INT(self) -> Tuple[int, int]:
        return (self.__recv_DATA_INT(), self.__recv_DATA_INT())

    def __recv_DATA_INT_INT_INT_INT(self) -> Tuple[int, int, int, int]:
        return (
            self.__recv_DATA_INT(),
            self.__recv_DATA_INT(),
            self.__recv_DATA_INT(),
            self.__recv_DATA_INT()
        )

    def __recv_DATA_INT_TABLE(self) -> List[List[int]]:
        rows = self.__recv_DATA_INT()
        columns = self.__recv_DATA_INT()
        data = []
        for i in range(0, rows):
            row = []
            for j in range(0, columns):
                row.append(self.__recv_DATA_INT())
            data.append(row)
        return data

    def __recv_WORD(self) -> int:
        byte_data = self.__recv_wrapper(2)
        return struct.unpack('!H', byte_data)[0]

    def __send_BYTE(self, byte_data: int):
        data = struct.pack('!B', byte_data)
        self.socket.sendall(data)

    def __send_BOOL(self, bool_data: bool):
        data = struct.pack('!?', bool_data)
        self.socket.sendall(data)

    def __send_INT(self, int_data: int):
        data = struct.pack('!i', int_data)
        self.socket.sendall(data)

    def __send_STRING(self, string_data: str):
        encoded_string_data = string_data.encode('utf-8')
        n = len(encoded_string_data)
        data = struct.pack(f'!H{n}s', n, encoded_string_data)
        self.socket.sendall(data)

    def __send_INT_LIST(self, int_list_data: List[int]):
        n = len(int_list_data)
        self.__send_INT(n)
        for int_data in int_list_data:
            self.__send_INT(int_data)

    def __send_STRING_LIST(self, string_list_data: List[str]):
        n = len(string_list_data)
        self.__send_INT(n)
        for string_data in string_list_data:
            self.__send_STRING(string_data)

    def __send_WORD(self, word_data: int):
        data = struct.pack('!H', word_data)
        self.socket.sendall(data)
