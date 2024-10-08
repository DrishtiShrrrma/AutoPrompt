from estimator.estimator_llm import LLMEstimator
import json


def set_function_from_iterrow(func):
    def wrapper(dataset):
        dataset['score'] = dataset.apply(func, axis=1)
        return dataset

    return wrapper


def set_ranking_function(params):
    evaluator = LLMEstimator(params)
    evaluator.init_chain(params.label_schema)
    evaluator.mode = 'score'

    def wrapper(dataset):
        generation_dataset = dataset.copy()
        generation_dataset['text'] = '###User input:\n' + generation_dataset['text'] + '\n####model prediction:\n' + \
                                     generation_dataset['prediction']

        generation_dataset = evaluator.apply_dataframe(generation_dataset)
        generation_dataset.score = generation_dataset.score.astype(int)
        dataset.score = generation_dataset.score
        return dataset

    return wrapper


def set_multiscore_function(scores_dic, num_workers=1):
    def wrapper(dataset):
        generation_dataset = dataset.copy()
        generation_dataset['text'] = '###User input:\n' + generation_dataset['text'] + '\n####model prediction:\n' + \
                                     generation_dataset['prediction']
        for metric_name, metric_function in scores_dic.items():
            generation_dataset['{}_{}'.format('score', metric_name)] = 'Discarded'
            generation_dataset['{}_{}'.format('reasoning', metric_name)] = 'Discarded'
        for metric_name, metric_function in scores_dic.items():
            res = metric_function(generation_dataset, num_workers)
            for index, score in res.items():
                generation_dataset.loc[index, '{}_{}'.format('score', metric_name)] = score['metric_score']
                generation_dataset.loc[index, '{}_{}'.format('reasoning', metric_name)] = score['metric_reason']

        columns_to_copy = ['{}_{}'.format('score', metric_name) for metric_name in scores_dic.keys()] + \
                          ['{}_{}'.format('reasoning', metric_name) for metric_name in scores_dic.keys()]
        dataset[columns_to_copy] = generation_dataset[columns_to_copy]
        return dataset

    return wrapper
