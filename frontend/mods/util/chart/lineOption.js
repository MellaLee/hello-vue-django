const lineOption = (options, title) => {
	let setoption = {};
	setoption.title = {
		text: title
	};
	setoption.legend = {
		right: '5%',
		data: [] 
	};
 	setoption.xAxis = {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    };
    setoption.yAxis = {
        type: 'value'
    };	
	setoption.series = [{
        data: [820, 932, 901, 934, 1290, 1330, 1320],
        type: 'line'
    }];
	return setoption;
};

export default lineOption;
