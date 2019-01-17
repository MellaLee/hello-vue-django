<template>
	<div id="app">
		<div class="header">
			<v-header @change="changeNavShow"></v-header>
		</div>
		<div class="nav" v-if="navShow">
			<v-navside></v-navside>
		</div>
		<div class="container" :class="{sidebar: navShow}">
			<v-breadcrumb></v-breadcrumb>
			<el-card>
				<router-view></router-view>
			</el-card>
		</div>
		<el-footer :class="{sidebar: navShow}">
			<el-button-group style="float:right">
				<el-button v-if="stepNum" :disabled="active == 1" icon="el-icon-arrow-left" type="primary" @click="back">上一步</el-button>
				<el-button v-if="stepNum" :disabled="active == stepNum" type="primary" @click="nextStep">
					下一步<i class="el-icon-arrow-right el-icon--right"></i>
				</el-button>
				<el-button v-if="manualMarkButton" :disabled="active != stepNum" type="primary" @click="manualMark" class="button-manual-mark">
					人工辅助标记
				</el-button>
				<el-button v-if="manualMarkButton" class="button-or" plain type="primary">OR</el-button>
				<el-button v-if="nextMoudleButton" :disabled="active != stepNum && stepNum != 0" type="primary" @click="nextMoudle">
					下一模块<i class="el-icon-arrow-right el-icon--right"></i>
				</el-button>
				<el-button v-else :disabled="active != stepNum && stepNum != 0" type="primary" @click="startCheck">
					{{ oneButtonText }}
					<i class="iconfont icon-jiance el-icon-right"></i>
				</el-button>
			</el-button-group>
		</el-footer>
	</div>
</template>

<script>
import $uploadLog from './mods/components/uploadLog.vue';
import $urlList from './mods/components/urlList.vue';
import $label from './mods/components/label.vue';
import $navSide from './mods/components/ui/navside.vue';
import $header from './mods/components/ui/header.vue';
import $breadcrumb from './mods/components/ui/breadcrumb.vue';

export default {
	name: 'app',
	data() {
		return {
			active: 1,
			navShow: true,
			nextMoudleButton: true,
			stepPath: {
				'/train/upload': 'feature',
				'/train/feature': 'cluster',
				'/train/cluster': 'semiSupervised',
			},
			manualMarkButton: false,
			oneButtonText: '开始检测',
		}
	},

	components: {
		'v-upload-log': $uploadLog,
		'v-url-list': $urlList,
		'v-label': $label,
		'v-navside': $navSide,
		'v-header': $header,
		'v-breadcrumb': $breadcrumb
	},

	watch:{
		$route(to, from) {
			if (to.path.indexOf('identify') > 0) {
				this.nextMoudleButton = false;
			}
			if (to.path.indexOf('cluster') > 0 && to.path.indexOf('label') < 0) {
				this.manualMarkButton = true;
			} else {
				this.manualMarkButton = false;
			}
			if (to.path.indexOf('check/label') > 0) {
				this.oneButtonText = '一键优化检测模型';
			}
			if (to.path.indexOf('semiSupervised') > 0) {
				this.oneButtonText = '开始识别';
			}
			if (to.path.indexOf('check') > 0) {
				this.oneButtonText = '修改类别标记';
			}
		}
	},

	computed: {
		stepNum() {
			return this.$store.state.step.stepNum;
		}
	},

	methods: {
		back(index) {
			this.active--;
			this.$store.dispatch('minusStep');
		},
		nextStep(index) {
			this.active ++;
			this.$store.dispatch('addStep');
			if (this.active > this.stepNum) {
				this.active = 0;
			}
		},
		changeNavShow() {
			this.navShow = !this.navShow;
		},
		nextMoudle() {
			this.$router.push(this.stepPath[this.$route.path]);
		},
		startCheck() {
			// TODO
		},
		manualMark() {
			this.$router.push('/train/cluster/label');
		}
	},
}
</script>

<style lang="less">
body {
	margin: 0px;
	background: #efefef;
	#app {
		.header {
			position: fixed;
			top: 0;
		}
		.nav {
			z-index: 100;
		}
		.container {
			margin-left: 0px;
			padding: 32px;
			margin-top: 60px;
			&.sidebar {
				margin-left: 280px;
			}
			.container-main {
				margin-top: 30px;
			}
		}
		.el-footer {
			background: #444;
			position: fixed;
			bottom: 0;
			right: 0;
			left: 0;
			&.sidebar {
				left: 280px;
			}
			.el-button {
				margin: 12px 1px;
			}
			.button-manual-mark {
				margin-left: 20px;
			}
			.button-or {
				margin: 12px 0px;
				border-radius: 35px;
			}
			.icon-jiance {
				font-size: 14px;
				margin-left: 5px;
			}
		}
	}
}
</style>
