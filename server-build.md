 ##Build Docker image for Rest API
The following commands will create a container image and push it to your container registry.
$ cd ../API0
$ docker build . -t delagrace/rest-api5
$ docker push delagrace/rest-api5

$ cd ../API1
$ docker build . -t delagrace/rest-api6
$ docker push delagrace/rest-api6

$ cd ../API2
$ docker build . -t delagrace/rest-api7
$ docker push delagrace/rest-api7

$ cd ../API3
$ docker build . -t delagrace/rest-api8
$ docker push delagrace/rest-api8

$ cd ../API4
$ docker build . -t delagrace/rest-api9
$ docker push delagrace/rest-api9


If you are using a private registry, the Kubernetes Service needs permissions to pull your private container image from your registry. You can provide the Kubernetes Service with your docker secrets by running this command:
$ kubectl create secret docker-registry regcred --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
4.2 Deploy and Expose Rest API
The following commands will first pull the container image from your registry and create a deployment named "rest-api", then create a Kubernetes Service which exposes this deployment

$ cd ..
$ kubectl create deployment rest-api --image=delagrace/rest-api5
deployment.apps/rest-api created
$ kubectl expose deployment rest-api --port=3000 --target-port=3000
service/rest-api exposed

$ cd ..
$ kubectl create deployment rest-api1 --image=delagrace/rest-api6
deployment.apps/rest-api1 created
$ kubectl expose deployment rest-api1 --port=4000 --target-port=4000
service/rest-api1 exposed

$ cd ..
$ kubectl create deployment rest-api2 --image=delagrace/rest-api7
deployment.apps/rest-api1 created
$ kubectl expose deployment rest-api2 --port=5000 --target-port=5000
service/rest-api1 exposed

$ cd ..
$ kubectl create deployment rest-api3 --image=delagrace/rest-api8
deployment.apps/rest-api1 created
$ kubectl expose deployment rest-api3 --port=6000 --target-port=6000
service/rest-api1 exposed

$ cd ..
$ kubectl create deployment rest-api4 --image=delagrace/rest-api9
deployment.apps/rest-api1 created
$ kubectl expose deployment rest-api4 --port=7000 --target-port=7000
service/rest-api1 exposed


5. Deploy Node-RED
Node-RED dashboard will be your front-end. You will be able to see incoming sensor data and the history of the ledger from this dashboard. Besides, all the HTTP requests will be execute via this tool.

Note: There is Node-RED service in the IBM Cloud Catalog. However, in this pattern you will use Node-RED inside a container.

Note: If you wish to use Node-RED service you can import the flow by using this

The following commands will build the Node-RED container image and push it to DockerHub, create a deployment named "node-red", then create a Kubernetes Service which exposes this deployment

Edit the Makefile and enter your DOCKERHUB_ID:=

$ cd node-red
$ make build
$ make push
$ kubectl create deployment node-red --image=delagrace/hyperledger-iot-nodered:1.0.3
deployment.apps/node-red created

$ cd node-red1
$ make build
$ make push
$ kubectl create deployment node-red1 --image=delagrace/hyperledger-iot-nodered1:1.0.3
deployment.apps/node-red created

$ cd node-red2
$ make build
$ make push
$ kubectl create deployment node-red2 --image=delagrace/hyperledger-iot-nodered2:1.0.3
deployment.apps/node-red created

$ cd node-red3
$ make build
$ make push
$ kubectl create deployment node-red3 --image=delagrace/hyperledger-iot-nodered3:1.0.3
deployment.apps/node-red created

$ cd node-red4
$ make build
$ make push
$ kubectl create deployment node-red4 --image=delagrace/hyperledger-iot-nodered4:1.0.3
deployment.apps/node-red created

Option 1
If you have Free Cluster use the following command to make nodered deployment accessible from the network.
$ cd ../node-red1
$ kubectl apply -f node-red-svc-nodePort.yaml
service/node-red created

$ cd ../node-red2
$ kubectl apply -f node-red-svc-nodePort.yaml
service/node-red created

$ cd ../node-red3
$ kubectl apply -f node-red-svc-nodePort.yaml
service/node-red created

$ cd ../node-red4
$ kubectl apply -f node-red-svc-nodePort.yaml
service/node-red created


Option 2
If you have a Standard Cluster, IBM Cloud will provide you an Ingress Controller and Application Load Balancer which you can use to access your cluster from network. So that, you need to create ingress rules by following.
Note that, you must modify hosts and the secretName fields in the "create-ingress.yaml". To learn your Ingress Subdomain and Ingress Secret execute the following commands.

$ kubectl config current-context
$ ibmcloud ks cluster get --cluster <your_cluster_name>
Copy the Ingress subdomain details, eg my-hyperledger-dee43bc8701fcd5837d6df963718ad39-0000 into the {{INGRESS-SUBDOMAIN}} sections of the create-ingress.yaml file.

  - hosts:
    - node-red.{{INGRESS-SUBDOMAIN}}.us-south.containers.appdomain.cloud
    secretName: {{INGRESS-SUBDOMAIN}}
  rules:
  - host: node-red.{{INGRESS-SUBDOMAIN}}.us-south.containers.appdomain.cloud
Now, you can create Node-RED service and Ingress rules.

$ kubectl apply -f node-red-svc-clusterIP.yaml
$ kubectl apply -f create-ingress.yaml
Understanding the Application
Congratulations! You have deployed your very first Hyperledger Fabric - IoT collabrative application. Now, it is time to understand how the manage the application.

Access to Node-RED
Option 1
If you have Free Cluster follow the below instructions to access to dashboard.

First, execute the below commands to get your Kubernetes Worker Node's external IP.

$ kubectl get pods -o wide
$ kubectl get nodes -o wide


Open your favorite browser and navigate to "Your_external_IP":30002 which will end up with Node-RED service. For example, 52.116.26.52:30002

Option 2
If you have Standard Cluster just navigate to host name of your cluster from the browser. For example, node-red.{{INGRESS-SUBDOMAIN}}.us-south.containers.appdomain.cloud

$ kubectl get ingress
Registration
Execute the three HTTP Post request respectively.

First POST will enroll an admin named "admin" to the Certificate Authority of the Organization 1.
Second POST will enroll a register and enroll user named "user1" to the Certificate Authority of the Organization 2.
Third POST Will register a new sensor which will be used to collect the data from.
You will end up with a screen as below. You can see the returning results on the right-hand side.



Dashboard
It is time to create an User Interface to make the application to look fancy.



Finally, navigate to "Your_External_IP":30002/ui or nodered.{{HOST-NAME}}.us-south.containers.appdomain.cloud/ui to see your dashboard. Toggle the Generate IoT readings switch to generate simulated IoT sensor data if you are not able to provide a sensor. You will be able to see your sensor data live on a gauge and chart. To query the sensor data history stored on the blockchain, navigate to the "Sensor History" tab from the hamburger menu. The data history is coming from the Ledger where the data is storing immutablly in the blockchain.

Here is the screenshots of the final views of the application.





