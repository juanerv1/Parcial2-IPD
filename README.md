# 🚀 Despliegue de Infraestructura con Minikube, Flask, MySQL y Tailscale

Este proyecto levanta una infraestructura completa con **Minikube**, incluyendo:

- **Base de datos MySQL**
- **API Flask**
- **Secretos y Gateway de Tailscale**
- **LoadBalancer interno para exponer la API**
- **Comunicación segura a través de Tailscale**

---

## 🧩 1️⃣ Iniciar Minikube

Asegúrate de tener Minikube corriendo:

```bash
minikube start
```

Verifica el estado del nodo:
```bash
kubectl get nodes
```

---

## 🧱 2️⃣ Configurar el entorno Docker dentro de Minikube

Permite que las imágenes se creen directamente en el entorno interno:

```bash
eval $(minikube docker-env)
```

---

## 🐳 3️⃣ Construir las imágenes Docker

Construye las imágenes necesarias:

```bash
# Imagen del backend Flask
docker build -t flask-api:latest -f Dockerfile.flask .

# Imagen del gateway Tailscale (si aplica)
docker build -t tailscale-gateway:latest -f Dockerfile.tailscale .
```

Verifica:
```bash
docker images
```

---

## 🗄️ 4️⃣ Crear y desplegar la base de datos MySQL

```bash
kubectl apply -f mysql-init-config.yaml     # ConfigMap o script init.sql
kubectl apply -f mysql-deployment.yaml    # Despliegue MySQL
```

Revisa los pods y servicios:
```bash
kubectl get pods
kubectl get svc
```

---

## ⚙️ 5️⃣ Desplegar la API Flask

```bash
kubectl apply -f flask-deployment.yaml
```

Verifica que el pod esté corriendo:
```bash
kubectl get pods -l app=flask-api
```

Prueba desde dentro del pod:
```bash
kubectl exec -it <flask-pod> -- curl http://localhost:5000/health
```

---

## 🔐 6️⃣ Crear el Secret para Tailscale

Ingresar la key de la VPN en el secret
```bash
kubectl apply -f tailscale-auth.yaml
kubectl get secrets
```

---

## 🌐 7️⃣ Desplegar el Gateway de Tailscale

```bash
kubectl apply -f tailscale-gateway.yaml
```

Verifica que esté corriendo correctamente:
```bash
kubectl logs -f deploy/tailscale-gateway
```

Debes ver una IP tipo:
```
peerapi: serving on http://100.64.x.x:53128
```

---

## 🧪 8️⃣ Probar la API desde Tailscale

Obtén la URL de servicio:
```bash
minikube service flask-service -n parcial2
```

O usa la IP de Tailscale directamente:
```
http://100.64.190.41:32744/health
```

---

## 🧾 🔍 Resumen de comandos

| Paso | Archivo / Acción | Comando |
|------|------------------|---------|
| 1 | Iniciar Minikube | `minikube start` |
| 2 | Configurar Docker local | `eval $(minikube docker-env)` |
| 3 | Construir imagen Flask | `docker build -t flask-api:latest -f Dockerfile.flask .` |
| 4 | Crear ConfigMap SQL | `kubectl apply -f sql-configure.yaml` |
| 5 | Desplegar MySQL | `kubectl apply -f sql-deployment.yaml` |
| 6 | Exponer MySQL | `kubectl apply -f sql-service.yaml` |
| 7 | Desplegar Flask | `kubectl apply -f flask-deployment.yaml` |
| 8 | Exponer Flask | `kubectl apply -f flask-service.yaml` |
| 9 | Crear Secret Tailscale | `kubectl apply -f tailscale-secret.yaml` |
| 10 | Desplegar Gateway Tailscale | `kubectl apply -f tailscale-gateway.yaml` |
| 11 | Ver logs Gateway | `kubectl logs -f deploy/tailscale-gateway` |

---

## 📱 10️⃣ Probar desde el celular

Desde la app de **Tailscale** en tu teléfono, puedes enviar peticiones HTTP a:
```
http://<IP_TAILSCALE>:<PUERTO>/endpoint
```

Por ejemplo:
```
http://100.64.190.41:32744/clientes
```

Ejemplo de cuerpo JSON para POST:
```json
{
  "nombre": "Juan Pérez",
  "correo": "juanperez@example.com",
  "telefono": "3001234567"
}
```

Puedes usar apps como **Postman**, **Insomnia** o **Hoppscotch.io**.

---

✅ **Autor:** Juan Esteban Rodríguez Valencia  
📅 **Última actualización:** 12 de noviembre de 2025
