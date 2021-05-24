def trimPems(pem):
    lines = pem.splitlines()
    concatenated = ''

    for x in range(1, len(lines) - 1):
        concatenated += lines[x]

    return concatenated

def isNumber(input):
    try:
        # Convert it into integer
        val = int(input)
        return True
    except ValueError:
        try:
            # Convert it into float
            val = float(input)
            return True
        except ValueError:
            return False