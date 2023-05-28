from BE.src.DTOs.topicSentimentDTO import ValenceDataPointDTO, ValenceChartDataDTO, TopicSentimentDTO, \
    AvgTopicSentimentDTO


def parse_valence_datasets(entries: list[TopicSentimentDTO]) -> list[ValenceChartDataDTO]:
    result = []
    for db_entry in entries:
        # initialize list
        data_points = []
        data_point = ValenceDataPointDTO(
            sentiment_score=db_entry.sentiment,
            date=db_entry.date_noted
        )
        data_points.append(data_point)
        new_entry = ValenceChartDataDTO(
            patient_id=db_entry.patient_id,
            topic=db_entry.topic,
            data=data_points
        )
        if not result:
            result.append(new_entry)
        else:
            topic_found = False
            for registered_entry in result:
                if registered_entry.topic == new_entry.topic:
                    topic_found = True
                    data_point = ValenceDataPointDTO(
                        sentiment_score=db_entry.sentiment,
                        date=db_entry.date_noted
                    )
                    registered_entry.data.append(data_point)
            if not topic_found:
                result.append(new_entry)
    return result


def parse_valence_entries(entries):
    result = add_topic_count(entries)
    result = calculate_avg_sentiments(result)
    return result


def add_topic_count(valence_activities: list[TopicSentimentDTO]):
    counted_activities = []
    for e in valence_activities:
        new_activity = {"topic": e.topic, "count": 1, "sentiment": [e.sentiment], "patient_id": e.patient_id}
        if not counted_activities:
            counted_activities.append(new_activity)
        else:
            topic_found = False
            for activity in counted_activities:
                if activity["topic"] == e.topic:
                    topic_found = True
                    activity["count"] += 1
                    activity["sentiment"].append(e.sentiment)
            if not topic_found:
                counted_activities.append(new_activity)
    return counted_activities


def calculate_avg_sentiments(activities) -> list[AvgTopicSentimentDTO]:
    result = []
    for e in activities:
        total = 0
        for s in e["sentiment"]:
            total += s
        if total > 0:
            sentiment = "positive"
        elif total < 0:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        new_activity_dto = AvgTopicSentimentDTO(
            topic=e["topic"],
            overall_sentiment=sentiment,
            nr_of_occurrences=e["count"],
            patient_id=e["patient_id"]
        )
        result.append(new_activity_dto)
    return result
