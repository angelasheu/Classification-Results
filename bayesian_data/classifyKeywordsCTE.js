var fs = require('fs');


// Classifier stuff
var classifier = require("classifier");
var class_1 = new classifier.Bayesian();
var class_2 = new classifier.Bayesian();
var class_3 = new classifier.Bayesian();
var class_5 = new classifier.Bayesian();
var class_6 = new classifier.Bayesian();
var class_9 = new classifier.Bayesian();
var class_10 = new classifier.Bayesian();
var class_13 = new classifier.Bayesian();
var class_14 = new classifier.Bayesian();

var currentClassifier;
var classifierJSON;

var categories = [1, 2, 3, 5, 6, 9, 10, 13, 14];
var classifiers = [class_1, class_2, class_3, class_5, class_6, class_9, class_10, class_13, class_14];

for (var i = 0; i < categories.length; i++) {
    currentCat = categories[i];
    currentClassifier = classifiers[i];
    
    // Train for positive examples
    var posEx = fs.readFileSync('cat' + currentCat + '_pos', 'utf8').toString().split('\n').slice(0,-1);
    for (var j = 0; j < posEx.length; j++) {
        currentClassifier.train(posEx[j], 'true');
    }
    
    // Train for neg examples
    var negEx = fs.readFileSync('cat' + currentCat + '_neg', 'utf8').toString().split('\n').slice(0,-1);
    for (var j = 0; j < negEx.length; j++) {
        currentClassifier.train(negEx[j], 'false');
    }

    classifierJSON =  currentClassifier.toJSON();
    fs.writeFileSync("classifierJSON_" + currentCat, JSON.stringify(classifierJSON), 'utf8');
    console.log("JSON written for cat " + currentCat);
}




    
