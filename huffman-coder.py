from huffman import HuffmanEncoder, HuffmanDecoder
import argparse


def compress(input_file_path, output_file_path):
    """ Compress with huffman encoding """

    encoder = HuffmanEncoder(input_file_path, output_file_path)
    encoder.compress()


def decompress(input_file_path, output_file_path):
    """ Decompress with huffman encoding """

    decoder = HuffmanDecoder(input_file_path, output_file_path)
    decoder.decompress()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="Compress using huffman encoding", action="store_true")
    parser.add_argument("-d", help="Decompress using huffman encoding", action="store_true" )
    parser.add_argument("-infile", "--infile", help="Input file path", type=str, required=True)
    parser.add_argument("-outfile", "--outfile", help="Output file location. Defaulted to output.txt", type=str)

    args = parser.parse_args()

    if args.c and args.d:
        raise Exception("Must provide either compress or decompress flag, not both" )

    if not args.c and not args.d:
        raise Exception("Must provide compress or decompress flag( -c, -d )")

    msg = "{} file {} with huffman encoding..."
    done_msg = "Complete. {} file here: {}"

    if args.c:
        print(msg.format("Compressing", args.infile))
        compress(args.infile, args.outfile)
        print(done_msg.format("Compressed", args.outfile))

    if args.d:
        print(msg.format("Decompressing", args.infile))
        decompress(args.infile, args.outfile)
        print(done_msg.format("Decompressed", args.outfile))

if __name__ == "__main__":
    main()
