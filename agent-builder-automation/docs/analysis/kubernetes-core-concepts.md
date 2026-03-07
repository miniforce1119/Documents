# Kubernetes 핵심 개념 정리

> 업데이트: 2026-03-07  
> 카테고리: concepts  
> 난이도: Intermediate

## 🎯 개요

Kubernetes(K8s)는 컨테이너화된 애플리케이션의 배포, 확장 및 관리를 자동화하는 오픈소스 플랫폼입니다. 이 문서는 Kubernetes의 핵심 개념을 정리합니다.

## 🏗️ 아키텍처 구성요소

### Control Plane (마스터 노드)

| 컴포넌트 | 역할 |
|----------|------|
| **API Server** | 모든 REST 명령어의 진입점 |
| **etcd** | 클러스터 데이터 저장소 |
| **Scheduler** | Pod를 노드에 할당 |
| **Controller Manager** | 컨트롤러 실행 |
| **Cloud Controller** | 클라우드 제공자 API 연동 |

### Worker Node (워커 노드)

- **kubelet**: 노드의 에이전트
- **kube-proxy**: 네트워크 프록시
- **Container Runtime**: 컨테이너 실행 (Docker, containerd 등)

## 📦 핵심 오브젝트

### 1. Pod

가장 작은 배포 단위. 하나 이상의 컨테이너를 포함합니다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
  labels:
    app: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.21
    ports:
    - containerPort: 80
```

**특징**:
- ✅ 동일 Pod 내 컨테이너는 네트워크/스토리지 공유
- ✅ 임시성 (Ephemeral) - 언제든 재시작 가능
- ✅ 고유한 IP 주소 할당

### 2. ReplicaSet

지정된 수의 Pod 복제본을 유지합니다.

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: nginx-replicaset
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
```

### 3. Deployment

ReplicaSet을 관리하며 롤링 업데이트를 지원합니다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
```

### 4. Service

Pod에 대한 안정적인 네트워크 엔드포인트를 제공합니다.

#### ClusterIP (기본)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
```

#### NodePort

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-nodeport
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
```

#### LoadBalancer

클라우드 제공자의 로드 밸런서를 생성합니다.

### 5. ConfigMap & Secret

#### ConfigMap (설정 데이터)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database_url: "mysql://db:3306"
  log_level: "info"
```

#### Secret (민감 데이터)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: YWRtaW4=  # base64 encoded
  password: cGFzc3dvcmQ=
```

### 6. Volume & PersistentVolume

#### PersistentVolume (PV)

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-storage
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
```

#### PersistentVolumeClaim (PVC)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

## 🔄 주요 개념

### Labels & Selectors

**Labels**: 오브젝트를 식별하고 그룹화

```yaml
metadata:
  labels:
    environment: production
    tier: frontend
    version: v1.2.3
```

**Selectors**: Labels로 오브젝트 선택

```yaml
selector:
  matchLabels:
    environment: production
    tier: frontend
```

### Namespaces

클러스터 내 가상 클러스터로 리소스 격리

```bash
# Namespace 생성
kubectl create namespace dev

# Namespace 내 리소스 조회
kubectl get pods -n dev
```

**기본 Namespaces**:
- `default`: 기본 네임스페이스
- `kube-system`: 시스템 컴포넌트
- `kube-public`: 공개 리소스
- `kube-node-lease`: 노드 하트비트

### Resource Quotas & Limits

#### Namespace 단위 쿼터

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: dev
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
```

#### Pod 단위 리소스

```yaml
spec:
  containers:
  - name: app
    image: app:1.0
    resources:
      requests:
        memory: "128Mi"
        cpu: "250m"
      limits:
        memory: "256Mi"
        cpu: "500m"
```

## 🚀 실전 예제

### 전체 애플리케이션 배포

```yaml
# 1. Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: myapp

---
# 2. ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: myapp
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"

---
# 3. Secret
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
  namespace: myapp
type: Opaque
stringData:
  DB_PASSWORD: "supersecret"

---
# 4. Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: myapp:1.0
        envFrom:
        - configMapRef:
            name: app-config
        env:
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: DB_PASSWORD
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"

---
# 5. Service
apiVersion: v1
kind: Service
metadata:
  name: web-service
  namespace: myapp
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 8080
```

## 🛠️ 주요 kubectl 명령어

```bash
# Pod 조회
kubectl get pods
kubectl get pods -o wide
kubectl describe pod <pod-name>

# Deployment 관리
kubectl create deployment nginx --image=nginx
kubectl scale deployment nginx --replicas=5
kubectl rollout status deployment nginx
kubectl rollout undo deployment nginx

# Service 관리
kubectl expose deployment nginx --port=80 --type=LoadBalancer
kubectl get services

# 로그 확인
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # 실시간

# 실행 중인 Pod 접근
kubectl exec -it <pod-name> -- /bin/bash

# 설정 적용
kubectl apply -f deployment.yaml
kubectl delete -f deployment.yaml
```

## 📊 헬스체크

### Liveness Probe (생존 확인)

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
```

### Readiness Probe (준비 상태 확인)

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

## 🔐 보안 Best Practices

1. ✅ **RBAC 활성화**: 역할 기반 접근 제어
2. ✅ **Network Policies**: 네트워크 격리
3. ✅ **Pod Security Policies**: Pod 보안 정책
4. ✅ **Secrets 관리**: 민감 정보 암호화
5. ✅ **Image Scanning**: 컨테이너 이미지 취약점 스캔

## 🔗 참고 자료

- [공식 문서](https://kubernetes.io/docs/)
- [Kubectl 치트시트](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)

## 📝 요약

Kubernetes는 강력한 컨테이너 오케스트레이션 플랫폼입니다. 핵심은:

- **Pod**: 최소 배포 단위
- **Deployment**: 선언적 업데이트
- **Service**: 안정적인 네트워크
- **ConfigMap/Secret**: 설정 관리
- **Volume**: 데이터 영속성

---

**난이도**: Intermediate  
**예상 학습 시간**: 2-3시간  
**다음 학습**: Helm Charts, Operators