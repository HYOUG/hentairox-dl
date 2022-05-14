def parse_pages(range_str:str, max_index:int) -> list:
    pages = []
    terms = range_str.split("+")
    terms = [el for el in terms if el != ""]
    terms = [el.replace(" ", "") for el in terms]
    
    for term in terms:
        subterms = term.split(":")
        if subterms[0] == "": subterms[0] = 0
        if subterms[1] == "": subterms[1] = max_index
        if subterms[2] == "": subterms[2] = 1
        subterms = [int(subterm) for subterm in subterms]
        start = subterms[0]
        
        if len(subterms) >= 2:
            if subterms[1] <= max_index:
                stop = subterms[1]
            else:
                stop = max_index
            if len(subterms) == 3:
                step = subterms[2]
            else:
                step = 1
        else:
            stop = subterms[0]+1
            step = 1
        
        pages += list(range(int(start), int(stop), int(step)))
    pages = sorted(list(set(pages)))
    return pages