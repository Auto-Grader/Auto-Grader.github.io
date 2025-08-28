TESTS = [
    {
        'name': 'empty_list',
        'input': [],
        'expected': [],
        'points': 10,
        'description': 'Empty list must remain empty. Common errors: throwing on len=0 or index errors.'
    },
    {
        'name': 'single_element',
        'input': [1],
        'expected': [1],
        'points': 10,
        'description': 'Single-element lists should be unchanged.'
    },
    {
        'name': 'already_sorted',
        'input': [1, 2, 3, 4],
        'expected': [1, 2, 3, 4],
        'points': 10,
        'description': 'Stable behavior on already sorted lists; ensure no out-of-bounds access.'
    },
    {
        'name': 'reverse_sorted',
        'input': [5, 4, 3, 2, 1],
        'expected': [1, 2, 3, 4, 5],
        'points': 10,
        'description': 'Reverse-sorted input is a common edge-case. Off-by-one errors often fail here.'
    },
    {
        'name': 'duplicates',
        'input': [2, 3, 2, 1, 3],
        'expected': [1, 2, 2, 3, 3],
        'points': 10,
        'description': 'Ensure duplicates are handled correctly and algorithm is stable (optional).'
    },
    {
        'name': 'negative_numbers',
        'input': [-1, 5, -3, 2],
        'expected': [-3, -1, 2, 5],
        'points': 10,
        'description': 'Sorting must handle negative numbers and mixed sign values.'
    },
    {
        'name': 'strings_order',
        'input': ['b', 'a', 'aa', ''],
        'expected': ['', 'a', 'aa', 'b'],
        'points': 10,
        'description': 'If asked to support general comparable elements, test string ordering. Some solutions assume numeric lists only.'
    },
    {
        'name': 'large_random_small',
        'input': list(range(50, 0, -1)),
        'expected': list(range(1, 51)),
        'points': 10,
        'description': 'Short performance / correctness check. Bubble sort should still finish quickly for 50 elements but check for timeouts in heavy implementations.'
    },
    {
        'name': 'mixed_types_failure',
        'input': [1, 'a', 2],
        'expected': None,
        'points': 10,
        'description': 'Mixed incomparable types should raise an exception or be handled. Accept either a raised TypeError or a documented behavior. For this assignment, we expect an exception (test passes if exception raised).'
    },
    {
        'name': 'inplace_vs_return',
        'input': [3, 1, 2],
        'expected': [1, 2, 3],
        'points': 10,
        'description': 'Accept either in-place modification (function returns None) or returning a sorted list. The final result must equal sorted(input).'
    }
]

MAX_SCORE = sum(t['points'] for t in TESTS)
