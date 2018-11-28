const lineOption = options => {
	let setoption = {};
	setoption.grid = {
		left: 50,
		top: 10
	};
 	setoption.xAxis = {
		type: 'category',
    };
    setoption.yAxis = {
        type: 'value'
    };	
	setoption.series = [{
        data: options,
        type: 'line'
	}];
	setoption.tooltip = [{
		trigger: 'axis'
	}];
	return setoption;
};

export default lineOption;
