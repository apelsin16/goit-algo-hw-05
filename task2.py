def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    iterations = 0

    while low <= high:
        mid = (low + high) // 2
        iterations += 1

        if arr[mid] < target:
            low = mid + 1
        elif arr[mid] > target:
            high = mid - 1
        else:
            return iterations, arr[mid]

    # Якщо елемент не знайдено, повертаємо кількість ітерацій та "верхню межу"
    if high >= 0 and low < len(arr):
        return iterations, arr[low]
    else:
        return iterations, None

# Приклад використання:
arr = [0.1, 0.3, 0.5, 0.7, 0.9]
target = 0.6
iterations, upper_bound = binary_search(arr, target)
print("Кількість ітерацій:", iterations)
if upper_bound is not None:
    print("Верхня межа:", upper_bound)
else:
    print("Верхня межа не знайдена.")
