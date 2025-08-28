def bubble_sort(arr):
    # Bug: loop bounds wrong (skips last swap when reverse sorted)
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 2):  # <-- off-by-one
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return None


if __name__ == '__main__':
    a = [5, 4, 3, 2, 1]
    bubble_sort(a)
    print(a)
