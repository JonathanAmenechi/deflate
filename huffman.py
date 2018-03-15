from collections import Counter
import heapq


class HuffmanNode(object):

    def __init__(self, symbol=None, freq=0):
        self.symbol  = symbol
        self.freq    = freq
        self.left    = None
        self.right   = None

    def __repr__(self):
        return "Node(Symbol:'{}',Freq:{})\n".format(self.symbol,self.freq)

    def __eq__(self,other):
        if isinstance(other, HuffmanNode):
            return self.freq == other.freq
        return False

    def __lt__(self,other):
        if isinstance(other, HuffmanNode):
            return self.freq < other.freq

    def __add__(self, other):
        if isinstance(other, HuffmanNode):
            return HuffmanNode( None, self.freq+other.freq )

class HuffmanTree(object):

    def __init__(self, text):
        self.bst = self._initialize_bst(text)
        self.root = self._construct_tree()
        self.codes = {}

    def __repr__(self):
        return "Huffman Tree\n" + str( self.codes )

    def _initialize_bst(self, text):
        """
        Initializes a binary search tree with the symbols provided in text

        Parameters
        ------------
        text: iterable of text to be compressed
        """
        bst = []
        counter = Counter(char for char in text)
        for symbol, frequency in counter.items():
            node = HuffmanNode(symbol, frequency)
            heapq.heappush(bst, node)
        return bst
    
    def _construct_tree(self):
        """
        Parameters
        ------------
        text: iterable of text to be compressed
        """
        root = None

        while(len(self.bst) > 1):
            node_a, node_b = heapq.heappop(self.bst), heapq.heappop(self.bst)
            merged_node = node_a + node_b
            merged_node.left = node_a
            merged_node.right = node_b
            heapq.heappush(self.bst, merged_node)

        root = heapq.heappop(self.bst)
        return root

    def generate_codes(self):
        if self.root is not None:
            starting_code = ""
            self._generate_codes( self.root, starting_code )

    def _generate_codes(self, current_node, current_code):

        if current_node is not None:
            if current_node.symbol is not None:
                self.codes[current_node.symbol]= current_code
            self._generate_codes(current_node.left, current_code + "0")
            self._generate_codes(current_node.right, current_code + "1")