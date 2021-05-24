def trimPems(pem):
    lines = pem.splitlines()
    concatenated = ''

    for x in range(1, len(lines) - 1):
        concatenated += lines[x]

    return concatenated