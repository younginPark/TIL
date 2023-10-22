# DOMException: play() failed because the user didn't interact with the document first.

SSO를 할 때 VOD 시청하는 경로로 바로 redirect 해주었다.

그런데 평소와 달리 VOD가 자동 재생되지 않았는데, 개발자 도구 콘솔에 이런 문구가 찍혀있었다.

```
DOMException: play() failed because the user didn't interact with the document first.
```

찾아보니 

- Improved user Experience (사용자 경험 향상)
- Minimized Incentives to install ad blockers (adBlock 굳이 설치 안해도 되게)
- Reduced data consumption (자동재생으로 인한 예상치 못한 데이터 사용을 줄일 수 있게)

위와 같은 이유들로 웹 개발 정책으로 인해 자동으로 재생되는 것을 일부러 막은 것이다.(https://developer.chrome.com/blog/autoplay/ 크롬, 엣지 모두 해당)

생각해보니 카카오톡에서 유튜브 링크를 받았을 때 유튜브가 음소거로 재생되었던게 생각났다.

다른 도메인에서 해당 VOD 페이지로 이동했을 때 자동 재생 시키고 싶다면,
muted 를 true를 주면 자동 재생 시킬 수 있다.

그런데 난 muted 를 true 해서 자동재생 시키면 사용자에게 왜 소리가 안나오냐고 문의가 올 것 같아서 그냥 재생 버튼을 잘 보이게 video player 왼쪽 상단에 두는 것으로 끝냈다.

구글링을 해보니 만약 이 정책을 깨고 싶다면 mouseover 같은 이벤트를 dom 엘리먼트들에 등록하여 자동재생 시키라고도 한다. (만약 이렇게 하게 된다면 성능저하 문제가 생길 수 있기 때문에 removeEventListener도 꼭 해줄것)

### 출처

[16. useEffect를 사용하여 마운트/언마운트/업데이트시 할 작업 설정하기](https://react.vlpt.us/basic/16-useEffect.html)

[https://velog.io/@zerozoo-front/useEffect와-addEventListener](https://velog.io/@zerozoo-front/useEffect%EC%99%80-addEventListener)