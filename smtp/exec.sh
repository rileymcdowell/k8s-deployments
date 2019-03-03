#!/bin/bash

kubectl exec -it $(kubectl get pods --output name | grep 'smtp' | cut -d '/' -f 2) /bin/bash
