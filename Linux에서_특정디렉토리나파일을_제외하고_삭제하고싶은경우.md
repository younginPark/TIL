# Linux에서 특정 디렉토리나 파일을 제외하고 삭제하고 싶은 경우

[How to delete all files except one named file from a specific folder](https://askubuntu.com/questions/624441/how-to-delete-all-files-except-one-named-file-from-a-specific-folder#answer-624445)

[What is the purpose of shopt -s extglob](https://askubuntu.com/questions/889744/what-is-the-purpose-of-shopt-s-extglob)

[glob](http://mywiki.wooledge.org/glob#extglob)

```
// 특정 폴더나 파일을 제외하고 모두 삭제하기
shopt -s extglob
rm -rf !("파일명1"|"파일명2"|"디렉토리명1")
```

- shotp -s extglob 를 통해 더 많은 패턴 매칭을 가능할 수 있게 허용해줌