#!/bin/bash
cat > workflows-demo-task-definition.json <<EOF
[
    {
      "volumesFrom": [],
      "memory": 300,
      "portMappings": [
        {
          "hostPort": 80,
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "entryPoint": [],
      "mountPoints": [],
      "name": "todo-demo",
      "environment": [],
      "links": [],
      "image": "$AWS_REGISTRY_URL/testing2:debug-$WERCKER_GIT_BRANCH",
      "command": ["python /pipeline/source/manage.py runserver -h 0.0.0.0"],
      "cpu": 10
    }
]
EOF
