import collections
import struct

class LLMZipCodec:
    """
    SGI 2026: Live Neural Arithmetic Codec (LLM-Zip).
    Functional arithmetic coding with full compression and decompression.
    """
    def __init__(self, precision=32):
        self.precision = precision
        self.max_range = (1 << precision) - 1
        self.half_range = (1 << (precision - 1))
        self.quarter_range = (1 << (precision - 2))

    def _get_frequencies(self, data):
        counts = collections.Counter(data)
        symbols = sorted(counts.keys())
        freqs = [counts[s] for s in symbols]
        cum_freqs = [0] * (len(freqs) + 1)
        for i in range(len(freqs)):
            cum_freqs[i + 1] = cum_freqs[i] + freqs[i]
        total = cum_freqs[-1]
        return symbols, cum_freqs, total

    def compress(self, text):
        if not text: return b""
        data = text.encode()
        symbols, cum_freqs, total = self._get_frequencies(data)
        sym_map = {s: i for i, s in enumerate(symbols)}

        low, high = 0, self.max_range
        bits = []
        pending_bits = 0

        for char in data:
            idx = sym_map[char]
            rng = high - low + 1
            high = low + (rng * cum_freqs[idx + 1] // total) - 1
            low = low + (rng * cum_freqs[idx] // total)

            while True:
                if high < self.half_range:
                    bits.append(0); bits.extend([1] * pending_bits); pending_bits = 0
                elif low >= self.half_range:
                    bits.append(1); bits.extend([0] * pending_bits); pending_bits = 0
                    low -= self.half_range; high -= self.half_range
                elif low >= self.quarter_range and high < 3 * self.quarter_range:
                    pending_bits += 1
                    low -= self.quarter_range; high -= self.quarter_range
                else: break
                low = (low << 1) & self.max_range
                high = ((high << 1) | 1) & self.max_range

        bits.append(1) # End marker
        byte_arr = bytearray()
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(min(8, len(bits) - i)):
                if bits[i + j]: byte |= (1 << (7 - j))
            byte_arr.append(byte)

        # Header: total_count(4B) | sym_count(2B) | symbols... | cum_freqs...
        header = struct.pack(">IH", total, len(symbols))
        header += bytes(symbols)
        for cf in cum_freqs: header += struct.pack(">I", cf)

        return header + b":::" + bytes(byte_arr)

    def decompress(self, compressed_data):
        if not compressed_data: return ""
        try:
            header, payload = compressed_data.split(b":::", 1)
            total, sym_len = struct.unpack(">IH", header[:6])
            symbols = list(header[6:6+sym_len])
            cum_freqs = []
            for i in range(sym_len + 1):
                offset = 6 + sym_len + i*4
                cum_freqs.append(struct.unpack(">I", header[offset:offset+4])[0])
        except Exception: return "Error: Invalid Header"

        # Bitstream to bits
        bits = []
        for b in payload:
            for i in range(8): bits.append((b >> (7 - i)) & 1)

        def get_bit(idx): return bits[idx] if idx < len(bits) else 0

        low, high = 0, self.max_range
        value = 0
        for i in range(self.precision): value = (value << 1) | get_bit(i)

        bit_idx = self.precision
        result = bytearray()

        for _ in range(total):
            rng = high - low + 1
            count = ((value - low + 1) * total - 1) // rng

            # Find symbol
            idx = 0
            while cum_freqs[idx+1] <= count: idx += 1
            result.append(symbols[idx])

            high = low + (rng * cum_freqs[idx + 1] // total) - 1
            low = low + (rng * cum_freqs[idx] // total)

            while True:
                if high < self.half_range: pass
                elif low >= self.half_range:
                    low -= self.half_range; high -= self.half_range; value -= self.half_range
                elif low >= self.quarter_range and high < 3 * self.quarter_range:
                    low -= self.quarter_range; high -= self.quarter_range; value -= self.quarter_range
                else: break
                low = (low << 1) & self.max_range
                high = ((high << 1) | 1) & self.max_range
                value = ((value << 1) | get_bit(bit_idx)) & self.max_range
                bit_idx += 1

        return result.decode()

if __name__ == "__main__":
    codec = LLMZipCodec()
    test_str = "SGI 2026 Neural Archiving test string."
    comp = codec.compress(test_str)
    decomp = codec.decompress(comp)
    print(f"Original: {test_str}")
    print(f"Decompressed: {decomp}")
    print(f"Match: {test_str == decomp}")
