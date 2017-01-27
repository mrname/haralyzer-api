#!/bin/bash
cat > workflows-demo-task-definition.json <<EOF
[
    {
      "volumesFrom": [],
      "memory": 300,
      "portMappings": [
        {
          "hostPort": 8080,
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "entryPoint": [],
      "mountPoints": [],
      "name": "todo-demo",
      "environment": [],
      "links": [],
      "image": "$AWS_REGISTRY_URL/testing:debug-$WERCKER_BRANCH_NAME",
      "command": [],
      "cpu": 10
    }
]
EOF
