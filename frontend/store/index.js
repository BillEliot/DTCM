export const state = () => ({
    searchResult: []
})

export const mutations = {
    setSearchResult(state, result) {
        state.searchResult = result
    }
}
