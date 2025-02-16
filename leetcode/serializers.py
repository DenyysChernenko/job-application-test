from rest_framework import serializers
import random

class RotateArraySerializer(serializers.Serializer):
    nums = serializers.ListField(
        child=serializers.IntegerField(), 
        allow_empty=True  
    )
    k = serializers.IntegerField(min_value=0)

    def validate(self, data):
        """Ensure k is within valid range."""
        nums, k = data["nums"], data["k"]

        if not nums:  
            return data

        data["k"] = k % len(nums)  
        return data

    def rotate(self):
        """Rotate array to the right by k places with O(1) space complexity."""
        nums, k = self.validated_data["nums"], self.validated_data["k"]

        if not nums or k == 0: 
            return nums

        self.reverse(nums, 0, len(nums) - 1)
        self.reverse(nums, 0, k - 1)
        self.reverse(nums, k, len(nums) - 1)
        return nums

    @staticmethod
    def reverse(arr, start, end):
        """Reverse elements in an array between start and end indexes."""
        while start < end:
            arr[start], arr[end] = arr[end], arr[start]
            start += 1
            end -= 1


class KthLargestSerializer(serializers.Serializer):
    nums = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="List of integers."
    )
    k = serializers.IntegerField(min_value=1, help_text="The k-th largest element to find.")

    def find_kth_largest(self):
        """
        Finds the k-th largest element in O(n) average time using QuickSelect.
        """
        nums = self.validated_data["nums"]
        k = self.validated_data["k"]

        if k > len(nums):
            raise serializers.ValidationError("k cannot be greater than the length of nums.")

        def quickselect(left, right, index):
            """
            In-place QuickSelect algorithm.
            """
            pivot_index = random.randint(left, right)
            pivot = nums[pivot_index]

            nums[right], nums[pivot_index] = nums[pivot_index], nums[right]  
            store_index = left

            for i in range(left, right):
                if nums[i] > pivot:  
                    nums[i], nums[store_index] = nums[store_index], nums[i]
                    store_index += 1

            nums[right], nums[store_index] = nums[store_index], nums[right]  

            if store_index == index:
                return nums[store_index]
            elif store_index > index:
                return quickselect(left, store_index - 1, index)
            else:
                return quickselect(store_index + 1, right, index)

        return quickselect(0, len(nums) - 1, k - 1)


class LongestIncreasingPathSerializer(serializers.Serializer):
    matrix = serializers.ListField(
        child=serializers.ListField(
            child=serializers.IntegerField(),
            allow_empty=False
        ),
        allow_empty=False
    )

    def validate_matrix(self, value):
        """
        Validates that the matrix is non-empty and rectangular.
        """
        if not value or not all(isinstance(row, list) for row in value):
            raise serializers.ValidationError("Matrix must be a non-empty 2D list.")

        row_length = len(value[0])
        if any(len(row) != row_length for row in value):
            raise serializers.ValidationError("All rows must have the same number of columns.")

        return value

    def find_longest_path(self):
        """
        Computes the longest increasing path in a matrix using DFS + memoization.
        """
        matrix = self.validated_data["matrix"]
        if not matrix:
            return 0

        rows, cols = len(matrix), len(matrix[0])
        memo = [[-1] * cols for _ in range(rows)]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def dfs(r, c):
            if memo[r][c] != -1:
                return memo[r][c]

            max_length = 1
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                    max_length = max(max_length, 1 + dfs(nr, nc))

            memo[r][c] = max_length
            return max_length

        return max(dfs(r, c) for r in range(rows) for c in range(cols))
    