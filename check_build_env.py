#!/usr/bin/env python3
"""
编译环境诊断脚本
检查 never_jscore 编译所需的所有依赖
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

def run_command(cmd, check=False):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        if check and result.returncode != 0:
            return None
        return result.stdout.strip()
    except Exception as e:
        return None

def check_item(name, cmd, expected=None):
    """检查单个工具"""
    print(f"检查 {name}...", end=" ")
    result = run_command(cmd)

    if result:
        version = result.split('\n')[0]
        print(f"✅ {version}")
        return True
    else:
        print(f"❌ 未找到")
        if expected:
            print(f"   建议: {expected}")
        return False

def main():
    print("=" * 60)
    print("never_jscore 编译环境诊断")
    print("=" * 60)
    print(f"平台: {platform.system()} {platform.machine()}")
    print(f"Python: {sys.version}")
    print("=" * 60)
    print()

    all_ok = True

    # 基础工具
    print("【基础工具】")
    all_ok &= check_item("Python", "python --version")
    all_ok &= check_item("pip", "pip --version")
    all_ok &= check_item("Rust", "rustc --version", "安装: https://rustup.rs/")
    all_ok &= check_item("Cargo", "cargo --version", "安装: https://rustup.rs/")
    all_ok &= check_item("maturin", "maturin --version", "安装: pip install maturin")
    print()

    # C/C++ 编译器
    print("【C/C++ 编译器】")
    system = platform.system()

    if system == "Windows":
        all_ok &= check_item("MSVC (cl.exe)", "cl.exe 2>&1",
                           "安装 Visual Studio Build Tools")
        all_ok &= check_item("link.exe", "link.exe /? 2>&1")
    elif system == "Darwin":  # macOS
        all_ok &= check_item("clang", "clang --version",
                           "安装: xcode-select --install")
        all_ok &= check_item("clang++", "clang++ --version")
    else:  # Linux
        gcc_ok = check_item("gcc", "gcc --version",
                          "安装: sudo apt install build-essential (Ubuntu)")
        gpp_ok = check_item("g++", "g++ --version")
        all_ok &= (gcc_ok and gpp_ok)
    print()

    # 构建工具
    print("【构建工具】")
    all_ok &= check_item("make", "make --version",
                        "Linux: sudo apt install make")
    all_ok &= check_item("cmake", "cmake --version",
                        "Linux: sudo apt install cmake")
    print()

    # Python 开发文件
    print("【Python 开发文件】")
    import sysconfig
    include_path = sysconfig.get_path('include')
    python_h = Path(include_path) / "Python.h"

    print(f"检查 Python.h...", end=" ")
    if python_h.exists():
        print(f"✅ {python_h}")
    else:
        print(f"❌ 未找到")
        if system == "Linux":
            print(f"   建议: sudo apt install python3-dev (Ubuntu)")
        all_ok = False
    print()

    # 系统库
    if system == "Linux":
        print("【系统库 (Linux)】")
        check_item("pkg-config", "pkg-config --version",
                  "安装: sudo apt install pkg-config")

        # 检查关键库
        libs = [
            ("libffi", "pkg-config --modversion libffi",
             "sudo apt install libffi-dev"),
            ("openssl", "pkg-config --modversion openssl",
             "sudo apt install libssl-dev")
        ]

        for name, cmd, install_cmd in libs:
            check_item(name, cmd, install_cmd)
        print()

    # 环境变量检查
    print("【环境变量】")

    env_vars = {
        "V8_FROM_SOURCE": "0 (推荐使用预编译 V8)",
        "RUSTC_WRAPPER": "sccache (可选，加速编译)",
    }

    for var, desc in env_vars.items():
        value = os.environ.get(var)
        print(f"{var}:", end=" ")
        if value:
            print(f"✅ {value}")
        else:
            print(f"⚠️  未设置 - {desc}")
    print()

    # 磁盘空间检查
    print("【磁盘空间】")
    try:
        import shutil
        total, used, free = shutil.disk_usage(os.getcwd())
        free_gb = free // (2**30)
        print(f"可用空间: {free_gb} GB", end=" ")
        if free_gb < 5:
            print("⚠️  空间不足，建议至少 5GB")
            all_ok = False
        else:
            print("✅")
    except Exception as e:
        print(f"❌ 无法检查: {e}")
    print()

    # 测试编译
    print("【测试编译】")
    print("尝试编译一个简单的 Rust 项目...")

    test_code = '''
fn main() {
    println!("Hello from Rust!");
}
'''

    test_dir = Path("./test_rust_compile")
    try:
        test_dir.mkdir(exist_ok=True)
        (test_dir / "main.rs").write_text(test_code)

        result = run_command(f"rustc {test_dir}/main.rs -o {test_dir}/test_exe")
        if (test_dir / ("test_exe.exe" if system == "Windows" else "test_exe")).exists():
            print("✅ Rust 编译测试通过")
        else:
            print("❌ Rust 编译失败")
            all_ok = False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        all_ok = False
    finally:
        # 清理
        import shutil
        if test_dir.exists():
            shutil.rmtree(test_dir, ignore_errors=True)
    print()

    # 总结
    print("=" * 60)
    if all_ok:
        print("✅ 所有检查通过！可以开始编译 never_jscore")
        print()
        print("下一步:")
        print("1. export V8_FROM_SOURCE=0  # (Linux/macOS)")
        print("   set V8_FROM_SOURCE=0     # (Windows)")
        print("2. maturin develop --release")
    else:
        print("❌ 发现问题，请根据上述建议安装缺失的依赖")
        print()
        print("快速修复 (根据你的系统):")
        print()
        print("Ubuntu/Debian:")
        print("  sudo apt update")
        print("  sudo apt install build-essential cmake python3-dev \\")
        print("                   libffi-dev libssl-dev pkg-config")
        print()
        print("macOS:")
        print("  xcode-select --install")
        print("  brew install cmake pkg-config")
        print()
        print("Windows:")
        print("  下载并安装 Visual Studio Build Tools:")
        print("  https://visualstudio.microsoft.com/downloads/")
        print("  勾选 'C++ 生成工具' 和 'Windows SDK'")
    print("=" * 60)

    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
