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
      "links": ["mysql", "redis"],
      "image": "$AWS_REGISTRY_URL/testing2:debug-$WERCKER_GIT_BRANCH",
      "command": ["/usr/local/bin/python", "manage.py", "db", "upgrade", "&&", "/usr/local/bin/python", "/pipeline/source/manage.py", "runserver", "-h", "0.0.0.0"],
      "cpu": 10
    },
    {
      "environment": [
        {
          "name": "MYSQL_ROOT_PASSWORD",
          "value": "testpass"
        },
        {
          "name": "MYSQL_DATABASE",
          "value": "haralyzer_api_test"
        }
      ],
      "name": "mysql",
      "image": "mysql",
      "cpu": 10,
      "memory": 500,
      "essential": true
    },
    {
      "name": "redis",
      "image": "redis",
      "cpu": 10,
      "memory": 500,
      "essential": true
    }
]
EOF
