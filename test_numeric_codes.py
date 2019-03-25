from numeric_codes import solver, encoder, decoder


def test_numeric_solver():
    words = ["SLOW", "WEST", "SALE", "RENT"]
    codes = ["8214", "1368", "1932"]
    query = "LAST"
    solution = solver(words, codes).pop()
    reply = encoder(solution, codes, query)
    assert( reply == "3914" )
    words = ["BLOT", "BOIL", "TRIO", "CUBE"]
    codes = ["4675", "1943", "4568"]
    query = "CLUE"
    solution = solver(words, codes).pop()
    reply = encoder(solution, codes, query)
    assert(reply == "1593")
    words = ["SWUM", "FERN", "WEST", "TRUE"]
    codes = ["7236", "1687", "8139"]
    query = "FUSE"
    solution = solver(words, codes).pop()
    reply = encoder(solution, codes, query)
    assert(reply == "X386")
    words = ["DOGS", "GRIN", "HAIL", "HIGH"]
    codes = ["4726", "9021", "8395"]
    query = "LASH"
    solution = solver(words, codes).pop()
    reply = encoder(solution, codes, query)
    assert(reply == "6754")
    words = ["SPIN", "TALK", "PINT", "NEST"]
    codes = ["1467", "6237", "3146"]
    query = "SNIP"
    solution = solver(words, codes).pop()
    reply = encoder(solution, codes, query)
    assert(reply == "3641")
    words = ["CHIP", "ROAD", "DARK", "PAIR"]
    codes = ["5219", "7386", "6281"]
    query = "DROP"
    solution = solver(words, codes).pop()
    reply = encoder(solution, codes, query)
    assert(reply == "51X6")
    words = ["PALM", "LAST", "ROSE", "MEAT"]
    codes = ["8647", "1458", "5437"]
    query = "TAPE"
    solution = solver(words, codes).pop()
    reply = encoder(solution, codes, query)
    assert(reply == "7416")
    words = ["FOUR", "HALF", "ROPE", "PALE"]
    codes = ["6857", "7492", "1853"]
    query = "RULE"
    solution = solver(words, codes).pop()
    reply = encoder(solution, codes, query)
    assert(reply == "2953")
    words = ["WAIT", "WORK", "KITE", "TEAM"]
    codes = ["2918", "7346", "6529"]
    query = "TAKE"
    solution = solver(words, codes).pop()
    reply = encoder(solution, codes, query)
    assert(reply == "2169")
    words = ["POUR", "RUDE", "TYPE", "DALE"]
    codes = ["1653", "9761", "5423"]
    query = "ROPE"
    solution = solver(words, codes).pop()
    reply = encoder(solution, codes, query)
    assert(reply == "1793")
    words = ["POND", "FLAG", "GRIP", "GOLD"]
    codes = ["8163", "5974", "3205"]
    query = "GIRL"
    solution = solver(words, codes).pop()
    reply = encoder(solution, codes, query)
    assert(reply == "3021")
    words = ["DEAR", "MEAD", "WARE", "DRAM"]
    codes = ["1435", "6342", "5231"]
    solution = solver(words, codes).pop()
    query = "DRAM"
    reply = encoder(solution, codes, query)
    assert(reply == "1435")
    query = "REAM"
    reply = encoder(solution, codes, query)
    assert(reply == "4235")
    query = "6234"
    reply = decoder(solution, codes, query)
    assert(reply == "WEAR")
    words = ["REST", "MITE", "STIR", "TRIM"]
    codes = ["1456", "3154", "4231"]
    solution = solver(words, codes).pop()
    query = "MITE"
    reply = encoder(solution, codes, query)
    assert(reply == "6512")
    query = "SEMI"
    reply = encoder(solution, codes, query)
    assert(reply == "3265")
    query = "1246"
    reply = decoder(solution, codes, query)
    assert(reply == "TERM")
