import  os

def add_hostname(parse_result,hostname):
    if type(parse_result).__name__=='list':
        for l in parse_result:
            l.append(hostname)
    return parse_result