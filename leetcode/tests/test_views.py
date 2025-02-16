from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class RotateArrayViewTestCase(APITestCase):
    def setUp(self):
        """Define the URL for the RotateArrayView endpoint."""
        self.url = reverse("rotate-array") 

    def test_valid_rotation(self):
        """Test rotating an array normally."""
        data = {"nums": [1, 2, 3, 4, 5, 6, 7], "k": 3}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], [5, 6, 7, 1, 2, 3, 4])

    def test_rotation_with_large_k(self):
        """Test rotating when k is greater than the length of the array."""
        data = {"nums": [1, 2, 3, 4, 5], "k": 7} 
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], [4, 5, 1, 2, 3])

    def test_empty_array(self):
        """Test rotating an empty array."""
        data = {"nums": [], "k": 3}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], [])

    def test_missing_k_value(self):
        """Test missing `k` in the request body."""
        data = {"nums": [1, 2, 3, 4, 5]}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_rotation(self):
        """Test when `k = 0`, the array should remain unchanged."""
        data = {"nums": [1, 2, 3, 4, 5], "k": 0}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], [1, 2, 3, 4, 5])

    def test_negative_k_value(self):
        """Test when `k` is negative (should return a validation error)."""
        data = {"nums": [1, 2, 3, 4, 5], "k": -2}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class KthLargestViewTestCase(APITestCase):
    def setUp(self):
        """Define the URL for the KthLargestView endpoint."""
        self.url = reverse("kth-largest")  

    def test_valid_kth_largest(self):
        """Test finding the k-th largest element in a normal case."""
        data = {"nums": [3, 2, 1, 5, 6, 4], "k": 2}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], 5)  

    def test_k_equals_one(self):
        """Test when k=1 (should return the maximum element)."""
        data = {"nums": [3, 2, 1, 5, 6, 4], "k": 1}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], 6)  

    def test_k_equals_length(self):
        """Test when k is the length of the array (should return the minimum element)."""
        data = {"nums": [3, 2, 1, 5, 6, 4], "k": 6}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], 1) 

    def test_with_duplicate_numbers(self):
        """Test when the array contains duplicate numbers."""
        data = {"nums": [4, 4, 4, 2, 2, 5, 5], "k": 3}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], 4)  

    def test_empty_list(self):
        """Test with an empty list (should return a validation error)."""
        data = {"nums": [], "k": 2}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_k_greater_than_length(self):
        """Test when k is larger than the array length (should return a validation error)."""
        data = {"nums": [3, 1, 2], "k": 5}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_negative_k_value(self):
        """Test when k is negative (should return a validation error)."""
        data = {"nums": [3, 2, 1], "k": -1}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LongestIncreasingPathViewTestCase(APITestCase):
    def setUp(self):
        """Define the URL for the LongestIncreasingPathView endpoint."""
        self.url = reverse("longest-increasing-path")  

    def test_valid_matrix(self):
        """Test a valid matrix that should return the correct longest increasing path."""
        data = {
            "matrix": [
                [9, 9, 4],
                [6, 6, 8],
                [2, 1, 1]
            ]
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], 4)  

    def test_empty_matrix(self):
        """Test an empty matrix, which should return a 400 Bad Request error."""
        data = {"matrix": []}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_single_row_matrix(self):
        """Test a single-row matrix, where the longest increasing path should be correct."""
        data = {"matrix": [[1, 2, 3, 4, 5]]}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], 5)

    def test_single_column_matrix(self):
        """Test a single-column matrix, where the longest increasing path should be correct."""
        data = {"matrix": [[1], [2], [3], [4], [5]]}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], 5)

    def test_single_element_matrix(self):
        """Test a matrix with a single element, where the longest increasing path is just 1."""
        data = {"matrix": [[42]]}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], 1)

    def test_non_increasing_matrix(self):
        """Test a matrix where all elements are the same."""
        data = {"matrix": [[5, 5], [5, 5]]}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], 1) 

    def test_large_matrix(self):
        """Test a larger matrix to check performance and correctness."""
        data = {
            "matrix": [
                [3, 4, 5],
                [3, 2, 6],
                [2, 2, 1]
            ]
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], 4)

