//ES5 compatible javascript to render mustache template

var customTags = [ '<%', '%>' ];

var bootstrapResultsReadyCallback = function bootstrapResultsReadyCallback(name, q, promos, results, resultsDiv) {
    fetch(gcs_results_template)
        .then(function (response) {
            return response.text();
        })
        .then(function (template) {
            var rendered = Mustache.render(template, {'results': results}, customTags);
            resultsDiv.innerHTML = rendered;
        });

    // Disable the default behaviour
    return true;
};