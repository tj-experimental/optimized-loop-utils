import enum
import collections

# class ArrayType(enum.Enum):
#     ONE = 0  # 1D
#     TWO = 1  # 2D 
#     THREE = 2 # 3D
#     FOUR = 3 # 4D

#     [ # 2 * 2
#         2, 3,
#         1, 3, 
#     ]
    
#     [ # 3 * 3
#         2, 3, 4,
#         1, 3, 4,
#         3, 4, 5 
#     ]

class SplitType(int, enum.Enum):
    NONE = 0
    HALF = 1
    THREE = 2
    AUTO = 3

def _apply_func_to_items(
    executor,
    func,
    items,
    func_args=(),
    size_func=len,
    flatten=False,
    split_type=SplitType.HALF,
    max_workers=4 # This should use the CPU count.
):
    with executor(max_workers=max_workers) as exe:
        # Handle chunks.
        total = size_func(items)
        
        chunk_count = int(total / split_type)
        
        chunks = range(0, total, chunk_count)
        
        chunk_max = max(chunks)
        
        has_more = chunk_max < total

        jobs = []

        for i in chunks:
            start = i
            end = i + chunk_count

            jobs.append(exe.submit(func, *func_args, items[start:end]))
        
        if has_more:
            # By how much just slice start from the last split.
            jobs.append(
                exe.submit(
                    func,
                    *func_args,
                    items[chunk_max:total],
                ),
            )
        # Flatten the results
        # TODO: Why is this returning duplicate records ? (
        # Shouldn't need to use set here)
        results = set()

        for item in [job.result() for job in jobs]:
            if isinstance(item, collections.Iterable) and flatten:
                results |= set([i for i in item])
            else:
                results.add(item)

        return results


def _apply_func_to_items_for_each_parent(
    executor,
    func,
    parents,
    items,
    func_args=(),
    size_func=len,
    split_type=SplitType.HALF,
    max_workers=4 # This should use the CPU count.
):
    with executor(max_workers=max_workers) as exe:
        # Handle chunks.
        total = size_func(items)
        
        chunk_count = int(total / split_type)
        
        chunks = range(0, total, chunk_count)
        
        chunk_max = max(chunks)
        
        has_more = chunk_max < total

        jobs = []

        for parent in parents:
            for i in chunks:
                start = i
                end = i + chunk_count

                jobs.append(exe.submit(func, *func_args, parent, items[start:end]))
            
            if has_more:
                # By how much just slice start from the last split.
                jobs.append(
                    exe.submit(
                        func,
                        *func_args,
                        parent,
                        items[chunk_max:total],
                    ),
                )
        # Flatten the results
        # TODO: Why is this returning duplicate records ? (
        # Shouldn't need to use set here)
        results = set()

        for item in [job.result() for job in jobs]:
            if isinstance(item, collections.Iterable) and flatten:
                results |= set([i for i in item])
            else:
                results.add(item)

        return results