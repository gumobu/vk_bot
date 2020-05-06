import re


def max_mistakes_count(word):
    if len(word) % 4 == 0:
        max_mistakes = len(word) // 4
    else:
        max_mistakes = len(word) // 4 + 1
    return max_mistakes


def final_string_determination(entry_string, comp_list):
    matrix = {}
    len1 = len(entry_string)
    cost_of_match = list()
    min_entry_y = [None for _ in range(len(comp_list))]
    count = 0

    for _ in range(len(comp_list)):
        max_cost = 0
        len2 = len(comp_list[_])
        string2 = comp_list[_]

        for x in range(-1, len1 + 1):
            matrix[(x, -1)] = x + 1
        for y in range(-1, len2 + 1):
            matrix[(-1, y)] = y + 1

        for y in range(len2):
            for x in range(len1):
                if entry_string[x] == string2[y]:
                    cost = matrix[x, y] = matrix[x - 1, y - 1] + 1
                    if cost > max_cost:
                        max_cost = cost
                        min_entry_y.insert(_, y)
                        min_entry_y.remove(min_entry_y[_ + 1])
                else:
                    matrix[x, y] = 0
        cost_of_match.append(max_cost)

    maximum = cost_of_match[0]
    for _ in range(len(cost_of_match)):
        if cost_of_match[_] > maximum:
            maximum = cost_of_match[_]
            str_id = _
        elif cost_of_match[_] == maximum:
            count += 1

    if count == 0:
        print(f'Your word is {comp_list[str_id]}')
    else:
        min_y = min_entry_y[0]
        minimum_y = list()
        for _ in range(len(min_entry_y)):
            if min_entry_y[_] < min_y:
                min_y = min_entry_y[_]
                str_id = _
                minimum_y = list().append(_)
            elif min_entry_y[_] == min_y:
                str_id = _
                minimum_y.insert(0, _)

    if len(minimum_y) == 1:
        return comp_list[str_id]
    else:
        for _ in range(len(minimum_y)):
            add_str = f'{comp_list[_]}, '
        return(f'Не получилось разобрать команду, написанную тобой. Возможно, подразумевались эти команды:'
               f' {add_str} попробуй одну из них.')


def damerau_levenshtein_distance(string1, object2):
    """
    An adapted version of Damerau-Levenstein distance algorithm.

    Can be used both for single strings comparing and for comparing single string with a list of string.
    """
    d = {}  # Sets empty dictionary for future using
    mistakes = []  # Sets an empty list for filling with lists (<recognized syting>, <number of differences>)
    len1 = len(string1)
    if type(object2) == tuple:
        itr = len(object2)  # Sets the number of compare iterations
        for _ in range(itr):
            string2 = object2[_]
            len2 = len(string2)
            max_mistakes = max_mistakes_count(string2)
            for x in range(-1, len1 + 1):
                d[(x, -1)] = x + 1
            for y in range(-1, len2 + 1):
                d[(-1, y)] = y + 1
            for x in range(len1):
                for y in range(len2):
                    if string1[x] == string2[y]:
                        cost = 0
                    else:
                        cost = 1
                    d[(x, y)] = min(
                        d[(x - 1, y)] + 1,  # deletion
                        d[(x, y - 1)] + 1,  # insertion
                        d[(x - 1, y - 1)] + cost,  # substitution
                    )
                    if x and y and string1[x] == string2[y - 1] and string1[x - 1] == string2[y]:
                        d[(x, y)] = min(d[(x, y)], d[x - 2, y - 2] + cost)  # transposition
            if d[len1 - 1, len2 - 1] <= max_mistakes:
                add = d[len1 - 1, len2 - 1]
                mistakes.append([object2[_], add])
        return mistakes


def main(w_input, string_tuple):
    search = r"^\s?\.\s?\b\w+\b"
    if re.match(search, w_input) is not None:
        # Checks if there is the only one word in the string and there is a dot before it
        a = re.match(search, w_input).group()
        mistakes = damerau_levenshtein_distance(a, string_tuple)
    else:
        pass
    if mistakes:
        minimum = mistakes[0][1]
        mistakes_check = [None]
        if len(mistakes) > 1:
            for _ in range(len(mistakes)):
                minimum = min(minimum, mistakes[_][1])  # Minimal mistakes count
                mistakes_check.append(_)
            if len(mistakes_check) > 1:
                list_of_variants = list()
                for _ in range(1, len(mistakes_check)):
                    list_of_variants.append(mistakes[mistakes_check[_]][0])
                return final_string_determination(w_input, list_of_variants)
        else:
            return mistakes[0][0]
    else:
        return 'Не удалось распознать команду. Попробуй еще раз.'
