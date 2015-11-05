import pyparsing as _p

def parse(liberty_string):
    #_p.ParserElement.enablePackrat() <- dont, kills memory - and slower...
    identifier=_p.Word(_p.alphanums+'._') # a name for..
    EOL = _p.LineEnd().suppress() # end of line
    ws = ' \t'
    _p.ParserElement.setDefaultWhitespaceChars(ws)
    linebreak = _p.Suppress("\\" + _p.LineEnd())
    o_linebreak =  _p.Optional(linebreak)
    library_name = identifier
    b_left = _p.Suppress("(")
    b_right = _p.Suppress(")")
    cb_left = _p.Suppress("{")
    cb_right = _p.Suppress("}")
    semicolon = _p.Suppress(";")
    colon = _p.Suppress(":")
    quote = _p.Suppress("\"")
    emptyquote = '""'
    comma = _p.Suppress(",")
    comment = _p.Suppress(_p.cStyleComment())
    valuestring = _p.Word(_p.alphanums+'\'=&_-+*/.$:!| ')
    valuestring_quoted = emptyquote | quote + _p.Word(_p.alphanums+'\'=&_-+*/.$:! ()|') + quote
    valuelist = _p.Group(quote + valuestring + _p.OneOrMore(comma + valuestring) + quote)
    value = valuestring | valuestring_quoted | valuelist
    key_value_pair = _p.Group(identifier + colon + value) + semicolon + EOL
    named_list = identifier + b_left + _p.Group( o_linebreak + value + _p.ZeroOrMore( comma + o_linebreak + value)) + o_linebreak + b_right + (semicolon + EOL | EOL)
    group = _p.Forward()
    group << _p.Group(
        _p.Group(identifier + b_left + _p.Optional((identifier + _p.ZeroOrMore( comma + identifier))|valuestring_quoted + _p.ZeroOrMore( comma + valuestring_quoted))) + b_right + cb_left + EOL
        + _p.Group( _p.ZeroOrMore(key_value_pair | named_list | group | EOL | comment))
        + cb_right + EOL
        )
    
    library =  _p.Suppress(_p.ZeroOrMore(comment | EOL)) + group + _p.Suppress(_p.ZeroOrMore(comment | EOL))
    
    key_value_pair.setParseAction(handle_parameters)
    named_list.setParseAction(handle_list)
    group.setParseAction(handle_groups)
    valuestring.setParseAction(parse_string_if_possible)
    
    return library.parseString(liberty_string)[0]['library']

def parse_string_if_possible(token):
    a=token[0]
    try:
        return float(a)
    except ValueError:
        return a

def merge(a, b, path=None):
    if path is None: path = []
    
    if type(a) == list and type(b) == list:
        a = a + b
    elif type(a) == list:
        a.append(b)
    elif type(b) == list:
        b.append(a)
        a = b
    else: 
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass # same leaf value
                elif type(a[key]) == list and type(b[key]) == list:
                    a[key] = a[key] + b[key]
                elif type(a[key]) == list:
                    a[key].append(b[key])
                elif type(b[key]) == list:
                    b[key].append(a[key])
                    a[key] = b[key]
                else:
                    a[key] = [a[key], b[key]]
            else:
                a[key] = b[key]
    return a

def handle_groups(token):
    d = {}
    group_type = token[0][0][0]
    group_name = False
    if len(token[0][0]) == 2:
        group_name = token[0][0][1]
        d[group_type] = {}
        d[group_type][group_name] = {}
        [merge(d[group_type][group_name],e) for e in token[0][1].asList()]
    else:
        d[group_type] = {}
        [d[group_type].update(e) for e in token[0][1].asList()]
    
    
    return d
    
def handle_parameters(token):
    d = {}
    d[token[0][0]] = token[0][1]
    return d

def handle_list(token):
    d = {}
    d[token[0]] = token[1].asList()
    return d


