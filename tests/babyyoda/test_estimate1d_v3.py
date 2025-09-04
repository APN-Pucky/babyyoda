import math

from babyyoda.grogu.estimate1d_v3 import GROGU_ESTIMATE1D_V3

# Sample data for testing estimate1d_v3 parsing
sample_data = """BEGIN YODA_ESTIMATE1D_V3 /MC_KROLL_WADA/m_ee
Path: /MC_KROLL_WADA/m_ee
ScaledBy: 4.73695254912828093e-09
Title:
Type: Estimate1D
---
Edges(A1): [0.000000e+00, 1.000000e-01, 2.000000e-01, 3.000000e-01, 4.000000e-01, 5.000000e-01, 6.000000e-01, 7.000000e-01, 8.000000e-01, 9.000000e-01, 1.000000e+00, 1.100000e+00, 1.200000e+00, 1.300000e+00, 1.400000e+00, 1.500000e+00, 1.600000e+00, 1.700000e+00, 1.800000e+00, 1.900000e+00, 2.000000e+00, 2.100000e+00, 2.200000e+00, 2.300000e+00, 2.400000e+00, 2.500000e+00, 2.600000e+00, 2.700000e+00, 2.800000e+00, 2.900000e+00, 3.000000e+00, 3.100000e+00, 3.200000e+00, 3.300000e+00, 3.400000e+00, 3.500000e+00, 3.600000e+00, 3.700000e+00, 3.800000e+00, 3.900000e+00, 4.000000e+00, 4.100000e+00, 4.200000e+00, 4.300000e+00, 4.400000e+00, 4.500000e+00, 4.600000e+00, 4.700000e+00, 4.800000e+00, 4.900000e+00, 5.000000e+00, 5.100000e+00, 5.200000e+00, 5.300000e+00, 5.400000e+00, 5.500000e+00, 5.600000e+00, 5.700000e+00, 5.800000e+00, 5.900000e+00, 6.000000e+00, 6.100000e+00, 6.200000e+00, 6.300000e+00, 6.400000e+00, 6.500000e+00, 6.600000e+00, 6.700000e+00, 6.800000e+00, 6.900000e+00, 7.000000e+00, 7.100000e+00, 7.200000e+00, 7.300000e+00, 7.400000e+00, 7.500000e+00, 7.600000e+00, 7.700000e+00, 7.800000e+00, 7.900000e+00, 8.000000e+00, 8.100000e+00, 8.200000e+00, 8.300000e+00, 8.400000e+00, 8.500000e+00, 8.600000e+00, 8.700000e+00, 8.800000e+00, 8.900000e+00, 9.000000e+00, 9.100000e+00, 9.200000e+00, 9.300000e+00, 9.400000e+00, 9.500000e+00, 9.600000e+00, 9.700000e+00, 9.800000e+00, 9.900000e+00, 1.000000e+01]
ErrorLabels: ["stats"]
# value      	errDn(1)     	errUp(1)
nan          	---          	---
3.032379e-03 	-2.274053e-06	2.274053e-06
4.691709e-04 	-5.128598e-07	5.128598e-07
2.678280e-04 	-3.480990e-07	3.480990e-07
1.818387e-04 	-2.690366e-07	2.690366e-07
1.338630e-04 	-2.214272e-07	2.214272e-07
1.027378e-04 	-1.879974e-07	1.879974e-07
8.087364e-05 	-1.628293e-07	1.628293e-07
6.457940e-05 	-1.429960e-07	1.429960e-07
5.274891e-05 	-1.271565e-07	1.271565e-07
4.324200e-05 	-1.136895e-07	1.136895e-07
3.607711e-05 	-1.028651e-07	1.028651e-07
3.003257e-05 	-9.296063e-08	9.296063e-08
2.517399e-05 	-8.439299e-08	8.439299e-08
2.154749e-05 	-7.768843e-08	7.768843e-08
1.826719e-05 	-7.097449e-08	7.097449e-08
1.566386e-05 	-6.547787e-08	6.547787e-08
1.350236e-05 	-6.049240e-08	6.049240e-08
1.158265e-05 	-5.586188e-08	5.586188e-08
9.922102e-06 	-5.148853e-08	5.148853e-08
8.668797e-06 	-4.803775e-08	4.803775e-08
7.688785e-06 	-4.508824e-08	4.508824e-08
6.825263e-06 	-4.236520e-08	4.236520e-08
6.021750e-06 	-3.969418e-08	3.969418e-08
5.379746e-06 	-3.742380e-08	3.742380e-08
4.672759e-06 	-3.485887e-08	3.485887e-08
4.095701e-06 	-3.262133e-08	3.262133e-08
3.632856e-06 	-3.066239e-08	3.066239e-08
3.227988e-06 	-2.886357e-08	2.886357e-08
2.839478e-06 	-2.701206e-08	2.701206e-08
2.569858e-06 	-2.565952e-08	2.565952e-08
2.275632e-06 	-2.413757e-08	2.413757e-08
2.058806e-06 	-2.299017e-08	2.299017e-08
1.865951e-06 	-2.181872e-08	2.181872e-08
1.647038e-06 	-2.045128e-08	2.045128e-08
1.503440e-06 	-1.956471e-08	1.956471e-08
1.335630e-06 	-1.836235e-08	1.836235e-08
1.231260e-06 	-1.767641e-08	1.767641e-08
1.106890e-06 	-1.672706e-08	1.672706e-08
1.002043e-06 	-1.586628e-08	1.586628e-08
9.096650e-07 	-1.515719e-08	1.515719e-08
8.350358e-07 	-1.446836e-08	1.446836e-08
7.538856e-07 	-1.373726e-08	1.373726e-08
7.029577e-07 	-1.326620e-08	1.326620e-08
6.426405e-07 	-1.267856e-08	1.267856e-08
5.449572e-07 	-1.164025e-08	1.164025e-08
5.287005e-07 	-1.145340e-08	1.145340e-08
4.888338e-07 	-1.101204e-08	1.101204e-08
4.438043e-07 	-1.051220e-08	1.051220e-08
3.987204e-07 	-9.941339e-09	9.941339e-09
3.790476e-07 	-9.680862e-09	9.680862e-09
3.333426e-07 	-9.068446e-09	9.068446e-09
3.086121e-07 	-8.727225e-09	8.727225e-09
3.033704e-07 	-8.662579e-09	8.662579e-09
2.685274e-07 	-8.149978e-09	8.149978e-09
2.389563e-07 	-7.675809e-09	7.675809e-09
2.289690e-07 	-7.511432e-09	7.511432e-09
2.025880e-07 	-7.079501e-09	7.079501e-09
1.825909e-07 	-6.701628e-09	6.701628e-09
1.784750e-07 	-6.596598e-09	6.596598e-09
1.590267e-07 	-6.242036e-09	6.242036e-09
1.468857e-07 	-5.987722e-09	5.987722e-09
1.400082e-07 	-5.846426e-09	5.846426e-09
1.260471e-07 	-5.557188e-09	5.557188e-09
1.101075e-07 	-5.190003e-09	5.190003e-09
1.005987e-07 	-4.955158e-09	4.955158e-09
9.918673e-08 	-4.899487e-09	4.899487e-09
1.018203e-07 	-4.977822e-09	4.977822e-09
8.334362e-08 	-4.494787e-09	4.494787e-09
8.883069e-08 	-4.645560e-09	4.645560e-09
7.688941e-08 	-4.318936e-09	4.318936e-09
6.661517e-08 	-4.044465e-09	4.044465e-09
6.175053e-08 	-3.882671e-09	3.882671e-09
5.995967e-08 	-3.802903e-09	3.802903e-09
5.435367e-08 	-3.627714e-09	3.627714e-09
5.757762e-08 	-3.729978e-09	3.729978e-09
4.565228e-08 	-3.325892e-09	3.325892e-09
4.287760e-08 	-3.218405e-09	3.218405e-09
4.097605e-08 	-3.158360e-09	3.158360e-09
3.643214e-08 	-2.957182e-09	2.957182e-09
3.385907e-08 	-2.853813e-09	2.853813e-09
3.185617e-08 	-2.765156e-09	2.765156e-09
3.085208e-08 	-2.717921e-09	2.717921e-09
2.676718e-08 	-2.542805e-09	2.542805e-09
3.250966e-08 	-2.802709e-09	2.802709e-09
2.701836e-08 	-2.543452e-09	2.543452e-09
2.676557e-08 	-2.530516e-09	2.530516e-09
2.034656e-08 	-2.209308e-09	2.209308e-09
1.930813e-08 	-2.145985e-09	2.145985e-09
1.603753e-08 	-1.960366e-09	1.960366e-09
1.935540e-08 	-2.151558e-09	2.151558e-09
1.639219e-08 	-1.974005e-09	1.974005e-09
1.481787e-08 	-1.882607e-09	1.882607e-09
1.468455e-08 	-1.864940e-09	1.864940e-09
1.359198e-08 	-1.800943e-09	1.800943e-09
9.523488e-09 	-1.506203e-09	1.506203e-09
1.189625e-08 	-1.682738e-09	1.682738e-09
9.041434e-09 	-1.467278e-09	1.467278e-09
9.029184e-09 	-1.465006e-09	1.465006e-09
1.044869e-08 	-1.575432e-09	1.575432e-09
8.340764e-09 	-1.410339e-09	1.410339e-09
nan          	---          	---
END YODA_ESTIMATE1D_V3"""


def test_grogu_estimate1d_v3_parsing():
    """Test parsing of YODA_ESTIMATE1D_V3 format."""
    # Parse the sample data
    estimate = GROGU_ESTIMATE1D_V3.from_string(sample_data)

    # Test basic properties
    assert estimate.d_key == "/MC_KROLL_WADA/m_ee"
    assert estimate.num_bins() == 102  # Should have 102 bins based on the sample data
    assert (
        estimate.num_edges() == 101
    )  # Should have 101 edges (0.0 to 10.0 in 0.1 increments)
    assert estimate.error_labels() == ["stats"]
    assert estimate.title() == ""
    assert estimate.type() == "Estimate1D"
    assert estimate.annotation("ScaledBy") == "4.73695254912828093e-09"


def test_grogu_estimate1d_v3_bin_data():
    """Test bin data parsing and access."""
    estimate = GROGU_ESTIMATE1D_V3.from_string(sample_data)

    # Test first bin (should be NaN)
    first_bin = estimate.d_bins[0]
    assert first_bin.has_nan()
    assert math.isnan(first_bin.value())

    # Test second bin (should have actual values)
    if estimate.num_bins() > 1:
        second_bin = estimate.d_bins[1]
        assert not second_bin.has_nan()
        assert abs(second_bin.value() - 3.032379e-03) < 1e-10
        assert len(second_bin.errors_dn()) == 1
        assert len(second_bin.errors_up()) == 1
        assert abs(second_bin.errors_dn()[0] - (-2.274053e-06)) < 1e-12
        assert abs(second_bin.errors_up()[0] - 2.274053e-06) < 1e-12


def test_grogu_estimate1d_v3_edges():
    """Test edge parsing."""
    estimate = GROGU_ESTIMATE1D_V3.from_string(sample_data)

    edges = estimate.xEdges()
    assert len(edges) == 101
    assert edges[0] == 0.0
    assert edges[1] == 0.1
    assert edges[2] == 0.2
    assert edges[-1] == 10.0


def test_grogu_estimate1d_v3_error_access():
    """Test error access methods."""
    estimate = GROGU_ESTIMATE1D_V3.from_string(sample_data)

    # Test errors_dn and errors_up methods
    errors_dn = estimate.errors_dn(0)  # First error source (stats)
    errors_up = estimate.errors_up(0)

    assert len(errors_dn) == estimate.num_bins()
    assert len(errors_up) == estimate.num_bins()

    # First bin should have NaN errors
    assert math.isnan(errors_dn[0])
    assert math.isnan(errors_up[0])

    # Second bin should have real error values
    if len(errors_dn) > 1:
        assert abs(errors_dn[1] - (-2.274053e-06)) < 1e-12
        assert abs(errors_up[1] - 2.274053e-06) < 1e-12


def test_grogu_estimate1d_v3_values():
    """Test values access method."""
    estimate = GROGU_ESTIMATE1D_V3.from_string(sample_data)

    values = estimate.values()
    assert len(values) == estimate.num_bins()

    # First value should be NaN
    assert math.isnan(values[0])

    # Second value should be the expected value
    if len(values) > 1:
        assert abs(values[1] - 3.032379e-03) < 1e-10


def test_grogu_estimate1d_v3_round_trip():
    """Test round-trip conversion (parse -> to_string -> parse again)."""
    estimate = GROGU_ESTIMATE1D_V3.from_string(sample_data)

    # Convert back to string
    reconstructed_string = estimate.to_string()

    # Parse the reconstructed string
    estimate2 = GROGU_ESTIMATE1D_V3.from_string(reconstructed_string)

    # Compare key properties
    assert estimate2.d_key == estimate.d_key
    assert estimate2.num_bins() == estimate.num_bins()
    assert estimate2.num_edges() == estimate.num_edges()
    assert estimate2.error_labels() == estimate.error_labels()
    assert estimate2.title() == estimate.title()
    assert estimate2.type() == estimate.type()

    # Compare values (handling NaN properly)
    values1 = estimate.values()
    values2 = estimate2.values()
    for v1, v2 in zip(values1, values2):
        if math.isnan(v1):
            assert math.isnan(v2)
        else:
            assert abs(v1 - v2) < 1e-10


def test_grogu_estimate1d_v3_empty_error_handling():
    """Test handling of malformed or empty input."""

    # Test minimal valid input
    minimal_data = """BEGIN YODA_ESTIMATE1D_V3 /test
Path: /test
Type: Estimate1D
---
Edges(A1): [0.0, 1.0]
ErrorLabels: ["stats"]
# value	errDn(1)	errUp(1)
1.0	0.1	0.1
END YODA_ESTIMATE1D_V3"""

    estimate = GROGU_ESTIMATE1D_V3.from_string(minimal_data)
    assert estimate.d_key == "/test"
    assert estimate.num_bins() == 1
    assert estimate.num_edges() == 2
