"""Substring search algorithms comparision. """

import timeit


def compute_lps(pattern):
    """Build longest prefix-suffix (LPS) array for KMP preprocessing."""

    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(main_string, pattern):
    """Find substring in the text using KMP algorithm"""

    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1


def build_shift_table(pattern):
    """Construct bad-character shift table for Boyer-Moore algorithm"""

    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    """Find substring in the text using Boyer–Moore algorithm"""

    shift_table = build_shift_table(pattern)
    i = 0

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i

        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


def polynomial_hash(s, base=256, modulus=101):
    """Compute polynomial rolling hash for string s."""
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value


def rabin_karp_search(main_string, substring):
    """Find substring in the text using Rabin-Karp algorithm"""

    substring_length = len(substring)
    main_string_length = len(main_string)

    base = 256
    modulus = 101

    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(
        main_string[:substring_length], base, modulus
    )

    h_multiplier = pow(base, substring_length - 1) % modulus

    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (
                current_slice_hash - ord(main_string[i]) * h_multiplier
            ) % modulus
            current_slice_hash = (
                current_slice_hash * base +
                ord(main_string[i + substring_length])
            ) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


def compare_pattern_search():
    """Compare runtime of the three substring search algorithms via timeit."""

    try:
        with open("article1.txt", encoding="utf-8") as f:
            article1 = f.read()
        with open("article2.txt", encoding="utf-8") as f:
            article2 = f.read()
    except OSError as exc:
        print(f"Failed to read input files: {exc}")
        return

    patterns = {
        "article1": {
            "existing": "безлічі готових бібліотек",
            "non_existing": "xyzabc123def456ghi789"
        },
        "article2": {
            "existing": "розгорнутий список",
            "non_existing": "nonexistent_pattern_xyz123"
        }
    }

    functions = {
        "Rabin-Karp": rabin_karp_search,
        "KMP": kmp_search,
        "Boyer-Moore": boyer_moore_search
    }

    articles = {
        "article1.txt": article1,
        "article2.txt": article2
    }

    number = 100

    print("=" * 80)
    print("Pattern Search Performance Comparison")
    print("=" * 80)
    print(f"Number of iterations per test: {number}")
    print()

    for article_name, article_content in articles.items():
        print(f"\n{'=' * 80}")
        print(f"Testing with: {article_name}")
        print(f"Text length: {len(article_content)} characters")
        print(f"{'=' * 80}\n")

        article_key = "article1" if "article1" in article_name else "article2"

        for pattern_type in ["existing", "non_existing"]:
            pattern = patterns[article_key][pattern_type]
            print(f"\nPattern ({pattern_type}): '{pattern}'")
            print(f"Pattern length: {len(pattern)} characters")
            print("-" * 80)

            result_check = {
                "Rabin-Karp": rabin_karp_search(article_content, pattern),
                "KMP": kmp_search(article_content, pattern),
                "Boyer-Moore": boyer_moore_search(article_content, pattern)
            }

            for func_name, func in functions.items():
                time_taken = timeit.timeit(
                    lambda: func(article_content, pattern),
                    number=number,
                )

                avg_time = time_taken / number
                result = result_check[func_name]

                status = "FOUND" if result != -1 else "NOT FOUND"
                position_info = (
                    f" at position {result}" if result != -1 else ""
                )

                print(
                    f"{func_name:15} | "
                    f"Time: {avg_time*1000:8.4f} ms | "
                    f"Total: {time_taken*1000:8.4f} ms | "
                    f"{status}{position_info}"
                )

            print()

    print("=" * 80)
    print("Comparison Complete")
    print("=" * 80)


if __name__ == "__main__":
    compare_pattern_search()
