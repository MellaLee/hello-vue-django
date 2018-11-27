import $request from './request.js';
import $api from '../model/api.js'

function sendRequest(url, para) {
    return $request({
        url,
        method: 'get',
        params: para
    }).then(
        rs => rs.data
    );
}

const Api = {};

Api.fetchUrlList = para => sendRequest($api['url-list'], para);

Api.fetchLabelList = para => sendRequest($api['label-list'], para);

export default Api;