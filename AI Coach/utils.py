import pandas as pd

class prompt_process:
    def __init__(self, file_path):
      self.file_path = file_path
      self.prompt_set = None
    
    def load_prompt(self):
      self.prompt_set = pd.read_excel(self.file_path)

    def get_prompt(self, prompt_id):
        prompt = f'''Mục tiêu: {self.prompt_set.loc[prompt_id,'Mục tiêu']}
                {self.prompt_set.loc[prompt_id,'Ràng buộc']}\n
                {self.prompt_set.loc[prompt_id,'Hồ sơ']}\n
                {self.prompt_set.loc[prompt_id,'Đặc điểm']}\n
                {self.prompt_set.loc[prompt_id,'Sự ưu tiên']}\n
                {self.prompt_set.loc[prompt_id,'Xã hội']}\n
                {self.prompt_set.loc[prompt_id,'Phản hồi']}\n
                {self.prompt_set.loc[prompt_id,'Câu chuyện']}\n
                {self.prompt_set.loc[prompt_id,'Ví dụ']}\n
                {self.prompt_set.loc[prompt_id,'Mô tả tình huống']}
                '''
        return prompt

      