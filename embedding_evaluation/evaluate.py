from embedding_evaluation.evaluate_similarity import EvaluationSimilarity
from embedding_evaluation.evaluate_feature_norm import EvaluationFeatureNorm
from embedding_evaluation.evaluate_concreteness import EvaluationConcreteness
import json

class Evaluation:

    def __init__(self, vocab_path=None, entity_subset=None, vocab=None, eval_conc=True, benchmark_subset=False):
        self.sim = EvaluationSimilarity(entity_subset=entity_subset, benchmark_subset=benchmark_subset)



    def evaluate(self, my_embedding):
        results = {}
        results["similarity"] = self.sim.evaluate(my_embedding)
        
        return results
            

    def evaluate_to_file(self, my_embedding, file_path=None):
        """ save results to a json """
        results = self.evaluate(my_embedding)
        self.save_to_file(results, file_path)

    def save_to_file(self, results, file_path=None):
        assert file_path is not None
        with open(file_path, "w") as fp:
            json.dump(results, fp, sort_keys=True, indent=4)

