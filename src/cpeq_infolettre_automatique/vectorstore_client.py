"""Client module for openAI API interaction."""

import json

import numpy as np
import openai
import tiktoken
from decouple import config


class VectorStore:
    def __init__(self, client):
        """Initializes the VectorStore with an OpenAI client using an API key from the environment."""
        self.client = client
        self.model = "text-embedding-3-large"
        # avoir un paramètre openAI client déjà instancié (On créer le client à l'extérieur et on l'injecte (injection de dépendances))

    def load_json_data(self, filepath):
        """Loads JSON data from a specified file path.

        Args:
            filepath (str): The path to the JSON file.

        Returns:
            dict: A dictionary loaded from the JSON file, or None if an error occurs.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: The file at {filepath} was not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: The file at {filepath} could not be decoded.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def save_json_data(self, data, filepath):
        """Save a given dictionary to a JSON file at a specified path. This function writes a Python dictionary to a JSON file, using UTF-8 encoding and formatting the output with indents for readability.

        Args:
            data (dict): The data to save.
            filepath (str): The file path where the JSON file will be saved.

        Returns:
            None
        """
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"Data successfully saved to {filepath}")
        except Exception as e:
            print(f"Failed to save data to {filepath}: {e}")

    def get_average_embeddings(self, model, rubrics_data):
        """Calculates average embeddings for each rubric using provided examples.

        Args:
            rubrics_data (list of dicts): A list of rubric sections, each containing examples.

        Returns:
            dict: A dictionary of rubric names mapped to their average embedding vectors.
        """
        rubric_embeddings = {}

        for rubric_section in rubrics_data:
            rubric_name = rubric_section["rubric"]
            articles = rubric_section["examples"]
            all_embeddings = []

            for article in articles:
                input_text = f"{article["title"]} {article["summary"]}"  # Combine title and summary for embedding
                try:
                    response = openai.embeddings.create(input=input_text, model=model)
                    embedding_vector = response.data[0].embedding
                    all_embeddings.append(embedding_vector)
                    print(
                        f"Embedding retrieved for: {article["title"]} (Vector length: {len(embedding_vector)})"
                    )
                except Exception as e:
                    print(f"Failed to retrieve embeddings for {article["title"]}: {str(e)}")

            # Calculate the average embedding if any embeddings were successfully retrieved
            if all_embeddings:
                average_embedding = np.mean(all_embeddings, axis=0)
                rubric_embeddings[rubric_name] = (
                    average_embedding.tolist()
                )  # Convert numpy array to list for JSON compatibility
                print(f"Average embedding calculated for rubric: {rubric_name}")

        return rubric_embeddings

    def get_embedding(self, text, max_tokens=8000):
        """Retrieves the embedding vector for a given text, truncating to a maximum token count.

        Args:
            text (str): The text to be embedded.
            max_tokens (int): Maximum number of tokens to consider.

        Returns:
            array: The embedding vector obtained from the OpenAI API.
        """
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(text)
        if len(tokens) > max_tokens:
            tokens = tokens[:max_tokens]
        truncated_text = encoding.decode(tokens)
        response = self.client.embeddings.create(input=truncated_text, model=self.model)
        return response.data[0].embedding if response else None

    def find_most_similar_category(self, text, embeddings_dict):
        """Determines the most similar category for a given text by comparing its embedding to precomputed average embeddings.

        Args:
            text (str): The text to classify.
            embeddings_dict (dict): Dictionary of average embeddings by category.

        Returns:
            tuple: A tuple containing the most similar category and its similarity score.
        """
        article_embedding = self.get_embedding(text)
        if article_embedding is None:
            return None, None

        similarity_scores = {}
        for category, avg_embedding in embeddings_dict.items():
            similarity_scores[category] = self.cosine_similarity(article_embedding, np.array(avg_embedding))

        most_similar_category = max(similarity_scores, key=similarity_scores.get)
        highest_similarity_score = similarity_scores[most_similar_category]
        return most_similar_category, highest_similarity_score

    @staticmethod
    def cosine_similarity(vec1, vec2):
        """Calculates the cosine similarity between two vectors.

        Args:
            vec1 (array): First vector.
            vec2 (array): Second vector.

        Returns:
            float: The cosine similarity score, between -1 (opposite) and 1 (identical).
        """
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
