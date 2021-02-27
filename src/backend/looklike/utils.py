def get_ids_from_string(string: str) -> list[int]:
    return [abs(int(id)) for id in string.strip('[]').split(',')]
