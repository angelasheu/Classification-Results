var fs = require('fs');
var classifier = require('classifier');

var categories = [1, 2, 3, 5, 6, 9, 10, 13, 14];
var classifiers = new Array(9);

// Instantiate classifiers from JSON data
for (var i = 0; i < categories.length; i++) {
    var cat = categories[i];
    var bayes = new classifier.Bayesian();
    var jsonString = fs.readFileSync('classifierJSON_' + cat, 'utf8');
    var jsonObj = JSON.parse(jsonString);
    bayes.fromJSON(jsonObj);
    classifiers[i] = bayes;
}

// Classifier for whether relevant or not
var bayesBin = new classifier.Bayesian();
var jsonString = fs.readFileSync('classifierJSON_bin', 'utf8');
var jsonObj = JSON.parse(jsonString);
bayesBin.fromJSON(jsonObj);


// Get correct labels for testing documents
var testArr = fs.readFileSync('testing_docs', 'utf8').toString().split('\n').slice(0, -1);
var testLabels = fs.readFileSync('testing_labels', 'utf8').toString().split('\n').slice(0, -1);

// Use to compare against actual labels
var catArr = new Array(testLabels.length);
for (var i = 0; i < catArr.length; i++) {
    catArr[i] = new Array();
}

for (var i = 0; i < testLabels.length; i++) {
    var label = testLabels[i];
    label = label.replace(/[[\]]/g,'');
    label = label.split(',');
    for (var j = 0; j < label.length; j++) {
        if (label[j] == '*') {
            catArr[i].push(j+1);
        }
    }
}

// Classify test documents
var result;
var expected;

for (var i = 0; i < classifiers.length; i++) {
    var category = categories[i];
    var classifier = classifiers[i];
    var trueCount = 0;

    console.log('\n *********** CATEGORY ' + category + '**********');

    for (var j = 0; j < testArr.length; j++) {
        var testDoc = testArr[j];
        var trueCats = catArr[j];
        result = classifier.classify(testDoc);
        expected = trueCats.indexOf(category) != -1;
        if (expected.toString() == result) {
            trueCount++;
        }

        console.log('TD ' + j + '; ' + 'Expected: ' + expected + " Returned: " + result);
    }
    console.log('Accuracy: ' + (trueCount/testArr.length).toPrecision(4));
}

// Testing for classifier_bin; classifier is bayesBin
var trueCount = 0;
console.log('\n *********** CATEGORY BIN **********');
for (var j = 0; j < testArr.length; j++) {
    var testDoc = testArr[j];
    var trueCats = catArr[j];
    result = bayesBin.classify(testDoc);
    expected = trueCats.length > 0;
    if (expected.toString() == result) {
        trueCount++;
    }

    console.log('TD ' + j + '; ' + 'Expected: ' + expected + " Returned: " + result);
}
console.log('Accuracy: ' + (trueCount/testArr.length).toPrecision(4));
