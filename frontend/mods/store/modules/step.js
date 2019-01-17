// 需要管理的状态，如数组、对象、字符等等
const state = {
  curStep: 1,
  stepNum: 2 
};

const getters = {
	stepStatus(state) {
		return state;
	}
};
// 提交mutation是更改state的唯一方法
const actions = {
	addStep({state, commit}) {
		commit('addCurStep');
	},
	minusStep({state, commit}) {
		commit('minusCurStep');
	},
	setStepNum({state, commit}, stepNum) {
		commit('setStepNumStatus', stepNum);
	}
};

// mutation
const mutations = {
	setStepNumStatus(state, num) {
		state.stepNum = num;
	},
	addCurStep(state) {
		state.curStep++;
	},
	minusCurStep(state) {
		state.curStep--;
	}
};

export default {
	state,
	getters,
	actions,
	mutations
};