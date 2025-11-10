# 🚀 Despliegue Flask + MySQL + Tailscale en Minikube

## 1️⃣ Iniciar Minikube
```bash
minikube start --driver=docker --cpus=4 --memory=6g
```

## 2️⃣ Activar MetalLB (para LoadBalancer)
```bash
minikube addons enable metallb
```

Asignar rango de IPs a MetalLB:
```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    address-pools:
    - name: default
      protocol: layer2
      addresses:
      - 192.168.49.240-192.168.49.250
EOF
```

---

## 3️⃣ (Opcional) Inicializar la base de datos con script SQL
```bash
kubectl apply -f mysql-init-config.yaml
```
> Asegúrate que tu `mysql-deployment.yaml` monte ese ConfigMap o initContainer.

---

## 4️⃣ Crear volumen y base de datos MySQL
```bash
kubectl apply -f mysql-deployment.yaml
```

Verificar estado:
```bash
kubectl get pods
kubectl get svc
```

---

## 5️⃣ Crear despliegue de la API Flask
```bash
kubectl apply -f flask-deployment.yaml
```

Verificar servicio:
```bash
kubectl get svc flask-service
```

---



## 6️⃣ Crear Secret con AuthKey de Tailscale
```bash
kubectl apply -f tailscale-secret.yaml
```

---

## 7️⃣ Crear Deployment del Tailscale Gateway
```bash
kubectl apply -f tailscale-gateway.yaml
```

Verificar que el pod está corriendo:
```bash
kubectl get pods -l app=tailscale-gateway
```

Ver logs:
```bash
kubectl logs -f deploy/tailscale-gateway
```

---

## 8️⃣ Aprobar rutas en el panel de Tailscale
Entra a tu cuenta → **Machines → k8s-gateway → Routes → Approve**.

Verifica rutas activas:
```bash
kubectl exec -it deploy/tailscale-gateway -- tailscale status
```

---

## 9️⃣ Probar conectividad
Pod de prueba:
```bash
kubectl run debug --rm -it --image=alpine -- sh
apk add --no-cache curl
curl http://flask-service:5000/clientes
```

Desde otra máquina en Tailscale:
```bash
curl http://<IP_TAILSCALE_GATEWAY>:30007/clientes
```

---

## 🔍 10️⃣ Verificar todo
```bash
kubectl get all
kubectl get endpoints flask-service
minikube service list
```

---

## ✅ Limpieza (opcional)
```bash
kubectl delete all --all
minikube delete
```
