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

    def __init__(self,text):
        self.code_lengths_by_symbols = {}
        self.codes = self._generate_code_tree(text)

    def _generate_code_tree(self, text):

        naive_huff_tree = HuffmanTree(text)
        symbol_codes = naive_huff_tree.codes

        # sort symbols by code length
        codes_symbols = self._get_symbols_by_code_length(symbol_codes)

        for code_length, symbols in codes_symbols.items():
            for symbol in symbols:
                self.code_lengths_by_symbols[symbol] = code_length

        assigned_codes = {}
        current_code = 0

        for code_length, symbols in codes_symbols.items():
            # shift the current code 1 bit to the left
            current_code = current_code << 1
            for sym in symbols:
                assigned_codes[sym] = current_code
                # increment the current code for every symbol for that code length
                current_code += 1
        return assigned_codes

    def _get_symbols_by_code_length(self, symbol_codes):
        d = {}
        for symbol, code in enumerate(symbol_codes):
            if isinstance(code, str):
                # count number of bits in the code
                num = int(code, 2).bit_length()

                # bit length erroneously gives a bit length of 0 for '00'
                num = num + 1 if num == 0 else num
                if d.get(num) is None:
                    d[num] = [symbol]
                else:
                    d[num].append(symbol)
        return OrderedDict(d)
