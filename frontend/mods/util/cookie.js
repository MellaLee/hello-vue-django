const cookie = {}; 

cookie.get = (name) => {
	let arr,
		reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
	if (arr = document.cookie.match(reg)) {
		return decodeURIComponent(arr[2]);
	}
};

export default cookie;
