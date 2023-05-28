import csv
from datetime import datetime

from BE.src.DTOs.patientDTO import PatientDTO
from BE.src.config import config_instance
from BE.src.db_handling.db_handler import DbHandler, db_handler
from BE.src.preprocessing.data_loader import parse_access_key


def feed_patients() -> None:
    """
    This function populates the database with patient data. As the input data is anonymized, it generates randomized
    data to complete patient information.
    """
    filepath = config_instance.raw_data_path

    try:
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file,
                                    fieldnames=['note', 'id', 'date', 'consultationId', 'patientId', 'accessKey'])
            next(reader)  # skip header row

            patient_ids = set()
            for row in reader:
                original_patient_id = row['patientId']
                patient_ids.add(original_patient_id)

            for patient_id in patient_ids:
                if db_handler.get_patient_through_original_id(patient_id) is None:
                    current_gender = "male"  # add artificial genders for patients
                    random_unique_lastname = "Testpatient " + datetime.now().__str__()
                    new_patient = PatientDTO(
                        original_id=patient_id,
                        forename="Anonym",
                        lastname=random_unique_lastname,
                        gender=current_gender
                    )
                    db_handler.insert_patient(new_patient)

    except FileNotFoundError:
        raise FileNotFoundError(f"ERROR: The file at {filepath} was not found.")

    except UnicodeDecodeError:
        raise ValueError(f"ERROR: The file at {filepath} is corrupted or not a text file.")


if __name__ == '__main__':
    feed_patients()
