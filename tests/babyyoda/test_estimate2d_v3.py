import math

from babyyoda.grogu.estimate2d_v3 import GROGU_ESTIMATE2D_V3

# Sample data for testing estimate2d_v3 parsing
sample_data = """BEGIN YODA_ESTIMATE2D_V3 /test2d
Path: /test2d
Title: Test 2D Estimate
Type: Estimate2D
---
Edges(A1): [0.0, 1.0, 2.0]
Edges(A2): [0.0, 0.5, 1.0]
ErrorLabels: ["stats"]
# value      	errDn(1)     	errUp(1)
1.000000e+02 	-1.000000e+01	1.000000e+01
2.000000e+02 	-1.414214e+01	1.414214e+01
3.000000e+02 	-1.732051e+01	1.732051e+01
4.000000e+02 	-2.000000e+01	2.000000e+01
END YODA_ESTIMATE2D_V3"""


def test_grogu_estimate2d_v3_parsing():
    """Test parsing of YODA_ESTIMATE2D_V3 format."""
    # Parse the sample data
    estimate = GROGU_ESTIMATE2D_V3.from_string(sample_data)

    # Test basic properties
    assert estimate.d_key == "/test2d"
    assert estimate.num_bins() == 4  # 2x2 grid
    assert estimate.error_labels() == ["stats"]
    assert estimate.title() == "Test 2D Estimate"
    assert estimate.type() == "Estimate2D"


def test_grogu_estimate2d_v3_edges():
    """Test edge parsing for 2D estimates."""
    estimate = GROGU_ESTIMATE2D_V3.from_string(sample_data)

    # Test X edges
    x_edges = estimate.xEdges()
    assert len(x_edges) == 3
    assert x_edges == [0.0, 1.0, 2.0]

    # Test Y edges
    y_edges = estimate.yEdges()
    assert len(y_edges) == 3
    assert y_edges == [0.0, 0.5, 1.0]

    # Test dimensions
    assert estimate.num_x_bins() == 2
    assert estimate.num_y_bins() == 2
    assert estimate.num_edges() == 6  # 3 + 3


def test_grogu_estimate2d_v3_bin_data():
    """Test bin data parsing and access."""
    estimate = GROGU_ESTIMATE2D_V3.from_string(sample_data)

    # Test values
    values = estimate.values()
    expected_values = [100.0, 200.0, 300.0, 400.0]
    for val, expected in zip(values, expected_values):
        assert abs(val - expected) < 1e-6

    # Test first bin
    first_bin = estimate.d_bins[0]
    assert not first_bin.has_nan()
    assert abs(first_bin.value() - 100.0) < 1e-6
    assert len(first_bin.errors_dn()) == 1
    assert len(first_bin.errors_up()) == 1
    assert abs(first_bin.errors_dn()[0] - (-10.0)) < 1e-6
    assert abs(first_bin.errors_up()[0] - 10.0) < 1e-6


def test_grogu_estimate2d_v3_error_access():
    """Test error access methods."""
    estimate = GROGU_ESTIMATE2D_V3.from_string(sample_data)

    # Test errors_dn and errors_up methods
    errors_dn = estimate.errors_dn(0)  # First error source (stats)
    errors_up = estimate.errors_up(0)

    assert len(errors_dn) == estimate.num_bins()
    assert len(errors_up) == estimate.num_bins()

    expected_errors_dn = [-10.0, -14.14214, -17.32051, -20.0]
    expected_errors_up = [10.0, 14.14214, 17.32051, 20.0]

    for i in range(len(errors_dn)):
        assert abs(errors_dn[i] - expected_errors_dn[i]) < 1e-4
        assert abs(errors_up[i] - expected_errors_up[i]) < 1e-4


def test_grogu_estimate2d_v3_bin_error_calculations():
    """Test bin-level error calculations."""
    estimate = GROGU_ESTIMATE2D_V3.from_string(sample_data)

    # Test first bin quadrature sum (only one error source, so should be same)
    first_bin = estimate.d_bins[0]
    total_dn, total_up = first_bin.quadSum()
    assert abs(total_dn - (-10.0)) < 1e-6
    assert abs(total_up - 10.0) < 1e-6

    # Test total error average
    avg_err = first_bin.totalErrAvg()
    expected_avg = 0.5 * (10.0 + 10.0)
    assert abs(avg_err - expected_avg) < 1e-6


def test_grogu_estimate2d_v3_round_trip():
    """Test round-trip conversion (parse -> to_string -> parse again)."""
    estimate = GROGU_ESTIMATE2D_V3.from_string(sample_data)

    # Convert back to string
    reconstructed_string = estimate.to_string()

    # Parse the reconstructed string
    estimate2 = GROGU_ESTIMATE2D_V3.from_string(reconstructed_string)

    # Compare key properties
    assert estimate2.d_key == estimate.d_key
    assert estimate2.num_bins() == estimate.num_bins()
    assert estimate2.num_edges() == estimate.num_edges()
    assert estimate2.error_labels() == estimate.error_labels()
    assert estimate2.title() == estimate.title()
    assert estimate2.type() == estimate.type()

    # Compare edges
    assert estimate2.xEdges() == estimate.xEdges()
    assert estimate2.yEdges() == estimate.yEdges()

    # Compare values (handling potential floating point precision issues)
    values1 = estimate.values()
    values2 = estimate2.values()
    for v1, v2 in zip(values1, values2):
        if math.isnan(v1):
            assert math.isnan(v2)
        else:
            assert abs(v1 - v2) < 1e-10


def test_grogu_estimate2d_v3_nan_handling():
    """Test handling of NaN values."""
    # Test data with NaN values
    nan_data = """BEGIN YODA_ESTIMATE2D_V3 /test_nan
Path: /test_nan
Type: Estimate2D
---
Edges(A1): [0.0, 1.0]
Edges(A2): [0.0, 1.0]
ErrorLabels: ["stats"]
# value	errDn(1)	errUp(1)
nan	---	---
END YODA_ESTIMATE2D_V3"""

    estimate = GROGU_ESTIMATE2D_V3.from_string(nan_data)
    assert estimate.num_bins() == 1

    first_bin = estimate.d_bins[0]
    assert first_bin.has_nan()
    assert math.isnan(first_bin.value())
    assert math.isnan(first_bin.errors_dn()[0])
    assert math.isnan(first_bin.errors_up()[0])


def test_grogu_estimate2d_v3_multi_error_sources():
    """Test handling of multiple error sources."""
    multi_err_data = """BEGIN YODA_ESTIMATE2D_V3 /test_multi
Path: /test_multi
Type: Estimate2D
---
Edges(A1): [0.0, 1.0, 2.0]
Edges(A2): [0.0, 1.0]
ErrorLabels: ["stats", "syst"]
# value	errDn(1)	errUp(1)	errDn(2)	errUp(2)
1.0e+02	-1.0e+01	1.0e+01	-5.0e+00	5.0e+00
2.0e+02	-1.4e+01	1.4e+01	-7.0e+00	7.0e+00
END YODA_ESTIMATE2D_V3"""

    estimate = GROGU_ESTIMATE2D_V3.from_string(multi_err_data)

    assert len(estimate.error_labels()) == 2
    assert estimate.error_labels() == ["stats", "syst"]
    assert estimate.num_bins() == 2

    # Test individual error access
    errors_dn_stats = estimate.errors_dn(0)  # stats errors
    errors_up_stats = estimate.errors_up(0)
    errors_dn_syst = estimate.errors_dn(1)  # syst errors
    errors_up_syst = estimate.errors_up(1)

    assert abs(errors_dn_stats[0] - (-10.0)) < 1e-6
    assert abs(errors_up_stats[0] - 10.0) < 1e-6
    assert abs(errors_dn_syst[0] - (-5.0)) < 1e-6
    assert abs(errors_up_syst[0] - 5.0) < 1e-6

    # Test quadrature sum for first bin
    first_bin = estimate.d_bins[0]
    total_dn, total_up = first_bin.quadSum()
    expected_total = math.sqrt(10.0**2 + 5.0**2)  # sqrt(100 + 25) = sqrt(125)
    assert abs(total_dn - (-expected_total)) < 1e-6
    assert abs(total_up - expected_total) < 1e-6


def test_grogu_estimate2d_v3_different_grid_sizes():
    """Test different grid sizes."""
    # Test 3x2 grid
    grid_data = """BEGIN YODA_ESTIMATE2D_V3 /test_grid
Path: /test_grid
Type: Estimate2D
---
Edges(A1): [0.0, 1.0, 2.0, 3.0]
Edges(A2): [0.0, 0.5, 1.0]
ErrorLabels: ["stats"]
# value	errDn(1)	errUp(1)
1.0	-0.1	0.1
2.0	-0.2	0.2
3.0	-0.3	0.3
4.0	-0.4	0.4
5.0	-0.5	0.5
6.0	-0.6	0.6
END YODA_ESTIMATE2D_V3"""

    estimate = GROGU_ESTIMATE2D_V3.from_string(grid_data)

    assert estimate.num_x_bins() == 3  # 4 edges = 3 bins
    assert estimate.num_y_bins() == 2  # 3 edges = 2 bins
    assert estimate.num_bins() == 6  # 3 x 2 = 6 bins

    # Check that all values are parsed correctly
    values = estimate.values()
    expected = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    for val, exp in zip(values, expected):
        assert abs(val - exp) < 1e-6


def test_grogu_estimate2d_v3_alice_real_data():
    """Test parsing of real ALICE experimental data."""
    # Real ALICE data with complex structure (truncated for testing)
    alice_data = """BEGIN YODA_ESTIMATE2D_V3 /ALICE_2020_I1797621/QGPdfXQ
Path: /ALICE_2020_I1797621/QGPdfXQ
ScaledBy: 1.00000000000000000e+00
Title:
Type: Estimate2D
---
Edges(A1): [1.000000e-06, 1.737801e-06, 3.019952e-06, 5.248075e-06, 9.120108e-06, 1.584893e-05, 2.754229e-05, 4.786301e-05, 8.317638e-05, 1.445440e-04, 2.511886e-04, 4.365158e-04, 7.585776e-04, 1.318257e-03, 2.290868e-03, 3.981072e-03, 6.918310e-03, 1.202264e-02, 2.089296e-02, 3.630781e-02, 6.309573e-02, 1.096478e-01, 1.905461e-01, 3.311311e-01, 5.754399e-01, 1.000000e+00]
Edges(A2): [0.000000e+00, 1.200000e+00, 2.400000e+00, 3.600000e+00, 4.800000e+00, 6.000000e+00, 7.200000e+00, 8.400000e+00, 9.600000e+00, 1.080000e+01, 1.200000e+01, 1.320000e+01, 1.440000e+01, 1.560000e+01, 1.680000e+01, 1.800000e+01, 1.920000e+01, 2.040000e+01, 2.160000e+01, 2.280000e+01, 2.400000e+01, 2.520000e+01, 2.640000e+01, 2.760000e+01, 2.880000e+01, 3.000000e+01]
ErrorLabels: ["stats"]
# value      	errDn(1)     	errUp(1)
nan          	---          	---
2.559224e+05 	-1.162043e+04	1.162043e+04
8.410882e+05 	-1.549672e+04	1.549672e+04
4.479346e+05 	-8.078740e+03	8.078740e+03
1.586730e+05 	-3.976580e+03	3.976580e+03
1.855366e+02 	-4.963814e+01	4.963814e+01
6.614561e+03 	-2.031409e+03	2.031409e+03
2.107288e+06 	-2.579696e+04	2.579696e+04
5.290625e+06 	-3.211873e+04	3.211873e+04
0.000000e+00 	---          	---
END YODA_ESTIMATE2D_V3"""

    estimate = GROGU_ESTIMATE2D_V3.from_string(alice_data)

    # Test basic structure
    assert estimate.d_key == "/ALICE_2020_I1797621/QGPdfXQ"
    assert estimate.type() == "Estimate2D"
    assert estimate.error_labels() == ["stats"]
    assert estimate.annotation("ScaledBy") == "1.00000000000000000e+00"

    # Test dimensions - should have 25x25 potential bins but only 10 data lines in our sample
    assert estimate.num_x_bins() == 25  # 26 edges = 25 bins
    assert estimate.num_y_bins() == 25  # 26 edges = 25 bins
    assert estimate.num_bins() == 10  # Only 10 data lines in our truncated sample

    # Test edge parsing
    x_edges = estimate.xEdges()
    y_edges = estimate.yEdges()
    assert len(x_edges) == 26
    assert len(y_edges) == 26
    assert x_edges[0] == 1.000000e-06
    assert x_edges[-1] == 1.000000e00
    assert y_edges[0] == 0.0
    assert y_edges[-1] == 30.0

    # Test specific values from the data
    values = estimate.values()

    # First bin should be NaN
    assert math.isnan(values[0])

    # Check some specific non-zero values
    assert abs(values[1] - 2.559224e05) < 1e-1
    assert abs(values[2] - 8.410882e05) < 1e-1
    assert abs(values[3] - 4.479346e05) < 1e-1

    # Last value should be 0.0
    assert values[-1] == 0.0

    # Test error values for non-NaN bins
    errors_dn = estimate.errors_dn(0)
    errors_up = estimate.errors_up(0)

    # Second bin errors
    assert abs(errors_dn[1] - (-1.162043e04)) < 1e-1
    assert abs(errors_up[1] - 1.162043e04) < 1e-1

    # Test NaN handling
    assert math.isnan(errors_dn[0])  # First bin should have NaN errors
    assert math.isnan(errors_up[0])

    # Test zero value handling (last bin)
    assert math.isnan(errors_dn[-1])  # Zero values have "---" errors
    assert math.isnan(errors_up[-1])


def test_grogu_estimate2d_v3_minimal_input():
    """Test minimal valid input."""
    minimal_data = """BEGIN YODA_ESTIMATE2D_V3 /test
Path: /test
Type: Estimate2D
---
Edges(A1): [0.0, 1.0]
Edges(A2): [0.0, 1.0]
ErrorLabels: ["stats"]
# value	errDn(1)	errUp(1)
1.0	0.1	0.1
END YODA_ESTIMATE2D_V3"""

    estimate = GROGU_ESTIMATE2D_V3.from_string(minimal_data)
    assert estimate.d_key == "/test"
    assert estimate.num_bins() == 1
    assert estimate.num_x_bins() == 1
    assert estimate.num_y_bins() == 1
    assert estimate.values()[0] == 1.0
