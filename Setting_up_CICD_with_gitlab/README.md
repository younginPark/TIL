## 개요
- 사내 보안 문제를 해결하기 위해 GitLab을 구축하여 사용하는 경우가 많음
- Docker를 사용하는 시스템에서 GitLab CI/CD 환경구성하는 내용을 정리하려 함
- CI/CD Pipeline 구성은 React 프로젝트 배포를 예시로 진행할 예정

## 해야 할 일
- GitLab 회원가입 및 Repository 생성
- React 프로젝트 생성
- GitLab Repository에 올리기
- React + Nginx 통해 docker 띄워 접속 확인
- Gitlab Runner 토큰 발급 및 등록
- gitlab-ci.yml 작성

---

### GitLab 회원가입 및 Repository 생성
1. GitLab에 접속하여 회원가입을 한다.  
  https://gitlab.com/-/trial_registrations/new
  ![register](image/gitlab_signin_230620/reigster.png)
2. 주어진 절차에 따라 진행하면 완료된다. (Group, Repository 생성, 회사 어디 다니는지 등..)
   ![login](image/gitlab_signin_230620/login.png)
3. 둘러보면 gitlab-ci.yml 에디터가 보이는데 이걸 통해서 추후에 파이프라인을 구축하게 된다.
   ![login](image/gitlab_signin_230620/gitlab_ci.png)

### React 프로젝트 생성하기
1. 터미널 열어 create-react-app 으로 생성
   ```
   npx create-react-app {원하는 프로젝트 이름}
   ```
2. 터미널 열어 npm start로 잘 실행되는지 확인
   ```
   npm start
   ```
   ![npm_start](image/make_react_project_230621/npm_start.png)
   
- 참고
  - npm이 아닌 npx create-react-app 을 쓰는 이유
  https://ljh86029926.gitbook.io/coding-apple-react/undefined/npm-npx

### GitLab Repository에 생성한 React 프로젝트 올리기
1. 프로젝트 생성한걸 GitLab에 커밋 및 푸쉬
   ![commit](image/push_project_in_gitlab_230622/commit.png)

### React + Nginx 통해 docker 띄워 접속 확인
1. React 빌드 순서
   - ```npm run build```
   - ```npm install -g serve```
   - ```npx serve -s build```
   ![npmrunbuild](image/react_build_230624/npm_run_build.png)
   ![npxservebuild](image/react_build_230624/npx_serve_build.png)
   
2. Nginx 사용해서 docker에 React 앱 띄우기
   - Nginx는 정적 파일들을 처리하는 웹서버
   - docker에서 Nginx 이미지를 사용하여 React 앱을 띄움
   - 시작
     - React 소스코드가 있는 경로에 nginx.conf 추가
      ```
      server {
         listen 80;
         access_log /var/log/nginx/access.log;
         error_log /var/log/nginx/error.log;
         location / {
            root /usr/share/nginx/html;
            index index.html index.html;
            try_files $uri $uri/ /index.html;
         }
      }
      ```
     - React 소스코드가 있는 경로에 Dockerfile 추가 (빌드, 배포 함께 진행)
      ```
      # React 빌드
      FROM node:20-alpine3.17 as build
      RUN mkdir /app
      WORKDIR /app
      COPY package*.json ./
      RUN npm install
      COPY . .
      RUN npm run build

      # Nginx를 웹서버로 배포
      FROM nginx:stable-alpine
      COPY --from=build /app/build /usr/share/nginx/html
      RUN rm /etc/nginx/conf.d/default.conf
      COPY nginx.conf /etc/nginx/conf.d
      EXPOSE 80
      CMD ["nginx", "-g", "daemon off;"]
      ```
   - Docker image 생성
     ```
     front-web % docker build -t front-web:230625 .
     ```
     ![build](image/230625/buildimage.png)
   - Docker container 실행
     ```
     docker run -d -p 3001:80 --name front-web front-web:230625
     ```
     ![run](image/230625/runcontainer.png)
   - 브라우저 접속하여 localhost:3000 확인
    ![localhost](image/230625/localhost.png)

### Docker 사용하여 Gitlab runner 등록
1. GitLab에 접속하여 프로젝트 러너 생성
   ![등록](image/230626/enroll01.png)
   ![등록2](image/230626/enroll.png)
   ![등록3](image/230626/enroll02.png)
   - 세번째 이미지에서 토큰 값을 잘 저장해둔다.
2. Docker 컨테이너 백그라운드 실행 및 토큰 등록
   ```
   docker run -d --name gitlab-runner gitlab/gitlab-runner:latest
   ```
   ```
   docker exec -it gitlab-runner bash
   ```
   ![터미널](image/230626/terminal.png)
3. GitLab runner 서비스 시작
   ```
   gitlab-runner start
   ```
   ```
   gitlab-runner run
   ```
4. 잘 등록되었는지 확인
   ![확인](image/230626/check.png)


### gitlab-ci.yml 작성하기
1. gitlab-ci.yml에 포함되어야 하는 내용
   1. react 빌드
   2. 빌드된 react를 nginx 서버에 띄우는 Dockerfile로 Docker 이미지 빌드
   3. 해당 Docker 이미지로 Docker run
   
2. gitlab-ci.yml
   ```
   stages:
     - build
     - docker-build
     - deploy

   # react 빌드
   react-build-job:
     stage: build
     image: node:20-alpine3.17
     script:
       - echo "Start building react app"
       - cd $CI_PROJECT_DIR/src
       - npm install
       - npm run build
       - echo "Build Successful"

   # 위에서 빌드된 react가 아닌 dockerfile을 이용하여 빌드
   docker-build-job:
     stage: docker-build
     image: docker:latest
     services:
       - name: docker:dind
         entrypoint: ["env", "-u", "DOCKER_HOST"]
         command: ["dockerd-entrypoint.sh"]
     variables:
       DOCKER_HOST: tcp://docker:2375/
       DOCKER_DRIVER: overlay2
       # See https://github.com/docker-library/docker/pull/166
       DOCKER_TLS_CERTDIR: ""
     before_script:
       - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY
       - echo $CI_REGISTRY
     script:
       - docker build -t registry.gitlab.com/personal5062525/mygitlab/nginx-web-static:$CI_COMMIT_SHORT_SHA .
       - docker push registry.gitlab.com/personal5062525/mygitlab/nginx-web-static:$CI_COMMIT_SHORT_SHA

   # 도커 이미지로 서버 배포
   force cicd
   deploy-app:
     stage: deploy
     image: docker:latest
     services:
       - name: docker:dind
         entrypoint: ["env", "-u", "DOCKER_HOST"]
         command: ["dockerd-entrypoint.sh"]
     variables:
       DOCKER_HOST: tcp://docker:2375/
       DOCKER_DRIVER: overlay2
       # See https://github.com/docker-library/docker/pull/166
       DOCKER_TLS_CERTDIR: ""
     before_script:
       - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY
     script:
       - docker pull registry.gitlab.com/personal5062525/mygitlab/nginx-web-static:$CI_COMMIT_SHORT_SHA
       - docker run -d -p 8080:80 --name nginx-web-static registry.gitlab.com/personal5062525/mygitlab/nginx-web-static:$CI_COMMIT_SHORT_SHA
   ```

3. docker deploy 통해 배포는 되는데 접속이 안되어 2번째 stage에서 빌드된 docker image를 pull 받아서 접속하였다.
   ![job](image/230702/job.png)
   ![pull](image/230702/imagepull.png)
   ![container](image/230702/container.png)
   ![localhost](image/230702/localhost.png)

#### Trouble Shooting
      - docker registry에 접속이 안되는 오류
         https://gitlab.com/gitlab-org/gitlab-runner/-/issues/4566#note_199261985
      - 그래서 docker run 되어 뜬 docker container가 어디서 뜬다는건데?
        - gitlab runner 가 뜨고 있는 ip에 8080으로 접속하면 되어야 한다는데 난 안된다..
        - 애초에 gitlab runner가 내 컴퓨터에서 뜨니까 deploy 하려면 내 컴퓨터 접속해서 해야할텐데 그 과정이 어떻게 되는건지 공부가 더 필요하다.
        - 우선 오늘은 여기까지..
