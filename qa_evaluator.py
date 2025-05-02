from concurrent.futures import as_completed
from typing import Callable, Dict, List, Union

from promptflow.tracing import ThreadPoolExecutorWithContext as ThreadPoolExecutor

from azure.ai.evaluation import (
    CoherenceEvaluator,
    F1ScoreEvaluator,
    FluencyEvaluator,
    GroundednessEvaluator,
    RelevanceEvaluator,
    SimilarityEvaluator,
)


class QAEvaluator:
    """
    Composite evaluator for question-answering tasks using Azure AI evaluation metrics.
    """

    id = "qa"  # Optional identifier for cloud-based evaluations

    def __init__(self, model_config, **kwargs):
        self._parallel = kwargs.pop("_parallel", False)

        # Create instances of all individual evaluators
        self._evaluators: List[
            Union[
                Callable[..., Dict[str, Union[str, float]]],
                Callable[..., Dict[str, float]]
            ]
        ] = [
            GroundednessEvaluator(model_config),
            RelevanceEvaluator(model_config),
            CoherenceEvaluator(model_config),
            FluencyEvaluator(model_config),
            SimilarityEvaluator(model_config),
            F1ScoreEvaluator(),
        ]

    def __call__(
        self,
        *,
        query: str,
        response: str,
        context: str,
        ground_truth: str,
        **kwargs
    ) -> Dict[str, Union[str, float]]:
        """
        Evaluates a QA response using multiple evaluators.

        :param query: The original question or prompt.
        :param response: The generated answer.
        :param context: The background or supporting context (can be empty).
        :param ground_truth: The expected correct answer.
        :return: A dictionary of evaluation metric scores.
        """
        results: Dict[str, Union[str, float]] = {}

        if self._parallel:
            with ThreadPoolExecutor(max_workers=len(self._evaluators)) as executor:
                futures = {
                    executor.submit(
                        evaluator,
                        query=query,
                        response=response,
                        context=context,
                        ground_truth=ground_truth,
                        **kwargs
                    ): evaluator.__class__.__name__
                    for evaluator in self._evaluators
                }
                for future in as_completed(futures):
                    name = futures[future]
                    try:
                        result = future.result()
                        results.update(result)
                    except Exception as e:
                        results[name] = f"Error: {str(e)}"
        else:
            for evaluator in self._evaluators:
                try:
                    result = evaluator(
                        query=query,
                        response=response,
                        context=context,
                        ground_truth=ground_truth,
                        **kwargs
                    )
                    results.update(result)
                except Exception as e:
                    results[evaluator.__class__.__name__] = f"Error: {str(e)}"

        return results
