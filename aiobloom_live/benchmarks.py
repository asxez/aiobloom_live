"""


origin author: https://github.com/joseph-fox
author: ASXE  https://github.com/asxez



Benchmark synchronous vs asynchronous (aiofiles-powered) I/O for
BloomFilter / ScalableBloomFilter.

The *compute* part of Bloom filters (add/contains) is identical between the
sync & async versions.  The only difference lies in serialization to disk.
Hence we focus on measuring:

1.  Single write (``tofile`` vs ``tofile_async``)
2.  Single read  (``fromfile`` vs ``fromfile_async``)
3.  N-way concurrent writes/reads to showcase async scalability

Run with:

    python Dromeda/utils/pybloom_live/benchmarks.py \
        --capacity 200_000 --iterations 5


------------------------- test results --------------------------
test results:
Building filter with capacity=10000000, error_rate=0.001 …

=======  Results  =======
Single write:  sync=  0.0080s   async=  0.0078s
Single read:   sync=  0.0566s   async=  0.0178s
16× concurrent writes: sync=  0.1386s   async=  0.0527s
16× concurrent reads:  sync=  0.9110s   async=  0.2411s

Speed-ups (sync/async):
  Single write : 1.02×
  Single read  : 3.17×
  Concur write : 2.63×
  Concur read  : 3.78×

"""

from __future__ import annotations

import argparse
import asyncio
import shutil
import tempfile
import time
from pathlib import Path
from typing import List, Tuple

from aiobloom_live import ScalableBloomFilter


def build_filter(capacity: int, error_rate: float) -> ScalableBloomFilter:
    """Populate a `ScalableBloomFilter` with *capacity* integer keys."""
    sbf = ScalableBloomFilter(initial_capacity=capacity, error_rate=error_rate)
    for i in range(capacity):
        sbf.add(i)
    return sbf


def time_sync_write(sbf: ScalableBloomFilter, path: Path) -> float:
    start = time.perf_counter()
    with open(path, "wb") as f:
        sbf.tofile(f)
    return time.perf_counter() - start


def time_sync_read(path: Path) -> Tuple[float, ScalableBloomFilter]:
    start = time.perf_counter()
    with open(path, "rb") as f:
        obj = ScalableBloomFilter.fromfile(f)
    return time.perf_counter() - start, obj


async def time_async_write(sbf: ScalableBloomFilter, path: Path) -> float:
    start = time.perf_counter()
    await sbf.tofile_async(str(path))
    return time.perf_counter() - start


async def time_async_read(path: Path) -> Tuple[float, ScalableBloomFilter]:
    start = time.perf_counter()
    obj = await ScalableBloomFilter.fromfile_async(str(path))  # type: ignore[attr-defined]
    return time.perf_counter() - start, obj


# ---------------------------------------------------------------------------
# Concurrent
# ---------------------------------------------------------------------------

def run_sync_many(fn, paths: List[Path]):
    """Execute *fn* sequentially over *paths* (blocking)."""
    start = time.perf_counter()
    results = [fn(p) for p in paths]
    duration = time.perf_counter() - start
    return duration, results


async def run_async_many(coro_factory, paths: List[Path]):
    """Launch *len(paths)* coroutines concurrently and wait for completion."""
    start = time.perf_counter()
    results = await asyncio.gather(*(coro_factory(p) for p in paths))
    duration = time.perf_counter() - start
    return duration, results


# ---------------------------------------------------------------------------
# Benchmark orchestrator
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Bloom filter I/O benchmark")
    parser.add_argument("--capacity", type=int, default=10000000,
                        help="Number of elements to insert into the filter")
    parser.add_argument("--error-rate", type=float, default=1e-6,
                        help="Target false-positive rate")
    parser.add_argument("--iterations", type=int, default=16,
                        help="Number of concurrent read/write operations to test")
    args = parser.parse_args()

    tmp_dir = Path(tempfile.mkdtemp(prefix="bloom_bench_"))
    try:
        print(f"Building filter with capacity={args.capacity}, error_rate={args.error_rate} …")
        sbf = build_filter(args.capacity, args.error_rate)

        sync_path = tmp_dir / "filter_sync.bin"
        async_path = tmp_dir / "filter_async.bin"

        # -------------------- single write --------------------
        t_sync_write = time_sync_write(sbf, sync_path)
        t_async_write = asyncio.run(time_async_write(sbf, async_path))

        # -------------------- single read ---------------------
        t_sync_read, _ = time_sync_read(sync_path)
        t_async_read, _ = asyncio.run(time_async_read(async_path))

        # ----- concurrent writes -----
        paths_async = [tmp_dir / f"async_{i}.bin" for i in range(args.iterations)]
        # Ensure no leftover files
        for p in paths_async:
            if p.exists():
                p.unlink()

        dur_sync_many, _ = run_sync_many(lambda p: time_sync_write(sbf, p), paths_async)
        dur_async_many, _ = asyncio.run(run_async_many(lambda p: time_async_write(sbf, p), paths_async))

        # ---------------- concurrent reads -------------------
        # prepare identical files via sync write to all path sets
        for p in paths_async:
            time_sync_write(sbf, p)

        dur_sync_read_many, _ = run_sync_many(lambda p: time_sync_read(p), paths_async)
        dur_async_read_many, _ = asyncio.run(run_async_many(lambda p: time_async_read(p), paths_async))

        # -------------------- reporting ----------------------
        print("\n=======  Results  =======")
        print(f"Single write:  sync={t_sync_write:8.4f}s   async={t_async_write:8.4f}s")
        print(f"Single read:   sync={t_sync_read:8.4f}s   async={t_async_read:8.4f}s")
        print(f"{args.iterations}× concurrent writes: sync={dur_sync_many:8.4f}s   async={dur_async_many:8.4f}s")
        print(
            f"{args.iterations}× concurrent reads:  sync={dur_sync_read_many:8.4f}s   async={dur_async_read_many:8.4f}s")

        def ratio(a, b):
            return a / b if b else float('inf')

        print("\nSpeed-ups (sync/async):")
        print("  Single write : {:.2f}×".format(ratio(t_sync_write, t_async_write)))
        print("  Single read  : {:.2f}×".format(ratio(t_sync_read, t_async_read)))
        print("  Concur write : {:.2f}×".format(ratio(dur_sync_many, dur_async_many)))
        print("  Concur read  : {:.2f}×".format(ratio(dur_sync_read_many, dur_async_read_many)))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
