"""空间音频：声像、距离与混音余量的核心实现。"""

import math

# 已知声道布局到通道数的映射，未知布局统一回落为立体声。
_LAYOUT_CHANNELS = {
    "mono": 1,
    "1.0": 1,
    "stereo": 2,
    "2.0": 2,
    "2.1": 3,
    "3.0": 3,
    "5.0": 5,
    "5.1": 6,
    "7.1": 8,
    "7.1.4": 12,
    "9.1.6": 16,
}

# 多普勒允许的最大径向速度比例，避免分母趋零导致音高发散。
_DOPPLER_LIMIT = 0.99


def pan_gain(angle):
    """等功率声像左右增益。

    左声道为 ``cos(angle)``、右声道为 ``sin(angle)``，任意角度下
    ``left**2 + right**2 == 1``，转身时总功率保持恒定，不会忽大忽小。
    """
    return [math.cos(angle), math.sin(angle)]


def distance_gain(distance, reference, max_distance):
    """距离衰减以参考距离为基准。

    增益为 ``reference / distance``：参考距离处为 1（0 dB），更远按反比
    衰减，比参考距离近时钳制为 1，不再继续放大。距离先钳制到
    ``max_distance``，保证衰减存在下限，也避免远距离增益塌陷到零。
    """
    if reference <= 0.0:
        return 1.0
    d = min(max(distance, 0.0), max_distance)
    if d <= 0.0:
        return 1.0
    return min(1.0, reference / d)


def occlusion_cutoff(base_cutoff, occlusion):
    """遮挡越强高频截止越低。

    遮挡系数先钳制到 ``[0, 1]``，截止频率按
    ``base_cutoff * (1 - occlusion / 2)`` 线性下移：无遮挡保持原截止，
    完全遮挡时截止减半，优先损失高频细节。
    """
    o = min(max(occlusion, 0.0), 1.0)
    return max(0.0, base_cutoff * (1.0 - 0.5 * o))


def reverb_blend(wet, zone):
    """混响湿度按区域权重混合。

    结果为 ``wet * zone`` 并钳制到 ``[0, 1]``：跨混响区时随区域权重
    连续变化，权重再大也不会产生硬切突变。
    """
    return min(max(wet * zone, 0.0), 1.0)


def doppler_pitch(source_velocity, listener_velocity, sound_speed):
    """多普勒频移并避免除零。

    采用经典形式 ``c / (c + v_rel)``，其中 ``v_rel`` 为声源相对听者的
    径向速度（远离为正，音高降低；接近为负，音高升高）。相对速度钳制
    在正负 ``0.99 * sound_speed`` 内，杜绝超音速导致的零分母与负音高；
    声速非正时直接返回 1.0。
    """
    if sound_speed <= 0.0:
        return 1.0
    relative = source_velocity - listener_velocity
    limit = _DOPPLER_LIMIT * sound_speed
    relative = min(max(relative, -limit), limit)
    return sound_speed / (sound_speed + relative)


def channel_count(layout):
    """声道布局映射到通道数。

    查已知布局表（如 ``5.1 -> 6``）；无法识别的布局不抛错，统一回落
    为立体声 2 通道，保证下游缓冲尺寸始终有效。
    """
    return _LAYOUT_CHANNELS.get(layout, 2)


def latency_compensation(distance, sound_speed):
    """按距离补偿声音传播延迟。

    返回传播时间 ``distance / sound_speed``（秒），用于把近端与远端声源
    在时间轴上对齐。距离为负或声速非正属于无效输入，返回 0.0 而不是
    触发除零。
    """
    if sound_speed <= 0.0 or distance <= 0.0:
        return 0.0
    return distance / sound_speed


def headroom_gain(total, ceiling):
    """混音总和超上限时整体降低。

    总和未超过 ``ceiling``（或总和非正）时返回 1.0，保留原有混音；
    超出时返回 ``ceiling / total`` 统一拉低全部声道，为后续处理留出
    余量且不改变各声道之间的比例。
    """
    if total <= 0.0 or total <= ceiling:
        return 1.0
    return ceiling / total


def hrtf_interp(left, right, blend):
    """双耳 HRTF 按 blend 插值。

    ``blend`` 先钳制到 ``[0, 1]``，再对左右两组 HRTF 系数逐元素做
    线性插值 ``left + (right - left) * blend``，避免越界权重造成的
    插值跳变。
    """
    b = min(max(blend, 0.0), 1.0)
    return [l + (r - l) * b for l, r in zip(left, right)]


def commit_mix(results):
    """批量混音全部成功才提交。

    结果序列非空且每一项都为真时返回 ``True``（原子提交）；任一失败
    或没有任何可提交结果时返回 ``False``，杜绝只提交一半的半成品混音。
    """
    return len(results) > 0 and all(bool(item) for item in results)
