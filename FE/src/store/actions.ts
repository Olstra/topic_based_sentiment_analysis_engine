import type {ActionTree} from 'vuex'
import type {RootState} from './state'
import type {JournalEntryDTO} from "@/DTOs/journalEntryDTO";
import axiosInstance from '@/services/http/http-common'
import {GET_PATIENTS_ENTRIES} from "@/constants/http/api";

export const actions: ActionTree<RootState, RootState> = {

  async fetchJournalEntries(
    { commit },
    payload: JournalEntryDTO
  ): Promise<void> {
    axiosInstance({
      method: "get",
      url: GET_PATIENTS_ENTRIES,
      data: payload,
    }).then(
      (response) => {
        console.log("Got this result back from BE API: ", response);
        console.log(payload);
        // TODO: commit changes: commit("setBankName", "TODO");
      },
      (error) => {
        alert(error);
        console.log("Error: ", error);
      }
    );
  },

};