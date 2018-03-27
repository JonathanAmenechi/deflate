# Implementing DEFLATE in Pure Python

Deflate is a compression method that combines two compression methods: LZ77 and Huffman Coding.

This implementation was done in Python 3.

Huffman Coding( complete )

* The huffman coding part of this implementation is complete.
* To try it out, clone the repo: `git clone https://github.com/JonathanAmenechi/deflate.git`
* To compress a file, run: `python huffman-coder -c infile "INPUT_FILE" -outfile "OUTPUT_FILE"`
* To decompress the file, run: `python huffman-coder -d -infile "PREVIOUSLY_COMPRESSED_FILE" -outfile "OUTPUT_FILE"`
* Tested on [Charles Dickens' Oliver Twsit](http://www.gutenberg.org/ebooks/730.txt.utf-8), a text file of 914KB. After compression, the file size was reduced to 530KB.
* Also tested on [The King James' Bible](http://corpus.canterbury.ac.nz/descriptions/large/bible.html) from the Canterbury Corpus. Reduced file size from around 4MB to around 2MB.

LZ77( Soon to come )


DEFLATE( Soon to come )


