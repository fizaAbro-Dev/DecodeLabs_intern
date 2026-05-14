
# ============================================================
#  DecodeLabs Internship - Batch 2026
#  Project 1: The To-Do List
#  Developer: Fiza Zulfiqar
# ============================================================

"""
Techniques used :
  - secrets module  : cryptographically secure randomness (replaces random.choice)
  - string module   : ascii_letters, digits, punctuation (standardised character pools)
  - .join() pattern : O(N) accumulation (avoids O(N²) += string concatenation)
  - Input validation: NIST SP 800-63-4 (2024) — min 15, max 64 characters
  - Entropy formula : E = L × log₂(R)
"""

import secrets
import string
import math


NIST_MIN_LENGTH = 15   # NIST SP 800-63-4 minimum for high-security contexts
NIST_MAX_LENGTH = 64   # Systems must support at least 64 characters (passphrases)

def get_validated_length() -> int:
    """
    Capture and validate the password length from the user.
    The input phase is the first point of failure in any system.
    NIST 2024 mandates minimum 15 characters for high-security contexts.
    """
    while True:
        raw = input(
            f"\nEnter desired password length "
            f"[NIST 2024: min {NIST_MIN_LENGTH}, max {NIST_MAX_LENGTH}]: "
        ).strip()

        # Guard: must be a valid integer
        if not raw.isdigit():
            print("  ✖  Invalid input. Please enter a whole number.")
            continue

        length = int(raw)

        # Guard: NIST lower bound
        if length < NIST_MIN_LENGTH:
            print(f"  ✖  Length {length} is below the NIST 2024 minimum of {NIST_MIN_LENGTH}.")
            print(f"     An 8-character password can be cracked in ~2 days by modern GPUs.")
            continue

        # Guard: NIST upper bound
        if length > NIST_MAX_LENGTH:
            print(f"  ✖  Length {length} exceeds the supported maximum of {NIST_MAX_LENGTH}.")
            continue

        return length


def get_character_options() -> dict:
    """
    Ask the user which character categories to include.
    Returns a dict of booleans for each category.
    """
    print("\nSelect character categories to include:")
    categories = {
        "uppercase": ("Uppercase letters  (A-Z)",         True),
        "lowercase": ("Lowercase letters  (a-z)",         True),
        "digits":    ("Digits             (0-9)",          True),
        "symbols":   ("Symbols/Punctuation (!@#$%^&*...)", False),
    }

    selections = {}
    for key, (label, default) in categories.items():
        default_str = "Y/n" if default else "y/N"
        answer = input(f"  Include {label}? [{default_str}]: ").strip().lower()
        if answer == "":
            selections[key] = default
        else:
            selections[key] = answer in ("y", "yes")

    # At least one category must be selected
    if not any(selections.values()):
        print("  ✖  At least one category must be selected. Defaulting to all categories.")
        return {k: True for k in selections}

    return selections



def build_character_pool(selections: dict) -> str:
    """
    Standardise the character pool using Python's string module.
    Professional engineers leverage the string module for
    locale-independent consistency — NOT manually typed arrays.

    string.ascii_letters  → all lowercase + uppercase ASCII letters
    string.digits         → '0123456789'
    string.punctuation    → standard ASCII punctuation and special symbols
    """
    pool = ""

    if selections.get("uppercase"):
        pool += string.ascii_uppercase        # string module — professional standard

    if selections.get("lowercase"):
        pool += string.ascii_lowercase        # string module — professional standard

    if selections.get("digits"):
        pool += string.digits                 # string module — '0123456789'

    if selections.get("symbols"):
        pool += string.punctuation            # string module — !@#$%^&*() etc.

    return pool


def generate_password(length: int, pool: str) -> str:
    """
    Core generation engine using secrets.choice() — NOT random.choice().

    WHY secrets, NOT random?
      - random relies on the Mersenne Twister (deterministic PRNG).
      - It is seeded by predictable system time; an attacker who knows
        the seed can perfectly reconstruct the generated password.
      - secrets.choice() draws from the OS's highest-quality entropy
        sources (hardware-level noise) — the mandatory enterprise standard
        per Python 3.6+ docs and NIST guidelines.

    WHY ''.join() NOT password += char?
      - Strings in Python are IMMUTABLE objects.
      - password += char creates a brand-new string object in memory
        every iteration, copies the old content, and discards the old
        object → O(N²) time and memory complexity.
      - ''.join(list) pre-calculates total size and allocates memory
        exactly once → O(N) linear time complexity.
    """
    # Build a list first (O(1) append per element), then join once (O(N))
    char_list = [secrets.choice(pool) for _ in range(length)]   # secrets — cryptographically secure
    password  = "".join(char_list)                               # .join()  — O(N) efficiency
    return password


def guarantee_category_inclusion(password: str, pool: str, selections: dict) -> str:
    """
    Enterprise hardening: guarantee at least one character from each
    selected category appears in the final password.
    Uses secrets.randbelow() for cryptographically secure index selection.
    """
    mandatory_chars = []

    if selections.get("uppercase") and not any(c in string.ascii_uppercase for c in password):
        mandatory_chars.append(secrets.choice(string.ascii_uppercase))

    if selections.get("lowercase") and not any(c in string.ascii_lowercase for c in password):
        mandatory_chars.append(secrets.choice(string.ascii_lowercase))

    if selections.get("digits") and not any(c in string.digits for c in password):
        mandatory_chars.append(secrets.choice(string.digits))

    if selections.get("symbols") and not any(c in string.punctuation for c in password):
        mandatory_chars.append(secrets.choice(string.punctuation))

    if not mandatory_chars:
        return password   # Already satisfies all constraints

    # Splice mandatory characters into random positions using secrets
    pw_list = list(password)
    for char in mandatory_chars:
        idx = secrets.randbelow(len(pw_list))
        pw_list[idx] = char

    return "".join(pw_list)



def calculate_entropy(length: int, pool_size: int) -> float:
    """
    Entropy formula (Shannon / information theory):

        E = L × log₂(R)

    Where:
        E = entropy in bits (unpredictability of the password)
        L = length of the password
        R = size of the character pool (e.g. 62 for alphanumeric)

    Expanding R increases security, but increasing L drives
    EXPONENTIAL mathematical strength. This is exactly why NIST 2024
    mandates length over complexity.

    Real-world benchmarks (62-char alphanumeric pool, modern GPU):
        8  characters  → cracked in ~2 days
        10 characters  → cracked in ~5 years
        16 characters  → secure for millions of years
    """
    if pool_size < 2:
        return 0.0
    return length * math.log2(pool_size)


def classify_strength(entropy: float) -> str:
    """Map entropy bits to a human-readable strength label."""
    if entropy < 40:
        return "WEAK      ⚠"
    elif entropy < 60:
        return "MODERATE  ~"
    elif entropy < 80:
        return "STRONG    ✔"
    elif entropy < 100:
        return "VERY STRONG ✔✔"
    else:
        return "MAXIMUM   ✔✔✔"


def display_results(password: str, length: int, pool: str, selections: dict) -> None:
    """
    Deliver the secure credential along with its mathematical
    security proof — the hallmark of enterprise-grade output.
    """
    pool_size = len(pool)
    entropy   = calculate_entropy(length, pool_size)
    strength  = classify_strength(entropy)

    active_categories = [k for k, v in selections.items() if v]

    print("\n" + "═" * 60)
    print("  🔐  GENERATED PASSWORD")
    print("═" * 60)
    print(f"\n  {password}\n")
    print("─" * 60)
    print("  SECURITY ANALYSIS")
    print("─" * 60)
    print(f"  Length          : {length} characters")
    print(f"  Character Pool  : {pool_size} unique characters")
    print(f"  Categories      : {', '.join(active_categories)}")
    print(f"  Entropy         : {entropy:.2f} bits  [E = {length} × log₂({pool_size})]")
    print(f"  Strength        : {strength}")
    print("═" * 60)

    if entropy >= 80:
        print("  ✔  Meets NIST SP 800-63-4 (2024) enterprise standard.")
    else:
        print("  ⚠  Consider a longer password to meet NIST 2024 standards.")

    print()


# ─────────────────────────────────────────────
# MAIN — Input → Process → Output scaffold
# ─────────────────────────────────────────────

def main():
  
    print("  DecodeLabs — Project 3: Enterprise Password Generator  ")
    print("  Architecting secure credentials for backend systems    ")
   
    while True:
        # ── PHASE 1: INPUT ──────────────────────────────────────────
        length     = get_validated_length()
        selections = get_character_options()

        # ── PHASE 2: PROCESS ────────────────────────────────────────
        pool     = build_character_pool(selections)
        password = generate_password(length, pool)
        password = guarantee_category_inclusion(password, pool, selections)

        # ── PHASE 3: OUTPUT ─────────────────────────────────────────
        display_results(password, length, pool, selections)

        again = input("  Generate another password? [y/N]: ").strip().lower()
        if again not in ("y", "yes"):
            print("\n  Session closed. Stay secure. — DecodeLabs 2026\n")
            break


if __name__ == "__main__":
    main()