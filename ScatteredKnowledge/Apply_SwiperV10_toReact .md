# Swiper Version 10 React에 적용하기
- Swiper Version 10은 .mjs 파일로 모듈을 구성되어 있어서 React에서는 바로 선언하여 적용이 불가능함
- Swiper Version 6까지만 React에서 바로 사용할 수 있는데 퍼블리싱 받은건 Swiper version 10으로 되어 있어서 6을 설치하여 퍼블리싱 적용 시 동일하게 적용 및 작동되지 않는다.
- 이때 **@babel/plugin-transform-modules-commonjs 노드도 함께 설치하면 Ecma Script 모듈들을 CommonJS로 변환시켜준다.**
- CommonJS를 써야 React에서 import 하여 사용 가능
- React는 Node.js 기반인데 Node.js의 기본 모듈은 CommonJS이고, 기본 Modern javascript의 기본 모듈은 Ecam Script 모듈이다.

### 참고
[CommonJS vs ES module](https://developer-alle.tistory.com/444)