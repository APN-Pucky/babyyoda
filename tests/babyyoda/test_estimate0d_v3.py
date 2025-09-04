import math

from babyyoda.grogu.estimate0d_v3 import GROGU_ESTIMATE0D_V3

# Sample data for testing estimate0d_v3 parsing
sample_data = """BEGIN YODA_ESTIMATE0D_V3 /_XSEC
Path: /_XSEC
Title:
Type: Estimate0D
---
ErrorLabels: ["stats"]
# value      	errDn(1)     	errUp(1)
4.740384e+07 	-6.773200e+03	6.773200e+03
END YODA_ESTIMATE0D_V3"""


def test_grogu_estimate0d_v3_parsing():
    """Test parsing of YODA_ESTIMATE0D_V3 format."""
    # Parse the sample data
    estimate = GROGU_ESTIMATE0D_V3.from_string(sample_data)

    # Test basic properties
    assert estimate.d_key == "/_XSEC"
    assert estimate.error_labels() == ["stats"]
    assert estimate.title() == ""
    assert estimate.type() == "Estimate0D"
    assert estimate.num_error_sources() == 1


def test_grogu_estimate0d_v3_value_access():
    """Test value access methods."""
    estimate = GROGU_ESTIMATE0D_V3.from_string(sample_data)

    # Test value access
    expected_value = 4.740384e07
    assert abs(estimate.value() - expected_value) < 1e-3
    assert abs(estimate.val() - expected_value) < 1e-3
    assert not estimate.has_nan()


def test_grogu_estimate0d_v3_error_access():
    """Test error access methods."""
    estimate = GROGU_ESTIMATE0D_V3.from_string(sample_data)

    # Test individual error access
    expected_err_dn = -6.773200e03
    expected_err_up = 6.773200e03

    assert abs(estimate.error_dn(0) - expected_err_dn) < 1e-3
    assert abs(estimate.error_up(0) - expected_err_up) < 1e-3

    # Test error lists
    errors_dn = estimate.errors_dn()
    errors_up = estimate.errors_up()

    assert len(errors_dn) == 1
    assert len(errors_up) == 1
    assert abs(errors_dn[0] - expected_err_dn) < 1e-3
    assert abs(errors_up[0] - expected_err_up) < 1e-3


def test_grogu_estimate0d_v3_error_calculations():
    """Test error calculation methods."""
    estimate = GROGU_ESTIMATE0D_V3.from_string(sample_data)

    # Test quadrature sum
    total_dn, total_up = estimate.quadSum()
    expected_total = 6.773200e03  # Only one error source

    assert abs(total_dn - (-expected_total)) < 1e-3
    assert abs(total_up - expected_total) < 1e-3

    # Test total error (alias)
    total_dn2, total_up2 = estimate.totalErr()
    assert abs(total_dn2 - total_dn) < 1e-10
    assert abs(total_up2 - total_up) < 1e-10

    # Test average error
    avg_err = estimate.totalErrAvg()
    expected_avg = 0.5 * (abs(total_dn) + abs(total_up))
    assert abs(avg_err - expected_avg) < 1e-3


def test_grogu_estimate0d_v3_round_trip():
    """Test round-trip conversion (parse -> to_string -> parse again)."""
    estimate = GROGU_ESTIMATE0D_V3.from_string(sample_data)

    # Convert back to string
    reconstructed_string = estimate.to_string()

    # Parse the reconstructed string
    estimate2 = GROGU_ESTIMATE0D_V3.from_string(reconstructed_string)

    # Compare key properties
    assert estimate2.d_key == estimate.d_key
    assert estimate2.error_labels() == estimate.error_labels()
    assert estimate2.title() == estimate.title()
    assert estimate2.type() == estimate.type()

    # Compare values (handling potential floating point precision issues)
    assert abs(estimate2.value() - estimate.value()) < 1e-10

    # Compare errors
    for err1, err2 in zip(estimate.errors_dn(), estimate2.errors_dn()):
        assert abs(err1 - err2) < 1e-10

    for err1, err2 in zip(estimate.errors_up(), estimate2.errors_up()):
        assert abs(err1 - err2) < 1e-10


def test_grogu_estimate0d_v3_nan_handling():
    """Test handling of NaN values."""
    # Test data with NaN value
    nan_data = """BEGIN YODA_ESTIMATE0D_V3 /test
Path: /test
Type: Estimate0D
---
ErrorLabels: ["stats"]
# value	errDn(1)	errUp(1)
nan	---	---
END YODA_ESTIMATE0D_V3"""

    estimate = GROGU_ESTIMATE0D_V3.from_string(nan_data)
    assert estimate.has_nan()
    assert math.isnan(estimate.value())
    assert math.isnan(estimate.error_dn(0))
    assert math.isnan(estimate.error_up(0))


def test_grogu_estimate0d_v3_multi_error_sources():
    """Test handling of multiple error sources."""
    multi_err_data = """BEGIN YODA_ESTIMATE0D_V3 /test
Path: /test
Type: Estimate0D
---
ErrorLabels: ["stats", "syst"]
# value	errDn(1)	errUp(1)	errDn(2)	errUp(2)
1.0e+06	-1.0e+03	1.0e+03	-2.0e+03	2.0e+03
END YODA_ESTIMATE0D_V3"""

    estimate = GROGU_ESTIMATE0D_V3.from_string(multi_err_data)

    assert estimate.num_error_sources() == 2
    assert estimate.error_labels() == ["stats", "syst"]

    # Test individual error access
    assert abs(estimate.error_dn(0) - (-1.0e03)) < 1e-6
    assert abs(estimate.error_up(0) - 1.0e03) < 1e-6
    assert abs(estimate.error_dn(1) - (-2.0e03)) < 1e-6
    assert abs(estimate.error_up(1) - 2.0e03) < 1e-6

    # Test quadrature sum (should combine both error sources)
    total_dn, total_up = estimate.quadSum()
    expected_total = math.sqrt(1.0e06 + 4.0e06)  # sqrt(1e3^2 + 2e3^2)
    assert abs(total_dn - (-expected_total)) < 1e-3
    assert abs(total_up - expected_total) < 1e-3


def test_grogu_estimate0d_v3_minimal_input():
    """Test minimal valid input."""
    minimal_data = """BEGIN YODA_ESTIMATE0D_V3 /test
Path: /test
Type: Estimate0D
---
ErrorLabels: ["stats"]
# value	errDn(1)	errUp(1)
1.0	0.1	0.1
END YODA_ESTIMATE0D_V3"""

    estimate = GROGU_ESTIMATE0D_V3.from_string(minimal_data)
    assert estimate.d_key == "/test"
    assert estimate.value() == 1.0
    assert estimate.error_dn(0) == 0.1
    assert estimate.error_up(0) == 0.1
    assert estimate.num_error_sources() == 1
