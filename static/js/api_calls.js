const error_data = {
    data:
        {success:false,message:"An internal server error occurred"}
    
}

function makeApiRequestwithToken(callback){
    var url = arguments[1];
    var form = arguments[2];
    var headers = arguments[3]
    axios.post(url, form
        ,{
        headers: headers
      }
      )
        .then(function(response) {
            callback(response);
        }).catch(function(error) {
            if (exists(error.response)) {
                // console.log(error.response.data)
            }
            if (error.response) {
                // Log the status code from the error response
                var statusCode = error.response.status;
                console.log('Status Code:', error.response.status);
                // You can also access the data from the error response if needed
                console.log('Error Data:', error.response.data);
                if(statusCode == 401){
                    window.location.assign("/login")
                }
                if(statusCode == 500){
                    callback(error_data)
                }
                if(statusCode == 400){
                    callback(error.response)
                }
                
            } else {
                console.log('Error:', error);
            }

        });

}


function makePutApiRequestwithToken(callback){
    var url = arguments[1];
    var form = arguments[2];
    var headers = arguments[3]
    axios.put(url, form
        ,{
        headers: headers
      }
      )
        .then(function(response) {
            callback(response);
        }).catch(function(error) {
            if (exists(error.response)) {
                // console.log(error.response.data)
            }
            if (error.response) {
                // Log the status code from the error response
                var statusCode = error.response.status;
                console.log('Status Code:', error.response.status);
                // You can also access the data from the error response if needed
                console.log('Error Data:', error.response.data);
                if(statusCode == 401){
                    window.location.assign("/login")
                }
                if(statusCode == 500){
                    callback(error_data)
                }
                if(statusCode == 400){
                    callback(error.response)
                }
                
            } else {
                console.log('Error:', error);
            }

        });

}

function makeGetApiRequestwithToken(callback) {
    var url = arguments[1];
    // var form = arguments[2];
    var headers = arguments[2]
    axios.get(url
        ,{headers: headers}
      ).then(function(response) {
        console.log(response)
        callback(response);
        }).catch(function(error) {
            if (exists(error.response)){
                // console.log(error.response.data)
            }
            if (error.response) {
                // Log the status code from the error response
                var statusCode = error.response.status;
                console.log('Status Code:', error.response.status);
                // You can also access the data from the error response if needed
                console.log('Error Data:', error.response.data);
                if(statusCode == 401){
                    // callback(error.response);
                    window.location.assign("/login")
                }
                if(statusCode == 500){
                    callback(error_data)
                }
                if(statusCode == 400){
                    callback(error.response)
                }
                
            } else {
                console.log('Error:', error.message);
            }

        });
}

function makeGetApiRequest(callback) {
    var url = arguments[1];
    // var form = arguments[2];
    axios.get(url)
        .then(function(response) {
            console.log(response);
            callback(response);
        }).catch(function(error) {
            console.log(error);
            if (exists(error.response)) {
                console.log(error.response.data)
            }
            if (error.response) {
                // Log the status code from the error response
                var statusCode = error.response.status;
                console.log('Status Code:', error.response.status);
                // You can also access the data from the error response if needed
                console.log('Error Data:', error.response.data);
                if(statusCode == 401){
                    window.location.assign("/login")
                }
                if(statusCode == 500){
                    callback(error_data)
                }
                
            } else {
                console.log('Error:', error.message);
            }
        });
}
function makePostApiRequest(callback) {
    var url = arguments[1];
    var form = arguments[2];
    axios.post(url,form)
        .then(function(response) {
            console.log(response);
            callback(response);
        }).catch(function(error) {
            console.log(error);
            if (exists(error.response)) {
                console.log(error.response.data)
            }
            if (error.response) {
                // Log the status code from the error response
                var statusCode = error.response.status;
                console.log('Status Code:', error.response.status);
                // You can also access the data from the error response if needed
                console.log('Error Data:', error.response.data);
                // if(statusCode == 401){
                //     window.location.assign("/login")
                // }
                if(statusCode == 400){
                    callback(error.response);
                }
                if(statusCode == 500){
                    callback(error_data)
                }
                
            } else {
                console.log('Error:', error.message);
            }
        });
}