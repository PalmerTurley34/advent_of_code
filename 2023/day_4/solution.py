from collections import defaultdict

def main():
    with open('inputs.txt') as file:
        lines = [line.strip() for line in file]
    total_points = 0
    num_copys = defaultdict(int)
    for line in lines:
        card, nums = line.split(': ')
        card_num = int(card.strip('Card '))
        winning_nums, card_nums = nums.split(' | ')
        winning_nums = [int(num.strip()) for num in winning_nums.split()]
        card_nums = [int(num.strip()) for num in card_nums.split()]
        total_matches = sum(num in winning_nums for num in card_nums)
        num_copys[card_num] += 1
        if not total_matches: continue
        for i in range(card_num + 1, card_num + total_matches + 1):
            num_copys[i] += 1 * num_copys[card_num]
        total_points += 2 ** (total_matches - 1)
    print(f'Part 1: {total_points}')
    print(f'Part 2: {sum(num_copys.values())}')
if __name__ == '__main__':
    main()