def index_raw(path: str) -> dict:
    index = {}  # Init index dictionary

    with open(path, "rb") as file:
        position = file.tell()  # Init position

        for i, _ in enumerate(file):
            index[str(i)] = position
            position = file.tell()  # Update position

    return index


def get_raw_line(path: str, index: dict, idx: int):
    with open(path, "rb") as file:
        position = index[idx]
        file.seek(position)
        line = file.readline()

    return line.decode("utf-8").strip()
