import job_search


class TestJobSearch:

    def test_addition(self):
        assert 4 == job_search.add(2, 2)

    def test_subtract(self):
        assert 2 == job_search.subtract(4, 2)
