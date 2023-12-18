def main(part=1):
    with open('inputs.txt') as file:
        lines = [line.strip() for line in file]
    if part == 2:
        lines = [
            line.replace('one', 'o1e').
            replace('two', 't2o').
            replace('three', 't3e').
            replace('four', 'f4r').
            replace('five', 'f5e').
            replace('six', 's6x').
            replace('seven', 's7n').
            replace('eight', 'e8t').
            replace('nine', 'n9e')
            for line in lines
        ]
    digits = [
        [char for char in line if char.isnumeric()]
        for line in lines
    ]
    final_numbers = [int(nums[0] + nums[-1]) for nums in digits]
    total_sum = sum(final_numbers)
    print(total_sum)

if __name__ == '__main__':
    main()
    main(2)