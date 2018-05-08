def lengths(x):
    if isinstance(x,list):
        yield len(x)
        for y in x:
            for z in lengths(y):
                yield z