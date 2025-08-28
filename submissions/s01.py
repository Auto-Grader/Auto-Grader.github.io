def bubble_sort(arr):
    # In-place bubble sort
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return None


if __name__ == '__main__':
    a = [5, 2, 9, 1]
    bubble_sort(a)
    print(a)
