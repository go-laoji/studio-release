# Moli Studio Releases

这里提供 Moli Studio Server 与 Moli 的预编译安装包。

## 下载与启动

1. 打开 [Releases](https://github.com/go-laoji/studio-release/releases)，选择正式版本。
2. 从同一个版本下载系统和架构对应的归档以及 `SHA256SUMS`。
3. 核对归档的 SHA-256，再解压。将 `moli`、`moli-studio-server` 和随包运行库留在同一目录。Windows 的程序名带 `.exe`。

| 系统 | x86-64 | ARM64 |
| --- | --- | --- |
| Linux | `moli-x86_64-unknown-linux-gnu.tar.gz` | `moli-aarch64-unknown-linux-gnu.tar.gz` |
| macOS | `moli-x86_64-apple-darwin.tar.gz` | `moli-aarch64-apple-darwin.tar.gz` |
| Windows | `moli-x86_64-pc-windows-msvc.zip` | `moli-aarch64-pc-windows-msvc.zip` |

在 Linux 上运行 `sha256sum <归档文件>`，在 macOS 上运行
`shasum -a 256 <归档文件>`。在 Windows PowerShell 中运行
`Get-FileHash -Algorithm SHA256 <归档文件>`。将输出和
`SHA256SUMS` 中对应文件名的摘要比较。

在解压目录启动 `moli-studio-server` 后，打开
[本机 Studio](http://127.0.0.1:9223)。Windows 上可运行
`.\moli-studio-server.exe`。编译和执行工作流需要 Node.js 24+。
各平台依赖、工作区路径和服务启动参数见包内的 `STUDIO-DEPLOYMENT.md`。

## 更新

独立部署的 Studio Server 会检查这里的正式版本。可在
**设置 → 程序更新** 手动检查。升级前停止 Studio，沿用原数据目录，
并按归档内的部署指南操作。Moli 也可独立运行。
