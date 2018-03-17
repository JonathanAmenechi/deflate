from huffman import HuffmanTree, CanonicalHuffmanTree
from pprint import pprint

def decode( s, mapping ):
    ascii_txt = ord(s)


    pass

def process_file_by_block(file_path, process_function, block_size=1024):
    with open(file_path, "rb") as fh:
        while True:
            block = fh.read(block_size)
            if not block:
                break
            process_function(block)

def process(block):
    chc = CanonicalHuffmanTree(block)
    pprint("Tree per block:")
    pprint(chc.codes)
    return chc.codes


def main():

    file_path = r"olivertwist.txt"
    process_function = process
    block_size = 1024
    process_file_by_block(file_path, process_function, block_size )

    # with open(r'olivertwist.txt', 'rb') as fh:
    #     for block in fh:
    #         chc = CanonicalHuffmanCode(block)
    #         pprint("Tree per block:\n")
    #         pprint(chc.codes)
    #
    # # print( "One: ")
    # # pprint( chc.codes[ 101 ] )
    # #
    # # print("Two: ")
    # # pprint( chc.codes[ 104 ] )
    # # pprint( chc.codes[ 105 ] )
    # #
    # # print("Three: ")
    # # pprint( chc.codes[ 32 ] )
    # # pprint( chc.codes[ 97 ] )
    # # pprint( chc.codes[ 110 ] )
    # # pprint( chc.codes[ 111 ] )
    # #
    # # print( "Four: " )
    # # pprint( chc.codes[ 116 ] )
    #
    # # pprint( chc.codes[ 100 ] )
    # # pprint( chc.codes[ 108 ] )
    # # pprint( chc.codes[ 112 ] )
    # # pprint( chc.codes[ 114 ] )
    # # pprint( chc.codes[ 115 ] )
    #
    # # with open(r'test.txt', 'rb') as fh:
    # #     h = HuffmanTree(fh.read())
    # # h.generate_codes()
    # #
    # # chc = CanonicalHuffmanCode( h.codes )
    # # encoded = chc.codes
    # # print(encoded)
    # """
    # '{0:08b}'.format(6)
    #
    # """

if __name__ == "__main__":
    main()