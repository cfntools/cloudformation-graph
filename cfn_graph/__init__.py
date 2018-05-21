def capitalize_keys(o):
    """TODO: should move to utils"""

    if isinstance(o, dict):
        not_string = [k for k in o if not isinstance(k, str)]
        if not_string:
            print(not_string)
            raise AttributeError('Keys should be strings for capitalization to work')
        # Recurse over dicts
        return {_cap_first(k): capitalize_keys(v) for k, v in o.items()}
    if isinstance(o, list):
        # recurse over lists:
        return [capitalize_keys(v) for v in o]
    # stop
    return o


def _cap_first(s:str) -> str:
    if len(s) <=1 :
        return s.upper()
    return s[0].upper() + s[1:]
