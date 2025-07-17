# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 ASXE  All Rights Reserved 


import asyncio
from aiobloom_live import ScalableBloomFilter


async def main():
    # 创建一个可伸缩的过滤器，无需担心容量问题
    sbf = ScalableBloomFilter(initial_capacity=100, error_rate=0.001)

    # 添加大量元素，过滤器将自动扩容
    for i in range(500):
        sbf.add(f"item_{i}")

    assert "item_499" in sbf
    assert "item_500" not in sbf

    # 异步保存与加载
    await sbf.tofile_async("sbf.bin")
    sbf2 = await ScalableBloomFilter.fromfile_async("sbf.bin")
    assert "item_499" in sbf2
    print("✅ ScalableBloomFilter 异步读写成功！")


if __name__ == "__main__":
    asyncio.run(main())
