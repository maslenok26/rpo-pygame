from copy import deepcopy

LEAF_KEYS = {'general', 'physics', 'render', 'components'}

def config(stats):
    if _is_leaf(stats):
        raise ValueError('Конфиг не должен быть одиночным листом')
    _merge(stats)
    return stats

def _merge(stats: dict[str, dict], defaults: dict[str, dict]=None):
    cur_defaults = deepcopy(defaults) if defaults else {}
    _save_default(cur_defaults, stats)
    for key, child in stats.items():
        if _is_leaf(child):
            leaf_stats = deepcopy(cur_defaults)
            _deep_update(leaf_stats, child)
            stats[key] = leaf_stats
        else:
            _merge(child, cur_defaults)

def _save_default(defaults, stats: dict[str, dict]):
    if 'default' not in stats: return
    _deep_update(defaults, stats['default'])
    stats.pop('default')

def _is_leaf(stats: dict[str, dict]):
    return stats.keys() & LEAF_KEYS

def _deep_update(target, source: dict[str, dict]):
    for key, source_child in source.items():
        if isinstance(source_child, dict) and key in target:
            _deep_update(target[key], source_child)
        else:
            target[key] = source_child