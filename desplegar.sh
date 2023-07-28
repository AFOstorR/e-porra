#!/usr/bin/env bash

PROJECT=grupo-5-modernizacion
LOCATION=us-central1
REPOSITORY_NAME=uniandes-misw-modernizacion-grupo5
RED_NAME=vpn-app-misw-g05
RED_K8s_NAME=red-k8s-app
RED_K8s_RANGE=192.168.32.0/19
RED_BD_NAME=red-dbs-misw-g05
RED_BD_IP=192.168.0.0
REGLA_FIREWALL_BD_NAME_1=allow-db-ingress
INSTANCE_SQL_NAME=grupo05bd
K8s_CLUSTER_NAME=uniandes-misw-modernizacion-grupo5-k8s
ROOT_PASSWORD=Grupo05_Tagamandapio

echo "Habilitar API Artifact Registry API"
gcloud services enable artifactregistry.googleapis.com

echo "Crear repositorio"
gcloud artifacts repositories create $REPOSITORY_NAME --location=$LOCATION --repository-format=docker --mode=standard-repository

echo "Autenticar en el respositorio"
gcloud auth configure-docker $LOCATION-docker.pkg.dev

echo "Cargar imagenes contenedor de los Microservicios"
docker build -t $LOCATION-docker.pkg.dev/$PROJECT/$REPOSITORY_NAME/backend-e-porra:1.0 ./Backend/.
docker push $LOCATION-docker.pkg.dev/$PROJECT/$REPOSITORY_NAME/backend-e-porra:1.0

docker build -t $LOCATION-docker.pkg.dev/$PROJECT/$REPOSITORY_NAME/mseventos-e-porra:1.0 ./Experimento/eventos/.
docker push $LOCATION-docker.pkg.dev/$PROJECT/$REPOSITORY_NAME/mseventos-e-porra:1.0

docker build -t $LOCATION-docker.pkg.dev/$PROJECT/$REPOSITORY_NAME/msapuestas-e-porra:1.0 ./Experimento/ms-apuestas/.
docker push $LOCATION-docker.pkg.dev/$PROJECT/$REPOSITORY_NAME/msapuestas-e-porra:1.0

echo "Habilitar API Compute Engine API"

gcloud services enable compute.googleapis.com
gcloud services enable servicenetworking.googleapis.com

echo "Crear red del grupo"
gcloud compute networks create $RED_NAME --project=$PROJECT --subnet-mode=custom --mtu=1460 --bgp-routing-mode=regional

echo "Crear subRed K8s"
gcloud compute networks subnets create $RED_K8s_NAME --range=$RED_K8s_RANGE --network=$RED_NAME --region=$LOCATION --project=$PROJECT

echo "Crear Red Base de datos"
gcloud compute addresses create $RED_BD_NAME --global --purpose=VPC_PEERING --addresses=$RED_BD_IP --prefix-length=24 --network=$RED_NAME --project=$PROJECT

echo "Habilitar red"
gcloud services vpc-peerings connect --service=servicenetworking.googleapis.com --ranges=$RED_BD_NAME --network=$RED_NAME --project=$PROJECT

echo "Regla de firewall"
gcloud compute firewall-rules create $REGLA_FIREWALL_BD_NAME_1 --direction=INGRESS --priority=1000 --network=$RED_NAME --action=ALLOW --rules=tcp:5432 --source-ranges=192.168.1.0/24 --target-tags=basesdedatos --project=$PROJECT

echo "Habilitar API SQL ADMIN"
gcloud services enable sqladmin.googleapis.com

echo "Crear instancia de SQL"
gcloud sql instances create $INSTANCE_SQL_NAME --database-version=POSTGRES_14 --tier=db-g1-small --no-assign-ip --enable-google-private-path --enable-google-private-path --network=$RED_NAME --storage-type=HDD --region=$LOCATION --root-password=$ROOT_PASSWORD --storage-size=10GB --no-storage-auto-increase --no-deletion-protection --no-backup

export DB_IP=$(gcloud sql instances describe $INSTANCE_SQL_NAME --project $PROJECT --format 'value(ipAddresses.ipAddress)')

echo "Crear pub/sub"
gcloud pubsub topics create Notificacion --message-retention-duration=1h

echo "Habilitar Kubernetes Engine API"
gcloud services enable container.googleapis.com

gcloud container --project $PROJECT clusters create-auto $K8s_CLUSTER_NAME --region $LOCATION --release-channel "regular" --network $RED_NAME --subnetwork $RED_K8s_NAME --cluster-ipv4-cidr "192.168.64.0/21" --services-ipv4-cidr "192.168.72.0/21"

echo "Conectarse al cluster K8s"
gcloud container clusters get-credentials $K8s_CLUSTER_NAME --region $LOCATION --project $PROJECT

echo "Instalar ingress-nginx controller"
kubectl create clusterrolebinding cluster-admin-binding \
  --clusterrole cluster-admin \
  --user $(gcloud config get-value account)

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.6.4/deploy/static/provider/cloud/deploy.yaml


echo "Crear el secret de conexion a la BD"
cat <<EOF | kubectl apply -f -
apiVersion: v1
stringData:
  uri : "postgresql+psycopg2://postgres:$ROOT_PASSWORD@$DB_IP/postgres"
kind: Secret
metadata:
  name: appsecrets
EOF

echo "Desplegar los container"
kubectl apply -f deployment/k8s-base-layer-deployment.yaml

echo "Configurando el ingress.ngix"
#sleep 300

echo "Desplegar ingress"
kubectl apply -f deployment/k8s-ingress-deloyment.yaml