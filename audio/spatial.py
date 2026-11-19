"""空间音频：声像、距离与混音余量：待实现的核心模块。"""


def pan_gain(angle):
    """等功率声像左右增益。"""
    raise NotImplementedError

def distance_gain(distance, reference, max_distance):
    """距离衰减以参考距离为基准。"""
    raise NotImplementedError

def occlusion_cutoff(base_cutoff, occlusion):
    """遮挡越强高频截止越低。"""
    raise NotImplementedError

def reverb_blend(wet, zone):
    """混响湿度按区域权重混合。"""
    raise NotImplementedError

def doppler_pitch(source_velocity, listener_velocity, sound_speed):
    """多普勒频移并避免除零。"""
    raise NotImplementedError

def channel_count(layout):
    """声道布局映射到通道数。"""
    raise NotImplementedError

def latency_compensation(distance, sound_speed):
    """按距离补偿声音传播延迟。"""
    raise NotImplementedError

def headroom_gain(total, ceiling):
    """混音总和超上限时整体降低。"""
    raise NotImplementedError

def hrtf_interp(left, right, blend):
    """双耳 HRTF 按 blend 插值。"""
    raise NotImplementedError

def commit_mix(results):
    """批量混音全部成功才提交。"""
    raise NotImplementedError
