from . import specification
from ..errors import (cl_error_lookup, error_lookup, cqp_error_lookup,
                      CQiException)
import math
import socket
import struct
import time


class APIClient:
    """
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
    timeout (int): Time to wait for bytes from the server. If the timeout is
        exceeded, an exception is raised. Default: ``math.inf``
    version (str): The version of the CQi protocol to use. Default: ``0.1``
    """

    def __init__(self, host, port=4877, timeout=math.inf, version='0.1'):
        self.host = host
        self.port = port
        self.socket = socket.socket()
        self.timeout = timeout
        self.version = version

    def ctrl_connect(self, username, password):
        self.socket.connect((self.host, self.port))
        # INPUT: (STRING username, STRING password)
        # OUTPUT: CQI_STATUS_CONNECT_OK, CQI_ERROR_CONNECT_REFUSED
        self.__send_WORD(specification.CTRL_CONNECT)
        self.__send_STRING(username)
        self.__send_STRING(password)
        return self.__recv_response()

    def ctrl_bye(self):
        # INPUT: ()
        # OUTPUT: CQI_STATUS_BYE_OK
        self.__send_WORD(specification.CTRL_BYE)
        response = self.__recv_response()
        self.socket.close()
        return response

    def ctrl_user_abort(self):
        # INPUT: ()
        # OUTPUT:
        self.__send_WORD(specification.CTRL_USER_ABORT)

    def ctrl_ping(self):
        # INPUT: ()
        # OUTPUT: CQI_STATUS_PING_OK
        self.__send_WORD(specification.CTRL_PING)
        return self.__recv_response()

    def ctrl_last_general_error(self):
        # INPUT: ()
        # OUTPUT: CQI_DATA_STRING
        # full-text error message for the last general error reported by the
        # CQi server
        self.__send_WORD(specification.CTRL_LAST_GENERAL_ERROR)
        return self.__recv_response()

    def ask_feature_cqi_1_0(self):
        # INPUT: ()
        # OUTPUT: CQI_DATA_BOOL
        self.__send_WORD(specification.ASK_FEATURE_CQI_1_0)
        return self.__recv_response()

    def ask_feature_cl_2_3(self):
        # INPUT: ()
        # OUTPUT: CQI_DATA_BOOL
        self.__send_WORD(specification.ASK_FEATURE_CL_2_3)
        return self.__recv_response()

    def ask_feature_cqp_2_3(self):
        # INPUT: ()
        # OUTPUT: CQI_DATA_BOOL
        self.__send_WORD(specification.ASK_FEATURE_CL_2_3)
        return self.__recv_response()

    def corpus_list_coprora(self):
        # INPUT: ()
        # OUTPUT: CQI_DATA_STRING_LIST
        self.__send_WORD(specification.CORPUS_LIST_CORPORA)
        return self.__recv_response()

    def corpus_charset(self, corpus):
        # INPUT: (STRING corpus)
        # OUTPUT: CQI_DATA_STRING
        self.__send_WORD(specification.CORPUS_CHARSET)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def corpus_properties(self, corpus):
        # INPUT: (STRING corpus)
        # OUTPUT: CQI_DATA_STRING_LIST
        self.__send_WORD(specification.CORPUS_PROPERTIES)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def corpus_positional_attributes(self, corpus):
        # INPUT: (STRING corpus)
        # OUTPUT: CQI_DATA_STRING_LIST
        self.__send_WORD(specification.CORPUS_POSITIONAL_ATTRIBUTES)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def corpus_structural_attributes(self, corpus):
        # INPUT: (STRING corpus)
        # OUTPUT: CQI_DATA_STRING_LIST
        self.__send_WORD(specification.CORPUS_STRUCTURAL_ATTRIBUTES)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def corpus_structural_attribute_has_values(self, attribute):
        # INPUT: (STRING attribute)
        # OUTPUT: CQI_DATA_BOOL
        self.__send_WORD(specification.CORPUS_STRUCTURAL_ATTRIBUTE_HAS_VALUES)
        self.__send_STRING(attribute)
        return self.__recv_response()

    def corpus_alignment_attributes(self, corpus):
        # INPUT: (STRING corpus)
        # OUTPUT: CQI_DATA_STRING_LIST
        self.__send_WORD(specification.CORPUS_ALIGNMENT_ATTRIBUTES)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def corpus_full_name(self, corpus):
        # INPUT: (STRING corpus)
        # OUTPUT: CQI_DATA_STRING
        # the full name of <corpus> as specified in its registry entry
        self.__send_WORD(specification.CORPUS_FULL_NAME)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def corpus_info(self, corpus):
        # INPUT: (STRING corpus)
        # OUTPUT: CQI_DATA_STRING_LIST
        # returns the contents of the .info file of <corpus> as a list of lines
        self.__send_WORD(specification.CORPUS_INFO)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def corpus_drop_corpus(self, corpus):
        # INPUT: (STRING corpus)
        # OUTPUT: CQI_STATUS_OK
        # try to unload a corpus and all its attributes from memory
        self.__send_WORD(specification.CORPUS_DROP_CORPUS)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def cl_attribute_size(self, attribute):
        # INPUT: (STRING attribute)
        # OUTPUT: CQI_DATA_INT
        # returns the size of <attribute>:
        #     number of tokens        (positional)
        #     number of regions       (structural)
        #     number of alignments    (alignment)
        self.__send_WORD(specification.CL_ATTRIBUTE_SIZE)
        self.__send_STRING(attribute)
        return self.__recv_response()

    def cl_lexicon_size(self, attribute):
        # INPUT: (STRING attribute)
        # OUTPUT: CQI_DATA_INT
        # returns the number of entries in the lexicon of a positional
        # attribute;
        # valid lexicon IDs range from 0 .. (lexicon_size - 1)
        self.__send_WORD(specification.CL_LEXICON_SIZE)
        self.__send_STRING(attribute)
        return self.__recv_response()

    def cl_drop_attribute(self, attribute):
        # INPUT: (STRING attribute)
        # OUTPUT: CQI_STATUS_OK
        # unload attribute from memory
        self.__send_WORD(specification.CL_DROP_ATTRIBUTE)
        self.__send_STRING(attribute)
        return self.__recv_response()

    """
    " NOTE: simple (scalar) mappings are applied to lists (the returned list
    "       has exactly the same length as the list passed as an argument)
    """

    def cl_str2id(self, attribute, strings):
        # INPUT: (STRING attribute, STRING_LIST strings)
        # OUTPUT: CQI_DATA_INT_LIST
        # returns -1 for every string in <strings> that is not found in the
        # lexicon
        self.__send_WORD(specification.CL_STR2ID)
        self.__send_STRING(attribute)
        self.__send_STRING_LIST(strings)
        return self.__recv_response()

    def cl_id2str(self, attribute, id):
        # INPUT: (STRING attribute, INT_LIST id)
        # OUTPUT: CQI_DATA_STRING_LIST
        # returns "" for every ID in <id> that is out of range
        self.__send_WORD(specification.CL_ID2STR)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(id)
        return self.__recv_response()

    def cl_id2freq(self, attribute, id):
        # INPUT: (STRING attribute, INT_LIST id)
        # OUTPUT: CQI_DATA_INT_LIST
        # returns 0 for every ID in <id> that is out of range
        self.__send_WORD(specification.CL_ID2FREQ)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(id)
        return self.__recv_response()

    def cl_cpos2id(self, attribute, cpos):
        # INPUT: (STRING attribute, INT_LIST cpos)
        # OUTPUT: CQI_DATA_INT_LIST
        # returns -1 for every corpus position in <cpos> that is out of range
        self.__send_WORD(specification.CL_ID2FREQ)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(cpos)
        return self.__recv_response()

    def cl_cpos2str(self, attribute, cpos):
        # INPUT: (STRING attribute, INT_LIST cpos)
        # OUTPUT: CQI_DATA_STRING_LIST
        # returns "" for every corpus position in <cpos> that is out of range
        self.__send_WORD(specification.CL_CPOS2STR)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(cpos)
        return self.__recv_response()

    def cl_cpos2struc(self, attribute, cpos):
        # INPUT: (STRING attribute, INT_LIST cpos)
        # OUTPUT: CQI_DATA_INT_LIST
        # returns -1 for every corpus position not inside a structure region
        self.__send_WORD(specification.CL_CPOS2STRUC)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(cpos)
        return self.__recv_response()

    """
    " NOTE: temporary addition for the Euralex2000 tutorial, but should
    "       probably be included in CQi specs
    """

    def cl_cpos2lbound(self, attribute, cpos):
        # INPUT: (STRING attribute, INT_LIST cpos)
        # OUTPUT: CQI_DATA_INT_LIST
        # returns left boundary of s-attribute region enclosing cpos, -1 if not
        # in region
        self.__send_WORD(specification.CL_CPOS2LBOUND)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(cpos)
        return self.__recv_response()

    def cl_cpos2rbound(self, attribute, cpos):
        # INPUT: (STRING attribute, INT_LIST cpos)
        # OUTPUT: CQI_DATA_INT_LIST
        # returns right boundary of s-attribute region enclosing cpos, -1 if
        # not in region
        self.__send_WORD(specification.CL_CPOS2RBOUND)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(cpos)
        return self.__recv_response()

    def cl_cpos2alg(self, attribute, cpos):
        # INPUT: (STRING attribute, INT_LIST cpos)
        # OUTPUT: CQI_DATA_INT_LIST
        # returns -1 for every corpus position not inside an alignment
        self.__send_WORD(specification.CL_CPOS2ALG)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(cpos)
        return self.__recv_response()

    def cl_struc2str(self, attribute, strucs):
        # INPUT: (STRING attribute, INT_LIST strucs)
        # OUTPUT: CQI_DATA_STRING_LIST
        # returns annotated string values of structure regions in <strucs>; ""
        # if out of range
        # check CQI_CORPUS_STRUCTURAL_ATTRIBUTE_HAS_VALUES(<attribute>) first
        self.__send_WORD(specification.CL_STRUC2STR)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(strucs)
        return self.__recv_response()

    """
    " NOTE: the following mappings take a single argument and return multiple
    "       values, including lists of arbitrary size
    """

    def cl_id2cpos(self, attribute, id):
        # INPUT: (STRING attribute, INT id)
        # OUTPUT: CQI_DATA_INT_LIST
        # returns all corpus positions where the given token occurs
        self.__send_WORD(specification.CL_ID2CPOS)
        self.__send_STRING(attribute)
        self.__send_INT(id)
        return self.__recv_response()

    def cl_idlist2cpos(self, attribute, id_list):
        # INPUT: (STRING attribute, INT_LIST id_list)
        # OUTPUT: CQI_DATA_INT_LIST
        # returns all corpus positions where one of the tokens in <id_list>
        # occurs; the returned list is sorted as a whole, not per token id
        self.__send_WORD(specification.CL_IDLIST2CPOS)
        self.__send_STRING(attribute)
        self.__send_INT_LIST(id_list)
        return self.__recv_response()

    def cl_regex2id(self, attribute, regex):
        # INPUT: (STRING attribute, STRING regex)
        # OUTPUT: CQI_DATA_INT_LIST
        # returns lexicon IDs of all tokens that match <regex>; the returned
        # list may be empty (size 0);
        self.__send_WORD(specification.CL_REGEX2ID)
        self.__send_STRING(attribute)
        self.__send_STRING(regex)
        return self.__recv_response()

    def cl_struc2cpos(self, attribute, struc):
        # INPUT: (STRING attribute, INT struc)
        # OUTPUT: CQI_DATA_INT_INT
        # returns start and end corpus positions of structure region <struc>
        self.__send_WORD(specification.CL_STRUC2CPOS)
        self.__send_STRING(attribute)
        self.__send_INT(struc)
        return self.__recv_response()

    def cl_alg2cpos(self, attribute, alg):
        # INPUT: (STRING attribute, INT alg)
        # OUTPUT: CQI_DATA_INT_INT_INT_INT
        # returns (src_start, src_end, target_start, target_end)
        self.__send_WORD(specification.CL_ALG2CPOS)
        self.__send_STRING(attribute)
        self.__send_INT(alg)
        return self.__recv_response()

    def cqp_query(self, mother_corpus, subcorpus_name, query):
        # INPUT: (STRING mother_corpus, STRING subcorpus_name, STRING query)
        # OUTPUT: CQI_STATUS_OK
        # <query> must include the ';' character terminating the query.
        self.__send_WORD(specification.CQP_QUERY)
        self.__send_STRING(mother_corpus)
        self.__send_STRING(subcorpus_name)
        self.__send_STRING(query)
        return self.__recv_response()

    def cqp_list_subcorpora(self, corpus):
        # INPUT: (STRING corpus)
        # OUTPUT: CQI_DATA_STRING_LIST
        self.__send_WORD(specification.CQP_LIST_SUBCORPORA)
        self.__send_STRING(corpus)
        return self.__recv_response()

    def cqp_subcorpus_size(self, subcorpus):
        # INPUT: (STRING subcorpus)
        # OUTPUT: CQI_DATA_INT
        self.__send_WORD(specification.CQP_SUBCORPUS_SIZE)
        self.__send_STRING(subcorpus)
        return self.__recv_response()

    def cqp_subcorpus_has_field(self, subcorpus, field):
        # INPUT: (STRING subcorpus, BYTE field)
        # OUTPUT: CQI_DATA_BOOL
        self.__send_WORD(specification.CQP_SUBCORPUS_HAS_FIELD)
        self.__send_STRING(subcorpus)
        self.__send_BYTE(field)
        return self.__recv_response()

    def cqp_dump_subcorpus(self, subcorpus, field, first, last):
        # INPUT: (STRING subcorpus, BYTE field, INT first, INT last)
        # OUTPUT: CQI_DATA_INT_LIST
        # Dump the values of <field> for match ranges <first> .. <last>
        # in <subcorpus>. <field> is one of the CQI_CONST_FIELD_* constants.
        self.__send_WORD(specification.CQP_DUMP_SUBCORPUS)
        self.__send_STRING(subcorpus)
        self.__send_BYTE(field)
        self.__send_INT(first)
        self.__send_INT(last)
        return self.__recv_response()

    def cqp_drop_subcorpus(self, subcorpus):
        # INPUT: (STRING subcorpus)
        # OUTPUT: CQI_STATUS_OK
        # delete a subcorpus from memory
        self.__send_WORD(specification.CQP_DROP_SUBCORPUS)
        self.__send_STRING(subcorpus)
        return self.__recv_response()

    """
    " NOTE: The following two functions are temporarily included for the
    "       Euralex 2000 tutorial demo
    """

    def cqp_fdist_1(self, subcorpus, cutoff, field, attribute):
        """ NOTE: frequency distribution of single tokens """
        # INPUT: (STRING subcorpus, INT cutoff, BYTE field, STRING attribute)
        # OUTPUT: CQI_DATA_INT_LIST
        # returns <n> (id, frequency) pairs flattened into a list of size 2*<n>
        # field is one of CQI_CONST_FIELD_MATCH, CQI_CONST_FIELD_TARGET,
        #                 CQI_CONST_FIELD_KEYWORD
        # NB: pairs are sorted by frequency desc.
        self.__send_WORD(specification.CQP_FDIST_1)
        self.__send_STRING(subcorpus)
        self.__send_INT(cutoff)
        self.__send_BYTE(field)
        self.__send_STRING(attribute)
        return self.__recv_response()

    def cqp_fdist_2(self, subcorpus, cutoff, field1, attribute1, field2,
                    attribute2):
        """ NOTE: frequency distribution of pairs of tokens """
        # INPUT: (STRING subcorpus, INT cutoff, BYTE field1, STRING attribute1,
        #         BYTE field2, STRING attribute2)
        # OUTPUT: CQI_DATA_INT_LIST
        # returns <n> (id1, id2, frequency) pairs flattened into a list of size
        # 3*<n>
        # NB: triples are sorted by frequency desc.
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
        if response_type == specification.CL_ERROR:
            raise cl_error_lookup[byte_data]()
        elif response_type == specification.CQP_ERROR:
            raise cqp_error_lookup[byte_data]()
        elif response_type == specification.DATA:
            return self.__recv_DATA(byte_data)
        elif response_type == specification.ERROR:
            raise error_lookup[byte_data]()
        elif response_type == specification.STATUS:
            return byte_data
        else:
            raise CQiException('Unknown response type: {}'.format(response_type))

    def __recv_DATA(self, data_type):
        if data_type == specification.DATA_BYTE:
            data = self.__recv_DATA_BYTE()
        elif data_type == specification.DATA_BOOL:
            data = self.__recv_DATA_BOOL()
        elif data_type == specification.DATA_INT:
            data = self.__recv_DATA_INT()
        elif data_type == specification.DATA_STRING:
            data = self.__recv_DATA_STRING()
        elif data_type == specification.DATA_BYTE_LIST:
            data = self.__recv_DATA_BYTE_LIST()
        elif data_type == specification.DATA_BOOL_LIST:
            data = self.__recv_DATA_BOOL_LIST()
        elif data_type == specification.DATA_INT_LIST:
            data = self.__recv_DATA_INT_LIST()
        elif data_type == specification.DATA_STRING_LIST:
            data = self.__recv_DATA_STRING_LIST()
        elif data_type == specification.DATA_INT_INT:
            data = self.__recv_DATA_INT_INT()
        elif data_type == specification.DATA_INT_INT_INT_INT:
            data = self.__recv_DATA_INT_INT_INT_INT()
        elif data_type == specification.DATA_INT_TABLE:
            data = self.__recv_DATA_INT_TABLE()
        else:
            raise CQiException('Unknown data type: {}'.format(data_type))
        return data

    def __recv_wrapper(self, bufsize):
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            # Check if the server already sent over the desired number of bytes
            if len(self.socket.recv(bufsize, socket.MSG_PEEK)) == bufsize:
                return self.socket.recv(bufsize)
            time.sleep(0.05)
        else:
            raise CQiException('Timeout: Not enough bytes')

    def __recv_DATA_BYTE(self):
        byte_data = self.__recv_wrapper(1)
        return struct.unpack('!B', byte_data)[0]

    def __recv_DATA_BOOL(self):
        byte_data = self.__recv_wrapper(1)
        return struct.unpack('!?', byte_data)[0]

    def __recv_DATA_INT(self):
        byte_data = self.__recv_wrapper(4)
        return struct.unpack('!i', byte_data)[0]

    def __recv_DATA_STRING(self):
        n = self.__recv_WORD()
        byte_data = self.__recv_wrapper(n)
        return struct.unpack('!{}s'.format(n), byte_data)[0].decode()

    def __recv_DATA_BYTE_LIST(self):
        data = []
        n = self.__recv_DATA_INT()
        while n > 0:
            data.append(self.__recv_DATA_BYTE())
            n -= 1
        return data

    def __recv_DATA_BOOL_LIST(self):
        data = []
        n = self.__recv_DATA_INT()
        while n > 0:
            data.append(self.__recv_DATA_BOOL())
            n -= 1
        return data

    def __recv_DATA_INT_LIST(self):
        data = []
        n = self.__recv_DATA_INT()
        while n > 0:
            data.append(self.__recv_DATA_INT())
            n -= 1
        return data

    def __recv_DATA_STRING_LIST(self):
        data = []
        n = self.__recv_DATA_INT()
        while n > 0:
            data.append(self.__recv_DATA_STRING())
            n -= 1
        return data

    def __recv_DATA_INT_INT(self):
        return (self.__recv_DATA_INT(), self.__recv_DATA_INT())

    def __recv_DATA_INT_INT_INT_INT(self):
        return (self.__recv_DATA_INT(),
                self.__recv_DATA_INT(),
                self.__recv_DATA_INT(),
                self.__recv_DATA_INT())

    def __recv_DATA_INT_TABLE(self):
        rows = self.__recv_DATA_INT()
        columns = self.__recv_DATA_INT()
        data = []
        for i in range(0, rows):
            row = []
            for j in range(0, columns):
                row.append(self.__recv_DATA_INT())
            data.append(row)
        return data

    def __recv_WORD(self):
        byte_data = self.__recv_wrapper(2)
        return struct.unpack('!H', byte_data)[0]

    def __send_BYTE(self, byte_data):
        data = struct.pack('!B', byte_data)
        self.socket.sendall(data)

    def __send_BOOL(self, bool_data):
        data = struct.pack('!?', bool_data)
        self.socket.sendall(data)

    def __send_INT(self, int_data):
        data = struct.pack('!i', int_data)
        self.socket.sendall(data)

    def __send_STRING(self, string_data):
        encoded_string_data = string_data.encode('utf-8')
        n = len(encoded_string_data)
        data = struct.pack('!H{}s'.format(n), n, encoded_string_data)
        self.socket.sendall(data)

    def __send_INT_LIST(self, int_list_data):
        n = len(int_list_data)
        self.__send_INT(n)
        for int_data in int_list_data:
            self.__send_INT(int_data)

    def __send_STRING_LIST(self, string_list_data):
        n = len(string_list_data)
        self.__send_INT(n)
        for string_data in string_list_data:
            self.__send_STRING(string_data)

    def __send_WORD(self, word_data):
        data = struct.pack('!H', word_data)
        self.socket.sendall(data)
