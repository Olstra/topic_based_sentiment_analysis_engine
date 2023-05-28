import type { MutationTree } from 'vuex'
import type { RootState } from './state'

export const mutations: MutationTree<RootState> = {
  setUserEmail(state, payload: string) {
    state.journalEntries = payload;
  },
};
