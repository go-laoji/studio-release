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

## Nginx 反向代理

Nginx 和 Docker 在同一台宿主机时，可以保留上面的本机端口映射，由 Nginx 对外提供 HTTPS。在前面的 `docker run` 命令中，将最后一行替换为下面两行，为容器内的服务启用 `--trust-proxy` 和 `--public-origin`。

```sh
  golaoji/trace-studio-server:latest \
  moli-studio-server --trust-proxy --public-origin https://studio.example.com
```

`--public-origin` 必须与浏览器实际访问的 HTTPS 源一致。填写 `https://`、域名和非默认端口（如有），末尾省略斜杠。

把下面的配置放进 `studio.example.com` 对应的 HTTPS `server` 块。如果修改了 Docker 的宿主机端口，同时更新 `proxy_pass`。

```nginx
location / {
    proxy_pass http://127.0.0.1:9223;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    proxy_buffering off;
    proxy_cache off;

    proxy_read_timeout 3600s;
}
```

使用非默认 HTTPS 端口时，将 Host 头改为 `proxy_set_header Host $http_host;`，以便 Studio 校验完整的主机名和端口。 启用代理后，通过配置的 HTTPS 域名访问工作台和 `/api/health`。

前端通过 SSE 接收实时数据。请同时设置 `proxy_buffering off;` 和 `proxy_cache off;`，让事件及时转发给浏览器，并关闭继承的代理缓存。

## 运行注意事项

- **端口与访问**。示例将服务绑定到宿主机的 `127.0.0.1`。远程部署时可通过 SSH 本地端口转发访问。如果宿主机的 `9223` 已被占用，需同时修改宿主机端口和 `MOLI_STUDIO_PORT`，例如改用 `-e MOLI_STUDIO_PORT=19223 -p 127.0.0.1:19223:8080`。容器的 `8080` 留给转发，`MOLI_STUDIO_PORT` 需使用其他端口。
- **数据与目录权限**。`trace-studio-data` 保存工作流、运行记录和本地配置。`trace-studio-ocr` 缓存 OCR 模型。使用宿主机目录替代命名卷时，确保容器用户 `1000:1000` 对挂载目录有写权限。
- **联网与 OCR**。登录和订阅授权需要容器能通过 HTTPS 访问项目站点。首次使用 OCR 时，容器需要联网下载并校验模型，后续可复用模型卷。
- **更新**。先备份数据卷并拉取目标标签，再停止并移除旧容器，使用相同的端口和卷启动新容器。
