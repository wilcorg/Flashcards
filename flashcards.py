import time
import argparse
memory_file = []


def add_card(card_set):
    term = input('The card:\n')
    log('The card:\n', 'out')
    while term in card_set.keys():
        term = input(f'The term "{term}" already exists. Try again:\n')
        log(f'{term}\n')
        log(f'The term "{term}" already exists. Try again:\n', 'out')

    definition = input('The definition of the card:\n')
    log('The definition of the card:\n', 'out')
    log(f'{definition}\n')

    while definition in [card['def'] for card in card_set.values()]:
        definition = input(f'The definition "{definition}" already exists. Try again:\n')
        log(f'{definition}')
        log(f'The term "{definition}" already exists. Try again:\n', 'out')

    card_set[term] = {'def': definition, 'm_count': 0}
    print(f'The pair ("{term}":"{definition}") has been added.\n')
    log(f'The pair ("{term}":"{definition}") has been added.\n', 'out')
    return card_set


def remove_card(card_set):
    term = input('Which card?\n')
    log('Which card:\n', 'out')
    log(f'{term}\n')

    if term in card_set.keys():
        card_set.pop(term)
        print('The card has been removed.\n')
        log('The card has been removed.\n', 'out')
    else:
        print(f'Can\'t remove "{term}": there is no such card.\n')
        log(f'Can\'t remove "{term}": there is no such card.\n', 'out')
    return card_set


def import_card(card_set, path):
    try:
        file = [line.split(':') for line in open(path, 'r').read().split('\n')][:-1]
        for term, definition, count in file:
            if term in card_set.keys():
                card_set.pop(term)
            card_set[term] = {'def': definition, 'm_count': int(count)}
        print(f'{len(file)} {"card" if len(file) == 1 else "cards"} have been loaded.\n')
        log(f'{len(file)} {"card" if len(file) == 1 else "cards"} have been loaded.\n', 'out')
    except FileNotFoundError:
        print('File not found.\n')
        log('File not found.\n', 'out')
    return card_set


def export_card(card_set, path):
    with open(path, 'w') as file:
        for term, definition in card_set.items():
            file.write(f'{term}:{definition["def"]}:{definition["m_count"]}\n')
    print(f'{len(card_set)} {"card" if len(card_set) == 1 else "cards"} have been saved.\n')
    log(f'{len(card_set)} {"card" if len(card_set) == 1 else "cards"} have been saved.\n', 'out')


def ask_card(card_set):
    import random
    count = int(input('How many times to ask?\n'))
    log('How many times to ask?\n', 'out')
    log(f'{count}\n')

    for _ in range(count):
        term = random.choice(list(card_set.keys()))
        definition = input(f'Print the definition of "{term}":\n')
        log(f'Print the definition of "{term}":\n', 'out')
        log(f'{definition}\n')

        if card_set[term]['def'] == definition:
            print('Correct')
            log('Correct\n', 'out')

        elif definition in [card['def'] for card in card_set.values()]:
            second_term = [k for k, v in card_set.items() if v['def'] == definition][0]
            print(f'Wrong. The right answer is "{definition}", '
                  f'but your definition is correct for "{second_term}".')

            log(f'Wrong. The right answer is "{definition}", '
                f'but your definition is correct for "{second_term}".', 'out')
            card_set[term]['m_count'] += 1
        else:
            print(f'Wrong. The right answer is "{definition}"')
            log(f'Wrong. The right answer is "{definition}"', 'out')
            card_set[term]['m_count'] += 1
    print()
    return card_set


def log(string, mode='in'):
    string = f'{time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())} | {"INPUT" if mode == "in" else "OUTPUT"}: {string}'
    memory_file.append(string)


def write_log():
    path = input('File name:\n')
    log('File name:\n', 'out')
    log(f'{path}\n')

    print('The log has been saved.\n')
    log('The log has been saved.\n', 'out')

    with open(path, 'w') as log_file:
        for line in memory_file:
            log_file.write(line)
    return


def hardest_card(card_set):
    if card_set.values():
        max_error_count = max([term['m_count'] for term in card_set.values()])
        hardest_terms = []
        for term, answer in card_set.items():
            if int(answer['m_count']) == max_error_count:
                hardest_terms.append(f'"{term}"')

        if not hardest_terms or max_error_count == 0:
            print('There are no cards with errors.\n')
            log('There are no cards with errors.\n', 'out')
        else:
            if len(hardest_terms) > 1:
                hardest_terms_str = ', '.join(hardest_terms) + '. '
            else:
                hardest_terms_str = hardest_terms[0] + '. '
            print(f'The hardest {"cards" if len(hardest_terms) > 1 else "card"} '
                  f'{"are" if len(hardest_terms) > 1 else "is"}: {hardest_terms_str}', end='')
            print(f'You have {max_error_count} {"error" if max_error_count == 1 else "errors"} answering'
                  f' {"it" if len(hardest_terms) == 1 else "them"}.\n')

            log(f'The hardest {"cards" if len(hardest_terms) > 1 else "card"} '
                f'{"are" if len(hardest_terms) > 1 else "is"}: {hardest_terms}', 'out')
            log(f'You have {max_error_count} {"error" if max_error_count == 1 else "errors"} answering'
                f' {"it" if len(hardest_terms) == 1 else "them"}.\n', 'out')
    else:
        print('There are no cards with errors.\n')
        log('There are no cards with errors.\n', 'out')
    return


def reset_stats(card_set):
    for term in card_set.keys():
        card_set[term]['m_count'] = 0
    print('Card statistics have been reset.\n')
    log('Card statistics have been reset.\n')
    return card_set


def menu(card_set):
    parser = argparse.ArgumentParser()
    parser.add_argument('--import_from')
    parser.add_argument('--export_to')
    args = parser.parse_args()
    if args.import_from:
        card_set = import_card(card_set, args.import_from)
    while True:
        action = input('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n')
        log('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n', 'out')
        log(f'{action}\n')
        if action == 'add':
            card_set = add_card(card_set)
        elif action == 'remove':
            card_set = remove_card(card_set)
        elif action == 'import':
            path = input('File name:\n')
            log('File name:\n', 'out')
            log(f'{path}\n')
            card_set = import_card(card_set, path)
        elif action == 'export':
            path = input('File name:\n')
            log('File name:\n', 'out')
            log(f'{path}\n')
            export_card(card_set, path)
        elif action == 'ask':
            card_set = ask_card(card_set)
        elif action == 'log':
            write_log()
        elif action == 'hardest card':
            hardest_card(card_set)
        elif action == 'reset stats':
            card_set = reset_stats(card_set)
        elif action == 'exit':
            print('Bye bye!')
            if args.export_to:
                export_card(card_set, args.export_to)
            break


def run():
    card_set = {}
    menu(card_set)


if __name__ == '__main__':
    run()
