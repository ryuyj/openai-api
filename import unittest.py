import unittest
from unittest.mock import patch
from openai import OpenAI

class TestChatGPTAPI(unittest.TestCase):

    @patch('openai.OpenAI')
    def test_chat_completions_create(self, mock_openai):
        # Mocking the OpenAI class and its methods
        mock_openai.return_value.chat.completions.create.return_value = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Recursion is a powerful concept in programming that involves a function calling itself. It allows for solving complex problems by breaking them down into smaller, more manageable subproblems. Each recursive call brings us closer to the base case, which is the simplest form of the problem. By solving the base case and combining the results, we can solve the original problem. However, it's important to define the base case and ensure that the recursive calls converge towards it to avoid infinite recursion."
                    }
                }
            ]
        }

        # Set up the environment variables
        os.environ["API_KEY"] = "your_api_key"

        # Import the module after setting the environment variables
        import first_ChatGPT_API

        # Call the function that makes the API call
        completion = first_ChatGPT_API.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
            ]
        )

        # Assert the expected output
        self.assertEqual(completion.choices[0].message.content, "Recursion is a powerful concept in programming that involves a function calling itself. It allows for solving complex problems by breaking them down into smaller, more manageable subproblems. Each recursive call brings us closer to the base case, which is the simplest form of the problem. By solving the base case and combining the results, we can solve the original problem. However, it's important to define the base case and ensure that the recursive calls converge towards it to avoid infinite recursion.")

if __name__ == '__main__':
    unittest.main()