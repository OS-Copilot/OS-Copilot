
def get_content(s, begin_str='[BEGIN]', end_str='[END]'):
    _begin = s.find(begin_str)
    _end = s.find(end_str)
    if _begin == -1 or _end == -1:
        return 'content not found!'
    else:
        return s[_begin + len(begin_str):_end].strip()

def string_to_function(string):
    exec(string, globals())
    return globals()[string.split(' ')[1].split('(')[0]]