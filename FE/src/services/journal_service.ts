import axiosInstance from "@/services/http/http-common";
import {GET_PATIENT_ENTRIES} from "@/constants/http/api";
import type {JournalEntryDTO} from "@/DTOs/journalEntryDTO";

export class JournalService {
  public postValues(payload: JournalEntryDTO): void {
    axiosInstance({
      method: "get",
      url: GET_PATIENT_ENTRIES+"1", // TODO add path variable for id
      data: payload,
    }).then(
      (response) => {
        console.log("Response: ", response);
      },
      (error) => {
        alert(error);
        console.log("Error: ", error);
      }
    );
  }
}
