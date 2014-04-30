import sys
from scipy import stats

total_test_docs = 30
thresholds = [0.5, 1.0]
categories = ['cat1', 'cat2', 'cat3', 'cat5', 'cat6', 'cat9', 'cat10', 'cat13', 'cat14']
classifier_reg = '10_clusters'
classifier_red = '10_clusters_reduced'
expected_results = { 'cat1': [],
                     'cat2': [3, 5, 8, 10, 11, 19],
                     'cat3': [1, 6, 7, 8, 12, 13, 18],
                     'cat5': [5, 16],
                     'cat6': [1, 4, 9, 10, 17, 18, 19, 20],
                     'cat9': [2, 7, 11, 20],
                     'cat10': [1, 15],
                     'cat13': [1, 6, 7, 8, 12, 13, 18],
                     'cat14': [14,]
                    }

def output_predictions(categories, category_predictions):
    results_list = []
    target = open('combined_output', 'w')
    target.write('++++++++++++ CLASSIFIED AS TRUE ++++++++++++\n')

    for threshold in thresholds:
        classified_results = {}
        target.write('\n\n ------- THRESHOLD ' + str(threshold) + ' ------\n')
        for cat in categories:
            target.write('\n*****' + cat + '*****\n')

            pred = category_predictions[cat]
            z_scores = stats.zscore(pred)

            true_results = []

            for i in range(len(z_scores)):
                #print (i + 1), ' : ', z_scores[i]
                if (abs(z_scores[i]) >= threshold):
                    target.write( str(i+1) + ' : ' + str(z_scores[i]) + '\n')
                    true_results.append(i+1) # Keep track of doc ids that are true

            classified_results[cat] = true_results
        results_list.append(classified_results)

    target.close()
    return results_list

def calculate_accuracies(results_list):

    target = open('combined_output', 'a')
    target.write('\n\n\n++++++++++++ ACCURACIES FOR COMBINED CLASSIFIER ++++++++++++\n')

    # Accuracies for test set
    i = 0
    for classified_results in results_list:
        target.write('\n\n ------- THRESHOLD ' + str(thresholds[i]) + ' ------\n')

        for cat in categories:
            target.write('\n*****' + cat + '*****\n')
            true_correct = 0
            false_as_true = 0
            ret_results = classified_results[cat]
            exp_results = expected_results[cat]
            for e in exp_results:
                if e in ret_results:
                    true_correct += 1
            for r in ret_results:
                if r not in exp_results:
                    false_as_true += 1


            true_acc = float(true_correct) / len(exp_results) if len(exp_results) > 0 else 'NaN'
            false_wrong = float(false_as_true) / (total_test_docs - len(exp_results))
            target.write('TRUE_ACC: ' + str(true_acc) + '\n')
            target.write('FALSE_POS: ' + str(false_wrong) + '\n')

        i += 1

    target.close()

def main(argv):

    category_predictions = {}

    for cat in categories:

        file_reg = classifier_reg + "/" + cat + "/predictions"
        fo = open(file_reg)
        reg_predictions = [float(x) for x in fo.read().split('\n')[:-1]]
        reg_zscores = stats.zscore(reg_predictions)

        file_red = classifier_red + "/" + cat + "/predictions"
        fo = open(file_red)
        red_predictions = [float(x) for x in fo.read().split('\n')[:-1]]
        red_zscores = stats.zscore(red_predictions)

        max_zscore = []

        # Take zscore that has the greatest deviation out of the two classifiers
        for i in range(len(reg_predictions)):
            reg_greater = abs(reg_zscores[i]) >= abs(red_zscores[i])
            val = reg_zscores[i] if reg_greater else red_zscores[i]
            max_zscore.append(val)


        category_predictions[cat] = max_zscore

    results_list = output_predictions(categories, category_predictions)

    calculate_accuracies(results_list)



if __name__ == "__main__":
    main(sys.argv)
