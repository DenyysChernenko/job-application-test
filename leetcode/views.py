from rest_framework import generics
from rest_framework.response import Response
from .serializers import RotateArraySerializer, KthLargestSerializer, LongestIncreasingPathSerializer


class RotateArrayView(generics.CreateAPIView):
    """
    API endpoint that rotates an array to the right by `k` positions.

    - **Input**: JSON with `nums` (list of integers) and `k` (integer).
    - **Output**: JSON with rotated array.
    - **Example**:
      ```json
      {
        "nums": [1, 2, 3, 4, 5, 6, 7],
        "k": 3
      }
      ```
      **Response**:
      ```json
      {
        "result": [5, 6, 7, 1, 2, 3, 4]
      }
      ```
    """

    serializer_class = RotateArraySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.rotate()
            return Response({"result": result})
        return Response(serializer.errors, status=400)


class KthLargestView(generics.CreateAPIView):
    """
    API endpoint that finds the k-th largest element in an unsorted array.

    - **Input**: JSON with `nums` (list of integers) and `k` (integer).
    - **Output**: JSON with the k-th largest element.
    - **Example**:
      ```json
      {
        "nums": [3, 2, 1, 5, 6, 4],
        "k": 2
      }
      ```
      **Response**:
      ```json
      {
        "result": 5
      }
      ```
    """

    serializer_class = KthLargestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.find_kth_largest()
            return Response({"result": result})
        return Response(serializer.errors, status=400)


class LongestIncreasingPathView(generics.CreateAPIView):
    """
    API endpoint that finds the longest increasing path in a 2D matrix.

    - **Input**: JSON with a 2D matrix of integers.
    - **Output**: JSON with the length of the longest increasing path.
    - **Example**:
      ```json
      {
        "matrix": [
          [9, 9, 4],
          [6, 6, 8],
          [2, 1, 1]
        ]
      }
      ```
      **Response**:
      ```json
      {
        "result": 4
      }
      ```
    """

    serializer_class = LongestIncreasingPathSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.find_longest_path()
            return Response({"result": result})
        return Response(serializer.errors, status=400)
    