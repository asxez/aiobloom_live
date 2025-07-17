<div align="center">

# 🔮 aiobloom_live

**A modern, high-performance, async-native Bloom filter library for Python**

</div>

<p align="center">
  <a href="https://pypi.org/project/aiobloom_live/"><img src="https://img.shields.io/pypi/v/aiobloom_live?color=blue&label=PyPI" alt="PyPI"></a>
  <a href="https://github.com/asxez/aiobloom_live/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/aiobloom_live?color=green" alt="License"></a>
  <a href="#"><img src="https://img.shields.io/pypi/pyversions/aiobloom_live" alt="Python Version"></a>
</p>

---

`aiobloom_live` is a powerful Bloom filter library built upon `pybloom_live`, fully embracing `async/await` syntax to deliver exceptional performance for high-concurrency I/O scenarios.

Whether you're processing massive data streams, building web crawlers, or in need of an efficient cache-miss detector, `aiobloom_live` provides a solution that combines an elegant API with ultimate performance.

## ✨ Core Features

*   **🚀 Blazing-Fast Async Performance**: Implements asynchronous file I/O using `aiofiles`, achieving several times the performance of synchronous operations in concurrent scenarios.
*   **🧩 Two Filter Modes**:
    *   `BloomFilter`: The classic fixed-size Bloom filter.
    *   `ScalableBloomFilter`: Automatically scales as the number of elements grows, no need to pre-estimate capacity.
*   **🕰️ Backward Compatible**: Retains a synchronous API (`tofile`, `fromfile`) fully compatible with `pybloom_live`, ensuring a seamless migration path for existing users.
*   **🔧 Serialization Support**: Supports serializing filters to `bytes` for easy transport over the network or in memory.

## 📊 Performance Benchmarks

The core advantage of `aiobloom_live` lies in its asynchronous I/O performance. Below are the results from a benchmark involving **16** concurrent read/write operations on a filter containing **10,000,000** elements with a 0.000001 error rate:

| Operation (16 concurrent) | Sync      | **Async** | **Performance Boost** |
| :------------------------ | :-------- | :-------- |:--------------------|
| **File Write**            | `0.3086s` | `0.2840s` | **`1.09×`**         |
| **File Read**             | `2.0815s` | `0.4776s` | **`4.36×`**         |

**Conclusion**: In concurrent I/O-intensive tasks, the asynchronous model of `aiobloom_live` demonstrates a significant performance advantage, with read speeds boosted by nearly **4.5x**!

## 🚀 Quick Start

### Installation

```bash
pip install aiobloom_live
```

### `BloomFilter` Example

```python
import asyncio
from aiobloom_live import BloomFilter

async def main():
    # Create a filter
    bf = BloomFilter(capacity=1000, error_rate=0.001)

    # Add elements
    bf.add("hello")
    bf.add("world")

    # Check for existence
    assert "hello" in bf
    assert "python" not in bf

    # Asynchronously save to a file
    await bf.tofile_async("bloom.bin")

    # Asynchronously load from a file
    bf2 = await BloomFilter.fromfile_async("bloom.bin")
    assert "hello" in bf2
    print("✅ BloomFilter async read/write successful!")

if __name__ == "__main__":
    asyncio.run(main())
```

### `ScalableBloomFilter` Example

```python
import asyncio
from aiobloom_live import ScalableBloomFilter

async def main():
    # Create a scalable filter without worrying about capacity
    sbf = ScalableBloomFilter(initial_capacity=100, error_rate=0.001)

    # Add a large number of elements, the filter will expand automatically
    for i in range(500):
        sbf.add(f"item_{i}")

    assert "item_499" in sbf
    assert "item_500" not in sbf
    
    # Async save and load
    await sbf.tofile_async("sbf.bin")
    sbf2 = await ScalableBloomFilter.fromfile_async("sbf.bin")
    assert "item_499" in sbf2
    print("✅ ScalableBloomFilter async read/write successful!")

if __name__ == "__main__":
    asyncio.run(main())
```

## API Reference

### `BloomFilter(capacity, error_rate)`
*   `add(key)` / `__contains__(key)[in operator]`: Add and check for an element.
*   `tofile_async(path)` / `fromfile_async(path)`: **Asynchronously** read from or write to a file.
*   `tofile(file_obj)` / `fromfile(file_obj)`: Synchronously read from or write to a file (compatible with `pybloom_live`).
*   `to_bytes()` / `from_bytes(data)`: Serialize and deserialize.

### `ScalableBloomFilter(initial_capacity, error_rate)`
*   Similar functionality to `BloomFilter`, but with an automatically expanding capacity.
*   `capacity`: (Property) Get the current total capacity.

## 🤝 How to Contribute

We warmly welcome contributions of all forms! Whether it's submitting issues, creating Pull Requests, or improving documentation, your help is greatly appreciated by the community.

1.  **Fork** this repository
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  **Open a Pull Request**

## 📄 License

This project is licensed under the [MIT](LICENSE) License. 
