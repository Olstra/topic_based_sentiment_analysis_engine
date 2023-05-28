from datetime import datetime
from unittest import TestCase

from BE.src.DTOs.patientDTO import PatientDTO
from BE.src.db_handling.db_handler import DbHandler


class DbHandlerTest(TestCase):
    db_handler = DbHandler()

    def test_insert_new_patient(self):
        # create test patient
        random_unique_forename = "Testpatient " + datetime.now().__str__()
        test_patient = PatientDTO(
            forename=random_unique_forename,
            lastname="Müller",
            gender="male",
        )
        self.db_handler.insert_patient(test_patient)

        test_patient_id = self.db_handler.get_patient_id(test_patient.forename, test_patient.lastname)

        # read created patient from db
        fetched_patient = self.db_handler.get_patient(test_patient_id)

        self.assertEqual(fetched_patient.forename, test_patient.forename, "'Forename' was not equal!")
        self.assertEqual(fetched_patient.lastname, test_patient.lastname, "'Lastname' was not equal!")
        self.assertEqual(fetched_patient.gender, test_patient.gender, "'Gender' was not equal!")
        self.assertEqual(fetched_patient.id, test_patient_id, "'ID' was not equal!")

        # delete patient if test was successful
        self.db_handler.delete_patient(test_patient_id)
