# Redis와 SignalR을 이용하여 채팅 서비스 만들기

## 단계
1. .NET 설치 
   - 이미 설치되어 있으므로 생략 (version 6)

2. VSCode에서 .NET 하는 법
   - 참고: https://learn.microsoft.com/en-us/dotnet/core/tutorials/with-visual-studio-code?pivots=dotnet-6-0

3. SignalR을 사용하여 실시간 앱 구현
   1. SignalR은 앱에 실시간 웹기능을 추가할 수 있는 오픈소스 라이브러리로 서버에서 클라이언트에게 컨텐츠를 푸쉬할 수 있음     (ex. 알림이 필요한 앱)
   2. SignalR 기능
      - 모든 연결된 클라이언트 혹은 특정 클라이언트에 알림 보냄
      - 늘어난 트래픽을 처리하도록 크기 조정
      - SignalR 허브 프로토콜 (Server to Client, Client to Server 호출 모두 가능)
      - 원시 WebSocket 보다 성능 상 단점이 없으며 오히려 fallback과 같은 전송 대체제가 제공됨
   3. 통신 처리 기술
      - WebSocket
      - Server-Sent 이벤트
      - 긴 폴링 



4. Redis 붙이기

###
- SignalR을 사용하여 실시간 앱 구현
  - https://learn.microsoft.com/ko-kr/aspnet/core/tutorials/signalr-typescript-webpack?view=aspnetcore-6.0&tabs=visual-studio-code