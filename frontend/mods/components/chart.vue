<template>
	<div class="c-chart" style="height: 300px; width: 630px">
		<div class="chart"></div>
	</div>
</template>

<script>
import $chart from '../util/chart/index.js';
export default {
	name: 'chart',

	props: {
		type: String,
		options: [Array, String],
		initOptions: {
			type: Object,
			default() {
				return {
					height: 233
				};
			}
		}
	},

	data() {
		return {
			chart: null
		};
	},

	watch: {
		options: {
			handler(options) {
				if (!this.chart && options) {
					this.initChart();
				} else {
					this.setChart();
				}
			},
			deep: true
		}
	},

	methods: {
		initChart() {
			this.chart = $chart.echarts.init(this.$el, this.initOptions);
			this.setChart();
		},
		setChart() {
			let	options = null;
			if ($chart[this.type] !== undefined) {
				options = $chart[this.type](this.options);
			}
			this.chart.setOption(options, true);
		}
	},

	mounted() {
		if (!this.chart && this.options) {
			this.initChart();
		}
	},

	destroy() {
		if (this.chart) {
			this.chart.dispose();
			this.chart = null;
		}
	}
}
</script>
