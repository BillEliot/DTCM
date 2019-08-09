export const state = () => ({
    searchResult: [],
    isLogin: false
})

export const mutations = {
    setSearchResult(state, result) {
        state.searchResult = result
    },
    setIsLogin(state, isLogin) {
        state.isLogin = isLogin
    }
}
