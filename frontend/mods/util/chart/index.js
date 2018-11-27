// 引入 ECharts 主模块
import $echarts from 'echarts/lib/echarts';
import 'echarts/lib/chart/line';
// 引入提示框和标题组件
import 'echarts/lib/component/tooltip';
import 'echarts/lib/component/title';
import 'echarts/lib/component/legendScroll';

import $lineOption from './lineOption';

const chart = {
	echarts: $echarts,
	line: $lineOption,
};

export default chart;
