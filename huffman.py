from collections import Counter, OrderedDict
import heapq
import sys

is_py3 = sys.version_info.major >= 3

class HuffmanNode(object):

    def __init__(self, symbol=None, freq=0):
        self.symbol  = symbol
        self.freq    = freq
        self.left    = None
        self.right   = None

    def __repr__(self):
        return "Node(Symbol:'{}',Freq:{})\n".format(self.symbol,self.freq)

    def __eq__(self, other):
        if isinstance(other, HuffmanNode):
            return self.freq == other.freq
        return False

    def __cmp__(self, other):
        if isinstance(other, HuffmanNode):
            return self.freq > other.freq

    def __lt__(self, other):
        if isinstance(other, HuffmanNode):
            return self.freq < other.freq

    def __add__(self, other):
        if isinstance(other, HuffmanNode):
            node = HuffmanNode(None, self.freq+other.freq)
            node.left = self
            node.right = other
            return node

    def is_leaf(self):
        return self.symbol != None


class HuffmanTree(object):

    SYMBOL_LIMIT = 257

    def __init__(self, text):
        self.heap = self._initialize_heap(text)
        self.root = self._construct_tree()
        self.codes = self._generate_code_tree()

    def __repr__(self):
        return "Huffman Tree\n" + str( self.codes )

    def _initialize_heap(self, byte_string):
        """
        Initializes a binary search tree with the symbols provided in text

        Parameters
        ------------
        text: iterable of text to be compressed
        """

        heap = []

        counter = Counter(b if is_py3 else ord(b) for b in byte_string)
        for symbol, frequency in counter.items():
            node = HuffmanNode(symbol, frequency)
            heapq.heappush(heap, node)
        return heap

    def _construct_tree(self):
        """
        Parameters
        ------------
        text: iterable of text to be compressed
        """
        root = None

        while(len(self.heap) > 1):
            node_a, node_b = heapq.heappop(self.heap), heapq.heappop(self.heap)
            merged_node = node_a + node_b
            heapq.heappush(self.heap, merged_node)

        root = heapq.heappop(self.heap)

        return root

    def _generate_code_tree(self):
        if self.root is not None:
            codes = [0] * self.SYMBOL_LIMIT
            starting_code = ""
            self._generate_codes(self.root, starting_code, codes)

        return codes

    def _generate_codes(self, current_node, current_code, codes):

        if current_node is not None:
            if current_node.symbol is not None:
                codes[current_node.symbol] = current_code
            self._generate_codes(current_node.left, current_code+"0", codes)
            self._generate_codes(current_node.right, current_code+"1", codes)


class CanonicalHuffmanTree(HuffmanTree):

    def __init__(self, text=None, code_lengths=None):
        self.canon_codes = [0] * self.SYMBOL_LIMIT
        if text:
            self.code_lengths_by_symbols = [0]*self.SYMBOL_LIMIT
            self.generate_code_length_per_symbol(text)
            self.root = self.generate_code_tree(self.code_lengths_by_symbols)

        elif code_lengths:
            if len(code_lengths) != self.SYMBOL_LIMIT:
                raise Exception("Code lengths not equal to SYMBOL LIMIT")
            self.root = self.generate_code_tree(code_lengths)

        else:
            raise Exception("Must provide either text or an array of code lengths")

    def generate_code_length_per_symbol(self, text):
        naive_huff_tree = HuffmanTree(text)
        symbol_codes = naive_huff_tree.codes
        self._get_symbols_by_code_length(symbol_codes)

    def generate_code_tree(self, code_length_by_symbols):
        """ Generates the canonical code tree """
        nodes = []

        #iterate through the code lengths, from largest to smallest
        for code_length in range(max(code_length_by_symbols), -1, -1):
            leaves = []
            if code_length > 0:
                for symbol, j in enumerate(code_length_by_symbols):
                    # create leaf nodes for all symbols of the current code length, in ascii order
                    if code_length == j:
                        leaves.append(HuffmanNode(symbol))

            #create intermediate nodes, which point to the leaf nodes
            #from the previous level
            for i in range(0, len(nodes), 2):
                leaves.append(nodes[i] + nodes[i+1])
            nodes = leaves

        root = nodes[0]
        self._generate_codes(root, "", self.canon_codes)
        return root

    def _get_symbols_by_code_length(self, symbol_codes):
        for symbol, naive_huff_code in enumerate(symbol_codes):
            if isinstance(naive_huff_code, str):
                code_length = len(naive_huff_code)
                self.code_lengths_by_symbols[symbol] = code_length

    def get_code_length(self, symbol):
        return self.code_lengths_by_symbols[symbol]

    def get_huffman_code(self, symbol):
        if symbol < self.SYMBOL_LIMIT:
            return self.canon_codes[symbol]


class Reader(object):

    def __init__(self, input_file_path, output_file_path=None):
        self.infile_path = input_file_path
        if output_file_path is None:
            output_file_path = 'output.txt'
        self.outfile_path = output_file_path
        self.bit_buffer = []

    def convert_to_bytes(self, num, bytelength=1, endian='big'):
        return num.to_bytes(bytelength, endian)


class HuffmanEncoder(Reader):

    def write_huffman_table(self, huffman_table, output_file_handler):
        for code_len in huffman_table:
            bin_repr = self.convert_to_bytes(code_len)
            output_file_handler.write(bin_repr)

    def compress(self):

        with open(self.infile_path, 'rb') as fh:
            text = fh.read()

        chc = CanonicalHuffmanTree(text)
        huffman_table = chc.code_lengths_by_symbols
        huff_codes = chc.canon_codes

        output_file_handler = open(self.outfile_path, 'wb+')
        try:
            self.write_huffman_table(huffman_table, output_file_handler)
            self.write_compressed_text(text, huff_codes, output_file_handler)
        except Exception as e:
            raise e
        finally:
            output_file_handler.close()

    def write_compressed_text(self, text, codes, output_file_handler):
        eof_marker = 256
        for symbol in text:
            huff_code = codes[symbol]
            code_length = len(huff_code)
            for bit in huff_code:
                self.write_current_bits(output_file_handler, bit)

        #write any remaining bits to the file
        self.flush_bit_buffer(output_file_handler)

    def write_current_bits(self, fh, bit):
        self.bit_buffer.append(bit)
        if len(self.bit_buffer) == 8:
            bit_str = "".join(self.bit_buffer)
            fh.write(bytes((int(bit_str, 2), )))
            self.bit_buffer = []

    def flush_bit_buffer(self, fh):
        while (len(self.bit_buffer) > 0):
            self.write_current_bits(fh, "0")


class HuffmanDecoder(Reader):

    def read_huffman_table(self, fh):

        huffman_table = [0] * 257
        for symbol in range(257):
            byte_string = fh.read(1)
            code_length = int.from_bytes(byte_string, 'big')
            huffman_table[symbol] = code_length
        return huffman_table

    def decompress(self):
        in_file = open(self.infile_path, 'rb')
        out_file = open(self.outfile_path, 'wb+')

        try:
            symbol_codes = self.read_huffman_table(in_file)
            canonical_huff_tree = CanonicalHuffmanTree(code_lengths=symbol_codes)
            while True:
                symbol = self.read_symbols(in_file, canonical_huff_tree.root)
                if symbol is None:
                    break
                else:
                    out_file.write(bytes((symbol,)))
        except Exception as e:
            raise e
        finally:
            in_file.close()
            out_file.close()

    def read_symbols(self, fh, root):
        node = root
        while True:
            # If the node is a leaf node
            # get the symbol
            if node.is_leaf():
                return node.symbol

            bit, end_of_file = self.read_input_bit(fh)
            if end_of_file:
                return

            if bit == "0":
                node = node.left
            elif bit == "1":
                node = node.right
            else:
                raise Exception("Invalid bit")

    def read_input_bit(self, fh):
        eof = False

        if len(self.bit_buffer) == 0:
            byte_string = fh.read(1)

            #End of file
            if len(byte_string) == 0:
                eof = True
                return "", eof

            bit_string = self.to_bit_string(byte_string)
            for b in bit_string:
                self.bit_buffer.append(b)

        top = self.bit_buffer.pop(0)
        return top, eof

    def to_bit_string(self, byte_string):
        b = bin(int.from_bytes(byte_string, 'big')).replace('b', '').lstrip('0')
        while len(b)<8:
            b = '0' + b
        return b



