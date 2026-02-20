import re

def parse_llm_list(l: str):
    l = re.sub(r"\\\"", "'", l)
    s, e = 0, 1
    while s < len(l) and l[s] != "[":
        s += 1
    while e < len(l) and l[e] != "]":
        e += 1
    if s >= e:
        return []
    l = l[s : e+1]
    s, e = 0, 1
    l_n = list()
    while s < len(l) and e < len(l):
        while s < len(l) and l[s] != "\"":
            s += 1
        e = s + 1
        while e < len(l) and l[e] != "\"":
            e += 1
        if len(l[s+1 : e]) > 0:
            l_n.append(l[s+1 : e])
        s = e+1
    return l_n


def parse_llm_list_int_value(l: str):
    l = re.sub(r"\\\"", "'", l)
    s, e = 0, 1
    while s < len(l) and l[s] != "[":
        s += 1
    while e < len(l) and l[e] != "]":
        e += 1
    if s >= e:
        return []
    l = l[s : e+1]
    s, e = 0, 1
    l_n = list()
    while s < len(l) and e < len(l):
        while s < len(l) and not l[s].isnumeric():
            s += 1
        e = s + 1
        while e < len(l) and l[e].isnumeric():
            e += 1
        if len(l[s : e]) > 0:
            l_n.append(l[s : e])
        s = e
    return l_n


def parse_llm_list_dict_value(l: str):
    l = re.sub(r"\\\"", "'", l)
    s, e = 0, 1
    while s < len(l) and l[s] != "[":
        s += 1
    while e < len(l) and l[e] != "]":
        e += 1
    if s >= e:
        return []
    l = l[s : e+1]
    s, e = 0, 1
    l_n = list()
    while s < len(l) and e < len(l):
        while s < len(l) and l[s] != "{":
            s += 1
        e = s + 1
        while e < len(l) and l[e] != "}":
            e += 1
        if len(l[s : e+1]) > 0:
            l_n.append(parse_llm_dict_str_value(l[s : e+1]))
        s = e+1
    return l_n


def parse_llm_dict(d: str):
    d = re.sub(r"\\\"", "'", d)
    s, e = 0, 1
    while s < len(d) and d[s] != "{":
        s += 1
    while e < len(d) and d[e] != "}":
        e += 1
    if s >= e:
        return {}
    d = d[s : e+1]
    s_key, e_key, s_values, e_values = 0, 1, 0, 0
    d_n = dict()
    while s_key < len(d) and e_key < len(d) and s_values < len(d) and e_values < len(d):
        while s_key < len(d) and d[s_key] != "\"":
            s_key += 1
        e_key = s_key + 1
        while e_key < len(d) and d[e_key] != "\"":
            e_key += 1
        key = d[s_key+1 : e_key]

        s_delimeter = e_key + 1
        while s_delimeter < len(d) and d[s_delimeter] != ":":
            s_delimeter += 1

        s_values = s_delimeter + 1
        while s_values < len(d) and d[s_values] != "[":
            s_values += 1
        e_values = s_values + 1
        while e_values < len(d) and d[e_values] != "]":
            e_values += 1
        values = parse_llm_list(d[s_values : e_values+1])

        if len(key) > 0:
            d_n[key] = values
        s_key = e_values + 1
    return d_n


def parse_llm_dict_str_value(d: str):
    d = re.sub(r"\\\"", "'", d)
    s, e = 0, 1
    while s < len(d) and d[s] != "{":
        s += 1
    while e < len(d) and d[e] != "}":
        e += 1
    if s >= e:
        return {}
    d = d[s : e+1]
    s_key, e_key, s_values, e_values = 0, 1, 0, 0
    d_n = dict()
    while s_key < len(d) and e_key < len(d) and s_values < len(d) and e_values < len(d):
        while s_key < len(d) and d[s_key] != "\"":
            s_key += 1
        e_key = s_key + 1
        while e_key < len(d) and d[e_key] != "\"":
            e_key += 1
        key = d[s_key+1 : e_key]

        s_delimeter = e_key + 1
        while s_delimeter < len(d) and d[s_delimeter] != ":":
            s_delimeter += 1

        s_values = s_delimeter + 1
        while s_values < len(d) and d[s_values] != "\"":
            s_values += 1
        e_values = s_values + 1
        while e_values < len(d) and d[e_values] != "\"":
            e_values += 1
        value = d[s_values+1 : e_values]

        if len(key) > 0:
            d_n[key] = value
        s_key = e_values + 1
    return d_n


def parse_llm_dict_list_value(d: str):
    d = re.sub(r"\\\"", "'", d)
    s, e = 0, 1
    while s < len(d) and d[s] != "{":
        s += 1
    while e < len(d) and d[e] != "}":
        e += 1
    if s >= e:
        return {}
    d = d[s : e+1]
    s_key, e_key, s_values, e_values = 0, 1, 0, 0
    d_n = dict()
    while s_key < len(d) and e_key < len(d) and s_values < len(d) and e_values < len(d):
        while s_key < len(d) and d[s_key] != "\"":
            s_key += 1
        e_key = s_key + 1
        while e_key < len(d) and d[e_key] != "\"":
            e_key += 1
        key = d[s_key+1 : e_key]

        s_delimeter = e_key + 1
        while s_delimeter < len(d) and d[s_delimeter] != ":":
            s_delimeter += 1

        s_values = s_delimeter + 1
        while s_values < len(d) and d[s_values] != "[":
            s_values += 1
        e_values = s_values + 1
        while e_values < len(d) and d[e_values] != "]":
            e_values += 1
        value = parse_llm_list(d[s_values : e_values+1])

        if len(key) > 0:
            d_n[key] = value
        s_key = e_values + 1
    return d_n