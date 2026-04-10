EASY_TASK = {
    "level": "easy",
    "initial_policy": {
        "RoleName": "JuniorDev",
        "Statement": [
            {"Effect": "Allow", "Action": ["*"], "Resource": "*"}
        ]
    },
    "logs": [
        {
            "timestamp": "2026-03-20",
            "action": "s3:GetObject",
            "resource": "arn:aws:s3:::company-data/file1.txt",
            "user": "junior_dev"
        },
        {
            "timestamp": "2026-03-21",
            "action": "s3:ListBucket",
            "resource": "arn:aws:s3:::company-data",
            "user": "junior_dev"
        }
    ],
    "required_actions": ["s3:GetObject", "s3:ListBucket"],
    "forbidden_actions": [
        "ec2:StartInstances",
        "dynamodb:Scan",
        "iam:DeleteUser"
    ]
}


MEDIUM_TASK = {
    "level": "medium",
    "initial_policy": {
        "RoleName": "DataTeam",
        "Statement": [
            {"Effect": "Allow", "Action": ["s3:GetObject", "s3:PutObject"], "Resource": "*"},
            {"Effect": "Allow", "Action": ["dynamodb:Scan", "dynamodb:Query"], "Resource": "*"},
            {"Effect": "Allow", "Action": ["ec2:StartInstances"], "Resource": "*"},
            {"Effect": "Allow", "Action": ["cloudwatch:PutMetricData"], "Resource": "*"}
        ]
    },
    "logs": [
        {
            "timestamp": "2026-03-22",
            "action": "s3:GetObject",
            "resource": "arn:aws:s3:::analytics-data/report.csv",
            "user": "data_engineer"
        },
        {
            "timestamp": "2026-03-23",
            "action": "s3:PutObject",
            "resource": "arn:aws:s3:::analytics-data/output.csv",
            "user": "data_engineer"
        },
        {
            "timestamp": "2026-03-23",
            "action": "cloudwatch:PutMetricData",
            "resource": "*",
            "user": "data_engineer"
        }
    ],
    "required_actions": [
        "s3:GetObject",
        "s3:PutObject",
        "cloudwatch:PutMetricData"
    ],
    "forbidden_actions": [
        "dynamodb:Scan",
        "dynamodb:Query",
        "ec2:StartInstances"
    ]
}


HARD_TASK = {
    "level": "hard",
    "initial_policy": {
        "RoleName": "BackendService",
        "Statement": [
            {"Effect": "Allow", "Action": ["rds:DescribeDBInstances"], "Resource": "*"},
            {"Effect": "Allow", "Action": ["sqs:SendMessage", "sqs:ReceiveMessage"], "Resource": "*"},
            {"Effect": "Allow", "Action": ["lambda:InvokeFunction"], "Resource": "*"},
            {"Effect": "Allow", "Action": ["cloudwatch:PutMetricData"], "Resource": "*"}
        ]
    },
    "logs": [
        {
            "timestamp": "2026-03-24",
            "action": "sqs:SendMessage",
            "resource": "arn:aws:sqs:us-east-1:123456789012:queue1",
            "user": "backend_service"
        },
        {
            "timestamp": "2026-03-24",
            "action": "lambda:InvokeFunction",
            "resource": "arn:aws:lambda:us-east-1:123456789012:function:processData",
            "user": "backend_service"
        }
    ],
    "required_actions": [
        "sqs:SendMessage",
        "lambda:InvokeFunction"
    ],
    "forbidden_actions": [
        "rds:DescribeDBInstances",
        "sqs:ReceiveMessage",
        "cloudwatch:PutMetricData"
    ]
}


TASKS = {
    "easy": EASY_TASK,
    "medium": MEDIUM_TASK,
    "hard": HARD_TASK
}
