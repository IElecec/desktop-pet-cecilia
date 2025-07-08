import requests

class DeepSeekAgent:
    def __init__(self, api_key, character_setting):
        self.api_key = api_key
        self.history = [{"role": "system", "content": character_setting}]
    
    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        
        response = requests.post(
            url="https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": "deepseek-chat",
                "messages": self.history,
                "temperature": 0.5,
            }
        )
        
        ai_reply = response.json()["choices"][0]["message"]["content"]
        self.history.append({"role": "assistant", "content": ai_reply})
        return ai_reply

import json

def load_key_from_json(file_path, key_name='secret_key'):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get(key_name)

# 使用示例
if __name__ == "__main__":
    # 替换为你的DeepSeek API密钥
    API_KEY = load_key_from_json('secret.json')
    
    # 创建特定人物角色（示例：侦探）
    detective = DeepSeekAgent(
        api_key=API_KEY,
        character_setting="你是一位经验丰富的侦探，说话简洁犀利，善于分析细节。用第一人称回答，保持冷静专业的语气。"
    )
    
    # 进行连续对话
    print(detective.chat("昨晚博物馆发生了钻石盗窃案"))
    print(detective.chat("监控显示嫌犯穿着黑色风衣"))