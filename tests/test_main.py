import runpy


# I'd write unit tests that guarantee the correct functionality
# of the script.
def test_main(ssm_mock, sns_mock):
    runpy.run_module("main", run_name="__main__")
