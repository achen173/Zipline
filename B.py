import sys
import struct

my_input = sys.stdin.buffer.read(struct.calcsize(">B"))
nbr = struct.unpack(">B", my_input)
sys.stdout.buffer.write(struct.pack(">B", nbr[0]+1))
sys.stdout.buffer.flush()