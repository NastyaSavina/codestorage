with open("/Users/me/Documents/code/python/work/parse_to_lowercase/source.txt", "r") as src:
    with open("/Users/me/Documents/code/python/work/parse_to_lowercase/result.txt", "w+") as res:
        for line in src.readlines():
            res_line = line
            if "'" in line:
                split_line = line.split("'")
                res_line = f"{str.lower(split_line[0])}'{split_line[1]}'{split_line[2]}"
            res.write(res_line)
            
