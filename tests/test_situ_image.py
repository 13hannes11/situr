from situr.image import extend_dim, remove_dim

import numpy as np
import unittest


class TestDimMethods(unittest.TestCase):
    def test_identical_after_expand_remove_(self):
        arr = np.random.rand(5, 2)
        self.assertTrue(
            np.array_equal(
                arr, remove_dim(extend_dim(np.copy(arr)))
            )
        )

    def test_extend_dim_only_extends(self):
        arr = np.random.rand(5, 2)
        self.assertTrue(
            np.array_equal(
                arr, extend_dim(np.copy(arr))[:, :-1]
            )
        )
