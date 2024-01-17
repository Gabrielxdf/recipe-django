from unittest import TestCase

from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),  # total number of pages avaliable
            qty_pages=4,  # number of pages to be shown to user
            current_page=1,  # the current page the user is in
        )
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa E501
        # Current page = 1 - Qty Page = 4 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 2 - Qty Page = 4 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 3 - Qty Page = 4 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )
        self.assertEqual([2, 3, 4, 5], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        # Current page = 10 - Qty Page = 4 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )
        self.assertEqual([9, 10, 11, 12], pagination)

        # Current page = 14 - Qty Page = 4 - Middle Page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=14,
        )
        self.assertEqual([13, 14, 15, 16], pagination)

    def test_make_sure_end_ranges_are_correct(self):
        # Current page = 19 - Qty Page = 4 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )
        self.assertEqual([17, 18, 19, 20], pagination)

        # Current page = 20 - Qty Page = 4 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )
        self.assertEqual([17, 18, 19, 20], pagination)
