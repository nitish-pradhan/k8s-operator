<h3 align="center">K8s operator for MongoDB application</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue)](/LICENSE)

</div>

---

<p align="center"> Kubernetes operator for a FastAPI application which uses MongoDB as backend.
                   Above application was deployed using K8 operator.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Future Enhancement](#enhancement)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## 🧐 About <a name = "about"></a>

Kubernetes operator for a FastAPI application which uses MongoDB as backend. Thr application was deployed using K8 operator. Operator was created using Kopf.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your kubernetes cluster for testing purposes.

### Prerequisites

What things you need to install the software and how to install them.

```
Kubernetes cluster with admin permission to deploy helm chart. Above application was tested in EKS.
```

### Installing

```
helm install fast-mongo-opr-v1 mongoapp-operator --values ./mongoapp-operator/values.yaml -n opr --create-namespace
```

This will install all the dependencies. Plase modify values file to change parameters.


## 🚀 Future enhancement <a name = "enhancement"></a>

Feature to expand the persistent volume associated with the Mongodb pod.

## ⛏️ Built Using <a name = "built_using"></a>

- [Python3](https://www.python.org/) - App & Operator
- [kopf](https://kopf.readthedocs.io/) - kopf
- [Docker](https://www.docker.com/) - Dockerize deployment
- [FastAPI](https://fastapi.tiangolo.com/) - APIs
- [MongoDB](https://mongodb.com/) - Backend
- [EKS](https://aws.amazon.com/eks/) - K8 cluster

## ✍️ Authors <a name = "authors"></a>

- [@nitish](https://github.com/nitish-pradhan)

## 🎉 Acknowledgements <a name = "acknowledgement"></a>

- Initial idea was proposed by Calix.
