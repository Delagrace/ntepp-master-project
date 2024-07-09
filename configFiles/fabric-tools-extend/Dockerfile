FROM hyperledger/fabric-peer:1.4

# Install Go
RUN apt-get update && apt-get install -y golang-go

# Set the GOPATH environment variable
ENV GOPATH=/opt/gopath
ENV PATH=$PATH:/usr/local/go/bin:/opt/gopath/bin

WORKDIR /opt/gopath/src/
