import Framework7 from 'framework7'

export default class ApiService {

  static getApiEndpoint() { return API_URL + '/api/' }

  static apiRequest(method, url, data, successCallback, errorCallback) {
    Framework7.request.promise({
      url: this.getApiEndpoint() + url,
      method: method,
      contentType: 'application/json',
      crossDomain: true,
      data: data,
      dataType: 'json',
      xhrFields: {
        withCredentials: true
      }
    }).then(function (response) {
      if (response.status === 200) {
        successCallback(response.data)
      }
    }, function (error) {
      errorCallback(error.xhr.response)
    })
  }

  static get (url, successCallback, errorCallback) {
    return this.apiRequest("GET", url, null, successCallback, errorCallback)
  }

  static post (url, data, successCallback, errorCallback) {
    return this.apiRequest("POST", url, data, successCallback, errorCallback)
  }

  static put (url, data, successCallback, errorCallback) {
    return this.apiRequest("PUT", url, data, successCallback, errorCallback)
  }
  
  static delete (url, successCallback, errorCallback) {
    return this.apiRequest("DELETE", url, null, successCallback, errorCallback)
  }
}
