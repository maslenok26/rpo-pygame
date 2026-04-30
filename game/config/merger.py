from __future__ import annotations
from copy import deepcopy

from .constants import CfgKey, ASSET_PATH_SEP

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..types import StatsLeaf, TreeContent, MergedTree

LEAF_KEYS = set(CfgKey.Leaf)

class Tree(dict):
    def __init__(
            self, *,
            defaults: StatsLeaf | None=None, content: TreeContent
            ):
        if self._is_leaf(content):
            raise ValueError('Дерево конфигов не должно быть листом')
        super().__init__()
        self.defaults = defaults
        self.update(content)

    def merge_defaults(
            self, parent_defaults: StatsLeaf | None=None, asset_path=None
            ) -> MergedTree:
        if self.defaults is None:
            cur_defaults = parent_defaults
        elif parent_defaults is None:
            cur_defaults = self.defaults
        else:
            cur_defaults = deepcopy(parent_defaults)
            self._deep_update(cur_defaults, self.defaults)
        no_defaults = cur_defaults is None
        has_assets = asset_path is not None
        for key, value in self.items():
            cur_asset_path = (
                asset_path + ASSET_PATH_SEP + key
                if has_assets else None
            )
            value: StatsLeaf | Tree
            if self._is_leaf(value):
                if no_defaults:
                    new_leaf = value
                else:
                    new_leaf = deepcopy(cur_defaults)
                    self._deep_update(new_leaf, value)
                if has_assets:
                    if CfgKey.Leaf.RENDER not in new_leaf:
                        new_leaf['render'] = {}
                    new_leaf['render']['asset_path'] = cur_asset_path
                self[key] = new_leaf
            else:
                value.merge_defaults(cur_defaults, cur_asset_path)
        del self.defaults
        return self

    def _deep_update(self, target, source: StatsLeaf):
        for source_key, source_value in source.items():
            if isinstance(source_value, dict) and source_key in target:
                self._deep_update(target[source_key], source_value)
            else:
                target[source_key] = source_value

    def _is_leaf(self, stats: StatsLeaf | Tree):
        stats_keys = stats.keys()
        if not stats_keys & LEAF_KEYS:
            return False
        if not stats_keys - LEAF_KEYS:
            return True
        raise ValueError('Некорректное использование ключей листа')