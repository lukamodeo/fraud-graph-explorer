# src/fraud_graph_explorer/validators/uk_nino.py

"""
Custom validator for the UK National Insurance Number (NINo).

python-stdnum does not ship a `stdnum.gb.nino` module (only nhs, sedol,
upn, utr, vat). Since the OECD TIN Portal classifies NINo as the
canonical UK TIN — not UTR — we need a custom validator that exposes
the same `is_valid(value) -> bool` interface as stdnum's country
modules, so it can be slotted into TIN_VALIDATORS['GB'] unchanged.

NINo format (per HMRC and OECD TIN Portal):
  - 2 prefix letters + 6 digits + 1 suffix letter = 9 characters
  - Case-insensitive
  - Internal spaces optional: "QQ 12 34 56 C" normalizes to "QQ123456C"
  - Disallowed prefix letters (any position): D, F, I, Q, U, V
  - Disallowed 2-letter whole prefixes: BG, GB, NK, TN, ZH (reserved)
  - Disallowed second-letter O (reserved historically)
  - Suffix letters historically A, B, C, D

Examples (valid):
    QQ123456C         (most common test value)
    AB123456A
    JM123456D

Examples (invalid):
    DQ123456A         (D not allowed as prefix)
    GB123456A         (GB reserved)
    QQ123456E         (E not in suffix range A-D)
    QQ123456          (no suffix letter)
    QQ1234567A        (too many digits)
    qq 12 34 56 c     (lowercase with spaces — but normalizes and passes)
"""

import re


# Order matters: negative-lookahead for reserved whole-prefixes first,
# then character classes for each position.
_NINO_RE = re.compile(
    r'^'
    r'(?!BG|GB|NK|TN|ZH)'                    # not a reserved whole-prefix
    r'[ABCEGHJKLMNPRSTWXYZ]'                  # 1st letter: no D, F, I, O, Q, U, V
    r'[ABCEGHJKLMNPRSTWXYZ]'                  # 2nd letter: same exclusions
    r'\d{6}'
    r'[A-D]'                                   # suffix letter A, B, C, D
    r'$'
)


def _normalize(value):
    """Uppercase and strip all internal whitespace."""
    if not isinstance(value, str):
        return ''
    return value.upper().replace(' ', '')


def is_valid(value):
    """Return True if `value` is a syntactically valid UK NINo."""
    cleaned = _normalize(value)
    if not cleaned:
        return False
    return bool(_NINO_RE.match(cleaned))


def compact(value):
    """Return the canonical compact form (uppercase, no spaces)."""
    return _normalize(value)


def format(value):
    """Return the HMRC display form: 'QQ 12 34 56 C'."""
    v = _normalize(value)
    if not v or len(v) != 9:
        return v  # don't try to format malformed input
    return f"{v[:2]} {v[2:4]} {v[4:6]} {v[6:8]} {v[8]}"


class _UKNINOValidator:
    """
    Module-level singleton that mirrors stdnum country-module API.

    Usage (matches stdnum.it.codicefiscale etc.):
        from .validators.uk_nino import nino
        nino.is_valid('QQ123456C')   # True
        nino.compact('qq 12 34 56 c')  # 'QQ123456C'

    The instance is a thin shim over the module-level functions
    so callers can use either style (nino.is_valid(...) or
    uk_nino.is_valid(...)).
    """

    is_valid = staticmethod(is_valid)
    compact = staticmethod(compact)
    format = staticmethod(format)


# Public instance — mirrors stdnum's pattern of a module-level object
nino = _UKNINOValidator()