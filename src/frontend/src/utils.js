import { elasticOut } from 'svelte/easing';


export function getAllUrlGetParams(url) {
    // get query string from url (optional) or window
    var queryString = url ? url.split('?')[1] : window.location.search.slice(1);
  
    // we'll store the parameters here
    var obj = {};
  
    // if query string exists
    if (queryString) {
        // stuff after # is not part of query string, so get rid of it
        queryString = queryString.split('#')[0];

        // split our query string into its component parts
        var arr = queryString.split('&');

        for (var i = 0; i < arr.length; i++) {
            // separate the keys and the values
            var a = arr[i].split('=');

            // set parameter name and value (use 'true' if empty)
            var paramName = a[0];
            var paramValue = typeof (a[1]) === 'undefined' ? true : a[1];

            // (optional) keep case consistent
            paramName = paramName.toLowerCase();
            if (typeof paramValue === 'string') paramValue = paramValue.toLowerCase();

            // if the paramName ends with square brackets, e.g. colors[] or colors[2]
            if (paramName.match(/\[(\d+)?\]$/)) {
                // create key if it doesn't exist
                var key = paramName.replace(/\[(\d+)?\]/, '');
                if (!obj[key]) obj[key] = [];

                // if it's an indexed array e.g. colors[2]
                if (paramName.match(/\[\d+\]$/)) {
                    // get the index value and add the entry at the appropriate position
                    var index = /\[(\d+)\]/.exec(paramName)[1];
                    obj[key][index] = paramValue;
                } else {
                    // otherwise add the value to the end of the array
                    obj[key].push(paramValue);
                }
            } else {
                // we're dealing with a string
                if (!obj[paramName]) {
                    // if it doesn't exist, create property
                    obj[paramName] = paramValue;
                } else if (obj[paramName] && typeof obj[paramName] === 'string'){
                    // if property does exist and it's a string, convert it to an array
                    obj[paramName] = [obj[paramName]];
                    obj[paramName].push(paramValue);
                } else {
                    // otherwise add the property
                    obj[paramName].push(paramValue);
                }
            }
        }
    }
  
    return obj;
}

export function get_time_from_unix(unix) {
    let date = new Date(unix * 1000)
    return date.toString('HH:MM:ss')
}

export function get_date_from_unix(unix) {
    let date = new Date(unix * 1000)
    return date.toString('dd.MM.yyyy')
}

export function formatBigNumber(number) {
    if (number > 1_000_000) {
        return `${(number / 1_000_000).toFixed(1)}M`
    } else if (number > 1_000) {
        return `${(number / 1_000).toFixed(1)}K`
    } else {
        return `${number}`
    }
}

export function whooshAnimation(node, params) {
    const existingTransform = getComputedStyle(node).transform.replace('none', '');

    return {
        delay: params.delay || 0,
        duration: params.duration || 500,
        easing: params.easing || elasticOut,
        css: (t, u) => `transform: ${existingTransform} scale(${t})`
    };
}
