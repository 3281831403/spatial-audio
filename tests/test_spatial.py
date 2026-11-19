import pytest

from audio import spatial as mod

CASES = [
    ('pan_gain', [0.0], [1.0, 0.0], True),
    ('pan_gain', [1.5707963267948966], [6.123233995736766e-17, 1.0], True),
    ('distance_gain', [10, 1, 100], 0.1, True),
    ('occlusion_cutoff', [8000, 0.5], 6000.0, True),
    ('reverb_blend', [0.8, 0.5], 0.4, True),
    ('doppler_pitch', [0, 0, 343], 1.0, True),
    ('channel_count', ['5.1'], 6, False),
    ('channel_count', ['unknown'], 2, False),
    ('latency_compensation', [343, 343], 1.0, True),
    ('headroom_gain', [2.0, 1.0], 0.5, True),
    ('headroom_gain', [0.5, 1.0], 1.0, True),
    ('hrtf_interp', [[0.0, 0.0], [1.0, 1.0], 0.5], [0.5, 0.5], True),
    ('commit_mix', [[True, True]], True, False),
    ('distance_gain', [0.5, 1.0, 100], 1.0, True),
    ('reverb_blend', [1.0, 1.5], 1.0, True),
]


@pytest.mark.parametrize("func_name,args,expected,approx", CASES)
def test_spatial_contract(func_name, args, expected, approx):
    func = getattr(mod, func_name)
    result = func(*args)
    if approx:
        assert result == pytest.approx(expected)
    else:
        assert result == expected
