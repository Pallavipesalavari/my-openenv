EASY_TASK = {
    "level": "easy",
    "initial_policy": {
        "RoleName": "JuniorDev",
        "Statement": [{"Effect": "Allow", "Action": ["*"], "Resource": "*"}]
    },
    "logs": [
        {"timestamp": "2026-03-20", "action": "s3:GetObject"},
        {"timestamp": "2026-03-21", "action": "s3:ListBucket"}
    ],
    "required_actions": ["s3:GetObject", "s3:ListBucket"],
    "forbidden_actions": ["*"]
}

MEDIUM_TASK = {
    "level": "medium",
    "initial_policy": {
        "RoleName": "DataTeam",
        "Statement": [
            {"Effect": "Allow", "Action": ["s3:GetObject", "s3:PutObject"], "Resource": "*"},
            {"Effect": "Allow", "Action": ["dynamodb:Scan", "dynamodb:Query"], "Resource": "*"},
            {"Effect": "Allow", "Action": ["ec2:StartInstances"], "Resource": "*"}
        ]
    },
    "logs": [
        {"timestamp": "2026-03-22", "action": "s3:GetObject"},
        {"timestamp": "2026-03-23", "action": "s3:PutObject"}
    ],
    "required_actions": ["s3:GetObject", "s3:PutObject"],
    "forbidden_actions": ["dynamodb:Scan", "dynamodb:Query", "ec2:StartInstances"]
}

HARD_TASK = {
    "level": "hard",
    "initial_policy": {
        "RoleName": "BackendService",
        "Statement": [
            {"Effect": "Allow", "Action": ["rds:DescribeDBInstances"], "Resource": "*"},
            {"Effect": "Allow", "Action": ["sqs:SendMessage", "sqs:ReceiveMessage"], "Resource": "*"}
        ]
    },
    "logs": [
        {"timestamp": "2026-03-24", "action": "sqs:SendMessage"}
    ],
    "required_actions": ["sqs:SendMessage"],
    "forbidden_actions": ["rds:DescribeDBInstances", "sqs:ReceiveMessage"]
}

TASKS = {"easy": EASY_TASK, "medium": MEDIUM_TASK, "hard": HARD_TASK}
