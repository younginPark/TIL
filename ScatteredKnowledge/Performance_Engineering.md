# 부하테스트
## Performance Engineering 진행 단계
- 요구사항 분석 단계
- 시스템 디자인 단계
- 개발 단계 (초기 스프린트 진행)
- 최종 테스트 단계
- 운영 단계

## 시스템 용량 산정
- Time
  - Response Time: Request Network Time + Transcation Time + Respone Network Time
  - Reuqest Network Time 과 Response Network Time: Request를 주고 받을 때 걸리는 시간
  - Transaction Time: 서버에서 실제 Transcrion 처리하는데 걸리는 시간
  - 그외 Think Time: 사용자가 화면을 보고 다음 행위를 하기까지 걸리는 시간
- User
  - Concurrent User: 시스템을 현재 사용하고 있는 사용자 수 (ex. 단위시간 10분 당 5명 중 총 3명의 사용자가 사용 중)
  - Active User: 현재 시스템에 트랜잭션을 시행하여 부하를 주고 있는 사용자 수, Active User의 수는 서버에서 실행되고 있는 Thread 혹은 Process의 수와 같다.
- Transaction: 사용자로부터의 요청을 다루는 단위 (정의하기 나름)
- TPS (Transaction Per Second): 초당 처리할 수 있는 트랜잭션의 수, TPS = Active User / 목표 Response Time (NetworkTime은 미세하다고 판단하여 무시 가정) 
- HPS (Hit Per Second): 시스템이 처리할 수 있는 모든 웹 Request의 초당 처리량 (ex. 비즈니스 트랜잭션 뿐만 아닌 이미지, js 같은거 포함)
- Peak Time: 서버가 순간적으로 가장 많은 부하를 받는 시간 정의

- 공식
  -  TPS = (Active User) / (Average Response Time) – F1
  -  TPS = (Concurrent User) / (Request Interval) – F2
  -  Active User = TPS * (Average Response Time) – F3
  -  Active User = (Concurrent User) * (Average Response Time) / (Request Interval) – F4
  -  Active User = (Concurrent User) * (Average Response Time) / [ (Average Response Time) + (Average Think Time) ] – F5


### 마무리
- 프로젝트가 막바지로 들어가면서 부하테스트가 진행 중이다.
- 부하테스트는 내가 하는게 아니라 담당팀과 협업하면서 진행되는데 희망하는 성능이나 부하 시 fail이 나면 내가 어디를 튜닝해야할지 알아야하고, 또 스크립트는 우리 모두의 의도대로 잘 작성된건지 확인이 필요한데 이 모든거에 대해 내가 제대로 참여를 못하고 있다.
- 열심히 찾아보며 하자..