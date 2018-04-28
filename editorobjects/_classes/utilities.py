def get_line_data(line):
    return (line[line.find('=') + 1:].strip()).replace(' ', '')


def get_line_key(line):
    return (line[:line.find('=')].strip()).replace(' ', '')


def get_line_param(line):
    line = line[line.find('_') + 1:]
    return line[line.find('_') + 1:line.find('=')].strip()
