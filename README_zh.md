<div align="center">

# 🔮 aiobloom_live

**一个现代、高效、支持异步操作的 Python 布隆过滤器库**

</div>

<p align="center">
  <a href="https://pypi.org/project/aiobloom_live/"><img src="https://img.shields.io/pypi/v/aiobloom_live?color=blue&label=PyPI" alt="PyPI"></a>
  <a href="https://github.com/asxez/aiobloom_live/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/aiobloom_live?color=green" alt="License"></a>
  <a href="#"><img src="https://img.shields.io/pypi/pyversions/aiobloom_live" alt="Python Version"></a>
</p>

---

`aiobloom` 是一个功能强大的布隆过滤器库，它在 `pybloom_live` 的基础上进行了异步改造，全面拥抱 `async/await` 语法，为高并发 I/O 场景提供了卓越的性能。

无论您是处理海量数据流、构建网络爬虫，还是需要一个高效的缓存未命中检测器，`aiobloom_live` 都能提供兼具优雅 API 和极致性能的解决方案。

## ✨ 核心特性

*   **🚀 极致的异步性能**: 基于 `aiofiles` 实现异步文件读写，在并发场景下 I/O 性能数倍于同步操作。
*   **🧩 两种过滤器模式**:
    *   `BloomFilter`: 经典的固定大小布隆过滤器。
    *   `ScalableBloomFilter`: 可根据元素数量自动扩容，无需预估容量。
*   **🕰️ 向后兼容**: 保留了与 `pybloom_live` 完全兼容的同步 API (`tofile`, `fromfile`)，确保老用户可以无缝迁移。
*   **🔧 序列化支持**: 支持将过滤器序列化为 `bytes`，方便在网络或内存中传输。

## 📊 性能基准测试

`aiobloom_live` 的核心优势在于其异步 I/O 的性能。以下是对一个包含 **10,000,000** 个元素，错误率为0.000001的过滤器进行 **16** 次并发读写操作的测试结果：

| 操作 (16 次并发) | 同步 (Sync) | **异步 (Async)** | **性能提升**    |
| :----------------- | :---------- | :----------------- |:------------|
| **文件写入**       | `0.3086s`   | `0.2840s`          | **`1.09×`** |
| **文件读取**       | `2.0815s`   | `0.4776s`          | **`4.36×`** |

**结论**: 在并发 I/O 密集型任务中，`aiobloom_live` 的异步模型展现出了巨大的性能优势，读取速度提升近 **4.5倍**！

## 🚀 快速开始

### 安装

```bash
pip install aiobloom_live
```

### `BloomFilter` 示例

```python
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
```

### `ScalableBloomFilter` 示例

```python
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
```

## API 参考

### `BloomFilter(capacity, error_rate)`
*   `add(key)` / `__contains__(key)[in operator]`: 添加和检查元素。
*   `tofile_async(path)` / `fromfile_async(path)`: **异步**读写文件。
*   `tofile(file_obj)` / `fromfile(file_obj)`: 同步读写文件 (兼容 `pybloom_live`)。
*   `to_bytes()` / `from_bytes(data)`: 序列化与反序列化。

### `ScalableBloomFilter(initial_capacity, error_rate)`
*   功能与 `BloomFilter` 类似，但容量可自动扩展。
*   `capacity`: (属性) 获取当前总容量。

## 🤝 如何贡献

我们热烈欢迎各种形式的贡献！无论是提交 Issue、发起 Pull Request，还是改进文档，都是对社区的巨大帮助。

1.  **Fork** 本仓库
2.  创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3.  提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4.  推送到分支 (`git push origin feature/AmazingFeature`)
5.  **发起 Pull Request**

## 📄 许可证

本项目基于 [MIT](LICENSE) 许可证开源。
