# cliwrap buffer 오류

```
videoKey: #######
fileName: ######.mp4
count: 3
Loop #0 SeekPoint: ##
fail: Microsoft.AspNetCore.Server.Kestrel[13]
      Connection id "###", Request id "#####": An unhandled exception was thrown by the application.
CliWrap.Exceptions.CommandExecutionException: Underlying process reported a non-zero exit code (137).

Command:
  /ffmpeg/ffmpeg -y -ss 47 -i "/path/#####/#####.mp4" -vf scale=-1:360 -vframes 1 /path/#####/thumbnailCandidate_1.jpg

Standard error:
  ffmpeg version 4.3.1-static https://johnvansickle.com/ffmpeg/  Copyright (c) 2000-2020 the FFmpeg developers
  built with gcc 8 (Debian 8.3.0-6)
 
  생략..
```

- 개발계랑 운영계 코드 똑같은데 개발계에서는 업로드 되므로 동영상 문제, 소스 코드 문제 아님
- 버퍼 문제라기에는 다른 영상들은 잘 올라감, 그런데 이 영상이 8K여서 다른 문제가 있을 수도 있음
- 만약 버퍼 문제라면 어느 서버에서 지워야 하나.. ⇒ 워커노드 골고루에 팟이 뜨게 될테고.., 이미 팟들은 한번씩 다 죽이고 살아나서 팟 내부는 건들 필요 없을듯
- 2개의 썸네일 팟이 같은 노드에 올라가 있는가? 아님, 워커1번, 3번에 올라가 있어서 각각 워커 캐시 버퍼들 지워줌 그런데도 안됨
- 해당 명령어가 잘못된게 있나 ffmpeg 명령어들 하나하나 어떤 의미였는지 다시 찾아봄
- pod에 직접 접속하여 ffmpeg 명령어를 그대로 쳤을 때 killed 되면서 멈춘 것을 알 수 있음
- 구글링을 통해 memory 문제라는 것을 알 수 있었음

[FFMPEG killed - not much information for troubleshooting](https://stackoverflow.com/questions/72052279/ffmpeg-killed-not-much-information-for-troubleshooting)

https://github.com/cypress-io/cypress/issues/16863

- deploy_dev.yaml 과 deploy_prod.yaml 을 비교해보니 개발계에는 resource requests, limits 설정 코드가 주석처리 되어 있었고, 운영계에는 설정되어 있었음
- 개발계의 해당 부분 주석을 풀어보고 8K 영상을 올렸을 때 운영계와 마찬가지로 썸네일 생성 부분이 막히는 것을 알 수 있었음
- 그럼 resource limits을 얼마나 해줘야하는지에 대한 best practice 필요

[Kubernetes requests vs limits: Why adding them to your Pods and Namespaces matters | Google Cloud Blog](https://cloud.google.com/blog/products/containers-kubernetes/kubernetes-best-practices-resource-requests-and-limits?hl=en)

[Setting the right requests and limits in Kubernetes](https://learnk8s.io/setting-cpu-memory-limits-requests)

[Checking kubernetes pod CPU and memory](https://stackoverflow.com/questions/54531646/checking-kubernetes-pod-cpu-and-memory)

⇒ kubectl exec -it pod_name -n namespace -- /bin/bash
    cat /sys/fs/cgroup/memory/memory.usage_in_bytes | numfmt --to=iec  (429M 이렇게 보여줌)

```markup
사용자이름@pod명:/app$ cat /sys/fs/cgroup/memory/memory.usage_in_bytes | numfmt --to=iec
35M
appuser@pod명:/app$ cat /sys/fs/cgroup/memory/memory.usage_in_bytes | numfmt --to=iec
35M
```

명령어 수동으로 계속 찍었을 때 최대 1.1G