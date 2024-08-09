"""
Implementation of the SHAKE-256 algorithm for Ed448
"""

try:
    import hashlib

    hashlib.new("shake256").digest(64)

    def shake_256(msg, outlen):
        return hashlib.new("shake256", msg).digest(outlen)

except (TypeError, ValueError):

    from ._compat import bytes_to_int, int_to_bytes

    # From little endian.
    def _from_le(s):
        return bytes_to_int(s, byteorder="little")

    # Rotate a word x by b places to the left.
    def _rol(x, b):
        return ((x << b) | (x >> (64 - b))) & (2**64 - 1)

    # Do the SHA-3 state transform on state s.
    def _sha3_transform(s):
        ROTATIONS = [
            0,
            1,
            62,
            28,
            27,
            36,
            44,
            6,
            55,
            20,
            3,
            10,
            43,
            25,
            39,
            41,
            45,
            15,
            21,
            8,
            18,
            2,
            61,
            56,
            14,
        ]
        PERMUTATION = [
            1,
            6,
            9,
            22,
            14,
            20,
            2,
            12,
            13,
            19,
            23,
            15,
            4,
            24,
            21,
            8,
            16,
            5,
            3,
            18,
            17,
            11,
            7,
            10,
        ]
        RC = [
            0x0000000000000001,
            0x0000000000008082,
            0x800000000000808A,
            0x8000000080008000,
            0x000000000000808B,
            0x0000000080000001,
            0x8000000080008081,
            0x8000000000008009,
            0x000000000000008A,
            0x0000000000000088,
            0x0000000080008009,
            0x000000008000000A,
            0x000000008000808B,
            0x800000000000008B,
            0x8000000000008089,
            0x8000000000008003,
            0x8000000000008002,
            0x8000000000000080,
            0x000000000000800A,
            0x800000008000000A,
            0x8000000080008081,
            0x8000000000008080,
            0x0000000080000001,
            0x8000000080008008,
        ]

        for rnd in range(0, 24):
            # AddColumnParity (Theta)
            c = [0] * 5
            d = [0] * 5
            for i in range(0, 25):
                c[i % 5] ^= s[i]
            for i in range(0, 5):
                d[i] = c[(i + 4) % 5] ^ _rol(c[(i + 1) % 5], 1)
            for i in range(0, 25):
                s[i] ^= d[i % 5]
            # RotateWords (Rho)
            for i in range(0, 25):
                s[i] = _rol(s[i], ROTATIONS[i])
            # PermuteWords (Pi)
            t = s[PERMUTATION[0]]
            for i in range(0, len(PERMUTATION) - 1):
                s[PERMUTATION[i]] = s[PERMUTATION[i + 1]]
            s[PERMUTATION[-1]] = t
            # NonlinearMixRows (Chi)
            for i in range(0, 25, 5):
                t = [
                    s[i],
                    s[i + 1],
                    s[i + 2],
                    s[i + 3],
                    s[i + 4],
                    s[i],
                    s[i + 1],
                ]
                for j in range(0, 5):
                    s[i + j] = t[j] ^ ((~t[j + 1]) & (t[j + 2]))
            # AddRoundConstant (Iota)
            s[0] ^= RC[rnd]

    # Reinterpret octet array b to word array and XOR it to state s.
    def _reinterpret_to_words_and_xor(s, b):
        for j in range(0, len(b) // 8):
            s[j] ^= _from_le(b[8 * j : 8 * j + 8])

    # Reinterpret word array w to octet array and return it.
    def _reinterpret_to_octets(w):
        mp = bytearray()
        for j in range(0, len(w)):
            mp += int_to_bytes(w[j], 8, byteorder="little")
        return mp

    def _sha3_raw(msg, r_w, o_p, e_b):
        """Semi-generic SHA-3 implementation"""
        r_b = 8 * r_w
        s = [0] * 25
        # Handle whole blocks.
        idx = 0
        blocks = len(msg) // r_b
        for i in range(0, blocks):
            _reinterpret_to_words_and_xor(s, msg[idx : idx + r_b])
            idx += r_b
            _sha3_transform(s)
        # Handle last block padding.
        m = bytearray(msg[idx:])
        m.append(o_p)
        while len(m) < r_b:
            m.append(0)
        m[len(m) - 1] |= 128
        # Handle padded last block.
        _reinterpret_to_words_and_xor(s, m)
        _sha3_transform(s)
        # Output.
        out = bytearray()
        while len(out) < e_b:
            out += _reinterpret_to_octets(s[:r_w])
            _sha3_transform(s)
        return out[:e_b]

    def shake_256(msg, outlen):
        return _sha3_raw(msg, 17, 31, outlen)
