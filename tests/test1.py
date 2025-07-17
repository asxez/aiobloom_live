# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 ASXE  All Rights Reserved 


import asyncio
from aiobloom_live import BloomFilter

async def main():
    # 创建过滤器
    bf = BloomFilter(capacity=1000, error_rate=0.001)

    # 添加元素
    bf.add("hello")
    bf.add("world")

    # 检查元素是否存在
    assert "hello" in bf
    assert "python" not in bf

    # 异步保存到文件
    await bf.tofile_async("bloom.bin")

    # 从文件异步加载
    bf2 = await BloomFilter.fromfile_async("bloom.bin")
    assert "hello" in bf2
    print("✅ BloomFilter 异步读写成功！")

if __name__ == "__main__":
    asyncio.run(main())
