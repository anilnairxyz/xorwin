from numeric_codes import solver, encoder, decoder


def test_numeric_solver():
    cases = [{"words": ["SLOW", "WEST", "SALE", "RENT"], "codes": ["8214", "1368", "1932"],
              "query": "LAST", "result": "3914"},
             {"words": ["BLOT", "BOIL", "TRIO", "CUBE"], "codes": ["4675", "1943", "4568"],
              "query": "CLUE", "result": "1593"},
             {"words": ["SWUM", "FERN", "WEST", "TRUE"], "codes": ["7236", "1687", "8139"],
              "query": "FUSE", "result": "X386"},
             {"words": ["DOGS", "GRIN", "HAIL", "HIGH"], "codes": ["4726", "9021", "8395"],
              "query": "LASH", "result": "6754"},
             {"words": ["SPIN", "TALK", "PINT", "NEST"], "codes": ["1467", "6237", "3146"],
              "query": "SNIP", "result": "3641"},
             {"words": ["CHIP", "ROAD", "DARK", "PAIR"], "codes": ["5219", "7386", "6281"],
              "query": "DROP", "result": "51X6"},
             {"words": ["PALM", "LAST", "ROSE", "MEAT"], "codes": ["8647", "1458", "5437"],
              "query": "TAPE", "result": "7416"},
             {"words": ["FOUR", "HALF", "ROPE", "PALE"], "codes": ["6857", "7492", "1853"],
              "query": "RULE", "result": "2953"},
             {"words": ["WAIT", "WORK", "KITE", "TEAM"], "codes": ["2918", "7346", "6529"],
              "query": "TAKE", "result": "2169"},
             {"words": ["POUR", "RUDE", "TYPE", "DALE"], "codes": ["1653", "9761", "5423"],
              "query": "ROPE", "result": "1793"},
             {"words": ["POND", "FLAG", "GRIP", "GOLD"], "codes": ["8163", "5974", "3205"],
              "query": "GIRL", "result": "3021"},
             {"words": ["DEAR", "MEAD", "WARE", "DRAM"], "codes": ["1435", "6342", "5231"],
              "query": "DRAM", "result": "1435"},
             {"words": ["DEAR", "MEAD", "WARE", "DRAM"], "codes": ["1435", "6342", "5231"],
              "query": "REAM", "result": "4235"},
             {"words": ["REST", "MITE", "STIR", "TRIM"], "codes": ["1456", "3154", "4231"],
              "query": "MITE", "result": "6512"},
             {"words": ["REST", "MITE", "STIR", "TRIM"], "codes": ["1456", "3154", "4231"],
              "query": "SEMI", "result": "3265"}
            ]
    for case in cases:
        solution = solver(case["words"], case["codes"]).pop()
        reply = encoder(solution, case["codes"], case["query"])
        assert(reply == case["result"])

    cases = [{"words": ["DEAR", "MEAD", "WARE", "DRAM"], "codes": ["1435", "6342", "5231"],
              "query": "6234", "result": "WEAR"},
             {"words": ["REST", "MITE", "STIR", "TRIM"], "codes": ["1456", "3154", "4231"],
              "query": "1246", "result": "TERM"}
            ]
    for case in cases:
        solution = solver(case["words"], case["codes"]).pop()
        reply = decoder(solution, case["codes"], case["query"])
        assert(reply == case["result"])
