import $axios from 'axios';

// 返回数据格式
// {
//     data: null,
//     // code为0时，表示请求成功
//     code: 0,
//     // 响应失败时给的错误消息
//     msg: ''
// }
const request = options => {
    let conf = Object.assign({
        url: '',
        method: 'get',
        responseType: 'text',
        // 是否自定义错误处理流程
        customError: false
    }, options);

    let promise = $axios(conf).then(rs => {
        if (rs && rs.data) {
            if (conf.customError || rs.data.code === 0) {
                return rs.data;
            } else if (rs.data.msg) {
                return Promise.reject(rs.data.msg);
            } else {
                return Promise.reject(`请求失败(${rs.code})`);
            }
        } else {
            return Promise.reject('数据格式错误');
        }
    }).catch(err => {
        let msg = '';
        if (err && err.response && err.response.status) {
            msg = '请求失败，请检查网络' + err.response.status;
        } else if (typeof err === 'string') {
            msg = err;
        } else {
            msg = '请求失败，网络环境异常';
        }
        return Promise.reject(msg);
    });

    return promise;
};

export default request;