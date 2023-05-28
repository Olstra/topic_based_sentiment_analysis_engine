import type { GetterTree } from 'vuex'
import type { RootState } from './state'

export const getters: GetterTree<RootState, RootState> = {
  journalEntries(state): string {
    return state.journalEntries;
  },
};
