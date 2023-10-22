# Kubernetes에서 오브젝트 delete 시에 matching 되는 이름으로 지우고 싶을 경우

```
kubectl get deployments -n default --no-headers=true | awk '/youngin-deployment/{print $1}'| xargs  kubectl delete -n default deployments
```

이런 식으로 
```
awk '/youngin-deployment/{print $1}'| 
```
여기에서 / / 사이에 있는 값들을 원하는 이름으로 바꿔주면 됨

### 출처
 https://faun.pub/delete-kubernetes-pods-with-a-regex-f396291bba0e