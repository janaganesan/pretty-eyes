import re
import pdb

def convert_assignment_to_dict(text):
    result = {}
    text = text.replace("\\\"", "")
    for m in re.finditer("\s*(\S+)=", text):
        t = text[m.end():]
        if t.startswith('"'):
            result[m.group(1)] = t.split('"')[1]
        else:
            result[m.group(1)] = t.split(' ')[0]
    return result


def convert_curly_string_to_dict(text, result=None):
    if result is None:
        result = {}
    m = re.search("\s*(\S+) \{", text)
    if m is None:
        return convert_assignment_to_dict(text)
    start = m.start()
    open = 0
    close = 0
    for x in range(start, len(text)):
        if text[x] == '{':
            open += 1
        elif text[x] == '}':
            close += 1
        if open != 0 and open == close:
            end = x
            break
    key = m.group(1)
    if key in result:
        key = "{0}__{1}".format(key, len([x for x in result.keys() if x.startswith(key)]))
    result[key] = text[m.end() - 1:end + 1]
    remaining = (text[:start] + text[end+1:]).rstrip()
    if re.search('[a-zA-Z]', remaining) is not None:
        convert_curly_string_to_dict(remaining, result=result)
    return result
    # Recursive method to convert innermost fields to dict
    # key = m.group(1)
    # if key in result:
    #     key = "{0}__{1}".format(key, len([x for x in result.keys() if x.startswith(key)]))
    # result[key] = {}
    # result[key] = convert_curly_string_to_dict(text[m.end() - 1:end + 1], result=result[key])
    # remaining = (text[:start] + text[end+1:]).rstrip()
    # if re.search('[a-zA-Z]', remaining) is not None:
    #     convert_curly_string_to_dict(remaining, result=result)
    # return result


def convert_curly_string_to_list(text):
    m = re.search("\S+ \{", text)
    if m is None:
        return [text]
    start = m.start()
    open = 0
    close = 0
    for x in range(start, len(text)):
        if text[x] == '{':
            open += 1
        elif text[x] == '}':
            close += 1
        if open != 0 and open == close:
            end = x
            break
    matched_text = []
    matched_text.append(text[start:end+1])
    matched_text += convert_curly_string_to_list(text[:start] + text[end+1:])
    return matched_text

def parse_text(text):
    collection = {}
    for type in ("NewOrderSingle", "OrderCancelReplaceRequest", "OrderCancelRequest", "ExecutionReport"):
        if type in text:
            collection['report_type'] = type
            break
    else:
        collection['report_type'] = "INVALID"
    collection['log_timestamp'] = text.split('|')[0].rstrip()
    curly_list = convert_curly_string_to_list(text)
    report = convert_curly_string_to_dict(' '.join(curly_list[:-1]))
    report.update(convert_curly_string_to_dict(curly_list[-1]))
    collection['report'] = report
    return collection
