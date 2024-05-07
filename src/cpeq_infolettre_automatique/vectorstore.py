"""Client module for openAI API interaction."""  # noqa: CPY001

# Importations

import json
from typing import Union

import numpy as np
import openai
import tiktoken
from decouple import config
from openai import OpenAI


# Open AI client
client = OpenAI(
    api_key=config("OPENAI_API_KEY"),
)


class VectorStore:
    def __init__(self, filepath: str):
        """Initialize the VectorStore with data loaded from a specified JSON file.

        Args:
            filepath (str): The path to the JSON file containing embedded data.
        """
        self.data = self.load_embedded_data(filepath)
        if self.data:
            self.global_mean_embedding = self.calculate_global_mean_embedding()

    def load_embedded_data(self, filepath: str) -> Union[dict, None]:
        """Load embedded data from a JSON file.

        Args:
            filepath (str): The path to the JSON file.

        Returns:
            Union[dict, None]: The data loaded from the JSON file, or None if an error occurs.
        """
        try:
            with open(filepath, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading embedded data from {filepath}: {e}")
            return None

    def calculate_global_mean_embedding(self) -> np.ndarray:
        """Calculate the global mean embedding from all embeddings in the dataset.

        Returns:
            np.ndarray: A numpy array representing the global mean embedding.
        """
        embeddings = [
            np.array(ex["embedding"]) for section in self.data for ex in section["examples"]
        ]
        return np.mean(embeddings, axis=0) if embeddings else np.zeros_like(embeddings[0])

    def get_category_embeddings(
        self, exclude_rubric: str = None, exclude_title: str = None
    ) -> dict[str, np.ndarray]:
        """Retrieve embeddings for each category, optionally excluding a specific example, and adjust by the global mean embedding.

        Args:
            exclude_rubric (str, optional): The rubric of the example to exclude.
            exclude_title (str, optional): The title of the example to exclude.

        Returns:
            dict[str, np.ndarray]: A dictionary of category names to their mean adjusted embeddings.
        """
        category_embeddings = {}
        for section in self.data:
            embeddings = [
                np.array(ex["embedding"]) - self.global_mean_embedding
                for ex in section["examples"]
                if not (section["rubric"] == exclude_rubric and ex["title"] == exclude_title)
            ]
            if embeddings:
                category_embeddings[section["rubric"]] = np.mean(embeddings, axis=0)
        return category_embeddings

    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculates the cosine similarity between two vectors.

        Args:
            vec1 (np.array): The first vector.
            vec2 (np.array): The second vector.

        Returns:
            float: The cosine similarity score, between -1 (opposite) and 1 (identical).
        """
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def dynamic_split_accuracy(
        self, numb_categories: int
    ) -> tuple[dict[str, list[dict[str, str | bool | list[tuple[str, float]]]]], float]:
        """Evaluate dynamic split accuracy for a given number of categories to consider as correct.

        Args:
            numb_categories (int): Number of categories to consider for top K accuracy.

        Returns:
            tuple[dict[str, list[dict[str, Union[str, bool, list[tuple[str, float]]]]]], float]: Results and global accuracy.
        """
        results = {}
        total_examples = 0
        correct_predictions = 0

        for section in self.data:
            rubric = section["rubric"]
            examples = section["examples"]
            results[rubric] = []

            for example in examples:
                total_examples += 1
                test_embedding = np.array(example["embedding"]) - self.global_mean_embedding
                adjusted_category_embeddings = self.get_adjusted_category_embeddings(
                    exclude_rubric=rubric, exclude_title=example["title"]
                )
                top_results = sorted(
                    [
                        (cat, self.cosine_similarity(test_embedding, emb))
                        for cat, emb in adjusted_category_embeddings.items()
                    ],
                    key=lambda item: item[1],
                    reverse=True,
                )[:numb_categories]

                is_correct = any(cat[0] == rubric for cat in top_results)
                correct_predictions += is_correct

                results[rubric].append({
                    "title": example["title"],
                    "similar_categories": top_results,
                    "is_correct": is_correct,
                })

        global_accuracy = correct_predictions / total_examples if total_examples > 0 else 0
        return results, global_accuracy

    def get_average_embeddings(
        self, model: str, rubrics_data: list[dict[str, str | list[dict[str, str]]]]
    ) -> dict[str, list[float]]:
        """Calculates average embeddings for each rubric using provided examples.

        Args:
            model (str): The OpenAI model to use for generating embeddings.
            rubrics_data (list[dict[str, str | list[dict[str, str]]]]): A list of rubric sections, each containing examples.

        Returns:
            dict[str, list[float]]: A dictionary mapping rubric names to their average embedding vectors.
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

    def get_embedding(self, text: str, max_tokens: int = 8000) -> Union[list[float], None]:
        """Retrieve the embedding vector for a given text, truncating to a maximum token count.

        Args:
            text (str): The text to be embedded.
            max_tokens (int): Maximum number of tokens to consider.

        Returns:
            Union[list[float], None]: The embedding vector obtained from the OpenAI API, or None if unavailable.
        """
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(text)
        if len(tokens) > max_tokens:
            tokens = tokens[:max_tokens]
        truncated_text = encoding.decode(tokens)
        response = self.client.embeddings.create(input=truncated_text, model=self.model)
        return response.data[0].embedding if response else None

    def find_most_similar_category(
        self, text: str, embeddings_dict: dict[str, list[float]]
    ) -> tuple[str | None, Union[float, None]]:
        """Determine the most similar category for a given text by comparing its embedding to precomputed average embeddings.

        Args:
            text (str): The text to classify.
            embeddings_dict (dict[str, list[float]]): Dictionary of average embeddings by category.

        Returns:
            tuple[Union[str, None], Union[float, None]]: Most similar category and its similarity score, or (None, None) if not found.
        """
        article_embedding = self.get_embedding(text)
        if article_embedding is None:
            return None, None

        similarity_scores = {}
        for category, avg_embedding in embeddings_dict.items():
            similarity_scores[category] = self.cosine_similarity(
                article_embedding, np.array(avg_embedding)
            )

        most_similar_category = max(similarity_scores, key=similarity_scores.get)
        highest_similarity_score = similarity_scores[most_similar_category]
        return most_similar_category, highest_similarity_score
