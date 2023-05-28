<template>
    <h2>Zusammenfassung Journaleintrag</h2>
    <p>{{ this.currentEntry }}</p>
    <p style="font-style: italic">Datum: {{ this.entry_date }}</p>
    <div>
        <button @click="loadPreviousEntry">Vorheriger Eintrag</button>
        <button @click="loadNextEntry">Nächster Eintrag</button>
    </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";
import axiosInstance from "@/services/http/http-common";
import {GET_PATIENT_ENTRIES} from "@/constants/http/api";
import type {JournalEntryDTO} from "@/DTOs/journalEntryDTO";

export default defineComponent({
    name: 'JournalEntrySummary',
    props: ['patientId'],
    data() {
        return {
            currentEntry: "",
            currentTextEntry: 0,
            patientID: this.$props.patientId,
            entry_date: "",
            allJournalEntries: [] as JournalEntryDTO[]
        }
    },
    methods: {
        parseEntryDate(date: Date): string {
            const result = new Date(date);
            return result.toLocaleDateString("de-CH");
        },
        loadPreviousEntry() {
            if (this.currentTextEntry > 0) {
                this.currentTextEntry--;
                this.currentEntry = this.allJournalEntries[this.currentTextEntry].text_entry;
                this.entry_date = this.parseEntryDate(
                    this.allJournalEntries[this.currentTextEntry].date_written
                );
            }
        },
        loadNextEntry() {
            if (this.currentTextEntry < this.allJournalEntries.length - 1) {
                this.currentTextEntry++;
                this.currentEntry = this.allJournalEntries[this.currentTextEntry].text_entry;
                this.entry_date = this.parseEntryDate(
                    this.allJournalEntries[this.currentTextEntry].date_written
                );
            }
        },
        async fetchData() {
            try {
                const response = await axiosInstance.get(GET_PATIENT_ENTRIES + this.patientID);
                this.allJournalEntries = response.data;
                this.currentEntry = this.allJournalEntries[0].text_entry;
                this.entry_date = this.parseEntryDate(this.allJournalEntries[0].date_written);
            } catch (error) {
                console.error(error);
            }
        }
    },
    mounted() {
        this.fetchData();
    }
})
</script>

<style scoped>
div {
    padding-left: 5%;
    padding-right: 5%;
}

button {
    margin-right: 8px;
    display: inline-block;
    background-color: #115bfb;
    color: white;
    border: none;
    padding: 8px 16px;
    font-size: 14px;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
    cursor: pointer;
    border-radius: 5px;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
}

button:hover {
    background-color: #afafaf;
}
</style>