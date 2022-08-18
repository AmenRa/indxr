from csv import reader


def csv_line_to_dict(line: str, fieldnames: list, delimiter: str) -> dict:
    return dict(
        zip(
            fieldnames,
            list(reader([line.decode("utf-8")], delimiter=delimiter))[0],
        )
    )


def csv_line_to_list(line: str, delimiter: str) -> list:
    return list(reader([line.decode("utf-8")], delimiter=delimiter))[0]


def index_csv(
    path: str,
    delimiter: str = ",",
    fieldnames: list = None,
    has_header: bool = True,
    return_dict: bool = True,
    key_id: str = "id",
) -> dict:
    assert (
        fieldnames or has_header
    ), "File must have header or fieldnames must be defined by user"

    index = {}

    with open(path, "rb") as file:
        position = file.tell()  # Init position

        for i, line in enumerate(file):
            if i == 0 and has_header:
                if not fieldnames:
                    fieldnames = line.decode("utf-8").strip().split(delimiter)

            elif return_dict:
                idx = csv_line_to_dict(
                    line=line, fieldnames=fieldnames, delimiter=delimiter
                )[key_id]
                index[idx] = position

            else:
                index[i] = position

            position = file.tell()  # Update position

    return fieldnames, index


def get_csv_line(
    path: str,
    index: dict,
    idx: str,
    delimiter: str = ",",
    fieldnames: list = None,
    return_dict: bool = True,
):
    with open(path, "rb") as file:
        position = index[idx]
        file.seek(position)
        line = file.readline()

    return (
        csv_line_to_dict(line=line, fieldnames=fieldnames, delimiter=delimiter)
        if return_dict
        else csv_line_to_list(line=line, delimiter=delimiter)
    )
