def chunk(l, n):
    """
    Seperate a list into a list of lists n size
    """
    if len(l) == 1:
        return [l]
    if n == 0:
        n = 1
    return [l[x:x+n] for x in range(0, len(l), n)]
