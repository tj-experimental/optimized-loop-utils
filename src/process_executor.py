from functools import partial
from concurrent.futures import ProcessPoolExecutor as Executor

from utils.base import (
    apply_func_to_items as base_apply_func_to_items,
    apply_func_to_items_for_each_parent as base_apply_func_to_items_for_each_parent,
)

apply_func_to_items = partial(base_apply_func_to_items, Executor)
apply_func_to_items_for_each_parent = partial(base_apply_func_to_items_for_each_parent, Executor)


__all__  = ['apply_func_to_items', 'apply_func_to_items_for_each_parent']