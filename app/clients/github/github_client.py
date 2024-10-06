from github import Github

from app.config import Environment
from app.utils.env_vars import validate_variables

class GitHubClient:
    def __init__(self):
        environment = validate_variables(Environment)
        self.client = Github(str(environment.SECRET_KEY_GITHUB))
        
    
    def get_gist(self, gist_id: str):
        try:
            gist = self.client.get_gist(gist_id)
            return gist
        except Exception as e:
            raise ValueError(f"Error fetching gist: {e}")

    def create_comment(self, gist_id: str, comment: str):
        try:
            gist = self.get_gist(gist_id)
            gist.create_comment(comment)
            return {"message": "Comment added successfully"}
        except Exception as e:
            raise ValueError(f"Error creating comment: {e}")
