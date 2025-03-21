from pymongo import MongoClient

client = MongoClient("mongodb://172.16.0.100:27017/")

# 基于字段 consent_to_share_data 决定数据是否可见
pipeline_redact = {
    "$redact": {
        "$cond": {
            "if": {"$eq": ["$consent_to_share_data", True]},
            "then": "$$KEEP",
            "else": "$$PRUNE",
        }
    }
}

# 删除 email 和 name 字段
pipeline_remove_email_and_name = {"$unset": ["email", "name"]}

obfuscate_day_of_date = {
    "$concat": [
        {
            "$substrCP": [  # 截取 $$action.date 的前 7 个字符
                "$$action.date",
                0,
                7,
            ]
        },
        "-XX",  # 拼接 "-XX"，将 2024-03-15 变成 2024-03-XX
    ]
}


rebuild_actions_elements = {
    "input": "$actions",
    "as": "action",
    "in": {"$mergeObjects": ["$$action", {"date": obfuscate_day_of_date}]},
}

# 更新 actions 数组
pipeline_set_actions = {
    "$set": {
        "actions": {"$map": rebuild_actions_elements},
    }
}

pipeline = [
    pipeline_redact,
    pipeline_remove_email_and_name,
    pipeline_set_actions,
]


if __name__ == "__main__":
    client["beat_streaming"].drop_collection("users_data_view")
    client["beat_streaming"].create_collection(
        "users_data_view", viewOn="users", pipeline=pipeline
    )
