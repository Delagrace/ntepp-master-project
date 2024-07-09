from kubernetes import client, config

# Load the kubeconfig file (usually located at ~/.kube/config)
config.load_kube_config()

# Create an instance of the API class
v1 = client.CoreV1Api()

# List all pods in the default namespace
print("Listing pods with their IPs:")
ret = v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    print(f"{i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}")

# Example: Get details of a specific pod
namespace = 'default'
pod_name = 'example-pod'
pod = v1.read_namespaced_pod(name=pod_name, namespace=namespace)
print(f"Details of pod {pod_name}:")
print(pod)

# Example: Send a request to a pod
# Assuming you have a pod with an exposed service, you can communicate with it.
# For instance, if there's a service exposing an HTTP endpoint on port 80:
import requests

service_ip = "your-service-ip"
service_port = 80
response = requests.get(f"http://{service_ip}:{service_port}/your-endpoint")
print(response.text)
