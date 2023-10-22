# ****HLS, m3u8****

- HLS (HTTP Live Streaming) : 미디어 세그먼트 파일인 작게 자른 오디오, 비디오 파일을 보냄
- m3u8 파일 : 재생목록 파일
- Master playlist
360p, 720p, 1080p 등 동일한 컨텐츠에 대해서 네트워크 비트 전송률에 따라 변형된 재생목록
해당 플레이리스트를 통해 사용자의 네트워크 환경에 따라 재생중단 최소화하여 스트리밍 가능

- 예시

```markup
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=1000000,RESOLUTION=640x360
360p/360p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=1500000,RESOLUTION=1280x720
720p/720p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=2500000,RESOLUTION=1920x1080
1080p/1080p.m3u8
```

- ffmpeg
    - -maxrate
    - -bufsize
    다음 영상 받아오는 크기 
    보통 -maxrate의 1~2배