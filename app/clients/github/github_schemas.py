from github import Github

class GitHubClient:
    def __init__(self, token: str):
        self.client = Github(token)
        
    
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
