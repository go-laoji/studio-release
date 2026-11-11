# Trace Studio

拓睿思是一个可自托管的浏览器自动化工作台，支持录制网页操作、可视化编排工作流，以及运行和调试流程。

[项目站点（sub.scrm.sale）](https://sub.scrm.sale/)

本仓库是项目的对外介绍入口。后续版本通过 Docker Hub 分发，GitHub Releases 停止发布新的安装包。

## Docker 镜像

镜像计划发布到 Docker Hub，名称为 `golaoji/trace-studio-server`。镜像发布后，可拉取 `golaoji/trace-studio-server:latest`，也可将下方命令中的 `latest` 换成同一个已发布的版本标签。

[Docker Hub 镜像标签](https://hub.docker.com/r/golaoji/trace-studio-server/tags)

## 启动

下面的命令适用于 `linux/amd64` 镜像。ARM64 主机需要在 Docker 中启用 x86-64 模拟。镜像已包含 Web 工作台、工作流运行所需的 Node.js 和浏览器。

```sh
docker pull --platform linux/amd64 golaoji/trace-studio-server:latest

docker run -d --name trace-studio-server \
  --platform linux/amd64 \
  --restart unless-stopped \
  -p 127.0.0.1:9223:8080 \
  -v trace-studio-data:/var/lib/moli-studio \
  -v trace-studio-ocr:/home/node/.oar/models/ppocr-v6-small \
  golaoji/trace-studio-server:latest
```

启动后，在 Docker 宿主机的浏览器打开 `http://127.0.0.1:9223`。可用 `curl -fsS http://127.0.0.1:9223/api/health` 检查服务状态，或用 `docker logs --tail 100 trace-studio-server` 查看启动日志。

## 运行注意事项

- **端口与访问**。示例将服务绑定到宿主机的 `127.0.0.1`。远程部署时可通过 SSH 本地端口转发访问。如果宿主机的 `9223` 已被占用，需同时修改宿主机端口和 `MOLI_STUDIO_PORT`，例如改用 `-e MOLI_STUDIO_PORT=19223 -p 127.0.0.1:19223:8080`。容器的 `8080` 留给转发，`MOLI_STUDIO_PORT` 需使用其他端口。
- **数据与目录权限**。`trace-studio-data` 保存工作流、运行记录和本地配置。`trace-studio-ocr` 缓存 OCR 模型。使用宿主机目录替代命名卷时，确保容器用户 `1000:1000` 对挂载目录有写权限。
- **联网与 OCR**。登录和订阅授权需要容器能通过 HTTPS 访问项目站点。首次使用 OCR 时，容器需要联网下载并校验模型，后续可复用模型卷。
- **更新**。先备份数据卷并拉取目标标签，再停止并移除旧容器，使用相同的端口和卷启动新容器。
