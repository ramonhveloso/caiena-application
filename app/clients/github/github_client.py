from github import Github, GithubException

from app.config import Environment
from app.utils.env_vars import validate_variables


class GitHubClient:
    def __init__(self):
        environment = validate_variables(Environment)
        self.client = Github(str(environment.SECRET_KEY_GITHUB))
        self.gist_id = str(environment.GIST_ID)

    async def get_gist(self):
        try:
            gist = self.client.get_gist(self.gist_id)
            return gist
        except GithubException as e:
            raise ValueError(f"Error fetching gist: {e}")

    async def create_gist_comment(self, comment: str):
        try:
            gist = await self.get_gist()
            created_comment = gist.create_comment(comment)
            comment_id = created_comment.id
            return {"message": "Comment added successfully", "comment_id": comment_id}
        except GithubException as e:
            raise ValueError(f"Error creating comment: {e}")

    async def edit_gist_comment(self, comment_id: int, new_comment: str):
        try:
            gist = await self.get_gist()
            comment = gist.get_comment(comment_id)
            comment.edit(new_comment)
            return {"message": "Comment edited successfully"}
        except GithubException as e:
            raise ValueError(f"Error editing comment: {e}")

    async def delete_gist_comment(self, comment_id: int):
        try:
            gist = await self.get_gist()
            comment = gist.get_comment(comment_id)
            comment.delete()
            return {"message": "Comment deleted successfully"}
        except GithubException as e:
            raise ValueError(f"Error deleting comment: {e}")
